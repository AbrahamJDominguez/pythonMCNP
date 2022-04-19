# -*- coding: utf-8 -*-
"""
#Utilidades

@author: Abrah
"""

from decimal import Decimal
from fractions import Fraction
import math
import copy
import numpy as np
from vector import vector


global SIG_FIGURES,FLOAT_EPS,SMALL_ANGLE
SIG_FIGURES = 10
FLOAT_EPS = 1 / (10 ** SIG_FIGURES)
SMALL_ANGLE=0.1

###############################################################################################################
############################ Funciones utiles #################################################################
###############################################################################################################

def verificaElementosLista(lista):
    sin_repetir=[]
    repetidos=[]
    
    for elem in lista:
        
        if not sin_repetir:
            sin_repetir.append(elem)
            
        else:
            if not verificaElementoinLista(sin_repetir, elem):#elem not in sin_repetir:
                sin_repetir.append(elem)
                
            else:
                repetidos.append(elem)
                
    
    for elem in sin_repetir:
        if sin_repetir.count(elem)>1:
            print("El filtro no funciono")
            verificaElementosLista(sin_repetir)
            
    return sin_repetir

def verificaElementoinLista(lista, elemento):
    
    hashes=[]
    
    for i in lista:
        hashes.append(hash(i))
    
    if hash(elemento) in hashes:
        return True
    
    else:
        return False
                

def keyValue(dic,valor):
    for i, j in dic.items():
        if j==valor:
            return i
    return False

def geomRenderVertices(poliedro):
    
    vertices={item: val.punto_arreglo() for item, val in enumerate(poliedro.con_puntos)}
    #print(vertices)
    return vertices

def geomRenderVertices2(poliedro,vertices):
    vertices2=geomRenderVertices(poliedro)
    orig=len(vertices)
    for num in vertices2:
        llave=keyValue(vertices, vertices2[num])
        if llave is False:
            #for item, val in enumerate(poliedro.con_puntos):
            vertices[orig] = vertices2[num]
            orig=len(vertices)
    #print(vertices)
    return vertices

def geomRenderCaras(poliedro, vertices:dict):
    caras=[]
    for cara in poliedro.poligonos_convexos:
            aux=[]
            for point in cara.puntos:
                llave=keyValue(vertices, point.punto_arreglo())
                #print(llave)

                if llave or llave==0:
                    aux.append(llave)

                else:
                    vertices[len(vertices)]=point.punto_arreglo()
                    #print(vertices)

            caras.append(aux)
    #print(caras)
    return caras, vertices

def puntos_circulo(centro, normal, radio, n=10):
    #print(normal)
    if n<=2:
        raise ValueError("n muy pequeña para construir un un poligono inscrito")
    if np.abs(normal.angulo(vector.x_uni()))<SMALL_ANGLE or np.abs(np.cos(normal.angulo(vector.x_uni())))==1:
        vector_base=vector.y_uni()
        if np.abs(normal.angulo(vector.y_uni()))< SMALL_ANGLE or np.abs(np.cos(normal.angulo(vector.y_uni())))==1:
            raise ValueError("No deberia poder ser normal a x e y")
    else:
        vector_base=vector.x_uni()
        
    #print(vector_base)
    v1=normal.normalizar().pcruz(vector_base).normalizar()
    v2=normal.normalizar().pcruz(v1)
    #print(v1, v2, "hola")
    v1=v1*radio
    v2=v2*radio
    lista_puntos=[]
    
    for i in range(n):
        angulo_i=(math.pi*2/n)*i
        
        lista_puntos.append(copy.deepcopy(centro).mover(v1*math.cos(angulo_i)+v2*math.sin(angulo_i)))
    
    #print(len(lista_puntos))
    return lista_puntos

def area_triangulo(pa,pb,pc):
    a=pa.distancia(pb)
    b=pb.distancia(pc)
    c=pc.distancia(pa)
    p=(a+b+c)/2
    return math.sqrt(p*(p-a)*(p-b)*(p-c))

def unifica_tipo(lista):
    tipos_valor = {
        Fraction: 1,
        Decimal: 2,
        float: 3,
        int: 4,
    }
    tipos = []
    for item in lista:
        for tipos_, valor in tipos_valor.items():
            if isinstance(item, tipos_):
                tipos.append((valor, tipos_))
                break
        else:
            tipos.append((0, type(item)))
    result_type = min(tipos)[1]
    return [result_type(i) for i in lista]

def isfloat(cadena):
    try:
        float(cadena)
        return True
    except:
        return False