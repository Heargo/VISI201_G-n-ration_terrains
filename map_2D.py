#Hugo Rey
#Generation de map 3d

#----------------------------
#█▀▄▀█ █▀█ █▀▄ █ █ █   █▀▀ █▀
#█ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█
#----------------------------
from PIL import Image
from outils import func_carte_hauteur, func_color, func_color_devinele, func_px_voisins
from algorithmes import func_noise_map
#--------------------------------------------
#
#██████╗░██████╗░  ███╗░░░███╗░█████╗░██████╗
#╚════██╗██╔══██╗  ████╗░████║██╔══██╗██╔══██╗
#░░███╔═╝██║░░██║  ██╔████╔██║███████║██████╔╝
#██╔══╝░░██║░░██║  ██║╚██╔╝██║██╔══██║██╔═══╝ 
#███████╗██████╔╝  ██║░╚═╝░██║██║░░██║██║      
#╚══════╝╚═════╝░  ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝      
#
#-------------------------------------------



def func_map_color(n=7,facteur=1,name='carte_couleur.png'):
	'''Créer une carte colorée en fonction de n (2^n)+1 px et du facteur de "dénivelé. name est le nom du fichier'''
	hauteur = func_carte_hauteur(n,facteur)
	px = hauteur.load()
	w, h = hauteur.size
	map_img = Image.new('RGB', (w,h), color=0)
	for x in range(w):
		for y in range(h):
			#base_color=func_color(px[x,y]) #determine la couleur en fonction de la hauteur
			base_color=func_color_devinele(func_px_voisins(px,hauteur.size,x,y,ancienne_position='None')[0],0)
			#f premet de rendre +- fade les couleurs (entre 0 et 1) 1 = carte de hauteur et 0 = couleurs vives
			f = 0.1
			color_to_add =(int(base_color[0]+((px[x,y]-base_color[0])*f)),int(base_color[1]+((px[x,y]-base_color[1])*f)),int(base_color[2]+((px[x,y]-base_color[2])*f)))	#nuance la couleur en fonction de la hauteur
			#print(color_to_add)
			map_img.putpixel((x,y),color_to_add)
	map_img.save(name)
	#ajout de la rivière :
	carte_couleur=Image.open('carte_couleur.png')
	data_loaded=carte_couleur.load()
	carte_hauteur=Image.open('carte_hauteur.png')
	hightmap=carte_hauteur.load()
	w,h = carte_couleur.size
	#func_add_river(data_loaded,(w,h),hightmap,0.001,100,20)
	print('done')
	return hauteur


def func_map_color_perlin(shape=(1000,1000),scale=100.0,octaves=5, persistence=0.5,lacunarity=2.0,seed=0,name='carte_couleur.png',hauteur_ocean=0,facteur_denivele=1):
	'''Créer une carte en couleur. name est le nom du fichier
	Entrée:
	-shape, type tuple. C'est les dimension du tableau
	-scale, type float. C'est à quel point on "zoom"
	-octaves, type int. C'est la quantitées de couches de détails qui vont se supperposer
	-persistence, type float. C'est l'impact que les octaves ont sur la forme générale
	-lacunarity, type float. C'est la quantitée de détails pris en compte pour les octaves
	-seed, type int. C'est la seed du tableau. Par défaut elle est à 0. Pour générer quelque-chose d'aléatoire il faut utiliser un random.'''
	map_data = func_noise_map(shape=shape,scale=scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,seed=seed,facteur=facteur_denivele)
	px= map_data[0]
	w, h = map_data[1][0], map_data[1][1]
	map_img = Image.new('RGB', (w,h), color=0)
	for y in range(h):
		for x in range(w):
			#print(px[x][y]+hauteur_ocean)
			base_color=func_color_devinele(func_px_voisins(px,map_data[1],x,y,algo='perlin',ancienne_position='None')[0],hauteur_ocean,algo='perlin')	#determine la couleur en fonction de la pente
			#base_color=func_color(px[x][y],hauteur_ocean=hauteur_ocean,algo='perlin') 													#determine la couleur en fonction de la hauteur
			#f premet de rendre +- fade les couleurs (entre 0 et 1) 1 = carte de hauteur et 0 = couleurs vives
			f = 0.1
			color_to_add =(int(base_color[0]+((px[x][y]-base_color[0])*f)),int(base_color[1]+((px[x][y]-base_color[1])*f)),int(base_color[2]+((px[x][y]-base_color[2])*f)))	#nuance la couleur en fonction de la hauteur
			#print(color_to_add)
			map_img.putpixel((x,y),color_to_add)
	map_img.save(name)
	print('done, seed = ',seed)
	return map_data


def func_creation_n_cartes(n):
	'''n est le nombre de carte'''
	for i in range(n):
		name = './exemples/carte_hauteur_'+str(i)+'.png'
		func_map_color(9,4,name=name)
