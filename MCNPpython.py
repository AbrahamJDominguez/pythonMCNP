from plano import plano
from poliedroConvexo import poliedroConvexo
from punto import punto
from vector import vector
from utilidades import FLOAT_EPS, isfloat, redond
import numpy as np
import copy
#print("hola")

planos=["p","px","py","pz"]
esferas=["so","sx","sy","sz","s"]
cilindros=["c/x","c/y","c/z","cx","cy","cz"]
macrocuerpos=["box","rcc","rpp", "sph", "trc"]

geometrias=(*planos, *esferas, *cilindros, *macrocuerpos)

superficies={"p":planos,"s":esferas,"c":cilindros}
superficiesGeom={"p":plano,"s":poliedroConvexo.esfera,"c":poliedroConvexo.cilindro}
macros={"trc":poliedroConvexo.conoTruncado,"box":poliedroConvexo.paralelepipedo,"rcc":poliedroConvexo.cilindro,"rpp":poliedroConvexo.paralelepipedo,"sph":poliedroConvexo.esfera}
figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}

params={"p":(4,9), "px":(1,),"py":(1,),"pz":(1,),"so":(1,),"sx":(2,),"sy":(2,),"sz":(2,),"c/x":(3,),"c/y":(3,),"c/z":(3,),
        "cx":(1,),"cy":(1,),"cz":(1,)}

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

    return len(lista), True

def listaFloat(lista,inicio=0,fin=-1):
	flotantes=[]; 
	if inicio==0 and fin==-1:
		for i in lista:
			flotantes.append(float(i))

	elif fin==-1:
		for i in range(inicio, len(lista)):
			flotantes.append(float(lista[i]))

	else:
		for i in range(inicio,fin):
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
		return plano().plano_xy().mover(vector(0,0,*param))

	else:
		raise ValueError(f" Se requieren 1 o 4 o 9 valores para iniciar plano, y elegir p, px, py, pz. Se dieron {len(param)} valores y tipo {tipo} ")

def planoaMCNP(plano):
    
    normal=plano.n
    p=plano.p
    
    if normal.paralelo(vector.x_uni()):
        #return (plano.for_gen()), "p"
        return (p.x), "px"
    
    elif normal.paralelo(vector.y_uni()):
        #return (plano.for_gen()), "p"
        return (p.y), "py"
    
    elif normal.paralelo(vector.z_uni()):
        #return (plano.for_gen()), "p"
        return (p.z), "pz"
    
    else:
        return (plano.for_gen()), "p"

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
    distancia_centro_punto=redond((esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()).magn())
    if esfera.punto_central == punto(0,0,0):

    	return (esfera.punto_central,distancia_centro_punto), "so"
    
    elif esfera.punto_central.y == 0 and esfera.punto_central.z == 0:
    	#distancia_centro_punto=esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()
    	return (esfera.punto_central.x,distancia_centro_punto), "sx"
    
    elif esfera.punto_central.x == 0 and esfera.punto_central.z == 0:
    	#distancia_centro_punto=esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()
    	return (esfera.punto_central.y,distancia_centro_punto), "sy"
    
    elif esfera.punto_central.x == 0 and esfera.punto_central.y == 0:
    	#distancia_centro_punto=esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()
    	return (esfera.punto_central.z,distancia_centro_punto), "sz"
    
    else:
        #distancia_centro_punto=esfera.punto_central.apunta()-list(esfera.con_puntos)[0].apunta()
        return (esfera.punto_central,distancia_centro_punto), "s"

def cilindroaMCNP(cilindro, lejos=100):
    if not lejos:
        lejos=100
        
    p=cilindro.poligonos_convexos[0].punto_cent
    p2=cilindro.poligonos_convexos[1].punto_cent.apunta()
    cond=False
    
    if (p.apunta()-p2).magn()>0 and (p.apunta()-p2).magn()>lejos:
        cond=True
        
    r=redond((cilindro.poligonos_convexos[0].punto_cent.apunta()-cilindro.poligonos_convexos[0].puntos[0].apunta()).magn())
    v=cilindro.poligonos_convexos[1].punto_cent.apunta()-cilindro.poligonos_convexos[0].punto_cent.apunta()
    
    if v.paralelo(vector.x_uni()) and (np.abs(p.y) > FLOAT_EPS  or np.abs(p.z) > FLOAT_EPS) and cond:
        return (p,r,v), "c/x"
    
    elif v.paralelo(vector.x_uni()) and (np.abs(p.y) < FLOAT_EPS  and np.abs(p.z) < FLOAT_EPS) and cond:
        return (p,r,v), "cx"
    
    elif v.paralelo(vector.y_uni()) and (np.abs(p.x) > FLOAT_EPS  or np.abs(p.z) > FLOAT_EPS) and cond:
        return (p,r,v), "c/y"
    
    elif v.paralelo(vector.y_uni()) and (np.abs(p.x) < FLOAT_EPS  and np.abs(p.z) < FLOAT_EPS) and cond:
        return (p,r,v), "cy"
    
    elif ((v.paralelo(vector.z_uni())) and (np.abs(p.y) > FLOAT_EPS  or np.abs(p.x) > FLOAT_EPS) and (cond)):
        return (p,r,v), "c/z"
    
    elif v.paralelo(vector.z_uni()) and (np.abs(p.y) < FLOAT_EPS  and np.abs(p.x) < FLOAT_EPS) and cond:
        return (p,r,v), "cz"
    
    else:
        return (p,r,v), "rcc"


def geomaMCNP(figs, figs_num, rec, lejos=100):
    
    cadena=""
    
    for fig in figs:
        if fig == "esferas":
            for i in range(len(figs[fig])):
                param=esferaaMCNP(figs[fig][i])
                num=figs_num[fig][i]
                
                if param[1] == "s":
                
                    cadena+=f"    {str(num)}       s {str(param[0][0].x)} {str(param[0][0].y)} {str(param[0][0].z)} {str(param[0][1])}\n"
                    
                elif param[1] == "so":
                    
                    cadena+=f"    {str(num)}       so {param[0][1]}\n"
                    
                else:
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0][0]} {param[0][1]}\n"
        
        elif fig == "cilindro":
            for i in range(len(figs[fig])):
                param=cilindroaMCNP(figs[fig][i], lejos)
                num=figs_num[fig][i]
                
                if param[1] == "rcc":
                
                    cadena+=f"    {str(num)}       rcc {str(param[0][0].x)} {str(param[0][0].y)} {str(param[0][0].z)} {str(param[0][2][0])} {str(param[0][2][1])} {str(param[0][2][2])} {str(param[0][1])}\n"
                    
                elif param[1] == "c/x":
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0][0].y} {param[0][0].z} {param[0][1]}\n"
                    
                elif param[1] == "c/y":
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0][0].x} {param[0][0].z} {param[0][1]}\n"
                    
                elif param[1] == "c/z":
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0][0].x} {param[0][0].y} {param[0][1]}\n"
                    
                elif param[1] == "cx" or param[1] == "cy" or param[1] == "cz":
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0][1]}\n"

        
        elif fig == "plano":
            for i in range(len(figs[fig])):
                param=planoaMCNP(figs[fig][i])
                num=figs_num[fig][i]
                
                if param[1] == "p":
                
                    cadena+=f"    {str(num)}       p {str(param[0][0])} {str(param[0][1])} {str(param[0][2])} {str(param[0][3])}\n"
                    
                else:
                    
                    cadena+=f"    {str(num)}       {param[1]} {param[0]}\n"
        
        elif fig == "conot":
            for i in range(len(figs[fig])):
                param=conoTruncadoaMCNP(figs[fig][i])
                num=figs_num[fig][i]
                
                cadena+=f"    {str(num)}       trc {str(param[0][0])} {str(param[0][1])} {str(param[0][2])} {str(param[0][3])} {str(param[0][4])} {str(param[0][5])} {str(param[0][6])} {str(param[0][7])}\n"
                
        elif fig == "paralelepipedos":
            for i in range(len(figs[fig])):
                param=ParalelepipedoaMCNP(figs[fig][i], rec,lejos=lejos)
                num=figs_num[fig][i]
                
                cadena+=f"    {str(num)}       {param[1]} "
                
                for i in param[0]:
                    cadena+=f"{str(i)} "
                    
                cadena+="\n"
                
        elif fig == "conot":
            for i in range(len(figs[fig])):
                param=conoTruncadoaMCNP(figs[fig][i])
                
                num=figs_num[fig][i] 
                cadena+=f"    {str(num)}       {param[1]} "
                
                for i in param[0]:
                    cadena+=f"{str(i)} "
                    
                cadena+="\n"
                
                
            
    figuras=cadena.split("\n")
                
    def orden(lista):
        l=lista.split(" ")
        while "" in l:
            l.remove("")
        
        if l:
            return int(l[0])
        
        else: 
            return 9999999
    
    
    figuras.sort(key=orden)
    figuras.pop()
    
    figuras="\n".join(figuras)
        

    return figuras

          
def MCNPacilindro(*param,tipo="rcc"):

	if tipo =="rcc":
		if len(param) == 7:
			centro=punto(param[0],param[1],param[2])
			vec=vector(param[3],param[4],param[5])
			r=param[6];
            
			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/x":
		if len(param) == 3:
			centro=punto(0,param[0],param[1])
			vec=vector(100,0,0);centro.mover(-(1/2)*vec)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/y":
		if len(param) == 3:
			centro=punto(param[0], 0, param[1])
			vec=vector(0,100,0);centro.mover(-(1/2)*vec)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "c/z":
		if len(param) == 3:
			centro=punto(param[0], param[1], 0)
			vec=vector(0,0,200);centro.mover(-(1/2)*vec)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)


	elif tipo == "cx":
		if len(param) == 1:
			centro=punto(-100,0,0)
			vec=vector(100,0,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "cy":
		if len(param) == 3:
			centro=punto(0, -100, 0)
			vec=vector(0,100,0)
			r=param[2]

			return poliedroConvexo.cilindro(centro, r, vec)

	elif tipo == "cz":
		if len(param) == 3:
			centro=punto(0, 0, -100)
			vec=vector(0,0,100)
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
        
def MCNPaParalelepipedo(*param, tipo="rpp"):
    #print(tipo)
    if tipo == "rpp":
        #print(len(param))
        if len(param) == 6:
            base=punto(param[0],param[2],param[4])
            vec1=vector( param[1] - param[0], 0, 0)
            vec2=vector( 0, param[3] - param[2], 0)
            vec3=vector( 0, 0, param[5]- param[4])
            
            return poliedroConvexo.paralelepipedo(base, vec1, vec2, vec3)
        
    elif tipo == "box":
        if len(param) == 9:
            alejar=100
            base=punto(param[0],param[1],param[2])
            vec1=vector( param[3], param[4], param[5])
            vec2=vector( param[6], param[7], param[8])
            vec3=(alejar/2)*vec1.pcruz(vec2)
            base.mover(vec3)
            
            return poliedroConvexo.paralelepipedo(base, vec1, vec2, vec3)
        
        elif len(param) == 12:
            base=punto(param[0],param[1],param[2])
            vec1=vector( param[3], param[4], param[5])
            vec2=vector( param[6], param[7], param[8])
            vec3=vector( param[9], param[10], param[11])
            
            return poliedroConvexo.paralelepipedo(base, vec1, vec2, vec3)
        
def ParalelepipedoaMCNP(paral, rec,lejos=100):
    cara=paral.poligonos_convexos[0]
    base=cara.puntos[0]
    cara2=paral.poligonos_convexos[1]
    vec1=cara.puntos[1].apunta()-base.apunta()
    vec2=cara.puntos[3].apunta()-base.apunta()
    idx=cara2.puntos.index(base)
    
    opuesto1=paral.poligonos_convexos[5].punto_cent.apunta()-paral.poligonos_convexos[0].punto_cent.apunta()
    opuesto2=paral.poligonos_convexos[4].punto_cent.apunta()-paral.poligonos_convexos[1].punto_cent.apunta()
    opuesto3=paral.poligonos_convexos[3].punto_cent.apunta()-paral.poligonos_convexos[2].punto_cent.apunta()
    
    if (opuesto1.magn() >= lejos or opuesto2.magn() >= lejos or opuesto3.magn() >= lejos) and paral != rec:
        if opuesto1.magn() >= lejos:
            return (*base, *opuesto2, *opuesto3), "box"
        
        if opuesto2.magn() >= lejos:
            return (*base, *opuesto1, *opuesto3), "box"
        
        if opuesto3.magn() >= lejos:
            return (*base, *opuesto1, *opuesto2), "box"          
    
    if idx + 1 > len(cara2.puntos)-1:
        cand1=0
        
    else:
        cand1= idx + 1
        
    if idx - 1 == -1:
        cand2=len(cara2.puntos)-1
        
    else:
        cand2= idx - 1
        
    vec3=cara2.puntos[cand1].apunta()-base.apunta()
    
    if vec3.paralelo(vec1) or vec3.paralelo(vec2):
        vec3=cara2.puntos[cand2].apunta()-base.apunta()
        if vec3.paralelo(vec1) or vec3.paralelo(vec2):
            raise ValueError("Error encontrado")
            
    if (vec1.paralelo(vector.x_uni()) or vec1.paralelo(vector.y_uni()) or vec1.paralelo(vector.z_uni()))\
    and (vec2.paralelo(vector.x_uni()) or vec2.paralelo(vector.y_uni()) or vec2.paralelo(vector.z_uni()))\
    and (vec3.paralelo(vector.x_uni()) or vec3.paralelo(vector.y_uni()) or vec3.paralelo(vector.z_uni())):
        x=0
        y=0
        z=0
        for vecs in [vec1, vec2, vec3]:
            if vecs.paralelo(vector.x_uni()):
                x=(copy.deepcopy(base).mover(vecs)).x
                
            elif vecs.paralelo(vector.y_uni()):
                y=(copy.deepcopy(base).mover(vecs)).y
                
            elif vecs.paralelo(vector.z_uni()):
                z=(copy.deepcopy(base).mover(vecs)).z
                
        return (base.x,x,base.y,y,base.z,z), "rpp"
    
    else:
        return (base.x, base.y, base.z, *vec1, *vec2, *vec3), "box"
            
    
        
        
def MCNPaConoTruncado(*param):
    if len(param) == 8:
        base=punto( param[0], param[1], param[2])
        vector_alt=vector( param[3], param[4], param[5])
        return poliedroConvexo.conoTruncado(base, param[6], param[7], vector_alt)
    
def conoTruncadoaMCNP(conot):
    base=conot.poligonos_convexos[0].punto_cent
    r1=(conot.poligonos_convexos[0].punto_cent.apunta()-conot.poligonos_convexos[0].puntos[0].apunta()).magn()
    r2=(conot.poligonos_convexos[1].punto_cent.apunta()-conot.poligonos_convexos[1].puntos[0].apunta()).magn()
    vec=conot.poligonos_convexos[1].punto_cent.apunta()-conot.poligonos_convexos[0].punto_cent.apunta()
    
    return (base.x, base.y, base.z, vec[0], vec[1], vec[2], r1, r2), "trc"
        
        
def MCNPGeomaLista(cadena, param_faltante=False):
    cadena=cadena.strip()
    lista=cadena.split(" ")
    
    while "" in lista:
        lista.remove("")
        
    if param_faltante:
        print(isfloat(lista[0]))
        print(verificarFloatLista(lista)[1])
        
    if not lista: 
        return False
        
    elif isfloat(lista[0]) and verificarFloatLista(lista)[1] and param_faltante:
        return float(lista[0])
    
    elif "c" in lista[0]:
        return False
    
    elif lista[0] == "mode":
        return "romper"
    
    elif lista[1].isnumeric():
        return False
    
    
    else:
        
        indice_dinero, _= verificarFloatLista(lista, 2)
        #print(indice_dinero, _)
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

            linea=linea.strip()
            #print(linea)
            lec=MCNPGeomaLista(linea)

            #print(lec)
            
            if not lec:
                continue
            
            elif lec == "romper":
                break
            
            if lec[1] not in geometrias:
                #print(lec[1])
                print("Lo sentimos, geometria por implementar")
                continue

            if lec:
                param=len(lec[2])
                
                if lec[1] in params:
                    
                    if param not in params[lec[1]]:
                        faltante=archivo.readline()
                        print(faltante)
                        
                        lec[2].append(MCNPGeomaLista(faltante, param_faltante=True))
                        #print(lec[2])
                
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
            
        return geom
    
def MCNPaGeom(con):
    
    figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}
    figuras_num={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}
    vol=0
    v=0
    rec=None
    
    for fig in con:
        
        print(fig)
        
        if fig[1][0] == "p":

            figuras_num["plano"].append(fig[0])
                
            figuras["plano"].append(MCNPaPlano(*fig[2], tipo=fig[1]))
            
        elif fig[1][0] == "s":
            figuras_num["esferas"].append(fig[0])
            f=MCNPaEsfera(*fig[2], tipo=fig[1])
            figuras["esferas"].append(f)
            v=f.volumen()
            if v > vol:
                vol=v
                rec=f
            
        elif fig[1][0] == "c" or fig[1] == "rcc":
            figuras_num["cilindro"].append(fig[0])
            f=MCNPacilindro(*fig[2], tipo=fig[1])
            figuras["cilindro"].append(f)
            v=f.volumen()
            if v > vol and fig[1] == "rcc":
                vol=v
                rec=f
            
        elif fig[1] == "rpp" or fig[1] == "box":
            #continue
            figuras_num["paralelepipedos"].append(fig[0])
            f=MCNPaParalelepipedo(*fig[2], tipo=fig[1])
            figuras["paralelepipedos"].append(f)
            v=f.volumen()
            if v > vol and len(fig[2]) in (6,2):
                vol=v
                rec=f
            
        elif fig[1] == "trc":
            figuras_num["conot"].append(fig[0])
            f=MCNPaConoTruncado(*fig[2])
            figuras["conot"].append(f)
            v=f.volumen()
            if v > vol:
                vol=v
                rec=f
        
    return figuras, figuras_num, rec
            

if __name__=="__main__":
    prueba="""    1       rpp -75 75 -75 75 -75 75  
    2       rpp -75 75 -75 75 -75 75"""

    flotantes=[MCNPGeomaLista(prueba)]
    
    print(flotantes)
    
    #if flotantes:
        
    #    print(flotantes)
        
    #    print(flotantes[1][0])
        
    #    print(flotantes[2])
    
    #muchotexto=lecturaMCNP("rayosx2.txt")
        
    #print(muchotexto)
    
    geometria=MCNPaGeom(flotantes)[0]
    #print(geometria)
    
    print(ParalelepipedoaMCNP(geometria["paralelepipedos"][0]))








