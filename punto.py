# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:09:00 2022

@author: Abrah
"""
from vector import vector
import math
from utilidades import unifica_tipo, SIG_FIGURES, FLOAT_EPS

class punto(object):

    clase=0
    
    def __init__(self,*args):
        
        if len(args)==1: #caso en que se utiliza una lista
            cden=args[0]
        elif len(args)==3: #caso en que se introducen 3 valores fuera de una lista
            cden=args
        else:
            raise TypeError("Se deben introducir 3 valores o un arreglo")
        self.x, self.y, self.z = unifica_tipo(cden)
        self.redond()

    @classmethod
    def origen(cls):
        return cls(0,0,0)

    def __repr__(self):   #representación en el print
        return "Punto({:0.2f},{:0.2f},{:0.2f})".format(self.x,self.y,self.z)

    def __eq__(self, vecb): #comparación con otro punto
        return(self.x == vecb.x and self.y == vecb.y and self.z == vecb.z)
    
    def __getitem__(self,item):  #obtención de un elemento con índice [i]
        return(self.x, self.y, self.z)[item]
    
    def __setitem__(self,item,valor):   # asignación de valor 
        setattr(self, "xyz"[item], valor) #es importante poner xyz en "xyz"[item] porque buscará en el string en el orden que se haya escrito

    def apunta(self):
        return vector(self.x,self.y,self.z)

    def distancia(self,other):
        return math.sqrt((self.x -other.x) ** 2 + (self.y -other.y) ** 2 + (self.z -other.z) ** 2)

    def mover(self, v):
        if isinstance(v,vector):
            self.x += v[0]
            self.y += v[1]
            self.z += v[2]
            return punto(self.apunta())
        else:
            raise NotImplementedError("El segundo parametro debe ser un vector")

    def punto_arreglo(self):
        return [self.x, self.y, self.z]
    
    def redond(self, dec=8):
        self.x=round(self.x,dec)
        self.y=round(self.y,dec)
        self.z=round(self.z,dec)
        
        if abs(self.x) < FLOAT_EPS:
            self.x=0
            
        if abs(self.y) < FLOAT_EPS:
            self.y=0
            
        if abs(self.z) < FLOAT_EPS:
            self.z=0
        
        

    def __hash__(self):
        return hash(("Point",
        round(self.x,SIG_FIGURES),
        round(self.y,SIG_FIGURES),
        round(self.z,SIG_FIGURES),
        round(self.x,SIG_FIGURES) * round(self.y,SIG_FIGURES),
        round(self.x,SIG_FIGURES) * round(self.z,SIG_FIGURES),
        round(self.y,SIG_FIGURES) * round(self.z,SIG_FIGURES),
        ))

if __name__== "__main__":
    p=punto(1,2,2)
    print(p.x)