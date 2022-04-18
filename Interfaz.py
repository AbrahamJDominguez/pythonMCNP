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
    figuras={"esferas":list(),"paralelepipedos":list(),"plano":list(),"cilindro":list(), "conot":list()}
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
        #self._boton_crear_cubo()
        #self._boton_crear_esfera()
        self._boton_reiniciar_rotacion()
        self._boton_generar_cubo()
        self._boton_generar_poliedro()
        self._boton_generar_esfera()
        self._boton_generar_cilindro()

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

    def _boton_crear_esfera(self):
        ttk.Button(self, text="Crear esfera", command=self._crear_esfera).place(relx=self.X_REL, rely=0.8, relheight=0.05, relwidth=0.2, anchor="ne")

    def _boton_crear_cubo(self):
        ttk.Button(self, text="Crear cubo", command=self._crear_cubo).place(relx=self.X_REL, rely=0.7, relheight=0.05, relwidth=0.2, anchor="ne")
        
    def _boton_generar_cubo(self):
        ttk.Button(self, text="Generar cubo", command=self._generar_cubo).place(relx=self.X_REL -.1, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_esfera(self):
        ttk.Button(self, text="Generar esfera", command=self._generar_esfera).place(relx=self.X_REL -.1, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_poliedro(self):
        ttk.Button(self, text="Generar poliedro", command=self._generar_poliedro).place(relx=self.X_REL, rely=0.6, relheight=0.05, relwidth=0.1, anchor="ne")

    def _boton_generar_cilindro(self):
        ttk.Button(self, text="Generar cilindro", command=self._generar_cilindro).place(relx=self.X_REL, rely=0.5, relheight=0.05, relwidth=0.1, anchor="ne")
        
    def _destruir_ventana_emergente(self):
        self.dialogo.destroy()
        interfaz.ventana-=1
        
    def _cerrado_tacha(self):
        interfaz.ventana-=1
        self.dialogo.destroy()
        

    def _generar_cubo(self):
        
        if interfaz.ventana <1:
    
            self.dialogo = tk.Toplevel()
            
            # Incrementa en 1 el contador de ventanas
            
            interfaz.ventana+=1
            
            # Recalcula posición de la ventana
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            # Obtiene identicador de la nueva ventana 
            
            ident = self.dialogo.winfo_id()
            
            # Construye mensaje de la barra de título
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            # Define el botón 'Cerrar' que cuando sea
            # presionado cerrará (destruirá) la ventana 
            # 'self.dialogo' llamando al método
            # 'self.dialogo.destroy'
            
            boton = ttk.Button(self.dialogo, text='CREAR', 
                               command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
    
            def Take_input():
                INPUT = inputtxt4.get("1.0", "end-1c")
                print(INPUT)
                if(INPUT == "120"):
                    Output.insert(tk.END, 'Captura de datos correcta')
                else:
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE PARALELEPIPEDOS")
            l1 = tk.Label(self.dialogo, text = "Base")
            l2 = tk.Label(self.dialogo, text = "Tamano en x")
            l3 = tk.Label(self.dialogo, text = "Tamano en y")
            l4 = tk.Label(self.dialogo, text = "Tamano en z")
            inputtxt1 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 3, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="GUARDAR DATOS", command = lambda:Take_input())
     
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

    def _generar_poliedro(self):
        
        if interfaz.ventana<1:
    
            self.dialogo = tk.Toplevel()
            
            # Incrementa en 1 el contador de ventanas
            
            interfaz.ventana+=1
            
            # Recalcula posición de la ventana
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            # Obtiene identicador de la nueva ventana 
            
            ident = self.dialogo.winfo_id()
            
            # Construye mensaje de la barra de título
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            # Define el botón 'Cerrar' que cuando sea
            # presionado cerrará (destruirá) la ventana 
            # 'self.dialogo' llamando al método
            # 'self.dialogo.destroy'
            
            boton = ttk.Button(self.dialogo, text='CREAR', 
                               command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
    
            def Take_input():
                INPUT = inputtxt4.get("1.0", "end-1c")
                print(INPUT)
                if(INPUT == "120"):
                    Output.insert(tk.END, 'Captura de datos correcta')
                else:
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE POLIEDROS")
            l1 = tk.Label(self.dialogo, text = "Número de lados")
            l2 = tk.Label(self.dialogo, text = "Posición x")
            l3 = tk.Label(self.dialogo, text = "Posición y")
            l4 = tk.Label(self.dialogo, text = "Tamaño")
            inputtxt1 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 3, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="GUARDAR DATOS", command = lambda:Take_input())
     
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
            
    def _generar_esfera_param(self, R, X, Y, Z):
        esfera=poliedroConvexo.esfera(punto(X,Y,Z),R)
        

        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))


        if hash(esfera) not in hashes:
            self.figuras["esferas"].append(esfera)
            self._cambioFig()
            self._cambio()
            
        
    def _generar_esfera(self):
        
        if interfaz.ventana<1:
                
    
            self.dialogo = tk.Toplevel()
            
            # Incrementa en 1 el contador de ventanas
            
            interfaz.ventana+=1
            
            # Recalcula posición de la ventana
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            # Obtiene identicador de la nueva ventana 
            
            ident = self.dialogo.winfo_id()
            
            # Construye mensaje de la barra de título
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            # Define el botón 'Cerrar' que cuando sea
            # presionado cerrará (destruirá) la ventana 
            # 'self.dialogo' llamando al método
            # 'self.dialogo.destroy'
            
            boton = ttk.Button(self.dialogo, text='CREAR', 
                               command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
    
            def Take_input():
                try:
                    INPUTR = float(inputtxt1.get("1.0", "end-1c"))
                    INPUTX = float(inputtxt2.get("1.0", "end-1c"))
                    INPUTY = float(inputtxt3.get("1.0", "end-1c"))
                    INPUTZ = float(inputtxt4.get("1.0", "end-1c"))
                    self._generar_esfera_param(INPUTR, INPUTX, INPUTY, INPUTZ)
                except:
                    Output.insert("end", "Error en la captura")
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE ESFERAS")
            l1 = tk.Label(self.dialogo, text = "Radio")
            l2 = tk.Label(self.dialogo, text = "Posición x")
            l3 = tk.Label(self.dialogo, text = "Posición y")
            l4 = tk.Label(self.dialogo, text = "Posicion z")
            inputtxt1 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 3, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="GUARDAR DATOS", command = lambda:Take_input())
     
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
            
    def _generar_cilindro(self):
        
        if interfaz.ventana<1:
    
            self.dialogo = tk.Toplevel()
            
            # Incrementa en 1 el contador de ventanas
            
            interfaz.ventana+=1
            
            # Recalcula posición de la ventana
            
            interfaz.posx_y += 50
            tamypos = '200x100+'+str(interfaz.posx_y)+ \
                      '+'+ str(interfaz.posx_y)
            self.dialogo.geometry(tamypos)
            self.dialogo.resizable(50,50)
            self.dialogo.minsize(400, 500)
            # Obtiene identicador de la nueva ventana 
            
            ident = self.dialogo.winfo_id()
            
            # Construye mensaje de la barra de título
            
            titulo = str(interfaz.ventana)+": "+str(ident)
            self.dialogo.title(titulo)
            
            # Define el botón 'Cerrar' que cuando sea
            # presionado cerrará (destruirá) la ventana 
            # 'self.dialogo' llamando al método
            # 'self.dialogo.destroy'
            
            boton = ttk.Button(self.dialogo, text='CREAR', 
                               command=self._destruir_ventana_emergente)   
            boton.pack(side=tk.BOTTOM, padx=20, pady=20)
    
            def Take_input():
                INPUT = inputtxt4.get("1.0", "end-1c")
                print(INPUT)
                if(INPUT == "120"):
                    Output.insert(tk.END, 'Captura de datos correcta')
                else:
                    Output.insert(tk.END, "ERROR EN CAPTURA DE DATOS!!!")
         
            l = tk.Label(self.dialogo, text = "GENERADOR DE CILINDROS")
            l1 = tk.Label(self.dialogo, text = "Altura")
            l2 = tk.Label(self.dialogo, text = "Posición x")
            l3 = tk.Label(self.dialogo, text = "Posición y")
            l4 = tk.Label(self.dialogo, text = "Posicion z")
            l5 = tk.Label(self.dialogo, text = "Radio")
            inputtxt1 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt2 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt3 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt4 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
            inputtxt5 = tk.Text(self.dialogo, height = 3, width = 25, bg = "light yellow")
     
            Output = tk.Text(self.dialogo, height = 3, width = 25, bg = "light cyan")
     
            Display = tk.Button(self.dialogo, height = 2, width = 20, text ="GUARDAR DATOS", command = lambda:Take_input())
     
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

        
    def _crear_esfera(self):
        esfera=poliedroConvexo.esfera(punto(2,2,2),2)
        #vertices={item: val.punto_arreglo() for item, val in enumerate(esfera.con_puntos)}
        #self._manejo_geometria._vertices= vertices

        hashes=[]
        for i in self.figuras["esferas"]:
            hashes.append(hash(i))


        if hash(esfera) not in hashes:
            self.figuras["esferas"].append(esfera)
            #print("nueva figura")
            self._cambioFig()
            self._cambio()
            
        #vertices=geomRenderVertices(esfera)
        #caras, vertices=geomRenderCaras(esfera, vertices)

        #self._manejo_geometria._caras=caras
        #self._manejo_geometria._vertices=vertices

        #caras=[]

        #for cara in esfera.poligonos_convexos:
        #    aux=[]
        #    for point in cara.puntos:
        #        aux.append(keyValue(vertices, point.punto_arreglo()))

        #    caras.append(aux)

        #self._manejo_geometria._caras=caras
        #self._cambioFig()
        #self._cambio()

    def _crear_cubo(self):
        cubo=poliedroConvexo.paralelepipedo(punto(1,1,1),vector(2,0,0),vector(0,2,0),vector(0,0,2))
        #vertices=geomRenderVertices(cubo)
        #vertices={item: val.punto_arreglo() for item, val in enumerate(cubo.con_puntos)}
        #self._manejo_geometria._vertices= vertices

        #caras, vertices=geomRenderCaras(cubo, vertices)
        hashes=[]
        for i in self.figuras["paralelepipedos"]:
            hashes.append(hash(i))

        if hash(cubo) not in hashes:
            self.figuras["paralelepipedos"].append(cubo)
            print("figura creada")
            self._cambioFig()
            self._cambio()

        #self._manejo_geometria._caras=caras
        #self._manejo_geometria._vertices=vertices
        #print(self._manejo_geometria._vertices)

        #caras=[]

        #for cara in cubo.poligonos_convexos:
        #    aux=[]
        #    for point in cara.puntos:
        #        aux.append(keyValue(vertices, point.punto_arreglo()))

        #    caras.append(aux)

        #self._manejo_geometria._caras=caras
        #self._cambioFig()
        #self._cambio()
        
    def _leer_archivo(self, evento):
        
        try:
        
            geoms=MCNPaGeom(lecturaMCNP(self.archivo))
            self.figuras=geoms[0]
            self.figuras_num=geoms[1]
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
                if geom == "plano":
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
