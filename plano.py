# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:17:41 2022

@author: Abrah
"""
from punto import punto
from vector import vector
from solucion import resuelve
from utilidades import SIG_FIGURES, FLOAT_EPS
from linea import linea
from objeto import objeto
import copy

class plano(objeto):
    clase=2

    @classmethod
    def plano_xy(cls):
        return cls(punto.origen(),vector.z_uni())

    @classmethod
    def plano_yz(cls):
        return cls(punto.origen(),vector.x_uni())

    @classmethod
    def plano_xz(cls):
        return cls(punto.origen(),vector.y_uni())

    def __repr__(self):
        return "Plano ({},{}) = 0".format(self.n,self.p)

    def in_general(self,a,b,c,d):
        sol=resuelve([[a,b,c,d]])
        self.n=vector(a,b,c).normalizar()
        self.p=punto(*sol(1,1))

    def in_punto_normal(self,p,normal):
        self.p=p
        self.n=normal.normalizar()

    def __init__(self, *args):
        if len(args)==3:
            a,b,c=args
            if (isinstance(a,punto) and isinstance(b,punto) and isinstance(c,punto)):
                vab=b.apunta()-a.apunta()
                vac=c.apunta()-a.apunta()

            elif(isinstance(a,punto) and isinstance(b,vector) and isinstance(c,vector)):
                vab, vac=b,c
                
            vec=vab.pcruz(vac)
            self.in_punto_normal(a,vec)

        elif len(args)==2:
            self.in_punto_normal(*args)

        elif len(args)==4:
            self.in_general(*args)  

    def __contains__(self,b):
        if isinstance(b,punto):
            #print(abs(b.apunta()*self.n-self.p.apunta()*self.n))
            return abs(b.apunta()*self.n-self.p.apunta()*self.n)<FLOAT_EPS
        if isinstance(b,linea):
            return punto(b.il) in self and paralelo(self,b)
        elif b.clase>self.clase:
            b.in_(self)
        else:
            raise NotImplementedError("")

    def __eq__(self, b):
        if isinstance(b, plano):
            return self.p in b and self.n.paralelo(b.n)
        else:
            return False
    def __neg__(self):
        return plano(self.p,-self.n)

    def __hash__(self):
        return hash(("plano",round(self.n[0],SIG_FIGURES),round(self.n[1],SIG_FIGURES),round(self.n[2],SIG_FIGURES),round(self.n * self.p.apunta(),SIG_FIGURES)))

    def punto_normal(self):
        return (self.p.apunta(),self.n)

    def for_gen(self):
        return(self.n[0],self.n[1],self.n[2],self.n*self.p.apunta())

    def f_param(self):
        s=resuelve([list(self.n)+[0]])
        v=vector(*s(1,1))
        
        assert v.ortogonal(self.n)

        s=resuelve([list(self.n)+[0],list(v)+[0],])
        w=vector(*s(1))
        return (self.p.apunta(),v,w)

    def mover(self,v):
        if isinstance(v,vector):
            self.p.mover(v)
            return plano(self.p,self.n)
        else:
            return NotImplementedError("El segundo parametro debe ser un vector")
        
    def crear_poli(self, lejos=100):
        from poligonoConvexo import poligonoConvexo
        
        param=self.for_gen()
        
        if abs(param[0])>0 and abs(param[1])>0 and abs(param[2])>0:
            
            p1=(-(param[0]*(-lejos)+param[1]*(-lejos))+param[3])/param[2]
            p2=(-(param[0]*p1+param[2]*(lejos/2))+param[3])/param[1]
            p3=(-(param[1]*p1+param[2]*p2)+param[3])/param[0]
            p4=(-(param[1]*(lejos)+param[2]*(lejos))+param[3])/param[0]
            
            p1=punto((-lejos),(-lejos), p1)
            p2=punto(p1.x, p2,(lejos/2))
            p3=punto(p3, p2.y, p1.z)
            p4=punto(p4,(lejos),(lejos))
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            return pol
        
        elif abs(param[0])!=0 and abs(param[1])==0 and abs(param[2])==0:
            
            p1=punto(param[3],-lejos, lejos)
            p2=punto(param[3], -lejos, -lejos)
            p3=punto(param[3], lejos, -lejos)
            p4=punto(param[3],lejos, lejos)
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            return pol
        
        elif abs(param[1])!=0 and abs(param[2])==0 and abs(param[0])==0:
            
            p1=punto(-lejos, param[3], lejos)
            p2=punto( -lejos, param[3], -lejos)
            p3=punto(lejos, param[3], -lejos)
            p4=punto(lejos, param[3],lejos)
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            return pol
        
        elif abs(param[2])!=0 and abs(param[1])==0 and abs(param[0])==0:
            
            p1=punto(-lejos, lejos, param[3])
            p2=punto( -lejos, -lejos, param[3])
            p3=punto(lejos, -lejos, param[3])
            p4=punto(lejos, lejos, param[3])
            
            pol=poligonoConvexo((p1,p2,p3,p4))

            pol.plano.p=self.p
            pol.plano.n=self.n
            
            return pol
        
        elif abs(param[2])==0 and abs(param[1])!=0 and abs(param[0])!=0:
            
            p1=(-(param[0]*(-lejos)+param[2]*(-lejos))+param[3])/param[1]
            p2=(-(param[0]*lejos+param[2]*(lejos))+param[3])/param[1]
            p3=(-(param[1]*(-lejos)+param[2]*(-lejos))+param[3])/param[0]
            p4=(-(param[1]*(lejos)+param[2]*(lejos))+param[3])/param[0]
            
            #p1=punto((-lejos), p1, -lejos)
            #p2=punto(lejos, p2, lejos)
            p3=punto(-lejos, -lejos, p3)
            p4=punto(-lejos, lejos, p4)
            
            otgn=-(p3.apunta()-p4.apunta())
            
            
            
            #p1=copy.deepcopy(p3).mover(-otgn.pcruz(self.n))
            p2=copy.deepcopy(p4).mover(-otgn.pcruz(self.n)).mover(-otgn)
            p1=copy.deepcopy(p2).mover(otgn)
            
            otgn=otgn.pcruz(self.n)
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            pol.mover(-(otgn.proyectar(pol.punto_cent.apunta())))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            
            return pol
        
        elif abs(param[1])==0 and abs(param[0])!=0 and abs(param[2])!=0:
            
            p1=(-(param[1]*(-lejos)+param[2]*(-lejos))+param[3])/param[0]
            p2=(-(param[1]*lejos+param[2]*(lejos))+param[3])/param[0]
            p3=(-(param[0]*(-lejos)+param[1]*(-lejos))+param[3])/param[2]
            p4=(-(param[0]*(-lejos)+param[1]*(lejos))+param[3])/param[2]
            
            # p1=punto(p1, -lejos, -lejos)
            # p2=punto(p2, lejos, lejos)
            p3=punto(-lejos, -lejos, p3)
            p4=punto(-lejos, lejos, p4)
            
            otgn=-(p3.apunta()-p4.apunta())
            
            
            
            #p1=copy.deepcopy(p3).mover(-otgn.pcruz(self.n))
            p2=copy.deepcopy(p4).mover(-otgn.pcruz(self.n)).mover(-otgn)
            p1=copy.deepcopy(p2).mover(otgn)
            
            otgn=otgn.pcruz(self.n)
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            pol.mover(-(otgn.proyectar(pol.punto_cent.apunta())))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            
            return pol
        
        elif abs(param[0])==0 and abs(param[1])!=0 and abs(param[2])!=0:
            
            p1=(-(param[0]*(-lejos)+param[2]*(-lejos))+param[3])/param[1]
            p2=(-(param[0]*lejos+param[2]*(lejos))+param[3])/param[1]
            p3=(-(param[0]*(-lejos)+param[1]*(-lejos))+param[3])/param[2]
            p4=(-(param[0]*(lejos)+param[1]*(lejos))+param[3])/param[2]
            
            #p1=punto(lejos, p1, -lejos)
            #p2=punto(p1.x, p2,lejos)
            p3=punto(-lejos, -lejos, p3)
            p4=punto(-lejos, lejos, p4)
            
            otgn=-(p3.apunta()-p4.apunta())
            
            
            
            #p1=copy.deepcopy(p3).mover(-otgn.pcruz(self.n))
            p2=copy.deepcopy(p4).mover(-otgn.pcruz(self.n)).mover(-otgn)
            p1=copy.deepcopy(p2).mover(otgn)
            
            otgn=otgn.pcruz(self.n)
            
            pol=poligonoConvexo((p1,p2,p3,p4))
            pol.mover(-(otgn.proyectar(pol.punto_cent.apunta())))
            
            pol.plano.p=self.p
            pol.plano.n=self.n
            
            return pol
            