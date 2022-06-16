#hay que cambiar la opcion cubo por la opcion paralelepipedo, para que sea mas general, es decir, que reciba 
#un punto y tres vectores diferentes
#que el cilindro no reciba altura, sino un vector para tener el caso mas general
#es posible que en la opcion de plano se agregen otras opciones para definirlo, tal vez poner pestañas o 
#algo por el estilo, se puede crear un plano recibiendo 2 vectores y un punto, con tres puntos, o la forma
#parametrica, que son 4 argumentos de la forma Ax+By+Cz-D=0
#tambien hay que cambiar la apertura del bloc de notas a una opcion con un boton en vez de que se abra en 
#caso de error al abrir, me referia a que el mismo archivo que se abre en el renderizador se abra en el 
#bloc

## Nota: Quite la opcion de cubo y le cambie el nombre a las opciones prisma a paralelepipedo
#          Clave    Valor
#            l        |
#            v        v
#figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}

#Para acceder al valor de la clave "esferas" escribes figuras["esferas"] y obtendras la lista

from tkinter import ttk
import math

import tkinter as tk
from tkinter import filedialog
#import MCNPpython
from punto import punto
from vector import vector
from plano import plano
#from poligonoConvexo import polignoConvexo
from poliedroConvexo import poliedroConvexo
from utilidades import geomRenderVertices2, geomRenderCaras, geomRenderVerticesP2, geomRenderPlano
from geometriaRender import geometria
from MCNPpython import lecturaMCNP, MCNPaGeom, geomaMCNP
from tkinter import messagebox
import os

############################################################################################################################################
################################################## Clase geometria para optimizar la creacion de formas, sus metodos etc ###################
############################################################################################################################################

class interfaz(tk.Tk):
    ANCHO_CANVAS=800
    ALTURA_CANVAS=600
    COLOR_CANVAS="white"
    X_REL=0.97
    TAMANO_PASO=1

    FONDO="#0b0b0b"
    figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}
    pplanos=[]
    rec=None
    lejos=None
    figuras_num={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}
    # Declara una variable de clase para contar ventanas
    ventana = 0
    # Declara una variable de clase para usar en el
    # cálculo de la posición de una ventana
    posx_y = 0

    def __init__(self, titulo="MCNPython", tam_min=(1200,600)):
        super().__init__()
        self.cambio=True
        self.cambioFig=False
        self._manejo_geometria=geometria(self.ANCHO_CANVAS,self.ALTURA_CANVAS)
        self._manejo_planos=geometria(self.ANCHO_CANVAS,self.ALTURA_CANVAS, opacidad=True)
        self._iniciar_ventana(titulo, tam_min)
        self._crear_herramientas()
        self._reiniciar_rotacion()
        self._opciones_archivo()
        #self.bind("<C>", self._leer_archivo)
        self.bind("<Configure>", self._cambio_ventana)
        self.bind("<Up>", self._mover_arriba)
        self.bind("<Down>", self._mover_abajo)
        self.bind("<Right>", self._mover_derecha)
        self.bind("<Left>", self._mover_izquierda)
        self.archivo=""
        
    def _barra_menu(self):
        self._barra_opciones=tk.Menu(self)
        
    def _opciones_archivo(self):
        self._barra_menu()
        self.menu_archivos=tk.Menu(self._barra_opciones, tearoff=0)
        self.menu_archivos.add_command(label="Abrir archivo", command=self._seleccionar_archivo)
        self._barra_opciones.add_cascade(label="Archivo", menu=self.menu_archivos)
        self.config(menu=self._barra_opciones)
        
    def _seleccionar_archivo(self):
        self.archivo=filedialog.askopenfilename()
        if self.archivo:
            self._leer_archivo("")
        
    def _leer_archivo(self, evento):
        # try:        
        geoms=MCNPaGeom(lecturaMCNP(self.archivo))
        self.figuras=geoms[0]
        self.figuras_num=geoms[1]
        self.rec=geoms[2]
        if self.rec:
            self.lejos=abs((self.rec.punto_central.apunta()-self.rec.poligonos_convexos[0].puntos[0].apunta()).magn())*0.45
        self._manejo_geometria._caras=[]
        self._manejo_geometria._vertices={}
        self._manejo_planos._caras=[]
        self._manejo_planos._vertices={}
        self._cambioFig()
        self._cambio()

        # except:
        #     print("No se pudo leer el archivo")
        #     if interfaz.ventana < 1:
        #         self.dial = tk.Toplevel()
        #         interfaz.ventana+=1
        #         interfaz.posx_y += 50
        #         tamypos = '200x100+'+str(interfaz.posx_y)+ \
        #                   '+'+ str(interfaz.posx_y)
        #         self.dial.geometry(tamypos)
        #         self.dial.resizable(50,50)
        #         self.dial.minsize(400, 650)
        #         ident = self.dial.winfo_id()
        #         titulo = str(interfaz.ventana)+": "+str(ident)
        #         self.dial.title(titulo)
        #         self.arbr = open(self.archivo)
        #         self.g=0
        #         def destruir():
        #             if self.g==0:
        #                 self.dial.destroy()
        #                 interfaz.ventana-=1
        #             else:
        #                 self.dial.destroy()
        #                 self.archiv.close()
        #                 interfaz.ventana-=1
        #         def escribir():
        #             self.arbr.close()
        #             self.archiv = open(self.archivo,"w")
        #             self.archiv.write(Lector.get("1.0", "end-1c"))
        #             self.g=1
        #         Lector = tk.Text(self.dial, height =30, width = 100, bg = "light cyan")
        #         Sescri = tk.Button(self.dial, height = 2, width = 20, text = "GUARDAR", command = lambda:escribir())
        #         cerrar = tk.Button(self.dial, height = 2, width = 20, text='CERRAR', command=destruir)
        #         Lector.insert(tk.END, self.arbr.read())
        #         Lector.pack()
        #         Sescri.pack()
        #         cerrar.pack()
        #         self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        #     else:
        #         print("Por favor cierre la otra ventana emergente")
        # #vertices={item: val.punto_arreglo() for item, val in enumerate(esfera.con_puntos)}
        # #self._manejo_geometria._vertices= vertices
                
    def _mover_arriba(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[1]-=self.TAMANO_PASO
        self._manejo_planos.POSICION_OBJ[1]-=self.TAMANO_PASO
        self._cambio()
        
    def _mover_abajo(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]-=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[1]+=self.TAMANO_PASO
        self._manejo_planos.POSICION_OBJ[1]+=self.TAMANO_PASO
        self._cambio()
        
    def _mover_derecha(self, event):
        self._manejo_geometria.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._manejo_planos.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._cambio()
        
    def _mover_izquierda(self, event):
        self._manejo_geometria.POSICION_OBJ[0]-=self.TAMANO_PASO
        self._manejo_planos.POSICION_OBJ[0]-=self.TAMANO_PASO
        self._cambio()

    def _iniciar_ventana(self, titulo, tam):
        self.title(titulo)
        self.minsize(*tam)
        self["bg"]=self.FONDO

    def _crear_herramientas(self):
        self._crear_lienzo()
        self._crear_herramienta_zoom()
        ttk.Separator(self, orient="horizontal").place(relx=self.X_REL, rely=0.100, relwidth=0.2, anchor="ne")
        self._crear_rotador_x()
        self._crear_rotador_y()
        self._crear_rotador_z()
        self._boton_reiniciar_rotacion()
        self._boton_convertir_txt()
        self._boton_generar_paralelepipedo()
        self._boton_generar_esfera()
        self._boton_generar_cilindro()
        self._boton_generar_plano()
        #self._boton_generar_dibujar()

    def _crear_lienzo(self):
        self.color_lienzo= tk.StringVar()
        self.color_lienzo.set("#FFFFFF")
        self.canvas= tk.Canvas(self, width=self.ANCHO_CANVAS, height=self.ALTURA_CANVAS, bg=self.color_lienzo.get())
        #print(type(self.canvas))
        self.canvas.place(relx=0.03, rely=0.050, relheight=0.9, relwidth=0.7)

    def _crear_herramienta_zoom(self):
        ttk.Label(self, text="Zoom", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.052, relheight=0.035, relwidth=0.2, anchor="ne")
        self.deslizante_zoom=ttk.Scale(self, from_=-5, to=5, orient="horizontal", command=self._cambio)
        self.deslizante_zoom.set(self._manejo_geometria._zoom)
        self.deslizante_zoom.place(relx=self.X_REL, rely=0.01, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_x(self):
        ttk.Label(self, text="Rotacion x", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.180, relheight=0.035, relwidth=0.2, anchor="ne")
        self.deslizante_rot_x=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_x.set(self._manejo_geometria._angulo_x)
        self.deslizante_rot_x.place(relx=self.X_REL, rely=0.22, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_y(self):
        ttk.Label(self, text="Rotacion y", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.290, relheight=0.035, relwidth=0.2, anchor="ne")
        self.deslizante_rot_y=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_y.set(self._manejo_geometria._angulo_y)
        self.deslizante_rot_y.place(relx=self.X_REL, rely=0.33, relheight=0.04, relwidth=0.2, anchor="ne")

    def _crear_rotador_z(self):
        ttk.Label(self, text="Rotacion z", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.400, relheight=0.035, relwidth=0.2, anchor="ne")
        self.deslizante_rot_z=ttk.Scale(self, from_=-math.pi, to=math.pi, orient="horizontal", command=self._cambio)
        self.deslizante_rot_z.set(self._manejo_geometria._angulo_z)
        self.deslizante_rot_z.place(relx=self.X_REL, rely=0.44, relheight=0.04, relwidth=0.2, anchor="ne")

    def _boton_reiniciar_rotacion(self):
        ttk.Button(self, text="Reiniciar angulos", command=self._reiniciar_rotacion).place(relx=self.X_REL, rely=0.9, relheight=0.05, relwidth=0.2, anchor="ne")
  
    def _boton_convertir_txt(self):
        ttk.Button(self, text="Generar texto", command=self._generar_txt).place(relx=self.X_REL, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_esfera(self):
        ttk.Button(self, text="Generar esfera", command=self._generar_esfera).place(relx=self.X_REL -.1, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_paralelepipedo(self):
        ttk.Button(self, text="Generar paralelepipedo", command=self._generar_paralelepipedo).place(relx=self.X_REL -.1, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_cilindro(self):
        ttk.Button(self, text="Generar cilindro", command=self._generar_cilindro).place(relx=self.X_REL, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_plano(self):
        ttk.Button(self, text="Generar plano", command=self._generar_plano).place(relx=self.X_REL -.1, rely=0.7, relheight=0.05, relwidth=0.1, anchor="ne")        

    def _boton_generar_dibujar(self):
        ttk.Button(self, text="Generar dibujar", command=self._generar_dibujar).place(relx=self.X_REL, rely=0.7, relheight=0.05, relwidth=0.1, anchor="ne")        

    def _destruir_ventana_emergente(self):
        self.dialogo.destroy()
        interfaz.ventana-=1
        
    def _cerrado_tacha(self):
        interfaz.ventana-=1
        self.dialogo.destroy()
        
    def _generar_txt(self):
        if self.lejos:
            txt=geomaMCNP(self.figuras, self.figuras_num, self.rec, lejos=self.lejos)
            
        else:
            txt=geomaMCNP(self.figuras, self.figuras_num, self.rec)
            
        print(txt)
        with open("cache.txt", "w") as archivo:
            archivo.write(txt)
            
        archivo=open("cache.txt")
        self.archivo="cache.txt"#"".join(archivo.readlines())
        archivo.close()
        self._leer_archivo("")

    def _crear_cilindro_param(self, Hx, Hy, Hz, R, X, Y, Z):
        cilindro=poliedroConvexo.cilindro(punto(X,Y,Z), R, vector(Hx,Hy,Hz))
        hashes=[]
        for i in self.figuras["cilindro"]:
            hashes.append(hash(i))
        if hash(cilindro) not in hashes:
            self.figuras["cilindro"].append(cilindro)
            
            indices=[]
            for i in self.figuras_num:
                indices+=self.figuras_num[i]
            
            if not indices:
                self.figuras_num["cilindro"].append(1)
            else:
                self.figuras_num["cilindro"].append(max(indices)+1)
            
            self._cambioFig()
            self._cambio()
            self._cambioFig()
            self._cambio()
            
    def _crear_conot_param(self, Hx, Hy, Hz, R, R2, X, Y, Z):
        cilindro=poliedroConvexo.conoTruncado(punto(X,Y,Z), R, R2,vector(Hx,Hy,Hz))
        hashes=[]
        for i in self.figuras["conot"]:
            hashes.append(hash(i))
        if hash(cilindro) not in hashes:
            self.figuras["conot"].append(cilindro)
            self._cambioFig()
            self._cambio()
            
            indices=[]
            for i in self.figuras_num:
                indices+=self.figuras_num[i]
                
            if not indices:
                self.figuras_num["conot"].append(1)
            else:
                self.figuras_num["conot"].append(max(indices)+1)

            
            self._cambioFig()
            self._cambio()
            
    # def _crear_cubo_param(self, B, X, Y, Z):
    #     cubo=poliedroConvexo.paralelepipedo(punto(X,Y,Z),vector(B,0,0),vector(0,B,0),vector(0,0,B))
    #     hashes=[]
    #     for i in self.figuras["paralelepipedos"]:
    #         hashes.append(hash(i))
    #     if hash(cubo) not in hashes:
    #         self.figuras["paralelepipedos"].append(cubo)
    #         self._cambioFig()
    #         self._cambio()

    def _crear_esfera_param(self, R, X, Y, Z):
        esfera=poliedroConvexo.esfera(punto(X,Y,Z),R)
        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))
        if hash(esfera) not in hashes:
            self.figuras["esferas"].append(esfera)
            
            indices=[]
            for i in self.figuras_num:
                indices+=self.figuras_num[i]
                
            if not indices:
                self.figuras_num["esferas"].append(1)
            else:
                self.figuras_num["esferas"].append(max(indices)+1)
            #self.figuras_num["esferas"].append(max(indices)+1)
            
            self._cambioFig()
            self._cambio()

    def _crear_prisma_param(self, X, Y, Z, x1, x2, x3, y1, y2, y3, z1, z2, z3 ):
        prisma=poliedroConvexo.paralelepipedo(punto(X,Y,Z),vector(x1,x2,x3),vector(y1,y2,y3),vector(z1,z2,z3))
        hashes=[]
        for i in self.figuras["paralelepipedos"]:
            hashes.append(hash(i))
        if hash(prisma) not in hashes:
            
            self.figuras["paralelepipedos"].append(prisma)
            
            indices=[]
            for i in self.figuras_num:
                indices+=self.figuras_num[i]
                
            if not indices:
                self.figuras_num["paralelepipedos"].append(1)
            else:
                self.figuras_num["paralelepipedos"].append(max(indices)+1)
            
            self._cambioFig()
            self._cambio()

    def _crear_plano_param(self, x1, x2, x3, y1, y2, y3, px, py, pz, op=1):
        
        if op == 1:
            
            if (vector(x1,x2,x3).paralelo(vector(y1,y2,y3))):
                print("los vectores son paralelos")
            else:
                
                plan=plano(punto(px,py,pz),vector(x1,x2,x3),vector(y1,y2,y3))
                hashes=[]
                
                    
        elif op == 2:
            if punto(x1, x2, x3) == punto(y1, y2, y3) or \
                punto(x1, x2, x3) == punto(px, py, pz) or \
                    punto(y1, y2, y3) == punto(px, py, pz): 
                print("Los puntos deben ser diferentes")
                
            else:
                plan=plano(punto(x1, x2, x3),punto(y1, y2, y3),punto(px, py, pz))
                hashes=[]
                
        elif op == 3:
            plan=plano(x1,x2,x3,y1)
            hashes=[]
                
        try:
            for i in self.figuras["plano"]:
                hashes.append(hash(i))
                
            if hash(plan) not in hashes:
                self.figuras["plano"].append(plan)
                
                indices=[]
                for i in self.figuras_num:
                    indices+=self.figuras_num[i]
                    
                if not indices:
                    self.figuras_num["plano"].append(1)
                else:
                    self.figuras_num["plano"].append(max(indices)+1)
                    
                
                self._cambioFig()
                self._cambio()
                
        except:
            print("El plano no pudo ser creado")
    
    # def _crear_linea_param(self, p1, p2, p3, x1, x2, x3):
    #     y1=(.772469*x3)*0.0001
    #     y2=(.673121*x1)*0.0001
    #     y3=(.569173*x2)*0.0001
    #     z1=((x2*y3)-(y2*x3))*0.0001
    #     z2=((x3*y1)-(y3*x1))*0.0001
    #     z3=((x1*y2)-(y1*x2))*0.0001
    #     m=10000
    #     linea=poliedroConvexo.paralelepipedo(punto(p1,p2,p3),vector(m*x1,m*x2,m*x3),vector(y1,y2,y3),vector(z1,z2,z3))
    #     hashes=[]
    #     for i in self.figuras["paralelepipedos"]:
    #         hashes.append(hash(i))
    #     if hash(linea) not in hashes:
    #         self.figuras["paralelepipedos"].append(linea)
    #         self._cambioFig()
    #         self._cambio()
    
    # def _crear_punto_param(self, X, Y, Z):
    #     r=0.00001
    #     punto1=poliedroConvexo.esfera(punto(X,Y,Z), r)
    #     hashes=[]
    #     for i in self.figuras["esferas"]:
    #         hashes.append(hash(i))
    #     if hash(punto1) not in hashes:
    #         self.figuras["esferas"].append(punto1)
    #         self._cambioFig()
    #         self._cambio()
              
    def _generar_cubo(self):      
        if interfaz.ventana <1:
            self.dialogo = tk.Toplevel()
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.minsize(400, 400)
            self.dialogo.maxsize(400, 400)
            
            titulo = "Paralelepipedos"
            self.dialogo.title(titulo)
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            def Cubog():
                base = float(inputtxt1.get("1.0", "end-1c"))
                posx = float(inputtxt2.get("1.0", "end-1c"))
                posy = float(inputtxt3.get("1.0", "end-1c"))
                posz = float(inputtxt4.get("1.0", "end-1c"))
                self._crear_cubo_param(base, posx, posy, posz)
                if(base < 0):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                else:
                    Output.insert(tk.END, 'Captura de datos correcta')
            l = tk.Label(self.dialogo, text = "PARALELEPIPEDOS")
            l1 = tk.Label(self.dialogo, text = "Base")
            l2 = tk.Label(self.dialogo, text = "Vector")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light green")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light green")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light green")
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            Output.pack(side=tk.BOTTOM, padx=20, pady=20)
            Crearr= tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Cubog())
            Crearr.pack(side=tk.BOTTOM, padx=20, pady=20)
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            inputtxt3.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            inputtxt4.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        else:
            print("Por favor cierre la otra ventana emergente")

    def _generar_esfera(self):
        if interfaz.ventana<1:
            self.dialogo = tk.Toplevel()
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.maxsize(400,400)
            self.dialogo.minsize(400,400)
            
            titulo = "Esferas"
            self.dialogo.title(titulo)
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            def Esfeg():
                radio = float(inputtxt1.get("1.0", "end-1c"))
                posx = float(inputtxt2.get("1.0", "end-1c"))
                posy = float(inputtxt3.get("1.0", "end-1c"))
                posz = float(inputtxt4.get("1.0", "end-1c"))
                if(radio == 0):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                else:
                    Output.insert(tk.END, 'Captura de datos correcta')
                    self._crear_esfera_param(radio, posx, posy, posz)
            l = tk.Label(self.dialogo, text = "ESFERAS")
            l1 = tk.Label(self.dialogo, text = "Radio")
            l2 = tk.Label(self.dialogo, text = "Vector posición")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            Output.pack(side=tk.BOTTOM, padx=20, pady=20)
            Crearr= tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Esfeg())
            Crearr.pack(side=tk.BOTTOM, padx=20, pady=20)
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            inputtxt3.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            inputtxt4.pack(side=tk.LEFT, anchor='n', padx=20, pady=20)
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        else:
            print("Por favor cierre la otra ventana emergente")
                        
    def _generar_cilindro(self):
        if interfaz.ventana<1:
            self.dialogo = tk.Toplevel()
            fininf=tk.BooleanVar()
            fininf.set(True)
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.maxsize(400,450)
            self.dialogo.minsize(400,450)
            
            titulo = "Cilindros"
            self.dialogo.title(titulo)
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            
            def Cilg():
                try:
                    vecx = float(inputtxt1.get("1.0", "end-1c"))
                    vecy = float(inputtxt6.get("1.0", "end-1c"))
                    vecz = float(inputtxt7.get("1.0", "end-1c"))
                    radio = float(inputtxt2.get("1.0", "end-1c"))
                    posx = float(inputtxt3.get("1.0", "end-1c"))
                    posy = float(inputtxt4.get("1.0", "end-1c"))
                    posz = float(inputtxt5.get("1.0", "end-1c"))
                    if inputtxt8.get("1.0", "end-1c") != "" and fininf.get():
                        radio2=float(inputtxt8.get("1.0", "end-1c"))
                        self._crear_conot_param(vecx, vecy, vecz, radio, radio2, posx, posy, posz)
                        
                    if(radio < 0):
                        
                        Output.insert(tk.END, "El radio ingresado no es valido")
                        
                    elif not inputtxt8.get("1.0", "end-1c"):
                        
                        Output.insert(tk.END, 'Captura de datos correcta')
                        if not fininf.get():
                            if not self.lejos:
                                v=vector(vecx,vecy,vecz)*100
                                p=punto(posx,posy,posz).mover(v*(-1/2))
                                self._crear_cilindro_param(v[0], v[1], v[2],
                                                           radio, p.x, p.y, p.z)
                            elif self.lejos:
                                v=vector(vecx,vecy,vecz)*self.lejos
                                p=punto(posx,posy,posz).mover(v*(-1/2))
                                self._crear_cilindro_param(v[0], v[1], v[2],
                                                           radio, p.x, p.y, p.z)
                        elif fininf.get():        
                            self._crear_cilindro_param(vecx, vecy, vecz, radio, posx, posy, posz)
                        
                except:
                    Output.insert(tk.END, "Uno o mas valores no son validos")
                
                
                    
            frameVec=tk.Frame(self.dialogo)
            frameVec.place(relx=0.1, rely=0.05, relwidth=0.8)
            frameRad=tk.Frame(self.dialogo)
            frameRad.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.15)
            framePos=tk.Frame(self.dialogo)
            framePos.place(relx=0.1, rely=0.35, relwidth=0.8)
                    
            l = tk.Label(self.dialogo, text = "GENERADOR DE CILINDROS")
            l1 = tk.Label(frameVec, text = "Vector dirección")
            l3 = tk.Label(framePos, text = "Posición")
            l2 = tk.Label(frameRad, text = "Radio")
            l4 = tk.Label(frameRad, text = "Radio 2 (Opcional)")
            
            inputtxt1 = tk.Text(frameVec, height = 2, width = 12, bg = "light yellow")
            inputtxt6 = tk.Text(frameVec, height = 2, width = 12, bg = "light yellow")
            inputtxt7 = tk.Text(frameVec, height = 2, width = 12, bg = "light yellow")
            inputtxt2 = tk.Text(frameRad, height = 2, width = 12, bg = "light yellow")
            inputtxt3 = tk.Text(framePos, height = 2, width = 12, bg = "light yellow")
            inputtxt4 = tk.Text(framePos, height = 2, width = 12, bg = "light yellow")
            inputtxt5 = tk.Text(framePos, height = 2, width = 12, bg = "light yellow")
            inputtxt8 = tk.Text(frameRad, height = 2, width = 12, bg = "light yellow")
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            tk.Radiobutton(self.dialogo, text="Finito",variable=fininf, value=True).\
                place(relx=0.2, rely=0.5)
            tk.Radiobutton(self.dialogo, text="Ininito",variable=fininf, value=False).\
                place(relx=0.5, rely=0.5)
            Output.pack(side=tk.BOTTOM, padx=20, pady=20)
            Crearr = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Cilg())
            Crearr.pack(side=tk.BOTTOM, padx=20, pady=20)
            l.pack()
            l1.pack()
            inputtxt1.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            inputtxt6.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            inputtxt7.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            l2.place(relx=0.25, rely=0.05)
            inputtxt2.place(relx=0.15, rely=0.5)
            l4.place(relx=0.6, rely=0.05)
            inputtxt8.place(relx=0.6, rely=0.5)
            l3.pack()
            inputtxt3.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            inputtxt4.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            inputtxt5.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        else:
            print("Por favor cierre la otra ventana emergente")

    def _generar_dibujar(self):
        if interfaz.ventana<1:
            self.dialogo = tk.Toplevel()
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.maxsize(400,400)
            self.dialogo.minsize(400,400)
            
            #titulo = str(interfaz.ventana)+": "+str(ident)
            #self.dialogo.title(titulo)
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            def Pung():
                x1 = float(inputtxt1.get("1.0", "end-1c"))
                x2 = float(inputtxt2.get("1.0", "end-1c"))
                x3 = float(inputtxt3.get("1.0", "end-1c"))
                Output.insert(tk.END, 'Captura de datos correcta')
                self._crear_punto_param(x1,x2,x3)
            def Ling():
                x1 = float(inputtxt1.get("1.0", "end-1c"))
                x2 = float(inputtxt2.get("1.0", "end-1c"))
                x3 = float(inputtxt3.get("1.0", "end-1c"))
                y1 = float(inputtxt4.get("1.0", "end-1c"))
                y2 = float(inputtxt5.get("1.0", "end-1c"))
                y3 = float(inputtxt6.get("1.0", "end-1c"))
                Output.insert(tk.END, 'Captura de datos correcta')
                self._crear_punto_param(x1,x2,x3,y1,y2,y3)            
            l1 = tk.Label(self.dialogo, text = "Punto").place(relx=0.7, rely=0.075, relheight=0.085, relwidth=0.4, anchor="ne")
            l = tk.Label(self.dialogo, text = "DIBUJA PUNTOS Y LINEAS").place(relx=0.7, rely=0.015, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt1.place(relx=0.3, rely=0.165, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt2.place(relx=0.6, rely=0.165, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt3.place(relx=0.9, rely=0.165, relheight=0.07, relwidth=0.2, anchor="ne")
            Crearr1 = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR PUNTO", command = lambda:Pung()).place(relx=0.7, rely=0.285, relheight=0.085, relwidth=0.4, anchor="ne")
            l2 = tk.Label(self.dialogo, text = "Linea").place(relx=0.7, rely=0.405, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt4.place(relx=0.3, rely=0.485, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt5 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt5.place(relx=0.6, rely=0.485, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt6 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt6.place(relx=0.9, rely=0.485, relheight=0.07, relwidth=0.2, anchor="ne")
            Crearr2 = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR VECTOR", command = lambda:Pung()).place(relx=0.7, rely=0.605, relheight=0.085, relwidth=0.4, anchor="ne")    
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            Output.place(relx=0.7, rely=0.725, relheight=0.085, relwidth=0.4, anchor="ne")            
        else:
            print("Por favor cierre la otra ventana emergente")
            
    def _generar_paralelepipedo(self):
        if interfaz.ventana<1:
            self.dialogo = tk.Toplevel()
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.maxsize(400,500)
            self.dialogo.minsize(400,500)
            
            titulo = "Paralelepipedos"
            self.dialogo.title(titulo)
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            def Prisg():
                b1= float(inputtxt1.get("1.0", "end-1c"))
                b2= float(inputtxt2.get("1.0", "end-1c"))
                b3= float(inputtxt3.get("1.0", "end-1c"))
                x1= float(inputtxt4.get("1.0", "end-1c"))
                x2= float(inputtxt5.get("1.0", "end-1c"))
                x3= float(inputtxt6.get("1.0", "end-1c"))
                y1= float(inputtxt7.get("1.0", "end-1c"))
                y2= float(inputtxt8.get("1.0", "end-1c"))
                y3= float(inputtxt9.get("1.0", "end-1c"))
                z1= float(inputtxt10.get("1.0", "end-1c"))
                z2= float(inputtxt11.get("1.0", "end-1c"))
                z3= float(inputtxt12.get("1.0", "end-1c"))
                self._crear_prisma_param(b1, b2, b3, x1, x2, x3, y1, y2, y3, z1, z2, z3)
                Output.insert(tk.END, 'Captura de datos correcta')          
            tk.Label(self.dialogo, text = "Vector posición").place(relx=0.7, rely=0.075, relheight=0.085, relwidth=0.4, anchor="ne")
            tk.Label(self.dialogo, text = "PARALELEPIPEDOS").place(relx=0.7, rely=0.015, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt1.place(relx=0.3, rely=0.145, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt2.place(relx=0.6, rely=0.145, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt3.place(relx=0.9, rely=0.145, relheight=0.07, relwidth=0.2, anchor="ne")
            tk.Label(self.dialogo, text = "Vector 1").place(relx=0.7, rely=0.245, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt4.place(relx=0.3, rely=0.305, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt5 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt5.place(relx=0.6, rely=0.305, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt6 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt6.place(relx=0.9, rely=0.305, relheight=0.07, relwidth=0.2, anchor="ne")
            tk.Label(self.dialogo, text = "Vector 2").place(relx=0.7, rely=0.405, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt7 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt7.place(relx=0.3, rely=0.465, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt8 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt8.place(relx=0.6, rely=0.465, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt9 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt9.place(relx=0.9, rely=0.465, relheight=0.07, relwidth=0.2, anchor="ne")
            tk.Label(self.dialogo, text = "Vector 3").place(relx=0.7, rely=0.565, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt10 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt10.place(relx=0.3, rely=0.625, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt11 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt11.place(relx=0.6, rely=0.625, relheight=0.07, relwidth=0.2, anchor="ne")
            inputtxt12 = tk.Text(self.dialogo, height = 2, width = 12, bg = "light yellow")
            inputtxt12.place(relx=0.9, rely=0.625, relheight=0.07, relwidth=0.2, anchor="ne")
            tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR FIGURA", command = lambda:Prisg()).place(relx=0.7, rely=0.725, relheight=0.085, relwidth=0.4, anchor="ne")    
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            Output.place(relx=0.7, rely=0.8, relheight=0.085, relwidth=0.4, anchor="ne")
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        else:
            print("Por favor cierre la otra ventana emergente")
    
    def _generar_plano(self):
        if interfaz.ventana<1:
            self.dialogo = tk.Toplevel()
            interfaz.ventana+=1
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.maxsize(400,400)
            self.dialogo.minsize(400,400)
            
            titulo = "Plano"
            op=tk.IntVar()
            op.set(1)
            
            def cambio():
                frameparam.place_forget()
                framevvp.place_forget()
                framevpp.place_forget()
                
                if op.get() == 1:
                    
                    framevvp.place(relx=0, relwidth=1,rely=0.15, relheight=0.535)
                    
                elif op.get() == 2:
                    
                    framevpp.place(relx=0, relwidth=1,rely=0.15, relheight=0.535)
                    
                elif op.get() == 3:
                    
                    frameparam.place(relx=0, relwidth=1,rely=0.15, relheight=0.535)
            
            tk.Radiobutton(self.dialogo, text="VVP", value=1,variable=op, command=cambio)\
                        .place(relx=0.02, rely=0.05, relheight=0.13)
                        
            tk.Radiobutton(self.dialogo, text="PPP", value=2,variable=op, command=cambio)\
                        .place(relx=0.32, rely=0.05, relheight=0.13)
                        
            tk.Radiobutton(self.dialogo, text="Param", value=3,variable=op, command=cambio)\
                        .place(relx=0.62, rely=0.05, relheight=0.13)
                        
            self.dialogo.title(titulo)
            tk.Label(self.dialogo, text = "PLANOS").place(relx=0.7, rely=0.015, relheight=0.085, relwidth=0.4, anchor="ne")
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
            def Plag():
                
                if op.get() == 1:
                    try:
                        x1= float(inputtxt1.get("1.0", "end-1c"))
                        x2= float(inputtxt2.get("1.0", "end-1c"))
                        x3= float(inputtxt3.get("1.0", "end-1c"))
                        y1= float(inputtxt4.get("1.0", "end-1c"))
                        y2= float(inputtxt5.get("1.0", "end-1c"))
                        y3= float(inputtxt6.get("1.0", "end-1c"))
                        p1= float(inputtxt7.get("1.0", "end-1c"))
                        p2= float(inputtxt8.get("1.0", "end-1c"))
                        p3= float(inputtxt9.get("1.0", "end-1c"))
                        self._crear_plano_param(x1, x2, x3, y1, y2, y3, p1, p2, p3)
                        Output.insert(tk.END, 'Captura de datos correcta') 
                        
                    except:
                        Output.insert(tk.END, "No se pudo crear la supereficie")
                        
                elif op.get() == 2:
                    try:
                        x1= float(p1x.get("1.0", "end-1c"))
                        x2= float(p1y.get("1.0", "end-1c"))
                        x3= float(p1z.get("1.0", "end-1c"))
                        y1= float(p2x.get("1.0", "end-1c"))
                        y2= float(p2y.get("1.0", "end-1c"))
                        y3= float(p2z.get("1.0", "end-1c"))
                        p1= float(p3x.get("1.0", "end-1c"))
                        p2= float(p3y.get("1.0", "end-1c"))
                        p3= float(p3z.get("1.0", "end-1c"))
                        self._crear_plano_param(x1, x2, x3, y1, y2, y3, p1, p2, p3, op=2)
                        Output.insert(tk.END, 'Captura de datos correcta') 
                        
                    except:
                        Output.insert(tk.END, "No se pudo crear la supereficie")
                        
                elif op.get() == 3:
                    try:
                        x1= float(a.get("1.0", "end-1c"))
                        x2= float(b.get("1.0", "end-1c"))
                        x3= float(c.get("1.0", "end-1c"))
                        y1= float(d.get("1.0", "end-1c"))
                        y2= ""
                        y3= ""
                        p1= ""
                        p2= ""
                        p3= ""
                        self._crear_plano_param(x1, x2, x3, y1, y2, y3, p1, p2, p3, op=3)
                        Output.insert(tk.END, 'Captura de datos correcta') 
                        
                    except:
                        Output.insert(tk.END, "No se pudo crear la supereficie")
 
            framevvp=tk.Frame(self.dialogo)   
            
            tk.Label(framevvp, text = "Vector 1").place(relx=0.7, rely=0.075, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt1 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt1 .place(relx=0.3, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt2 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt2.place(relx=0.6, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt3 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt3.place(relx=0.9, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(framevvp, text = "Vector 2").place(relx=0.7, rely=0.305, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt4 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt4.place(relx=0.3, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt5 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt5.place(relx=0.6, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt6 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt6.place(relx=0.9, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(framevvp, text = "Punto").place(relx=0.7, rely=0.585, relheight=0.085, relwidth=0.4, anchor="ne")
            inputtxt7 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt7.place(relx=0.3, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt8 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt8.place(relx=0.6, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            inputtxt9 = tk.Text(framevvp, height = 2, width = 12, bg = "light yellow")
            inputtxt9.place(relx=0.9, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            
            framevpp=tk.Frame(self.dialogo)   
            
            tk.Label(framevpp, text = "Punto 1").place(relx=0.7, rely=0.075, relheight=0.085, relwidth=0.4, anchor="ne")
            p1x = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p1x .place(relx=0.3, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            p1y = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p1y.place(relx=0.6, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            p1z = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p1z.place(relx=0.9, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(framevpp, text = "Punto 2").place(relx=0.7, rely=0.305, relheight=0.085, relwidth=0.4, anchor="ne")
            p2x = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p2x.place(relx=0.3, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            p2y = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p2y.place(relx=0.6, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            p2z = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p2z.place(relx=0.9, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(framevpp, text = "Punto 3").place(relx=0.7, rely=0.585, relheight=0.085, relwidth=0.4, anchor="ne")
            p3x = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p3x.place(relx=0.3, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            p3y = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p3y.place(relx=0.6, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            p3z = tk.Text(framevpp, height = 2, width = 12, bg = "light yellow")
            p3z.place(relx=0.9, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            
            frameparam=tk.Frame(self.dialogo) 
            
            tk.Label(frameparam, text = "A").place(relx=0.7, rely=0.075, relheight=0.085, relwidth=0.4, anchor="ne")
            a = tk.Text(frameparam, height = 2, width = 12, bg = "light yellow")
            a.place(relx=0.6, rely=0.175, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(frameparam, text = "B").place(relx=0.7, rely=0.305, relheight=0.085, relwidth=0.4, anchor="ne")
            b = tk.Text(frameparam, height = 2, width = 12, bg = "light yellow")
            b.place(relx=0.6, rely=0.405, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(frameparam, text = "C").place(relx=0.7, rely=0.585, relheight=0.085, relwidth=0.4, anchor="ne")
            c = tk.Text(frameparam, height = 2, width = 12, bg = "light yellow")
            c.place(relx=0.6, rely=0.665, relheight=0.1, relwidth=0.2, anchor="ne")
            tk.Label(frameparam, text = "D").place(relx=0.7, rely=0.785, relheight=0.085, relwidth=0.4, anchor="ne")
            d = tk.Text(frameparam, height = 2, width = 12, bg = "light yellow")
            d.place(relx=0.6, rely=0.885, relheight=0.1, relwidth=0.2, anchor="ne")
            
            cambio()
            
            
            tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR PLANO", command = lambda:Plag()).place(relx=0.7, rely=0.685, relheight=0.085, relwidth=0.4, anchor="ne")    
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
            Output.place(relx=0.7, rely=0.765, relheight=0.085, relwidth=0.4, anchor="ne")
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
        else:
            print("Por favor cierre la otra ventana emergente")

    def _figurasRender(self):
        if self.cambioFig:
            caras=self._manejo_geometria._caras
            vertices=self._manejo_geometria._vertices
            
            carasp=self._manejo_planos._caras
            verticesp=self._manejo_planos._vertices
            
            for geom in self.figuras:
                if geom == "plano":
                    for fig in self.figuras[geom]:
                        try:
                            lejos=abs((self.rec.punto_central.apunta()-self.rec.poligonos_convexos[0].puntos[0].apunta()).magn())*0.45
                        except AttributeError:
                            lejos=100
                            
                        verticesp=geomRenderVerticesP2(fig, verticesp, lejos=lejos)
                        
                        if not verticesp:
                            continue
                        
                        carasp=geomRenderPlano(fig, verticesp, lejos=lejos)[0]+carasp
                                           
                    continue
                
                for fig in self.figuras[geom]:
                    #print(hash(fig))
                    vertices=geomRenderVertices2(fig,vertices)
                    if not vertices:
                        continue
                    #print(vertices)
                    caras=geomRenderCaras(fig,vertices)[0]+caras
            #print(caras)
            #print(vertices)
            
            
            self._manejo_geometria._caras=caras
            self._manejo_geometria._vertices=vertices
            self._manejo_planos._caras=carasp
            self._manejo_planos._vertices=verticesp

    def _cambio(self,*arg):
        self.cambio=True

    def _cambioFig(self, *args):
        self.cambioFig=True

    def _reiniciar_rotacion(self):
        self._manejo_geometria.reiniciar_angulos()
        self._manejo_planos.reiniciar_angulos()
        self.deslizante_rot_x.set(0)
        self.deslizante_rot_y.set(0)
        self.deslizante_rot_z.set(0)
        self._cambio()

    def _obtener_rotacion(self):
        self._manejo_geometria._angulo_x=self.deslizante_rot_x.get()
        self._manejo_geometria._angulo_y=self.deslizante_rot_y.get()
        self._manejo_geometria._angulo_z=self.deslizante_rot_z.get()
        self._manejo_planos._angulo_x=self.deslizante_rot_x.get()
        self._manejo_planos._angulo_y=self.deslizante_rot_y.get()
        self._manejo_planos._angulo_z=self.deslizante_rot_z.get()

    def _obtener_zoom(self):
        self._manejo_geometria._zoom=self.deslizante_zoom.get()
        self._manejo_planos._zoom=self._manejo_geometria._zoom
        
    def _cambio_ventana(self, evento):
        self._manejo_geometria.CANVAS_WIDTH=self.canvas.winfo_width()
        self._manejo_geometria.CANVAS_HEIGHT=self.canvas.winfo_height()
        self._manejo_planos.CANVAS_WIDTH=self.canvas.winfo_width()
        self._manejo_planos.CANVAS_HEIGHT=self.canvas.winfo_height()

    def dibujar(self):
        self._obtener_rotacion()
        self._obtener_zoom()
        #print(type(self.canvas))
        if self.cambioFig:
            self._figurasRender()
            self.cambioFig=False
        if self.cambio and len(self._manejo_geometria._caras):
            self.canvas.delete("all")
            if len(self._manejo_planos._caras):
                self.canvas=self._manejo_planos.dibujar_objeto(self.canvas,  root=self)
            self.canvas=self._manejo_geometria.dibujar_objeto(self.canvas)

            self.cambio=False

class main_():
    def __init__(self):
        self._iniciarInterfaz()
        self._actualizarPantalla()
        self._gui.mainloop()

    def _iniciarInterfaz(self):
        self._gui=interfaz()

    def _actualizarPantalla(self):
        if self._gui:
            self._gui.dibujar()
            self._gui.after(10, self._actualizarPantalla)
main_()
