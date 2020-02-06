from diamant_carre import func_carte_hauteur
from PIL import Image


def func_color(px):
	'''Donne une couleur en fonction de px
	px : entier entre 0-255
	sortie : tuple (R,V,B)'''
	#océan profond
	if px <=20:
		color =(2, 45, 71)
	elif px <=40:
		color =(9, 59, 87)
	elif px <=60:
		color =(12, 77, 114)
	#océan
	elif px <=84:
		color =(16, 80, 110)
	elif px <=90:
		color =(23, 85, 112)
	elif px <=100:
		color =(33, 90, 113)
	#peu de profondeur
	elif px <=110:
		color =(43, 95, 115)
	#plages
	elif px <=115:
		color =(224, 205, 169)
	#plaines
	elif px <=130:
		color =(70, 115, 63)
	elif px <=145:
		color =(58, 100, 54)
	elif px <=160:
		color =(52, 92, 50)
	elif px <=180:
		color =(47, 87, 45)
	#forets
	elif px <=190:
		color =(42, 82, 39)
	elif px <=220:
		color =(32, 72, 29)
	#montage
	elif px <=230:
		color =(90, 68, 50)
	elif px <=235:
		color =(97, 75, 58)
	elif px <=240:
		color =(107, 85, 68)
	#roches
	elif px <=250:
		color =(122, 122, 122)
	elif px <=252:
		color =(132, 132, 132)
	#neige
	elif px <=254:
		color =(240, 240, 240)
	else:
		color =(255, 255, 255)

	return color

def func_color_perlin(px,hauteur_ocean=0):
	'''Donne une couleur en fonction de px
	px : float entre -1 et 1
	hauteur_ocean float entre -1 et 1
	sortie : tuple (R,V,B)'''
	#océan profond
	if px <=-0.75+hauteur_ocean:
		color =(2, 45, 71)
	elif px <=-0.5+hauteur_ocean:
		color =(9, 59, 87)
	elif px <=-0.45+hauteur_ocean:
		color =(12, 77, 114)
	#océan
	elif px <=-0.35+hauteur_ocean:
		color =(16, 80, 110)
	elif px <=-0.25+hauteur_ocean:
		color =(23, 85, 112)
	elif px <=-0.15+hauteur_ocean:
		color =(33, 90, 113)
	#peu de profondeur
	elif px <=-0.05+hauteur_ocean:
		color =(43, 95, 115)
	#plages
	elif px <=0.05+hauteur_ocean:
		color =(224, 205, 169)
	#plaines
	elif px <=0.2+hauteur_ocean:
		color =(70, 115, 63)
	elif px <=0.25+hauteur_ocean:
		color =(58, 100, 54)
	elif px <=0.3+hauteur_ocean:
		color =(52, 92, 50)
	elif px <=0.35+hauteur_ocean:
		color =(47, 87, 45)
	#forets
	elif px <=0.5+hauteur_ocean:
		color =(42, 82, 39)
	elif px <=0.8+hauteur_ocean:
		color =(32, 72, 29)
	#montage
	elif px <=0.85+hauteur_ocean:
		color =(90, 68, 50)
	elif px <=0.89+hauteur_ocean:
		color =(97, 75, 58)
	elif px <=0.91:
		color =(107, 85, 68)
	#roches
	elif px <=0.93+hauteur_ocean:
		color =(122, 122, 122)
	elif px <=0.98+hauteur_ocean:
		color =(132, 132, 132)
	#neige
	elif px <=0.999+hauteur_ocean:
		color =(240, 240, 240)
	else:
		color =(255, 255, 255)

	return color


def func_map_color(n=7,facteur=1,name='carte_couleur.png'):
	'''Créer une carte colorée en fonction de n (2^n)+1 px et du facteur de "dénivelé. name est le nom du fichier'''
	func_carte_hauteur(n,facteur) #creation d'une carte de hauteur (carte_hauteur.png)
	hauteur = Image.open('carte_hauteur.png') 
	px = hauteur.load()
	w, h = hauteur.size
	map_img = Image.new('RGB', (w,h), color=0)
	for x in range(w):
		for y in range(h):
			base_color=func_color(px[x,y]) #determine la couleur en fonction de la hauteur
			#f premet de rendre +- fade les couleurs (entre 0 et 1) 1 = carte de hauteur et 0 = couleurs vives
			f = 0.1
			color_to_add =(int(base_color[0]+((px[x,y]-base_color[0])*f)),int(base_color[1]+((px[x,y]-base_color[1])*f)),int(base_color[2]+((px[x,y]-base_color[2])*f)))	#nuance la couleur en fonction de la hauteur
			#print(color_to_add)
			map_img.putpixel((x,y),color_to_add)
	map_img.save(name)

#func_map_color(10,3)

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
	for x in range(w):
		for y in range(h):
			base_color=func_color_perlin(px[x][y],hauteur_ocean) #determine la couleur en fonction de la hauteur
			#f premet de rendre +- fade les couleurs (entre 0 et 1) 1 = carte de hauteur et 0 = couleurs vives
			f = 0.1
			color_to_add =(int(base_color[0]+((px[x][y]-base_color[0])*f)),int(base_color[1]+((px[x][y]-base_color[1])*f)),int(base_color[2]+((px[x][y]-base_color[2])*f)))	#nuance la couleur en fonction de la hauteur
			#print(color_to_add)
			map_img.putpixel((x,y),color_to_add)
	map_img.save(name)
	print('done, seed = ',seed)

def func_creation_n_cartes(n):
	for i in range(1,n):
		name = './exemples facteur 2/carte_hauteur_'+str(i)+'.png'
		func_map_color(10,2,name=name)

#func_creation_n_cartes(20)
