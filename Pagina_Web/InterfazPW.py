from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
import Utiles.Genericos as genericos
from PIL import ImageTk, Image

class InterfazWeb():
    
    def __init__(self, cliente=None):
        
        self.cliente = cliente
        self.Interfaz = Tk()
        self.Interfaz.title("Productores Agricolas Unidos Website")
        self.Interfaz.geometry('1024x768')
        self.Interfaz.config(bg='#fcfcfc')
        self.Interfaz.resizable(width=0, height=0)
        genericos.centrar_ventana(self.Interfaz, 1024, 768)
        
        self.crear_widgets()
        self.Interfaz.mainloop()
        
    def crear_widgets(self):
        # Crear el marco superior (barra de navegación)
        self.crear_barra_navegacion()
        
        # Crear el marco lateral izquierdo (categorías)
        self.crear_barra_lateral()
        
        # Crear el marco central (productos)
        self.crear_area_productos()
        
    def crear_barra_navegacion(self):
        nav_frame = Frame(self.Interfaz, bg="#274b2c", height=200, pady=10)
        nav_frame.pack(side=TOP, fill=X)
        
        # Botón de carrito de compras
        carrito_img = genericos.leer_imagen("./Resources/Imgs/carritoWeb.png", (30, 30))
        btn_carrito = Button(nav_frame, image=carrito_img, command=self.ver_carrito, bg="#274b2c", bd=0)
        btn_carrito.image = carrito_img  # Mantener referencia
        btn_carrito.pack(side=RIGHT, padx=20)
        
        # Label
        lbl_pagina_web = Label(nav_frame, text="Productores Agricolas Unidos", font=Font(family='Times', size=16, weight=BOLD), fg='white', bg="#274b2c")
        lbl_pagina_web.pack(side=LEFT, padx=10)
        
        # Barra de búsqueda
        self.buscar_var = StringVar()
        entry_buscar = Entry(nav_frame, textvariable=self.buscar_var, width=50)
        entry_buscar.pack(side=LEFT, padx=20)
        
        lupa_img = genericos.leer_imagen("./Resources/Imgs/lupa.png", (20, 20))
        btn_buscar = Button(nav_frame, image=lupa_img, command=self.buscar_productos, bg="#4a684d")
        btn_buscar.image = lupa_img  # Mantener referencia
        btn_buscar.pack(side=LEFT)
        
        if self.cliente is None:
            # Botones de Iniciar Sesión y Registrarse
            btn_iniciar_sesion = Button(nav_frame, text="Iniciar Sesión", font=Font(family='Times', size=12), background='white', command=self.iniciar_sesion, fg='white', bg="#274b2c", bd=0)
            btn_iniciar_sesion.pack(side=RIGHT, padx=10)
        
            btn_registrarse = Button(nav_frame, text="Registrarse", font=Font(family='Times', size=12), background='white', command=self.registrarse, fg='white', bg="#274b2c", bd=0)
            btn_registrarse.pack(side=RIGHT)
        else:
            lbl_usuario = Label(nav_frame, text=f"Bienvenido, {self.cliente[0]}", font=Font(family='Times', size=12), fg='white', bg="#274b2c")
            lbl_usuario.pack(side=RIGHT, padx=10)

            btn_cerrar_sesion = Button(nav_frame, text="Cerrar Sesión", font=Font(family='Times', size=12), background='white', command=self.cerrar_sesion, fg='white', bg="#274b2c", bd=0)
            btn_cerrar_sesion.pack(side=RIGHT)
        
        
        
    def crear_barra_lateral(self):
        sidebar_frame = Frame(self.Interfaz, bg="#4a684d", width=100, padx=20)
        sidebar_frame.pack(side=LEFT, fill=Y)
        
        # Ejemplo de botones de categorías
        categorias = ["Tomates", "Papas", "Chips", "Salsas", "Otros"]
        for categoria in categorias:
            btn_categoria = Button(sidebar_frame, text=categoria, font=Font(family='Times', size=16), background='white', command=lambda c=categoria: self.ver_categoria(c))
            btn_categoria.pack(fill=X, pady=10, padx=10)
            
        logo_empresa = genericos.leer_imagen("./Resources/Imgs/logoProvisional.png", (100, 100))       
        lbllogo = Label(sidebar_frame, image=logo_empresa, bg='#4a684d')
        lbllogo.image = logo_empresa
        lbllogo.pack(side=BOTTOM, pady=20)
            
    def crear_area_productos(self):
        # Crear un contenedor para el Canvas y el Scrollbar
        container = Frame(self.Interfaz)
        container.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # Crear un Canvas dentro del contenedor
        canvas = Canvas(container, bg="#FFFFFF")
        canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Añadir una barra de desplazamiento vertical al contenedor
        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configurar el Canvas para que use la Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear el product_frame dentro del Canvas
        self.product_frame = Frame(canvas, bg="#FFFFFF")
        
        # Añadir el product_frame al Canvas
        canvas.create_window((0, 0), window=self.product_frame, anchor='nw')
        
        # Actualizar el scrollregion del Canvas cuando cambie el tamaño del product_frame
        self.product_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Configurar las columnas del grid en product_frame
        for col in range(3):
            self.product_frame.grid_columnconfigure(col, weight=1)
        
        # Aquí puedes cargar los productos
        self.cargar_productos()
        
    def cargar_productos(self):
        # Ejemplo de lista de productos
        productos = [
            {"nombre": "Producto 1", "precio": "$10", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 2", "precio": "$20", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 3", "precio": "$30", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 4", "precio": "$40", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 5", "precio": "$50", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 6", "precio": "$60", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 7", "precio": "$70", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 8", "precio": "$80", "imagen": "./Resources/Imgs/logoProvisional.png"},
            # Puedes agregar más productos si lo deseas
        ]

        for idx, producto in enumerate(productos):
            frame_producto = Frame(self.product_frame, bd=2, relief=RIDGE)
            frame_producto.grid(row=idx // 4, column=idx % 4, padx=20, pady=10)

            # Cargar imagen del producto
            try:
                img = ImageTk.PhotoImage(Image.open(producto["imagen"]).resize((150, 150)))
            except:
                img = ImageTk.PhotoImage(Image.new('RGB', (150, 150), color='gray'))

            lbl_imagen = Label(frame_producto, image=img)
            lbl_imagen.image = img  # Mantener referencia
            lbl_imagen.pack()

            lbl_nombre = Label(frame_producto, text=producto["nombre"])
            lbl_nombre.pack()

            lbl_precio = Label(frame_producto, text=producto["precio"], fg="green")
            lbl_precio.pack()

            btn_agregar = Button(frame_producto, text="Agregar al Carrito", command=lambda p=producto: self.agregar_al_carrito(p))
            btn_agregar.pack(pady=5)
            
    def ver_carrito(self):
        messagebox.showinfo("Carrito", "Esta funcionalidad está en desarrollo.")
        
    def iniciar_sesion(self):
        messagebox.showinfo("Iniciar Sesión", "Esta funcionalidad está en desarrollo.")
        
    def cerrar_sesion(self):
        messagebox.showinfo("Cerrar Sesión", "Esta funcionalidad está en desarrollo.")   
           
    def registrarse(self):
        messagebox.showinfo("Registrarse", "Esta funcionalidad está en desarrollo.")
        
    def buscar_productos(self):
        termino = self.buscar_var.get()
        messagebox.showinfo("Buscar", f"Buscando productos que coincidan con: {termino}")
        
    def ver_categoria(self, categoria):
        messagebox.showinfo("Categoría", f"Mostrando productos de la categoría: {categoria}")
        
    def agregar_al_carrito(self, producto):
        messagebox.showinfo("Agregar al Carrito", f"{producto['nombre']} ha sido agregado al carrito.")
