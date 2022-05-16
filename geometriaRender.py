# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:51:06 2022

@author: Abrah
"""
from utilidades import FLOAT_EPS, geomRenderVertices2, geomRenderCaras
from matrix import matrix
from PIL import Image, ImageDraw, ImageTk
import math

class geometria:
    def __init__(self, canvas_width, canvas_height, opacidad=False):
        self.CANVAS_WIDTH = canvas_height
        self.CANVAS_HEIGHT= canvas_height
        self.POSICION_OBJ = [canvas_width // 2, canvas_height-20]
        self.ESCALA_OBJ = 2500
        self._angulo_x=0
        self._angulo_y=0
        self._angulo_z=0
        self._zoom=3
        self._caras=[]
        self._vertices={}
        self.LLENAR=""
        self.COLOR_LINEA="#0000FF"
        self.COLOR_PUNTO="#000000"
        self.opacidad=opacidad

    def cambiar_color_llenado(self, color, no_llenado=False):
        if(no_llenado):
            self.LLENAR=""
        else:
            self.LLENAR=color

    def cambiar_color_linea(self, color):
        self.COLOR_LINEA=color

    def actualizar_posicion(self, x, y):
        self.POSICION_OBJ[0]+=x
        self.POSICION_OBJ[1]+=y

    def _matriz_rotacion(self):
        rot_x=matrix.rotx(self._angulo_x)
        rot_y=matrix.roty(self._angulo_y)
        rot_z=matrix.rotz(self._angulo_z)

        return rot_x, rot_y, rot_z

    def _transformar_2d(self,punto, rot_x, rot_y, rot_z):
        rotado2d=rot_x*punto
        rotado2d=rot_y*rotado2d
        rotado2d=rot_z*rotado2d
        
        try:
            z=0.5/(1/10**self._zoom-rotado2d[2][0])
            
        except ZeroDivisionError:
            z=0.00001

        matriz_proyeccion=matrix(2,3)
        matriz_proyeccion[0][0]=z
        matriz_proyeccion[1][1]=z

        proyectado2d=matriz_proyeccion*rotado2d

        x=int(proyectado2d[0][0]*self.ESCALA_OBJ)+self.POSICION_OBJ[0]
        y=-int(proyectado2d[1][0]*self.ESCALA_OBJ)+self.POSICION_OBJ[1]

        return x, y

    def reiniciar_angulos(self):
        self._angulo_x=0
        self._angulo_y=0
        self._angulo_z=0

    def dibujar_punto(self, point, canvas):
        POINT_SIZE=2
        canvas.create_oval(point[0],point[1],point[0],point[1], width=POINT_SIZE, fill=self.COLOR_PUNTO)
        return canvas

    def dibujar_caras(self, canvas, puntos, root):

        for cara in self._caras:
            #print(puntos)
            dibujar=[puntos[cara[i]] for i in range(len(cara))]

            cond=False
            cont=0
            #print(dibujar)

            for point in dibujar:
                
                if point[0]<0 or point[1]<0 or point[0] > self.CANVAS_WIDTH or point[1] > self.CANVAS_HEIGHT:# and not self.opacidad:
                    cond=True
                    continue
                
                cond=False
                cont+=1

                #canvas = self.dibujar_punto(point, canvas)
                
            if cond and cont<2:
                continue
                
            if self.opacidad:
                
                #im=self.create_polygon_tr(root, canvas, *dibujar)
                #canvas.create_image(0,0, image=im)
                canvas.create_polygon(dibujar, outline= self.COLOR_LINEA, fill= "blue",stipple="gray50")
                
            
            if not self.opacidad:

                canvas.create_polygon(dibujar, outline= self.COLOR_LINEA, fill= self.LLENAR)
                
            

        return canvas

    def dibujar_linea(self, canvas, puntos):

        puntos_proyectados={}
        rot_x, rot_y, rot_z =self._matriz_rotacion()
        i=0

        for point in puntos:
            x,y=self._transformar_2d(point, rot_x, rot_y, rot_z)
            puntos_proyectados[i]=[x,y]
            i+=1

        canvas.create_line(puntos_proyectados[0],puntos_proyectados[1])

    def dibujar_objeto(self, canvas, root=""):
        puntos_proyectados = {}

        rot_x, rot_y, rot_z =self._matriz_rotacion()   
        for vertice in self._vertices.items():
            x, y = self._transformar_2d(vertice[1], rot_x, rot_y, rot_z)
            puntos_proyectados[vertice[0]]=[x,y]

        #print(puntos_proyectados[vertice[0]][1])
        #
        # print(puntos_proyectados)
        return self.dibujar_caras(canvas, puntos_proyectados, root=root )


    def create_polygon_tr(self, root,canvas, *args, fill="blue", alpha=0.8):
        
        if args:
            
            #try:
            aux=[]
            for i in args:
                aux+=i
            images = []  # to hold the newly created image(s)  
            # Get and process the input data
            fill = canvas.winfo_rgb(fill)\
                   + (int(alpha* 255),)
                   
            fill=(0, 0, 65535, 127)
    
            image = Image.new("RGBA", (max(aux[::2]), max(aux[1::2])))
            ImageDraw.Draw(image).polygon(aux, fill=fill, outline=self.COLOR_LINEA)
    
            #images.append()  # prevent the Image from being garbage-collected
            #canvas.create_image(0, 0, image=images[-1], anchor="nw")# insert the Image to the 0, 0 coords

            
            return ImageTk.PhotoImage(image)
            
            # except:
                
            #     return canvas
            
        else:
            return canvas
    
