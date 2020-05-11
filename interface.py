#Hugo Rey
#Generation de map 3d

#----------------------------
#█▀▄▀█ █▀█ █▀▄ █ █ █   █▀▀ █▀
#█ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█
#----------------------------
from random import randint, uniform, seed
from PIL import Image
import noise
import numpy as np
import tkinter as tk
from tkinter import ttk
from map_2D import func_map_color, func_map_color_perlin


#variables "tampon" pour stocker les données généré via l'apperçu afin de les utiliser pour générer la carte 3D
data_map_perlin=[]
data_map_dc=[]



def tk_2d_map_dc():
	'''Cette procédure est appelée lorsque l'utilisateur clique sur le bouton d'apperçu 2D avec une génération via diamant-carré.'''
	global data_map_dc
	#recupere les parametres
	n= scale_n.get()
	f=scale_f.get()
	couleur = liste_color.get()
	#genere la carte et la stocke dans la variable tampon 
	data_map_dc= func_map_color(n,f,couleur_option=couleur)
	#actualise le canvas 
	map_img_canvas=tk.PhotoImage(file='./carte_couleur.png')
	canvas_map.after(500,canvas_map.create_image(0,0,image=map_img_canvas, anchor=tk.NW))

def tk_2d_map_perlin():
	'''Cette procédure est appelée lorsque l'utilisateur clique sur le bouton d'apperçu 2D avec une génération via le bruit de perlin.'''
	global data_map_perlin
	#recupere les parametres
	shape= (int(spin_x.get()),int(spin_y.get())) 	
	scale=scale_echelle.get()
	octaves=scale_octaves.get()
	persistence=scale_persistence.get()
	lacunarity=scale_lacunarity.get()
	seed=int(spin_seed.get())
	facteur_denivele=scale_f_perlin.get()
	hauteur_ocean=scale_hauteur_ocean.get()
	couleur = liste_color.get()
	#genere la carte
	data_map_perlin =func_map_color_perlin(shape=shape,scale=scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,seed=seed,facteur_denivele=facteur_denivele,hauteur_ocean=hauteur_ocean,couleur_option=couleur)
	#actualise le canvas
	map_img_canvas=tk.PhotoImage(file='./carte_couleur.png')
	canvas_map.after(500,canvas_map.create_image(0,0,image=map_img_canvas, anchor=tk.NW))


def tk_3d_map_dc():
	'''Cette procédure est appelée lorsque l'utilisateur clique sur générer un fichier OBJ via diamant-carré.'''
	#récupère les données stockées dans les variables tampon
	px = data_map_dc.load()
	X, Y = data_map_dc.size
	#Creer le fichier obj
	with open("map.obj", "w") as carte:
		#v (coordonnées de points)
		for x in range(X):
			for y in range(Y):
				x, y = float(x), float(y)
				z=px[x,y]
				if z <=115:
					carte.write("v "+str(x)+" "+str(0)+" "+str(y)+"\n")
				else:
					carte.write("v "+str(x)+" "+str(float(z)-115)+" "+str(y)+"\n")	
		
		#vt (coordonnées de texture)
		for x in range(X):
			for y in range(Y,0,-1):
				i, j = x/X, y/Y	
				carte.write("vt "+str(i)+" "+str(j)+"\n")
		

		#f (faces)
		for x in range(X-1):
			for y in range(Y-1):
				num=(y*Y+x)+1
				carte.write("f "+str(num+Y)+"/"+str(num+Y)+" "+str(num+Y+1)+"/"+str(num+Y+1)+" "+str(num+1)+"/"+str(num+1)+" "+str(num)+"/"+str(num)+"\n")



def tk_3d_map_perlin():
	'''Cette procédure est appelée lorsque l'utilisateur clique sur générer un fichier OBJ via le bruit de perlin.'''
	#récupère les données stockées dans les variables tampon
	hauteur_ocean=scale_hauteur_ocean.get()
	px= data_map_perlin[0]
	X,Y = data_map_perlin[1][0], data_map_perlin[1][1]
	#Creer le fichier obj
	with open("map.obj", "w") as carte:
		#v (coordonnées de points)
		for x in range(X):
			for y in range(Y):
				z=px[x][y]
				if z <=hauteur_ocean:
					carte.write("v "+str(x)+" "+str(hauteur_ocean*500)+" "+str(y)+"\n")
				else:
					carte.write("v "+str(x)+" "+str((float(px[x][y])-hauteur_ocean)*500)+" "+str(y)+"\n")
		#vt (coordonnées de texture)
		for x in range(X):
			for y in range(Y,0,-1):
				i, j = x/X, y/Y	
				carte.write("vt "+str(i)+" "+str(j)+"\n")

		#f (faces)
		for x in range(X-1):
			for y in range(Y-1):
				num=(y*Y+x)+1
				carte.write("f "+str(num+Y)+"/"+str(num+Y)+" "+str(num+Y+1)+"/"+str(num+Y+1)+" "+str(num+1)+"/"+str(num+1)+" "+str(num)+"/"+str(num)+"\n")





#définition de la fenêtre
root = tk.Tk()
root.title("Génération de relief")

#définition du canvas + titre
label_appercu = tk.Label(root,text='Aperçu de la carte')
canvas_map = tk.Canvas(root)

#info user
label_info = tk.Label(root,text="Veuillez générer un apperçu 2D avant de générer le fichier obj")

#choix de la couleur
label_color_option = tk.Label(root, text = "Veuillez choisir le méthode de coloration :")
listeoption = ["Cartoon","Réaliste"]
liste_color = ttk.Combobox(root, values=listeoption)
liste_color.current(1)




#label diamant carre
label_diam_carre= tk.Label(root,text='Génération via\n la méthode Diamant-carré')
#n
scale_n=tk.Scale(root, orient='horizontal', from_=2, to=12,resolution=1, length=300,label='ordre de grandeur de la map (2^n)')
scale_n.set(7)
#f
scale_f=tk.Scale(root, orient='horizontal', from_=0, to=10,resolution=0.05, length=300,label='facteur de dénivelé')
scale_f.set(1)
#bouton generation 
bouton_map_dc_2d=tk.Button(root,text='Apperçu 2D',command=tk_2d_map_dc)
bouton_map_dc_3d=tk.Button(root,text='Génerer fichier OBJ',command=tk_3d_map_dc)



#label perlin noise
label_perlin= tk.Label(root,text='Génération via\n bruit de perlin')
#dimension image
label_spin_x = tk.Label(root,text='largeur :')
spin_x= tk.Spinbox(root,from_=200, to=1000,increment =1)
label_spin_y = tk.Label(root,text='hauteur :')
spin_y= tk.Spinbox(root,from_=200, to=1000,increment =1)
#echelle
scale_echelle=tk.Scale(root,orient='horizontal', from_=1, to=2000,resolution=1, length=300,label='Echelle')
scale_echelle.set(50)
#octaves
scale_octaves=tk.Scale(root,orient='horizontal', from_=1, to=10,resolution=1, length=300,label='Octaves')
scale_octaves.set(5)
#persitence
scale_persistence=tk.Scale(root,orient='horizontal', from_=-5, to=5,resolution=0.01, length=300,label='Persistence')
scale_persistence.set(0.5)
#lacunarity
scale_lacunarity=tk.Scale(root,orient='horizontal', from_=-5, to=5,resolution=0.01, length=300,label='lacunarity')
scale_lacunarity.set(2)
#seed
label_spin_seed =tk.Label(root,text='seed :')
spin_seed= tk.Spinbox(root,from_=0, to=2000,increment =1)
#facteur denivele
scale_f_perlin=tk.Scale(root, orient='horizontal', from_=-1, to=1,resolution=0.01, length=300,label='facteur de dénivelé')
scale_f_perlin.set(0.1)
#hauteur_ocean
scale_hauteur_ocean=tk.Scale(root, orient='horizontal', from_=-1, to=1,resolution=0.01, length=300,label='hauteur_ocean')
scale_hauteur_ocean.set(0)
#bouton generation 
bouton_map_perlin_2d=tk.Button(root,text='Apperçu 2D',command=tk_2d_map_perlin)
bouton_map_perlin_3d=tk.Button(root,text='Génerer fichier OBJ',command=tk_3d_map_perlin)


#Emplacement des éléments tkinter (grid)

#partie gauche
label_appercu.grid(row=0,column=0)
canvas_map.grid(row=1, column=0,rowspan=9)
label_info.grid(row=11,column=0)
label_color_option.grid(row=12,column=0)
liste_color.grid(row=13,column=0)

#partie droite

#diamant carre
label_diam_carre.grid(row=0,column=2,columnspan=4)
scale_n.grid(row=1,column=2,columnspan=4)
scale_f.grid(row=2,column=2,columnspan=4)
bouton_map_dc_2d.grid(row=3,column=1,columnspan=2)
bouton_map_dc_3d.grid(row=3,column=3,columnspan=2)

#perlin noise
label_perlin.grid(row=4,column=2,columnspan=4)
label_spin_x.grid(row=5,column=2)
spin_x.grid(row=5,column=3)
label_spin_y.grid(row=6,column=2)
spin_y.grid(row=6,column=3)
scale_echelle.grid(row=7,column=2,columnspan=4)
scale_octaves.grid(row=8,column=2,columnspan=4)
scale_persistence.grid(row=9,column=2,columnspan=4)
scale_lacunarity.grid(row=10,column=2,columnspan=4)
scale_f_perlin.grid(row=11,column=2,columnspan=4)
scale_hauteur_ocean.grid(row=12,column=2,columnspan=4)
label_spin_seed.grid(row=13,column=2)
spin_seed.grid(row=13,column=3)
bouton_map_perlin_2d.grid(row=14,column=1,columnspan=2,pady=10)
bouton_map_perlin_3d.grid(row=14,column=3,columnspan=2,pady=10)


root.mainloop()