#Hugo Rey
#Generation de map 3d

#----------------------------
#█▀▄▀█ █▀█ █▀▄ █ █ █   █▀▀ █▀
#█ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█
#----------------------------
from random import randint, uniform
import noise


#---------------------------------------------------
#█▀▄ █ ▄▀█ █▀▄▀█ ▄▀█ █▄ █ ▀█▀ ▄▄ █▀▀ ▄▀█ █▀█ █▀█ █▀▀
#█▄▀ █ █▀█ █ ▀ █ █▀█ █ ▀█  █     █▄▄ █▀█ █▀▄ █▀▄ ██▄
#---------------------------------------------------

def func_diamant_carre(n,f):
	'''n est un entier naturel, il défini la taille du tableau grace a la formule suivante : (2^n)+1
	f est le facteur de "dénivelé" plus il est bas, plus le paysage ressembleras à une plaine, plus il est
	élevé, plus les paysages seront abruptes'''

	#calcul de la taille du tableau (hauteur)
	h = (2**n)+1
	#Creation d'un tableau de 0 de coté h
	t = []
	tempo=[]
	for x in range(h):
		for y in range(h):
			tempo+=[0]
		t+=[tempo]
		tempo=[]

	#print(t)
	#initialisation des premiers coins
	t[0][0] = randint(-h,h)
	t[0][h-1] = randint(-h,h)
	t[h-1][h-1] = randint(-h,h)
	t[h-1][0] = randint(-h,h)

	#initialisation du pas
	i = h-1
	while i > 1:
		#d est le futur pas
		d = int(i/2) 

		#début phase diamant
		for x in range(d,h,i):
			for y in range(d,h,i):
				moyenne = (t[x-d][y-d] + t[x-d][y+d] + t[x+d][y+d] + t[x+d][y-d])/4
				#en fonction de la moyenne de hauteur, on calcul différement le nouveau point...
				#si on est inférieur a la moitié de la hauteur max...
				if moyenne <=h/2:
					t[x][y] = moyenne + randint(int(-d*f),int(d*f))
				#si on est entre la moitié et le dernier tiers...
				elif moyenne<=2*h/3 :
					t[x][y] = moyenne - randint(int(-d*f),int(d*f))
				#si on est dans le dernier tier...
				else :
					t[x][y] = moyenne - randint(0,int(d*f))


		decalage = 0

		#début phase du carré
		for x in range(0,h,d):
			if decalage == 0:
				decalage = d
			else:
				decalage = 0
			for y in range(decalage,h,i):
				somme = 0
				n = 0
				if x >= d:
					somme += t[x-d][y]
					n +=1
				if x + d < h:
					somme += t[ x+d][y]
					n +=1
				if y >= d:
					somme +=t[x][y-d]
					n +=1
				if y + d < h:
					somme += t[x][y+d]
					n +=1
				t[x][y] = somme/n + randint(int(-d*f),int(d*f))
		#mise à jour du pas
		i = d
	#renvoie le tableau
	return t


#------------------------------------------
#█▀█ █▀▀ █▀█ █   █ █▄ █   █▄ █ █▀█ █ █▀ █▀▀
#█▀▀ ██▄ █▀▄ █▄▄ █ █ ▀█   █ ▀█ █▄█ █ ▄█ ██▄
#------------------------------------------

def func_noise_map(shape,scale,octaves, persistence,lacunarity,seed,facteur):
	'''Renvoie un tableau créer grace au bruit de perlin. Les valeurs du tableau sont comprises entre -1 et 1
	Entrée:
	-shape, type tuple. C'est les dimension du tableau
	-scale, type float. C'est à quel point on "zoom"
	-octaves, type int. C'est la quantitées de couches de détails qui vont se supperposer
	-persistence, type float. C'est l'impact que les octaves ont sur la forme générale
	-lacunarity, type float. C'est la quantitée de détails pris en compte pour les octaves
	-seed, type int. C'est la seed du tableau. Par défaut elle est à 0. Pour générer quelque-chose d'aléatoire il faut utiliser un random.
	Sortie : un tuple qui comporte : (tableau,shape,seed)
	'''
	#Creation d'un tableau remplit de 0 de coté h
	t = []
	tempo=[]
	for x in range(shape[0]):
		for y in range(shape[1]):
			tempo+=[0]
		t+=[tempo]
		tempo=[]
	#rempli le tableau avec des valeurs entre -1*facteur et 1*facteur d'après le bruit de perlin.
	for i in range(shape[0]):
		for j in range(shape[1]):
			t[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed)
			t[i][j]*=facteur
	return t, shape, seed
