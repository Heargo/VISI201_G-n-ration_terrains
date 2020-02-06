import noise
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

'''
shape = (1024,1024)
scale = 100.0
octaves = 5
persistence = 0.5
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=0)
        
plt.imshow(world)
plt.show()
'''
def func_noise_map(shape=(100,100),scale=100.0,octaves=5, persistence=0.5,lacunarity=2.0,seed=0,facteur=1):
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
	#Creation d'un tableau de 0 de coté h
	t = []
	tempo=[]
	for x in range(shape[0]):
		for y in range(shape[1]):
			tempo+=[0]
		t+=[tempo]
		tempo=[]
	#rempli le tableau avec des valeurs entre -1 et 1 d'après le bruit de perlin.
	for i in range(shape[0]):
		for j in range(shape[1]):
			t[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed)
			t[i][j]*=facteur
	return t, shape, seed

#noise_map()
