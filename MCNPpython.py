from plano import plano
from poliedroConvexo import poliedroConvexo
from punto import punto
from vector import vector

planos=["p","px","py","pz"]
esferas=["so","sx","sy","sz","s"]
cilindros=["c/x","c/y","c/z","cx","cy","cz"]
macrocuerpos=["box","rcc","rpp", "sph"]

geometrias=(*planos, *esferas, *cilindros, *macrocuerpos)

superficies={"p":planos,"s":esferas,"c":cilindros}
superficiesGeom={"p":plano,"s":poliedroConvexo.esfera,"c":poliedroConvexo.cilindro}
macros={"box":poliedroConvexo.paralelepipedo,"rcc":poliedroConvexo.cilindro,"rpp":poliedroConvexo.paralelepipedo,"sph":poliedroConvexo.esfera}

def verificarFloatLista(lista,inicio=0,fin=-1):
    if fin == -1:
        for i in range(inicio, len(lista)):
            try:
                float(lista[i])
            except:
                return lista.index(lista[i]), False

    else:
        for i in range(inicio, fin):
            print(i)
            try:
                float(lista[i])
            except:
                return lista.index(lista[i]), False

    return i, True

def listaFloat(lista,inicio=0,fin=-1):
	flotantes=[]; 
	if inicio==0 and fin==-1:
		for i in lista:
			flotantes.append(float(i))

	elif fin==-1:
		for i in range(inicio, len(lista)):
			flotantes.append(float(lista[i]))

	else:
		for i in range(inicio,fin+1):
			flotantes.append(float(lista[i])); 

	return flotantes

def MCNPaPlano(*param,tipo="p"):
	if tipo=="p":
		if len(param)==4:
			return plano(*param)

		elif len(param)==9:
			punto1=punto(param[0],param[1],param[2])
			punto2=punto(param[3],param[4],param[5])
			punto3=punto(param[6],param[7],param[8])
			return plano(punto1,punto2,punto3)

	elif tipo=="px" and len(param)==1:
		return plano().plano_yz().mover(vector(*param,0,0))

	elif tipo=="py" and len(param)==1:
		return plano().plano_xz().mover(vector(0,*param,0))

	elif tipo=="pz" and len(param)==1:
		return plano().plano_xz().mover(vector(0,0,*param))

	else:
		raise ValueError(f" Se requieren 1 o 4 o 9 valores para iniciar plano, y elegir p, px, py, pz. Se dieron {len(param)} valores y tipo {tipo} ")

def planoaMCNP(plano):

	return plano.for_gen()

def MCNPaEsfera(*param,tipo="s"):

	if tipo=="s" or tipo == "sph":
		if len(param)==4:
			centro=punto(param[0],param[1],param[2])
			return poliedroConvexo.esfera(centro, param[3])

	elif tipo=="so":
		if len(param)==1:
			centro=punto(0,0,0)
			return poliedroConvexo.esfera(centro,*param)

	elif tipo=="sx":
		if len(param)==2:
			centro=punto(param[0],0,0)
			return poliedroConvexo.esfera(centro,param[1])

	elif tipo=="sy":
		if len(param)==2:
			centro=punto(0,param[0],0)
			return poliedroConvexo.esfera(centro,param[1])

	elif tipo=="sz":
		if len(param)==2:
			centro=punto(0,0,param[0])
			return poliedroConvexo.esfera(centro,param[1])

	else:
		raise ValueError("Los valores introducidos no fueron validos para crear una esfera")

def esferaaMCNP(esfera):
	distancia_centro_punto=esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()
	return (esfera.punto_central,distancia_centro_punto.magn())

def cilindroaMCNP(cilindro):
	p=cilindro.poligonos_convexos[0].punto_cent
	r=(cilindro.poligonos_convexos[0].punto_cent.apunta()-cilindro.poligonos_convexos[0].puntos[0].apunta()).magn()
	v=cilindro.poligonos_convexos[3].puntos[0].apunta()-cilindro.poligonos_convexos[3].puntos[1].apunta()

	return p, r, v

def MCNPacilindro(*param,tipo="rcc"):

	if tipo =="rcc":
		if len(param) == 7:
			centro=punto(param[0],param[1],param[2])
			vec=vector(param[3],param[4],param[5])
			r=param[6]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/x":
		if len(param) == 3:
			centro=punto(0,param[0],param[1])
			vec=punto(100,0,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/y":
		if len(param) == 3:
			centro=punto(param[0], 0, param[1])
			vec=punto(0,100,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/z":
		if len(param) == 3:
			centro=punto(param[0], param[1], 0)
			vec=punto(0,0,100)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)


	elif tipo == "cx":
		if len(param) == 1:
			centro=punto(-100,0,0)
			vec=punto(100,0,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "cy":
		if len(param) == 3:
			centro=punto(0, -100, 0)
			vec=punto(0,100,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "cz":
		if len(param) == 3:
			centro=punto(0, 0, -100)
			vec=punto(0,0,100)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "gq":
		if len(param) == 7:
			centro=punto(param[0],param[1],param[2])
			vec=vector(param[3],param[4],param[5])
			centro=centro.mover(-10*vec)
			vec=20*vec
			r=param[7]

			return poliedroConvexo.cilindro(centro, r, vec)

	else:
		raise ValueError("El tipo ingresado no es compatible con los parametros ingresados ")
        
def MCNPaLista(cadena):
    lista=cadena.split(" ")
    
    while "" in lista:
        lista.remove("")
    
    if "c" in lista[0]:
        return False
    
    else:    
        
        indice_dinero, _= verificarFloatLista(lista, 2)
        lis=listaFloat(lista, inicio=2, fin= indice_dinero)
        num=int(lista[0])
        tipo=lista[1]
        
        return num, tipo, lis 
    

def lecturaMCNP(ruta_archivo):
    #import copy
    import numpy as np
    
    geom=[]
    #cont=0

    with open(ruta_archivo, "r") as archivo:
        
        for linea in archivo:
            cont=0
            
            lec=MCNPaLista(linea)
            
            if lec[1] not in geometrias:
                print("Lo sentimos, geometria por implementar")
                continue

            if lec:
                param=lec[2]
                
                if not geom:
                    geom.append(lec)
                    
                else:
                    
                    for i in range(len(geom)):
                        if lec[0] == geom[i][0]:
                            print("Posible error detectado, dos geometrias con el mismo id")
                            lec[0]=max(np.transpose(geom)[0])+1
                            
                    geom.append(lec)
                            
                        

            else:
                continue
            
            
if __name__=="__main__":
    prueba="""    1       rpp -75 75 -75 75 -75 75 """

    flotantes=MCNPaLista(prueba)
    
    if flotantes:
        
        print(flotantes)
        
        print(flotantes[1] in geometrias)
        
        print(flotantes[2])







