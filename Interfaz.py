from tkinter import ttk
import math

import tkinter as tk
from tkinter import filedialog
#import MCNPpython
from punto import punto
from vector import vector
#from plano import plano
from linea import linea
#from poligonoConvexo import polignoConvexo
from poliedroConvexo import poliedroConvexo
from matrix import matrix
from utilidades import geomRenderVertices2, geomRenderCaras
from geometriaRender import geometria
from MCNPpython import lecturaMCNP, MCNPaGeom
from tkinter import messagebox

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
    figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list()}

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

    def _mover_arriba(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[1]-=self.TAMANO_PASO
        self._cambio()

    def _mover_abajo(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]-=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[1]+=self.TAMANO_PASO
        self._cambio()

    def _mover_derecha(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[0]+=self.TAMANO_PASO
        self._cambio()

    def _mover_izquierda(self, event):
        #self._manejo_geometria.POSICION_OBJ[0]-=self.TAMANO_PASO
        self._manejo_geometria.POSICION_OBJ[0]-=self.TAMANO_PASO
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
        self._boton_generar_cubo()
        self._boton_generar_plano()
        self._boton_generar_esfera()
        self._boton_generar_cilindro()
        self._boton_generar_piramide()
        self._boton_generar_dibujar()
        self._boton_generar_archivo()

    def _crear_lienzo(self):
        self.color_lienzo= tk.StringVar()
        self.color_lienzo.set("#FFFFFF")

        self.canvas= tk.Canvas(self, width=self.ANCHO_CANVAS, height=self.ALTURA_CANVAS, bg=self.color_lienzo.get())
        #print(type(self.canvas))
        self.canvas.place(relx=0.03, rely=0.050, relheight=0.9, relwidth=0.7)

    def _crear_herramienta_zoom(self):
        ttk.Label(self, text="Zoom", foreground="#FFFFFF", background="#131313").place(relx=self.X_REL, rely=0.052, relheight=0.035, relwidth=0.2, anchor="ne")

        self.deslizante_zoom=ttk.Scale(self, from_=0.01, to=10000, orient="horizontal", command=self._cambio)
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
  
    def _boton_generar_cubo(self):
        ttk.Button(self, text="Generar cubo", command=self._generar_cubo).place(relx=self.X_REL -.1, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_esfera(self):
        ttk.Button(self, text="Generar esfera", command=self._generar_esfera).place(relx=self.X_REL -.1, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_plano(self):
        ttk.Button(self, text="Generar poliedro", command=self._generar_plano).place(relx=self.X_REL, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_cilindro(self):
        ttk.Button(self, text="Generar cilindro", command=self._generar_cilindro).place(relx=self.X_REL, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_piramide(self):
        ttk.Button(self, text="Generar piramide", command=self._generar_cubo).place(relx=self.X_REL - 0.1, rely=0.7, relheight=0.05, relwidth=0.1, anchor="ne")        

    def _boton_generar_dibujar(self):
        ttk.Button(self, text="Generar dibujar", command=self._generar_dibujar).place(relx=self.X_REL, rely=0.7, relheight=0.05, relwidth=0.1, anchor="ne")        

    def _boton_generar_archivo(self):
        ttk.Button(self, text="Generar archivo", command=self._generar_archivo).place(relx=self.X_REL -.1, rely=0.8, relheight=0.05, relwidth=0.1, anchor="ne")        

    def _destruir_ventana_emergente(self):
        self.dialogo.destroy()
        interfaz.ventana-=1
        
    def _cerrado_tacha(self):
        interfaz.ventana-=1
        self.dialogo.destroy()
        
    def _generar_archivo(self):
        
        if interfaz.ventana <1:
    
            self.dialogo = tk.Toplevel()
            
            interfaz.ventana+=1
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            
            ident = self.dialogo.winfo_id()
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)

            self.cont=0
            self.An="NOMBRE DEL ARCHIVO"
            
            def Arch():
                if(self.cont == 0):
                    Output.insert(tk.END, 'Archivo abierto')
                    self.cont=1
                    self.An=inputtxt1.get("1.0", "end-1c")
                    self.archivo= open(self.An + ".txt")
                elif(self.cont == 1):
                    self.archivo.close()
                    Output.insert(tk.END, 'Archivo abierto')
                    self.An=inputtxt1.get("1.0", "end-1c")
                    self.archivo= open(self.An + ".txt")
                else:
                    Output.insert(tk.END, "ERROR DE ARCHIVO!!!")
                    
            def Leer():
        
                if interfaz.ventana < 2:
    
                    self.dial = tk.Toplevel()
            
                    interfaz.ventana+=1
            
                    interfaz.posx_y += 50
                    tamypos = '200x100+'+str(interfaz.posx_y)+ \
                              '+'+ str(interfaz.posx_y)
                    self.dial.geometry(tamypos)
                    self.dial.resizable(50,50)
                    self.dial.minsize(400, 650)
            
                    ident = self.dial.winfo_id()
            
                    titulo = str(interfaz.ventana)+": "+str(ident)
                    self.dial.title(titulo)
                    
                    #self.archivo.close()
                    #self.archiv = open(self.An + ".txt")
                    self.g=0

                    def destruir():
                        if self.g==0:
                            self.dial.destroy()
                            interfaz.ventana-=1
                        else:
                            self.dial.destroy()
                            self.archiv.close()
                            self.archivo = open(self.An + ".txt")
                            interfaz.ventana-=1
                            

                    def escribir():
                        self.archivo.close()
                        self.archiv = open(self.An + ".txt","w")
                        self.archiv.write(Lector.get("1.0", "end-1c"))
                        self.g=1

                    Lector = tk.Text(self.dial, height =30, width = 100, bg = "light cyan")
                    Sescri = tk.Button(self.dial, height = 2, width = 20, text = "GUARDAR", command = lambda:escribir())
                    cerrar = tk.Button(self.dial, height = 2, width = 20, text='CERRAR', command=destruir)
                    
                    Lector.insert(tk.END, self.archivo.read())
                    
                    Lector.pack()
                    Sescri.pack()
                    cerrar.pack()

                    self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
            
                else:
                    print("Por favor cierre la otra ventana emergente")

            def Gua():
                self.archivo.close()    

            l = tk.Label(self.dialogo, text = "ARCHIVOS")
            l1 = tk.Label(self.dialogo, text = "NOMBRE DEL ARCHIVO")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
     
            Display1 = tk.Button(self.dialogo, height = 2, width = 20, text = "ABIR ARCHIVO", command = lambda:Arch())
            Display2 = tk.Button(self.dialogo, height = 2, width = 20, text = "Leer archivo", command = lambda:Leer())
            Display3 = tk.Button(self.dialogo, height = 2, width = 20, text = "Cerrar archivo", command = lambda:Gua())
            
            l.pack()
            l1.pack()
            inputtxt1.pack()
            Display1.pack()
            Display2.pack()
            Display3.pack()
            Output.pack()
            
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
            
        else:
            print("Por favor cierre la otra ventana emergente")


    def _crear_cilindro_param(self, H, R, X, Y, Z):
        cilindro=poliedroConvexo.cilindro(punto(X,Y,Z), R, vector(0,0,H))
        
        hashes=[]
        for i in self.figuras["cilindro"]:
            hashes.append(hash(i))

        if hash(cilindro) not in hashes:
            self.figuras["cilindro"].append(cilindro)
            self._cambioFig()
            self._cambio()
            
    def _crear_cubo_param(self, B, X, Y, Z):
        cubo=poliedroConvexo.paralelepipedo(punto(X,Y,Z),vector(B,0,0),vector(0,B,0),vector(0,0,B))
        
        hashes=[]
        for i in self.figuras["paralelepipedos"]:
            hashes.append(hash(i))

        if hash(cubo) not in hashes:
            self.figuras["paralelepipedos"].append(cubo)
            self._cambioFig()
            self._cambio()

    def _crear_esfera_param(self, R, X, Y, Z):
        esfera=poliedroConvexo.esfera(punto(X,Y,Z),R)
        
        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))

        if hash(esfera) not in hashes:
            self.figuras["esferas"].append(esfera)
            self._cambioFig()
            self._cambio()

    def _crear_plano_param(self, x1, x2, x3, y1, y2, y3):
        plano=poliedroConvexo.paralelepipedo(punto(0,0,0),vector(x1,x2,x3),vector(y1,y2,y3),vector(y1,y2,y3))
        
        hashes=[]
        for i in self.figuras["plano"]:
            hashes.append(hash(i))

        if hash(plano) not in hashes:
            self.figuras["plano"].append(plano)
            self._cambioFig()
            self._cambio()

    def _crear_piramide_param(self, R, X, Y, Z):
        esfera=poliedroConvexo.esfera(punto(X,Y,Z),R)
        
        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))

        if hash(esfera) not in hashes:
            self.figuras["esferas"].append(esfera)
            self._cambioFig()
            self._cambio()

    # def _crear_linea_param(self, x1, x2, x3, y1, y2, y3):
    #     linea=poliedroConvexo.paralelepipedo(punto(x1,x2,x3),vector(y1,y2,y3),vector(y1,y2,y3),vector(y1,y2,y3))
        
    #     hashes=[]
    #     for i in self.figuras["paralelepipedos"]:
    #         hashes.append(hash(i))

    #     if hash(cubo) not in hashes:
    #         self.figuras["paralelepipedos"].append(linea)
    #         self._cambioFig()
    #         self._cambio()
    
    # def _crear_punto_param(self, X, Y, Z):
    #     punto=poliedroConvexo.esfera(punto(X,Y,Z), 0)
        
    #     hashes=[]
    #     for i in self.figuras["esferas"]:
    #         hashes.append(hash(i))

    #     if hash(esfera) not in hashes:
    #         self.figuras["esferas"].append(punto)
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
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            
            ident = self.dialogo.winfo_id()
            
            titulo = str(interfaz.ventana)+": "+str(ident)
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
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE PARALELEPIPEDOS")
            l1 = tk.Label(self.dialogo, text = "Base")
            l2 = tk.Label(self.dialogo, text = "Posición en x")
            l3 = tk.Label(self.dialogo, text = "Posición en y")
            l4 = tk.Label(self.dialogo, text = "Posición en z")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Cubog())
     
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            l4.pack()
            inputtxt4.pack()
            Display.pack()
            Output.pack()
            
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
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            
            ident = self.dialogo.winfo_id()
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)

            def Esfeg():
                radio = float(inputtxt1.get("1.0", "end-1c"))
                posx = float(inputtxt2.get("1.0", "end-1c"))
                posy = float(inputtxt3.get("1.0", "end-1c"))
                posz = float(inputtxt4.get("1.0", "end-1c"))
                self._crear_esfera_param(radio, posx, posy, posz)
                if(radio < 0):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                else:
                    Output.insert(tk.END, 'Captura de datos correcta')
                    
            l = tk.Label(self.dialogo, text = "GENERADOR DE ESFERAS")
            l1 = tk.Label(self.dialogo, text = "Radio")
            l2 = tk.Label(self.dialogo, text = "Posición x")
            l3 = tk.Label(self.dialogo, text = "Posición y")
            l4 = tk.Label(self.dialogo, text = "Posicion z")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Esfeg())
     
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            l4.pack()
            inputtxt4.pack()
            Display.pack()
            Output.pack()
            
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
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            
            ident = self.dialogo.winfo_id()
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
    
            def Plag():
                X1 = float(inputtxt1.get("1.0", "end-1c"))
                X2 = float(inputtxt2.get("1.0", "end-1c"))
                X3 = float(inputtxt3.get("1.0", "end-1c"))
                Y1 = float(inputtxt4.get("1.0", "end-1c"))
                Y2 = float(inputtxt5.get("1.0", "end-1c"))
                Y3 = float(inputtxt6.get("1.0", "end-1c"))
                if(punto(X1,X2,X3) == punto(0,0,0)):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                elif(punto(Y1,Y2,Y3) == punto(0,0,0)):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                else:
                    Output.insert(tk.END, 'Captura de datos correcta')
                    self._crear_plano_param(X1, X2, X3, Y1, Y2, Y3)
                     
            l = tk.Label(self.dialogo, text = "GENERADOR DE PLANOS")
            l1 = tk.Label(self.dialogo, text = "X_1")
            l2 = tk.Label(self.dialogo, text = "X_2")
            l3 = tk.Label(self.dialogo, text = "X_3")
            l4 = tk.Label(self.dialogo, text = "Y_1")
            l5 = tk.Label(self.dialogo, text = "Y_2")
            l6 = tk.Label(self.dialogo, text = "Y_3")            
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt5 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt6 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Plag())
     
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            l4.pack()
            inputtxt4.pack()
            l5.pack()
            inputtxt5.pack()
            l6.pack()
            inputtxt6.pack()
            Display.pack()
            Output.pack()
            
            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)
            
        else:
            print("Por favor cierre la otra ventana emergente")
    
    def _generar_piramide(self):
        
        if interfaz.ventana <1:
    
            self.dialogo = tk.Toplevel()
            
            interfaz.ventana+=1
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            
            ident = self.dialogo.winfo_id()
            
            titulo = str(interfaz.ventana)+": "+str(ident)
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
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE PARALELEPIPEDOS")
            l1 = tk.Label(self.dialogo, text = "Base")
            l2 = tk.Label(self.dialogo, text = "Posición en x")
            l3 = tk.Label(self.dialogo, text = "Posición en y")
            l4 = tk.Label(self.dialogo, text = "Posición en z")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Cubog())
     
            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            l4.pack()
            inputtxt4.pack()
            Display.pack()
            Output.pack()
            
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
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 600)

            ident = self.dialogo.winfo_id()

            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)

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

            l = tk.Label(self.dialogo, text = "DIBUJA PUNTOS Y LINEAS")
            l1 = tk.Label(self.dialogo, text = "X1")
            l2 = tk.Label(self.dialogo, text = "X2")
            l3 = tk.Label(self.dialogo, text = "X3")
            l4 = tk.Label(self.dialogo, text = "Y1")
            l5 = tk.Label(self.dialogo, text = "Y2")
            l6 = tk.Label(self.dialogo, text = "Y3")

            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt5 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt6 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")

            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")

            Display1 = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR PUNTO", command = lambda:Pung())
            Display2 = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR LINEA", command = lambda:Ling())

            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            Display1.pack()
            l4.pack()
            inputtxt4.pack()
            l5.pack()
            inputtxt5.pack()
            l6.pack()
            inputtxt6.pack()
            Display2.pack()
            Output.pack()

            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)

        else:
            print("Por favor cierre la otra ventana emergente")

    def _generar_cilindro(self):

        if interfaz.ventana<1:

            self.dialogo = tk.Toplevel()

            interfaz.ventana+=1

            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 550)

            ident = self.dialogo.winfo_id()

            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)

            boton = ttk.Button(self.dialogo, text='CERRAR', command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)

            def Cilg():
                altura = float(inputtxt1.get("1.0", "end-1c"))
                radio = float(inputtxt5.get("1.0", "end-1c"))
                posx = float(inputtxt2.get("1.0", "end-1c"))
                posy = float(inputtxt3.get("1.0", "end-1c"))
                posz = float(inputtxt4.get("1.0", "end-1c"))
                self._crear_cilindro_param(altura, radio, posx, posy, posz)
                if(radio < 0):
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
                else:
                    Output.insert(tk.END, 'Captura de datos correcta')

            l = tk.Label(self.dialogo, text = "GENERADOR DE CILINDROS")
            l1 = tk.Label(self.dialogo, text = "Altura")
            l2 = tk.Label(self.dialogo, text = "Posición x")
            l3 = tk.Label(self.dialogo, text = "Posición y")
            l4 = tk.Label(self.dialogo, text = "Posicion z")
            l5 = tk.Label(self.dialogo, text = "Radio")
            inputtxt1 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")
            inputtxt5 = tk.Text(self.dialogo, height = 2, width = 25, bg = "light yellow")

            Output = tk.Text(self.dialogo, height = 2, width = 25, bg = "light cyan")

            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="CREAR", command = lambda:Cilg())

            l.pack()
            l1.pack()
            inputtxt1.pack()
            l2.pack()
            inputtxt2.pack()
            l3.pack()
            inputtxt3.pack()
            l4.pack()
            inputtxt4.pack()
            l5.pack()
            inputtxt5.pack()
            Display.pack()
            Output.pack()

            self.dialogo.protocol("WM_DELETE_WINDOW", self._cerrado_tacha)

        else:
            print("Por favor cierre la otra ventana emergente")

    def _leer_archivo(self, evento):

        try:        
            geoms=MCNPaGeom(lecturaMCNP(self.archivo))
            self.figuras=geoms
            self._cambioFig()
            self._cambio()

        except:
            print("No se pudo leer el archivo")

        #vertices={item: val.punto_arreglo() for item, val in enumerate(esfera.con_puntos)}
        #self._manejo_geometria._vertices= vertices

    def _figurasRender(self):

        if self.cambioFig:
            caras=self._manejo_geometria._caras
            vertices=self._manejo_geometria._vertices

            for geom in self.figuras:
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

    def _cambio(self,*arg):
        self.cambio=True

    def _cambioFig(self, *args):
        self.cambioFig=True

    def _reiniciar_rotacion(self):
        self._manejo_geometria.reiniciar_angulos()
        self.deslizante_rot_x.set(0)
        self.deslizante_rot_y.set(0)
        self.deslizante_rot_z.set(0)

        self._cambio()

    def _obtener_rotacion(self):
        self._manejo_geometria._angulo_x=self.deslizante_rot_x.get()
        self._manejo_geometria._angulo_y=self.deslizante_rot_y.get()
        self._manejo_geometria._angulo_z=self.deslizante_rot_z.get()

    def _obtener_zoom(self):
        self._manejo_geometria._zoom=self.deslizante_zoom.get()

    def _cambio_ventana(self, evento):
        self._manejo_geometria.CANVAS_WIDTH=self.canvas.winfo_width()
        self._manejo_geometria.CANVAS_HEIGHT==self.canvas.winfo_height()

    def dibujar(self):
        self._obtener_rotacion()
        self._obtener_zoom()
        #print(type(self.canvas))
        if self.cambioFig:
            self._figurasRender()
            self.cambioFig=False

        if self.cambio and len(self._manejo_geometria._caras):

            self.canvas.delete("all")
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