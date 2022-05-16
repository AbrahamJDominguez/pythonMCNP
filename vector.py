# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:09:27 2022

@author: Abrah
"""
import math
from aux_vector import unifica_tipo, FLOAT_EPS

class vector(object):

    @classmethod
    def cero(cls):
        return cls(0,0,0)

    @classmethod
    def x_uni(cls):
        return cls(1,0,0)

    @classmethod
    def y_uni(cls):
        return cls(0,1,0)

    @classmethod
    def z_uni(cls):
        return cls(0,0,1)

    def __init__(self, *args):    #definimos las propiedades del vector
        if len(args)==3:          #si se reciben 3 argumentos se asume que es un vector del origen al punto
            self.v=list(args)
        elif len(args)==2:        #si se reciben 2 argumentos se asume que es el vector resultante de estos 2 (el orden cambiará la dirección)
            A,B=args
            self.v=[B.x-A.x,
                    B.y-A.y,
                    B.z-A.z]
        elif len(args)==1:       #lo mismo que con 3 argumentos, pero en esta ocasion se recibe un arreglo
            self.v=list(args[0])
        else:
            raise TypeError("La cantidad de argumentos entregados es incorrecta")
        self.v=unifica_tipo(self.v) #hacemos que el vector contenga solo un tipo de dato
        self.redond()

    def __repr__(self):
        return "Vector({}, {}, {})".format(*self.v)

    def __eq__(self,vectorb):    #se comparan los componentes para ver si es igual
        return abs(self.v[0] == vectorb.v[0] and self.v[1] == vectorb.v[1] and self.v[2] == vectorb.v[2])

    def __add__(self,vectorb):   #definimos la suma entre vectores
        return vector(x+y for x, y in zip(self, vectorb))

    def __sub__(self,vectorb):   #definimos la resta entre vectores
        return vector(x-y for x, y in zip(self, vectorb))

    def __mul__(self, vectorb):  #definimos la multiplicacion, se separa en 2 casos, con otro vector y con un escalar, se toma el p. punto
        if isinstance(vectorb, vector):
            return sum(x*y for x, y in zip(self, vectorb))
        return vector([x*vectorb for x in self.v])

    def __rmul__(self, vectorb): #es necesario definir que pasa si el vector se encuentra del lado derecho del producto, solo le decimos que cambie el orden
        return self * vectorb

    def __neg__(self): #definimos que hace al multiplicar por -1
        return -1*self

    def __getitem__(self,item): 
        return self.v[item]

    def __setitem__(self, item, valor):
        self.v[item]=valor
        
    def pcruz(self, vectorb):

        if isinstance(vectorb, vector):

            a, b = self.v, vectorb
                
            return vector( a[1]*b[2]-b[1]*a[2],
                           -a[0]*b[2]+b[0]*a[2],
                           a[0]*b[1]-b[0]*a[1])

    def magn(self):
        return (self*self)**(1/2)

    def normalizar(self):
        if self.magn()!=0:
            return float(1/self.magn())*self

        else:
            return vector.cero()

    def angulo(self,vectorb):
        return math.acos(self*vectorb/(self.magn()*vectorb.magn()))
    
    def proyectar(self, vectorb):
        return self*((self*vectorb)/self.magn()**2)

    def ortogonal(self, vectorb):
        return self*vectorb == 0

    def paralelo(self, vectorb):
        return abs(abs(self*vectorb)-abs(self.magn()*vectorb.magn()))<FLOAT_EPS #deben ser iguales si el angulo entre ellos es 0 o 180

    def redond(self, dec=8):
        self.v[0]=round(self.v[0],dec)
        self.v[1]=round(self.v[1],dec)
        self.v[2]=round(self.v[2],dec)
        
        if abs(self.v[0]) < FLOAT_EPS:
            self.v[0]=0
            
        if abs(self.v[1]) < FLOAT_EPS:
            self.v[1]=0
            
        if abs(self.v[2]) < FLOAT_EPS:
            self.v[2]=0
            
            
            