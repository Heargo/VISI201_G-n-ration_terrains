#import des modules. Numpy pour gérer les tableaux et random pour l'aléatoire.
import numpy as np
from random import randint
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def diamant_carre(n):
    '''n est un entier naturel, il défini la taille du tableau grace a la formule suivante : (2^n)+1'''

    #calcul de la taille du tableau (hauteur)
    h = (2**n)+1
    #Creation d'un tableau de 0 de coté h
    t = np.zeros((h,h))
    #initialisation des premiers coins
    t[0, 0] = randint(-h, h)
    t[0, h-1] = randint(-h, h)
    t[h-1, h-1] = randint(-h, h)
    t[h-1, 0] = randint(-h, h)

    #initialisation du pas
    i = h-1
    while i > 1:
    	#d est le futur pas
        d = int(i/2) 

        #début phase diamant
        for x in range(d,h,i):
            for y in range(d,h,i):
                moyenne = (t[x-d,y-d] + t[x-d,y+d] + t[x+d,y+d] + t[x+d,y-d])/4
                t[x, y] = moyenne + randint(-d, d)

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
                    somme += t[x-d,y]
                    n +=1
                if x + d < h:
                    somme += t[x+d,y]
                    n +=1
                if y >= d:
                    somme +=t[x,y-d]
                    n +=1
                if y + d < h:
                    somme += t[x,y+d]
                    n +=1
                t[x, y] = somme/n + randint(-d, d)
        #mise à jour du pas
        i = d

    #renvoie le tableau
    return t

def dc_to_black_and_white(t):
    '''converti le tableau t en valeurs entre 0 et 255'''
    h = t.shape[0]
    #parcourt chaque case de t
    for x in range(0,h):
        for y in range(0,h):            
            #carte de hauteur
            t[x,y]=int(((t[x,y]*127.5)/h)+127.5)

    return t



n = 8
img_dc =  diamant_carre(n)

tbl_img =dc_to_black_and_white(img_dc)

#print(tbl_img)

plt.imshow(tbl_img)
plt.show()
