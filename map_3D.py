#Hugo Rey
#Generation de map 3d

#----------------------------
#█▀▄▀█ █▀█ █▀▄ █ █ █   █▀▀ █▀
#█ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄█
#----------------------------
from PIL import Image
from map_2D import func_map_color, func_map_color_perlin

#---------------------------------------------------
#█▀▄ █ ▄▀█ █▀▄▀█ ▄▀█ █▄ █ ▀█▀ ▄▄ █▀▀ ▄▀█ █▀█ █▀█ █▀▀
#█▄▀ █ █▀█ █ ▀ █ █▀█ █ ▀█  █     █▄▄ █▀█ █▀▄ █▀▄ ██▄
#---------------------------------------------------

def func_obj_generation(n=7,f=4):
	hauteur= func_map_color(n,f)
	px = hauteur.load()
	X, Y = hauteur.size
	
	with open("map.obj", "w") as carte:
		for x in range(X):
			for y in range(Y):
				x, y = float(x), float(y)
				z=px[x,y]
				if z <=115:
					carte.write("v "+str(x)+" "+str(0)+" "+str(y)+"\n")
				else:
					carte.write("v "+str(x)+" "+str(float(z)-115)+" "+str(y)+"\n")	
		
		#vt
		for x in range(X):
			for y in range(Y,0,-1):
				i, j = x/X, y/Y	#test valeur entre 0 et 1
				carte.write("vt "+str(i)+" "+str(j)+"\n")
		

		#f
		for x in range(X-1):
			for y in range(Y-1):
				num=(y*Y+x)+1
				carte.write("f "+str(num+Y)+"/"+str(num+Y)+" "+str(num+Y+1)+"/"+str(num+Y+1)+" "+str(num+1)+"/"+str(num+1)+" "+str(num)+"/"+str(num)+"\n")



#------------------------------------------
#█▀█ █▀▀ █▀█ █   █ █▄ █   █▄ █ █▀█ █ █▀ █▀▀
#█▀▀ ██▄ █▀▄ █▄▄ █ █ ▀█   █ ▀█ █▄█ █ ▄█ ██▄
#------------------------------------------

def func_obj_generation_perlin(shape=(1000,1000),scale=500.0,octaves=5, persistence=0.5,lacunarity=2.0,seed=0,name='carte_couleur.png',hauteur_ocean=0,facteur_denivele=0.3):
	map_data = func_map_color_perlin(shape=shape,scale=scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,seed=seed,facteur_denivele=facteur_denivele,hauteur_ocean=hauteur_ocean)
	px= map_data[0]
	X,Y = map_data[1][0], map_data[1][1]
	with open("map.obj", "w") as carte:
		for x in range(Y):
			for y in range(X):
				carte.write("v "+str(x)+" "+str(float(px[x][y])*500)+" "+str(y)+"\n")
					
		#vt
		for x in range(X):
			for y in range(Y,0,-1):
				i, j = round(x/X,2), round(y/Y,2)		#test valeur entre 0 et 1
				carte.write("vt "+str(i)+" "+str(j)+"\n")

		#f
		for x in range(Y-1):
			for y in range(X-1):
				num=(y*Y+x)+1
				carte.write("f "+str(num+Y)+"/"+str(num+Y)+" "+str(num+Y+1)+"/"+str(num+Y+1)+" "+str(num+1)+"/"+str(num+1)+" "+str(num)+"/"+str(num)+"\n")