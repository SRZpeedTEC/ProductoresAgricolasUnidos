from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
import Utiles.Genericos as genericos
from PIL import ImageTk, Image

class InterfazWeb():
    
    def __init__(self):
    
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
        nav_frame = Frame(self.Interfaz, bg="#A0D683", height=200, pady=10)
        nav_frame.pack(side=TOP, fill=X)
        
        # Botón de carrito de compras
        carrito_img = genericos.leer_imagen("./Resources/Imgs/carrito.png", (30, 30))
        btn_carrito = Button(nav_frame, image=carrito_img, command=self.ver_carrito, bg="#A0D683", bd=0)
        btn_carrito.image = carrito_img  # Mantener referencia
        btn_carrito.pack(side=RIGHT, padx=10)
        
        # Botones de Iniciar Sesión y Registrarse
        btn_iniciar_sesion = Button(nav_frame, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#FFFFFF", bd=0)
        btn_iniciar_sesion.pack(side=RIGHT, padx=10)
        
        btn_registrarse = Button(nav_frame, text="Registrarse", command=self.registrarse, bg="#FFFFFF", bd=0)
        btn_registrarse.pack(side=RIGHT)
        
        # Barra de búsqueda
        self.buscar_var = StringVar()
        entry_buscar = Entry(nav_frame, textvariable=self.buscar_var, width=50)
        entry_buscar.pack(side=LEFT, padx=50)
        
        btn_buscar = Button(nav_frame, text="Buscar", command=self.buscar_productos)
        btn_buscar.pack(side=LEFT)
        
    def crear_barra_lateral(self):
        sidebar_frame = Frame(self.Interfaz, bg="#F0F0F0", width=100, padx=20)
        sidebar_frame.pack(side=LEFT, fill=Y)
        
        # Ejemplo de botones de categorías
        categorias = ["Tomates", "Papas", "Chips", "Salsas", "Otros"]
        for categoria in categorias:
            btn_categoria = Button(sidebar_frame, text=categoria, command=lambda c=categoria: self.ver_categoria(c))
            btn_categoria.pack(fill=X, pady=5, padx=10)
    def crear_area_productos(self):
        self.product_frame = Frame(self.Interfaz, bg="#FFFFFF")
        self.product_frame.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # Aquí puedes cargar los productos
        self.cargar_productos()
        
    def cargar_productos(self):
        # Ejemplo de lista de productos
        productos = [
            {"nombre": "Producto 1", "precio": "$10", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 2", "precio": "$20", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 3", "precio": "$30", "imagen": "./Resources/Imgs/logoProvisional.png"},
            {"nombre": "Producto 4", "precio": "$40", "imagen": "./Resources/Imgs/logoProvisional.png"},
        ]
        
        for idx, producto in enumerate(productos):
            frame_producto = Frame(self.product_frame, bd=2, relief=RIDGE)
            frame_producto.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
            
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
        self.Interfaz.destroy()
        from Pagina_Web.Ventanas_Web.Login_Cliente import Login_Cliente
        Login_Cliente()
        # Luego, una vez que el login sea exitoso, puedes re-mostrar la ventana original
        if Login_Cliente.inicio_exitoso:  # Supongo que tienes una manera de verificar si el login fue exitoso
            self.Interfaz.deiconify()  # Mostrar la ventana de nuevo
        else:
            self.Interfaz.deiconify()  # Si el login falla, la ventana original se vuelve a mostrar
        
    def registrarse(self):
        self.Interfaz.destroy()
        from Pagina_Web.Ventanas_Web.Registro_Cliente import Registrar_Cliente
        Registrar_Cliente()
        
    def buscar_productos(self):
        termino = self.buscar_var.get()
        messagebox.showinfo("Buscar", f"Buscando productos que coincidan con: {termino}")
        
    def ver_categoria(self, categoria):
        messagebox.showinfo("Categoría", f"Mostrando productos de la categoría: {categoria}")
        
    def agregar_al_carrito(self, producto):
        messagebox.showinfo("Agregar al Carrito", f"{producto['nombre']} ha sido agregado al carrito.")

    
        
        
        