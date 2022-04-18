# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:40:32 2022

@author: Abrah
"""

from poligonoConvexo import poligonoConvexo
from punto import punto
from plano import plano
from vector import vector
from utilidades import SIG_FIGURES, puntos_circulo, FLOAT_EPS, verificaElementoinLista, verificaElementosLista
import copy
import math
from seg_lin import seg_lin


class piramide(object):
    def __init__(self,pc,p,llamada=True):
        if llamada:
            print("La clase piramide es una geomtria auxiliar, usar la clase poliedroConvexo")
        if isinstance(pc,poligonoConvexo) and isinstance(p,punto):
            self.poligonoConv=pc
            self.punto=p
            if self.punto in self.poligonoConv.plano:
                raise ValueError("No se puede crear la piramide si el punto está en el plano")
        else:
            raise ValueError("Los valores introducidos no son del tipo poligonoConvexo y punto")

    def __repr__(self):
        return "Piramide({},{})".format(self.poligonoConv,self.punto)

    def altura(self):
        p0=self.poligonoConv.puntos[0]
        return abs(vector(p0,self.punto)*self.poligonoConv.plano.n.normalizar())

    def volumen(self):
        h=self.altura()
        return (1/3)*h*self.poligonoConv.area()


class poliedroConvexo(object):
    clase=5

    @classmethod
    def paralelepipedo(cls,base, v1,v2,v3):
        if isinstance(base,punto) and isinstance(v1,vector) and isinstance(v2, vector) and isinstance(v3, vector):
            if v1.magn()<FLOAT_EPS or v2.magn()<FLOAT_EPS or v3.magn()<FLOAT_EPS:
                raise ValueError("La magnitud de los vectores no puede ser cero")
            elif v1.paralelo(v2) or v1.paralelo(v3) or v2.paralelo(v3):
                raise ValueError("Los vectores no deben ser paralelos entre si")
            else:
                opuesto=copy.deepcopy(base).mover(v1).mover(v2).mover(v3)
                rec1=poligonoConvexo.paralelogramo(base,v1,v2)
                rec2=poligonoConvexo.paralelogramo(base,v1,v3)
                rec3=poligonoConvexo.paralelogramo(base,v2,v3)
                rec4=poligonoConvexo.paralelogramo(opuesto,-v2,-v3)
                rec5=poligonoConvexo.paralelogramo(opuesto,-v1,-v3)
                rec6=poligonoConvexo.paralelogramo(opuesto,-v1,-v2)
                return cls((rec1,rec2,rec3,rec4,rec5,rec6))
        else:
            raise TypeError("El paralelepipedo se construye con un punto y 3 vectores, alguno de los siguientes no es admitido {} {} {} {}".format(base,v1,v2,v3))
    @classmethod
    def esfera(cls,centro, radio, n1=10, n2=3):
        lista_pgc=[]
        cm=puntos_circulo(centro=centro, normal=vector.z_uni(), radio=radio, n=n1)
        lim_sup=copy.deepcopy(centro).mover(radio*vector.z_uni())
        lim_inf=copy.deepcopy(centro).mover(-radio*vector.z_uni())
        cs=[]
        ci=[]
        for i in range(n2-1):

            ang_i=math.pi*(i+1)/(2*n2)
            alt_i=radio*math.sin(ang_i)
            r_i=radio*math.cos(ang_i)

            cs.append(puntos_circulo(centro=copy.deepcopy(centro).mover(alt_i*vector.z_uni()),normal=vector.z_uni(),radio=r_i,n=n1))
            ci.append(puntos_circulo(centro=copy.deepcopy(centro).mover(-alt_i*vector.z_uni()),normal=vector.z_uni(),radio=r_i,n=n1))

        for i in range(n1):
            ini=i
            fin=(i+1)%n1
            #se construyen rectangulos con los puntos que forman los circulos
            lista_pgc.append(poligonoConvexo((cm[ini],cm[fin],cs[0][fin],cs[0][ini])))
            lista_pgc.append(poligonoConvexo((cm[ini],cm[fin],ci[0][fin],ci[0][ini])))

            for j in range(1,n2-1):
                #se construyen rectangulos con los puntos entre los ciruclos intermedios
                lista_pgc.append(poligonoConvexo((cs[j-1][ini],cs[j-1][fin],cs[j][fin],cs[j][ini])))
                lista_pgc.append(poligonoConvexo((ci[j-1][ini],ci[j-1][fin],ci[j][fin],ci[j][ini])))
            #cerrando la esfera
            lista_pgc.append(poligonoConvexo((lim_sup,cs[n2-2][fin],cs[n2-2][ini])))
            lista_pgc.append(poligonoConvexo((lim_inf,ci[n2-2][fin],ci[n2-2][ini])))

        return cls(tuple(lista_pgc))

    @classmethod
    def cilindro(cls,cent_circulo,radio, vector_alt,n=10):
        lim_sup=copy.deepcopy(cent_circulo).mover(vector_alt)

        circ_inf=poligonoConvexo.circulo(centro=cent_circulo,normal=vector_alt,radio=radio,n=n)
        circ_inf_puntos=puntos_circulo(centro=cent_circulo,normal=vector_alt,radio=radio,n=n)

        circ_sup=poligonoConvexo.circulo(centro=lim_sup,normal=vector_alt,radio=radio,n=n)
        circ_sup_puntos=puntos_circulo(centro=lim_sup,normal=vector_alt,radio=radio,n=n)

        lista_pgc=[circ_inf,circ_sup]
        
        #print(len(circ_sup_puntos))

        for i in range(len(circ_sup_puntos)):
            ini=i
            fin=(i+1)%len(circ_sup_puntos)
            lista_pgc.append(poligonoConvexo((circ_sup_puntos[ini],circ_sup_puntos[fin],circ_inf_puntos[fin],circ_inf_puntos[ini])))
            
                        
            
        return cls(tuple(lista_pgc))
    
    @classmethod
    def conoTruncado(cls,cent_circulo,radio_1, radio_2, vector_alt,n=10):
        lim_sup=copy.deepcopy(cent_circulo).mover(vector_alt)

        circ_inf=poligonoConvexo.circulo(centro=cent_circulo,normal=vector_alt,radio=radio_1,n=n)
        circ_inf_puntos=puntos_circulo(centro=cent_circulo,normal=vector_alt,radio=radio_1,n=n)

        circ_sup=poligonoConvexo.circulo(centro=lim_sup,normal=vector_alt,radio=radio_2,n=n)
        circ_sup_puntos=puntos_circulo(centro=lim_sup,normal=vector_alt,radio=radio_2,n=n)

        lista_pgc=[circ_inf,circ_sup]
        
        #print(len(circ_sup_puntos))

        for i in range(len(circ_sup_puntos)):
            ini=i
            fin=(i+1)%len(circ_sup_puntos)
            lista_pgc.append(poligonoConvexo((circ_sup_puntos[ini],circ_sup_puntos[fin],circ_inf_puntos[fin],circ_inf_puntos[ini])))
            
                        
            
        return cls(tuple(lista_pgc))

    def __init__(self, poli_conv, checar_convex=True):
        self.poligonos_convexos=list(copy.deepcopy(poli_conv))
        self.con_puntos=set()
        self.con_segm=set()
        self.piram=set()
        
        aux=[]
        auxp=[]        

        for poli_convexo in self.poligonos_convexos:
            
            for point in poli_convexo.puntos:
                if not auxp:
                    auxp.append(point)
                    
                elif not verificaElementoinLista(auxp, point):
                    auxp.append(point)
                    
                
            auxp=verificaElementosLista(auxp)
                
                
            for point in auxp:
                self.con_puntos.add(point)

            for segment in poli_convexo.segmentos():
                
                if not aux:
                    aux.append(segment)
                    
                elif not verificaElementoinLista(aux, segment):
                    aux.append(segment)
                
            aux=verificaElementosLista(aux)
                
            for segment in aux:
                self.con_segm.add(segment)
                

        self.punto_central=self.punto_central()
        #print(self.punto_central)

        for i in range(len(self.poligonos_convexos)):
            poligono_convexo=self.poligonos_convexos[i]
            if vector(self.punto_central,poligono_convexo.plano.p)*poligono_convexo.plano.n < -FLOAT_EPS:
                self.poligonos_convexos[i]=-poligono_convexo
            self.piram.add(piramide(poligono_convexo,self.punto_central,llamada=False))

        if not self._normales_():
            raise ValueError("No todas las normales apuntan afuera")

        if not self._car_euler_() and checar_convex:
            raise ValueError("Verificar los puntos, la geometria introducida no es convexa")


    def _car_euler_(self):
        num_puntos=len(self.con_puntos)
        num_seg=len(self.con_segm)
        num_caras=len(self.poligonos_convexos)

        return num_puntos-num_seg+num_caras == 2

    def _normales_(self):
        for poligono_convexo in self.poligonos_convexos:
            if vector(self.punto_central,poligono_convexo.plano.p)*poligono_convexo.plano.n < -FLOAT_EPS:
                return False
        return True

    def punto_central(self):
        x,y,z=0,0,0
        num_puntos=len(self.con_puntos)
        for point in self.con_puntos:
            x+=point.x
            y+=point.y
            z+=point.z

        return punto(x/num_puntos,y/num_puntos,z/num_puntos)

    def __repr__(self):
        return f"Poliedro Convexo({self.poligonos_convexos})"

    def __contains__(self,otro):
        if isinstance(otro,punto):
            for poligono in self.poligonos_convexos:
                vector_dir=vector(poligono.punto_cent,otro)
                if vector_dir*poligono.plano.n > FLOAT_EPS:
                    return False
            return True

        elif isinstance(otro,seg_lin):
            return ((otro.punto_in in self) and (otro.punto_fin in self))

        elif isinstance(otro,poligonoConvexo):
            for point in otro.puntos:
                if not point in self:
                    return False
            return True

        elif isinstance(otro,poliedroConvexo):
            for point in otro.con_puntos:
                if not point in self:
                    return False
            return True

        else:
            raise NotImplementedError("")

    def mover(self,v):
        if isinstance(v,vector):
            lista_poli=[]
            for poligono in self.poligonos_convexos:
                lista_poli.append(poligono.mover(v))

            self.poligonos_convexos=tuple(lista_poli)
            self.con_puntos=set()
            self.con_segm=set()
            self.piram=set()
            for poligono in self.poligonos_convexos:
                for point in poligono.puntos:
                    self.con_puntos.add(point)

                for segmento in poligono.segmetos():
                    self.con_segm.add(segmento)

            self.punto_central=self.punto_central()
            for i in range(len(self.poligonos_convexos)):
                poligono_convexo=self.poligonos_convexos[i]
                if vector(self.punto_central,poligono_convexo.plano.p)*poligono_convexo.plano.n < -FLOAT_EPS:
                    self.poligonos_convexos[i]=-poligono_convexo
                self.piram.add(piramide(poligono_convexo,self.punto_central,llamada=False))

            if not self._normales_():
                raise ValueError("No todas las normales apuntan afuera")

            if not self._car_euler_():
                raise ValueError("Verificar los puntos, la geometria introducida no cierra")

        else:
            raise TypeError("El parametro debe ser un vector, no un {}".format(type(v)))

    def long(self):
        l=0
        for segmento in self.con_segm:
            l+=segmento.long()
        return l

    def area(self):
        a=0
        for poligono in self.poligonos_convexos:
            a+=poligono.area()

        return a

    def volumen(self):
        v=0
        for piram in self.piram:
            v+=piram.volumen()
        return v

    def vertices(self):

        self.dict_puntos={}
        v=1
        for cara in self.poligonos_convexos:
            for point in cara.puntos:
                if point not in self.dict_puntos.values():
                    self.dict_puntos[v]=point
                    v+=1

        return self.dict_puntos

    def caras(self):
        self.caras=[]
        self.vertices()
        for cara in self.poligonos_convexos:
            llavev=[list(self.dict_puntos.keys())[list(self.dict_puntos.values()).index(point)] for point in cara.puntos]
            self.caras.append(llavev)

        return self.caras

    def _suma_puntos_hash(self):
        suma=0
        for i in self.con_puntos:
            suma+=hash(i)
        return suma

    def _suma_poligonos_hash(self):
        suma=0
        for i in self.poligonos_convexos:
            suma+=hash(i)
        return suma

    def __hash__(self):
        return hash(("poliedroConvexo", round(self._suma_poligonos_hash(),SIG_FIGURES),round(self._suma_puntos_hash(),SIG_FIGURES)))

if __name__=="__main__":
    poliedroConvexo.cilindro(punto(16, 0.0, 15.0), 7.1, vector(-15, 0.0, 0.0))
    
    lista=[punto(1,0,1),punto(1,0,0),punto(1,1,0)]
    
    if punto(1,0,1) in lista:
        print(lista.index(punto(1,0,1)))