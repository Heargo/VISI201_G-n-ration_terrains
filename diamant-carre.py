#import des modules.
from random import randint
from PIL import Image

def diamant_carre(n):
    '''n est un entier naturel, il défini la taille du tableau grace a la formule suivante : (2^n)+1'''

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
    t[0][0] = randint(-h, h)
    t[0][h-1] = randint(-h, h)
    t[h-1][h-1] = randint(-h, h)
    t[h-1][0] = randint(-h, h)

    #initialisation du pas
    i = h-1
    while i > 1:
    	#d est le futur pas
        d = int(i/2) 

        #début phase diamant
        for x in range(d,h,i):
            for y in range(d,h,i):
                moyenne = (t[x-d][y-d] + t[x-d][y+d] + t[x+d][y+d] + t[x+d][y-d])/4
                t[x][y] = moyenne + randint(-d, d)

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
                    somme += t[x+d][y]
                    n +=1
                if y >= d:
                    somme +=t[x][y-d]
                    n +=1
                if y + d < h:
                    somme += t[x][y+d]
                    n +=1
                t[x][y] = somme/n + randint(-d, d)
        #mise à jour du pas
        i = d

    #renvoie le tableau
    return t

def tableau_to_img(t):
    '''converti le tableau t en valeurs entre 0 et 255'''
    h = len(t)
    carte_hauteur = Image.new('L', (h,h), color=0)
    #parcourt chaque case de t
    for x in range(0,h):
        for y in range(0,h):            
            #carte de hauteur
            carte_hauteur.putpixel((x,y),int(((t[x][y]*127.5)/h)+127.5))


    carte_hauteur.save('carte_hauteur.png')



n = 5
tableau_diamant_carre =  diamant_carre(n)
tableau_to_img(tableau_diamant_carre)
