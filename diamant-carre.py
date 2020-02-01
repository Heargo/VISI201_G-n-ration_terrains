#import des modules.
from random import randint
from PIL import Image


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
                t[x][y] = moyenne + randint(int(-d*f),int(d*f))

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
                t[x][y] = somme/n + randint(int(-d*f),int(d*f))
        #mise à jour du pas
        i = d
    #renvoie le tableau
    return t

def func_tableau_to_img(t):
    '''converti chaque valeurs du tableau t en valeurs en nuance de gris (0-255)
    Sortie : une image (objet modifiable avec PIL)'''
    h = len(t)
    carte_hauteur = Image.new('L', (h,h), color=0)
    #parcourt chaque case de t
    for x in range(0,h):
        for y in range(0,h):            
            #carte de hauteur
            carte_hauteur.putpixel((x,y),int(((t[x][y]*127.5)/h)+127.5))

    return carte_hauteur

def func_carte_hauteur(n=7,facteur=1):
    '''créer une carte de hauteur sous la forme d'une image png en fonction de n et du facteur de "dénivelé"
    Pour n = 7 (valeur par defaut): 129x129 pixels (0.2s)
    Pour n = 10 : 1025x1025 pixels (3.2s)
    Pour n = 12 : 4097x4097 pixels (51.5s)
    entre (), le temps de génération avec 8Go de RAM, i5-7400CPU 3.00GHz'''
    carte_hauteur = func_tableau_to_img(func_diamant_carre(n,facteur))
    carte_hauteur.save('carte_hauteur.png')
    d = (2**n)+1
    print('--carte_hauteur.png saved--')
    print('dimension: ',d,'x',d)


func_carte_hauteur()
