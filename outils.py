#Hugo Rey
#Generation de map 3d

#----------------------------
#█▀▄▀█ █▀█ █▀▄ █ █ █   █▀▀ █▀
#█ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█
#----------------------------
from PIL import Image
from random import randint, uniform, seed
from algorithmes import func_diamant_carre




def func_convert_to_pixels_values(n=7,facteur=1):
    '''converti chaque valeurs du tableau img en valeurs en nuance de gris (0-255)
    Sortie : une image (objet modifiable avec PIL)'''
    #chargement du tableau de valeur
    img= func_diamant_carre(n,facteur)
    h = len(img)
    #creation d'une image noire
    carte_hauteur = Image.new('L', (h,h), color=0)
    #parcourt chaque case de img
    for x in range(0,h):
        for y in range(0,h):            
            #et on met une nuance de gris entre 0 et 255 (127.5 étant le niveau 0, celui de la mer)
            carte_hauteur.putpixel((x,y),int(((img[x][y]*127.5)/h)+127.5))

    return carte_hauteur

def func_carte_hauteur(n=7,facteur=1):
    '''créer une carte de hauteur sous la forme d'une image png en fonction de n et du facteur de "dénivelé"
    Pour n = 7 (valeur par defaut): 129x129 pixels (0.2s)
    Pour n = 10 : 1025x1025 pixels (3.2s)
    Pour n = 12 : 4097x4097 pixels (51.5s)
    entre (), le temps de génération avec 8Go de RAM, i5-7400CPU 3.00GHz'''
    #creer une carte de hauteur
    carte_hauteur = func_convert_to_pixels_values(n,facteur)
    carte_hauteur.save('carte_hauteur.png')
    #message utilisateur
    '''
    d = (2**n)+1
    print('--carte_hauteur.png saved--')
    print('dimension: ',d,'x',d)
    '''
    return carte_hauteur

def func_color(px,hauteur_ocean=0,algo='dc'):
	'''Donne une couleur en fonction de px
	px : entier entre 0-255
	sortie : tuple (R,V,B)'''
	if algo=='dc':
		dico_hauteur_color = {
		#Océan profond
		(0,20):(2,45,71),
		(21,40):(9, 59, 87),
		(41,60):(12, 77, 114),
		#Océan
		(61,84):(16, 80, 110),
		(85,90):(23, 85, 112),
		(91,100):(33, 90, 113),
		#Peu de profondeur
		(101,110):(43, 95, 115),
		#Plages
		(111,115):(224, 205, 169),
		#Plaines
		(116,130):(70, 115, 63),
	    (131,145):(58, 100, 54),
	    (146,160):(52, 92, 50),
	    (161,180):(47, 87, 45),
	    #Forets
	 	(181,190):(42, 82, 39),
	 	(191,220):(32, 72, 29),
	 	#Montage
	    (221,230):(90, 68, 50),
	    (231,235):(97, 75, 58),
		(236,240):(107, 85, 68),
		#Roches
	    (240,250):(122, 122, 122),
		(251,252):(132, 132, 132),
		#Neige
		(253,254):(240, 240, 240),
		(255,255):(255, 255, 255)
		}

		for k in dico_hauteur_color.keys():
			if k[0]<=px<=k[1]:
				color =dico_hauteur_color[k]

	else:
		dico_hauteur_color = {
		#Océan profond
		(-1,-0.035):(2,45,71),
		(-0.0349,-0.04):(9, 59, 87),
		(-0.039,-0.030):(12, 77, 114),
		#Océan
		(-0.029,-0.025):(16, 80, 110),
		(-0.024,-0.020):(23, 85, 112),
		(-0.019,-0.015):(33, 90, 113),
		#Peu de profondeur
		(-0.014,-0.005):(43, 95, 115),
		#Plages
		(-0.004,0.0003):(224, 205, 169),
		#Plaines
		(0.0004,0.02):(70, 115, 63),
		(0.21,0.025):(58, 100, 54),
		(0.026,0.03):(52, 92, 50),
		(0.031,0.035):(47, 87, 45),
		#Forets
		(0.036,0.05):(42, 82, 39),
		(0.051,0.06):(32, 72, 29),
		#Montage
		(0.061,0.065):(90, 68, 50),
		(0.066,0.070):(97, 75, 58),
		(0.071,0.075):(107, 85, 68),
		#Roches
		(0.076,0.080):(122, 122, 122),
		(0.081,0.085):(132, 132, 132),
		#Neige
		(0.086,0.090):(240, 240, 240),
		(0.091,1):(255, 255, 255)
		}

		for k in dico_hauteur_color.keys():
			if k[0]<=px+hauteur_ocean<=k[1]:
				color =dico_hauteur_color[k]

	return color

def dans_img(X,Y, x, y):
    """Teste si les coordonnes x et y sont dans l'image de dimension X,Y."""
    return 0<=x<X and 0<=y<Y

def func_px_voisins(carte_hauteur,size, i, j,ancienne_position,algo='dc'):
	"""Donne la liste des coordonnées (tableaux de 2 entiers) des cases
	voisines de la case "(i,j)" X et Y sont les dimension de l'image.
	algo permet d'adapter la syntaxe...pour diamant-carré on utilise PIL alors que pour perlin noise
	On utilise simplement un tableau de python
	ancienne_position permet de sortir les voisin sauf celui sur lequel le curseur était avant.
	"""
	liste_px=[]
	coordo_px=[]
	if algo=='dc':								
		px=carte_hauteur
		X,Y = size[1],size[0]
		if dans_img(X,Y,i,j):
			if dans_img(X,Y,i-1,j-1) and (i-1,j-1)!=ancienne_position :
				liste_px.append(px[i-1,j-1])
				coordo_px.append([i-1,j-1])
			if dans_img(X,Y,i,j-1) and (i,j-1)!=ancienne_position :
				liste_px.append(px[i,j-1])
				coordo_px.append([i,j-1])
			if dans_img(X,Y,i+1,j-1) and (i+1,j-1)!=ancienne_position :
				liste_px.append(px[i+1,j-1])
				coordo_px.append([i+1,j-1])
			if dans_img(X,Y,i-1,j) and (i-1,j)!=ancienne_position :
				liste_px.append(px[i-1,j])
				coordo_px.append([i-1,j])
			if dans_img(X,Y,i+1,j) and (i+1,j)!=ancienne_position :
				liste_px.append(px[i+1,j])
				coordo_px.append([i+1,j])
			if dans_img(X,Y,i-1,j+1) and (i-1,j+1)!=ancienne_position :
				liste_px.append(px[i-1,j+1])
				coordo_px.append([i-1,j+1])
			if dans_img(X,Y,i,j+1) and (i,j+1)!=ancienne_position :
				liste_px.append(px[i,j+1])
				coordo_px.append([i,j+1])
			if dans_img(X,Y,i+1,j+1) and (i+1,j+1)!=ancienne_position :
				liste_px.append(px[i+1,j+1])
				coordo_px.append([i+1,j+1])
	else :										
		px= carte_hauteur
		
		X, Y = size[0], size[1]
		if dans_img(X,Y,i,j):
			if dans_img(X,Y,i-1,j-1):
				liste_px.append(px[i-1][j-1])
			if dans_img(X,Y,i,j-1):
				liste_px.append(px[i][j-1])
			if dans_img(X,Y,i+1,j-1):
				liste_px.append(px[i+1][j-1])
			if dans_img(X,Y,i-1,j):
				liste_px.append(px[i-1][j])
			if dans_img(X,Y,i+1,j):
				liste_px.append(px[i+1][j])
			if dans_img(X,Y,i-1,j+1):
				liste_px.append(px[i-1][j+1])
			if dans_img(X,Y,i,j+1):
				liste_px.append(px[i][j+1])
			if dans_img(X,Y,i+1,j+1):
				liste_px.append(px[i+1][j+1])


	return liste_px, coordo_px			

def func_color_devinele(pixels,hauteur_ocean=0,algo='dc'):
	'''
	pixels est une liste [px1,px2,px3,px4,px5,px6,px7,px8,px]
	choisi une couleur en fonction de "l'inclinaison" d'un pixel et de la hauteur de l'océan
	px1 px2 px3
	px4 px  px5
	px6 px7 px8
	algo est une chaine de caractère 'dc' ou 'perlin' : permet de savoir quel sera l'odre de grandeur des moyennes
	'''
	#px est le pixel central
	#print(pixels)
	#print(pixels[-1])
	px = pixels[-1]
	somme=0
	#color=(0,0,0)
	#on calcule la moyenne des ecart d'altitude par rapport au pixel central
	for i in range(0,len(pixels)-1):
		ecart =abs(px-pixels[i])
		#print(ecart)
		somme+=ecart
	pente=round(somme/len(pixels),5)


	if algo=='dc':
		#					Océan profonde 										Océan 												Peu de profondeur					Neige
		dico_hauteur_color = {(0,20):(2,45,71),(21,40):(9, 59, 87),(41,60):(12, 77, 114),(61,84):(16, 80, 110),(85,90):(23, 85, 112),(91,100):(33, 90, 113),(101,110):(43, 95, 115),(111,115):(224, 205, 169),(254,254):(240, 240, 240),(255,255):(255, 255, 255)}
		#					#plaine 																forets 						Montagne 											Roches
		dico_pente_color = {(0,0.5):(70, 115, 63),(0.51,1):(58, 100, 54),(1.01,1.5):(52, 92, 50),(1.51,1.75):(47, 87, 45),(1.76,2):(42, 82, 39),(2.01,2.5):(32, 72, 29),(2.51,3):(90, 68, 50),(3.01,4):(97, 75, 58),(4.01,4.5):(107, 85, 68),(4.51,5):(122, 122, 122),(5.01,255):(132, 132, 132)}

		if px+hauteur_ocean <=115 or 253<px+hauteur_ocean:
			for k in dico_hauteur_color.keys():
				if k[0]<=px+hauteur_ocean<=k[1]:
					color =dico_hauteur_color[k]
		else:
			for k in dico_pente_color.keys():
				if k[0]<=pente<=k[1]:
					color =dico_pente_color[k]

	else:

		#					Océan profonde 										Océan 												Peu de profondeur											Neige
		dico_hauteur_color = {(-1,-0.035):(2,45,71),(-0.034,-0.4):(9, 59, 87),(-0.39,-0.030):(12, 77, 114),(-0.029,-0.025):(16, 80, 110),(-0.024,-0.020):(23, 85, 112),(-0.019,-0.015):(33, 90, 113),(-0.014,-0.005):(43, 95, 115),(-0.004,0):(224, 205, 169),(0.9,0.9):(240, 240, 240),(1,1):(255, 255, 255)}
		#					#plaine 																forets 						Montagne 											Roches
		dico_pente_color = {(0,0.00050):(70, 115, 63),(0.00051,0.00100):(58, 100, 54),(0.00101,0.00150):(52, 92, 50),(0.00151,0.00200):(47, 87, 45),(0.00201,0.00230):(42, 82, 39),(0.00231,0.00250):(32, 72, 29),(0.00251,0.00300):(90, 68, 50),(0.00301,0.00330):(97, 75, 58),(0.00331,0.00350):(107, 85, 68),(0.00351,0.00400):(122, 122, 122),(0.00401,1):(132, 132, 132)}

		if px+hauteur_ocean <=0.0003 or 0.90<px+hauteur_ocean:
			for k in dico_hauteur_color.keys():
				if k[0]<=round(px+hauteur_ocean,3)<=k[1]:
					color =dico_hauteur_color[k]
		else:
			for k in dico_pente_color.keys():
				if k[0]<=pente<=k[1]:
					color =dico_pente_color[k]

	
	#print('-------------------------PENTE :',pente)
	#print(color)
	return color




#[les fonctions qui suivent ont des bugs à fixer]

def trace_river(carte_river,carte_hauteur,size,depart,hauteur_ocean,ancienne_position):
	'''Cette fonction trace un rivière jusqu'a la mer'''
	#print('En cours')
	px_hauteur = carte_hauteur
	img = carte_river
	x,y=depart[0],depart[1]
	#print(depart,px_hauteur[x,y])
	#si on a attein l'océan, on arrete de tracer la rivière
	if px_hauteur[x,y]<=hauteur_ocean:
		#print('Et elle est finie')
		return
	#sinon on continue
	else:
		#on met la case en bleu
		img[x,y]=(43, 95, 115)
		#on défini le prochain voisin
		data_voisins =func_px_voisins(carte_hauteur,size,x,y,ancienne_position)
		liste_hauteur,liste_coordos=data_voisins[0],data_voisins[1]
		#print(liste_coordos,liste_hauteur)
		futur_pixel=liste_coordos[liste_hauteur.index(min(liste_hauteur))]
		#print('FUTUR PIXEL',futur_pixel,min(liste_hauteur))
		#print("nous somme à une hauteur de :",px_hauteur[x,y],"Et la hauteur la plus basse autour est:",min(liste_hauteur),"Elle se situe en:",futur_pixel)
		if min(liste_hauteur)>px_hauteur[x,y]:
			#print('et elle descent plus..')
			#print("ON ERRODE")
			#print(px_hauteur[futur_pixel[0],futur_pixel[1]])
			px_hauteur[futur_pixel[0],futur_pixel[1]]=px_hauteur[x,y]-1 #on errode a la hauteur du pixel actuel
			#print(px_hauteur[futur_pixel[0],futur_pixel[1]])
			#on appele trace_river en recursif:
			trace_river(img,px_hauteur,size,depart,hauteur_ocean,(x,y))
		else:
			#on appele trace_river en recursif:
			trace_river(img,px_hauteur,size,futur_pixel,hauteur_ocean,(x,y))
	#print(carte_river)
	return carte_river



def func_add_river(data,size,higth_map,proba_apparition,hauteur_ocean,hauteur_depart_river):
	'''parcourt la carte de hauteur et pose démarre une rivière avec une certaine probilité''' 
	nb_riviere=0
	px_hauteur = higth_map
	w, h = size[0], size[1]
	#on parcourt chaque pixel de la carte de hauteur
	for x in range(w):
		for y in range(h):
			#print(px_hauteur[x,y])
			#si le pixel est assez haut
			if px_hauteur[x,y] >hauteur_ocean+hauteur_depart_river:
				#génération en fonction de la proba
				alea=uniform(0,1)
				if alea <=proba_apparition:
					#on ouvre la carte en couleur
					#print('on commence un rivière')
					#on met a jour la carte avec une rivière qui à été tracée
					carte_river=trace_river(carte_river=data,carte_hauteur=higth_map,size=size,depart=[x,y],hauteur_ocean=hauteur_ocean,ancienne_position='None')
					nb_riviere+=1
					#print('une rivière fait')

	#creation de l'image finale
	#Boucle pour creer une image a partir de map river 		
	map_river_final = Image.new('RGB', (w,h), color=0)
	for x in range(w):
		for y in range(h):
			pixel_to_add=carte_river[x,y]
			map_river_final.putpixel((x,y),pixel_to_add)
	map_river_final.save('carte_couleur_riviere.png')
	print('Nombre de rivière sur la map',nb_riviere)