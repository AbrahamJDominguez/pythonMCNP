# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:37:33 2022

@author: Abrah
"""

from utilidades import puntos_circulo, FLOAT_EPS, area_triangulo
from punto import punto
from vector import vector
from plano import plano
import copy
import math
from seg_lin import seg_lin


class poligonoConvexo(object):
    clase=4
    @classmethod
    def circulo(cls,centro,normal,radio,n=10):
        return cls(puntos_circulo(centro,normal,radio,n))

    @classmethod
    def paralelogramo(cls,punto_base,v1,v2):
        if isinstance(punto_base,punto) and isinstance(v1,vector) and isinstance(v2,vector):
            if v1.magn()<FLOAT_EPS  or v2.magn()<FLOAT_EPS:
                raise ValueError("Vectores no validos")
            elif v1.paralelo(v2):
                raise ValueError("Los vectores no pueden ser paralelos")
            else:
                return cls((punto_base, copy.deepcopy(punto_base).mover(v1),
                            copy.deepcopy(punto_base).mover(v2),copy.deepcopy(punto_base).mover(v1).mover(v2)))
        else:
            raise TypeError("El paralelogramo requiere punto, vector, vector, no {}, {}, {}".format(type(punto_base),type(v1),type(v2)))

    def __init__(self,pts,reverso=False,checar_convex=False):
        puntos=copy.deepcopy(pts)
        self.puntos=sorted(set(puntos),key=puntos.index)
        #print(len(self.puntos))
        if len(puntos)<3:
            raise ValueError("La cantidad de puntos no es suficiente")
        if reverso:
            self.plano= -plano(self.puntos[0],self.puntos[1],self.puntos[2])
        else:
            self.plano= plano(self.puntos[0],self.puntos[1],self.puntos[2])
        
        self.punto_cent=self.punto_central()

        if checar_convex:   
            self.ordenar_puntos_concavo()

        else:
            self.ordenar_puntos()

    def __getitem__(self,item):
        return self.puntos[item]

    def punto_central(self):
        x,y,z=(0,0,0)
        num_puntos=len(self.puntos)
        for p in self.puntos:
            x+=p.x
            y+=p.y
            z+=p.z
        return punto(float(x)/num_puntos,float(y)/num_puntos,float(z)/num_puntos)

    def ordenar_puntos_concavo(self):
        normal=(self.plano.n).normalizar()
        v0=vector(self.punto_cent,self.puntos[0]).normalizar()
        v1=normal.pcruz(v0)
        dic_angulo_punto=dict()
        for point in self.puntos:
            pv = point.apunta()-self.punto_cent.apunta()
            coord_y=pv*v0
            coord_z=pv*v1
            angulo_vec=math.atan2(coord_z,coord_y)

            if angulo_vec<0:
                angulo_vec+=2*math.pi
            dic_angulo_punto[angulo_vec].append(point)

        for i in dic_angulo_punto.keys():
            if len(dic_angulo_punto[i]) >1:
                distancias=[]
                for j in dic_angulo_punto[i]:
                    distancias.append((j.apunta()-self.punto_cent.apunta()).magn())

                distancias.sort()



    def ordenar_puntos(self):

        normal=(self.plano.n).normalizar()
        v0=vector(self.punto_cent,self.puntos[0]).normalizar()
        v1=normal.pcruz(v0)
        dic_angulo_punto=dict()

        for point in self.puntos:
            if not point in self.plano:
                raise ValueError(f"No es convexo, el punto {point} no está en el plano {self.plano}")
            pv = point.apunta()-self.punto_cent.apunta()
            coord_y=pv*v0
            coord_z=pv*v1
            #print(f"{coord_y}, {coord_z}")
            angulo_vec=math.atan2(coord_z,coord_y)

            if angulo_vec<0:
                angulo_vec+=2*math.pi
            dic_angulo_punto[angulo_vec]=point

        lista_puntos=[dic_angulo_punto[ang] for ang in sorted(dic_angulo_punto)]
        self.puntos=tuple(lista_puntos)
        return True

    def segmentos(self):
        for i in range(len(self.puntos)):
            index0=i
            if i==(len(self.puntos)-1):
                index1=0
            else:
                index1=i+1
            yield seg_lin(self.puntos[index0],self.puntos[index1])

    def area(self):
        area=0
        for i in range(len(self.puntos)):
            index0=i
            if i==len(self.puntos)-1:
                index1=0
            else:
                index1=i+1
            area+=area_triangulo(self.punto_cent,self.puntos[index0],self.puntos[index1])
        return area

    def __repr__(self):
        return "Polígono de puntos {}".format(self.puntos)

    def __contains__(self,other):
        if isinstance(other, punto):
            r1 = other in self.plano
            normal=self.plano.n.normalizar()
            r2=True

            for i in range(len(self.puntos)):
                index0=i
                if i ==len(self.puntos) - 1:
                    index1=0
                else:
                    index1=i+1

                v0=vector(self.puntos[index0],self.puntos[index1])
                v1=normal.pcruz(v0)
                vec=vector(self.puntos[index0],other)
                if vec*v1<-FLOAT_EPS:
                    r2=False
                    break
            return r1 and r2
        elif isinstance(other,seg_lin):
            return (other.punto_in in self) and (other.punto_fin in self)
        else:
            return NotImplementedError("")

    def in_(self,other):
        if isinstance(other,plano):
            return self.plano == other
        else:
            raise TypeError("")

    def __eq__(self,other):
        if isinstance(other,poligonoConvexo):
            return (self.puntos == other.puntos)
        else:
            return False

    def __neg__(self):
        return poligonoConvexo(self.puntos, reverso=True)

    def __hash__(self):
        return hash(("poligonoConvexo",
        hash(self.plano) + hash(-self.plano),
        hash(self.plano) * hash(-self.plano)
        ))

    def long(self):
        long=0
        for seg in self.segmentos():
            long+=seg.long()
        return long

    def mover(self,v):

        if isinstance(v,vector):
            lista_puntos=[]
            for puntos in self.puntos:
                lista_puntos.append(puntos.mover(v))
            self.puntos = tuple(lista_puntos)
            self.plano=plano(self.puntos[0],self.puntos[1],self.puntos[2])
            self.punto_cent=self.punto_central()
            return poligonoConvexo(self.puntos)

        else:
            raise TypeError("El parametro debe ser un vector")

    def dict_punto(self):
        return dict((i+1,j) for i, j in enumerate(self.puntos))

    def triangulacion_delaunay(self):
        pass
