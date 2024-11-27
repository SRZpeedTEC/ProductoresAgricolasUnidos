from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
from tkinter import Toplevel, IntVar
import Utiles.Genericos as genericos
from PIL import ImageTk, Image
from Pagina_Web.Funciones.guardar_en_carrito import GuardarEnCarrito
from Pagina_Web.Funciones.cargar_productos import CargarProducto
from Pagina_Web.Funciones.obtener_productos import Obtener_productos
from Pagina_Web.Funciones.buscar_producto import buscarProductos
from Pagina_Web.Funciones.actualizar_productos import ActualizarProducto


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
        nav_frame = Frame(self.Interfaz, bg="#B90518", height=200, pady=10)
        nav_frame.pack(side=TOP, fill=X)
        
        # Botón de carrito de compras
        carrito_img = genericos.leer_imagen("./Resources/Imgs/carritoWeb.png", (30, 30))
        btn_carrito = Button(nav_frame, image=carrito_img, command=self.ver_carrito, bg="#B90518", bd=0)
        btn_carrito.image = carrito_img  # Mantener referencia
        btn_carrito.pack(side=RIGHT, padx=20)
        
        # Label
        lbl_pagina_web = Label(nav_frame, text="Productores Agricolas Unidos", font=Font(family='Times', size=16, weight=BOLD), fg='white', bg="#B90518")
        lbl_pagina_web.pack(side=LEFT, padx=10)
        
        # Barra de búsqueda
        self.buscar_var = StringVar()
        entry_buscar = Entry(nav_frame, textvariable=self.buscar_var, width=50)
        entry_buscar.pack(side=LEFT, padx=20)
        
        lupa_img = genericos.leer_imagen("./Resources/Imgs/lupa.png", (20, 20))
        btn_buscar = Button(nav_frame, image=lupa_img, command=self.buscar_productos, bg="#B90518")
        btn_buscar.image = lupa_img  # Mantener referencia
        btn_buscar.pack(side=LEFT)
        
        if self.cliente is None:
            # Botones de Iniciar Sesión y Registrarse
            btn_iniciar_sesion = Button(nav_frame, text="Iniciar Sesión", font=Font(family='Times', size=12), background='white', command=self.iniciar_sesion, fg='white', bg="#B90518", bd=0)
            btn_iniciar_sesion.pack(side=RIGHT, padx=10)
        
            btn_registrarse = Button(nav_frame, text="Registrarse", font=Font(family='Times', size=12), background='white', command=self.registrarse, fg='white', bg="#B90518", bd=0)
            btn_registrarse.pack(side=RIGHT)
        else:
            lbl_usuario = Label(nav_frame, text=f"Bienvenido {self.cliente[0]}", font=Font(family='Times', size=12), fg='white', bg="#B90518")
            lbl_usuario.pack(side=RIGHT, padx=10)

            btn_cerrar_sesion = Button(nav_frame, text="Cerrar Sesión", font=Font(family='Times', size=12), background='white', command=self.cerrar_sesion, fg='white', bg="#B90518", bd=0)
            btn_cerrar_sesion.pack(side=RIGHT)
        
        
        
    def crear_barra_lateral(self):
        sidebar_frame = Frame(self.Interfaz, bg="#c16767", width=100, padx=20)
        sidebar_frame.pack(side=LEFT, fill=Y)

        # Botones de categorías
        categorias = ["Tomates", "Papas", "Chips", "Salsas", "Otros"]
        for categoria in categorias:
            btn_categoria = Button(sidebar_frame, text=categoria, font=Font(family='Times', size=16), background='#e8dede', command=lambda c=categoria: self.ver_categoria(c))
            btn_categoria.pack(fill=X, pady=10, padx=10)

        btn_deshacer_filtro = Button(sidebar_frame, text="Sin filtros", font=Font(family='Times', size=16), background='#e8dede', command=lambda: self.cargar_productos())
        btn_deshacer_filtro.pack(fill=X, pady=10, padx=10)

        # Botón "Ver Historial"
        btn_ver_historial = Button(sidebar_frame, text="Ver Historial", font=Font(family='Times', size=16), background='yellow', command=self.ver_historial)
        btn_ver_historial.pack(fill=X, pady=10, padx=10, side=BOTTOM)


        # Logo de la empresa
        logo_empresa = genericos.leer_imagen("./Resources/Imgs/logoProvisional.png", (100, 100))
        lbllogo = Label(sidebar_frame, image=logo_empresa, bg='#c16767')
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
        
            
    def ver_carrito(self):   
        from Pagina_Web.Ventanas_Web.Ventana_Carrito import VentanaCarrito
        VentanaCarrito(self.Interfaz, self.cliente, self)  # Pasar self.Interfaz como parent
        
    def iniciar_sesion(self):
        self.Interfaz.destroy()
        from Pagina_Web.Ventanas_Web.Login_Cliente import Login_Cliente
        Login_Cliente()
        
    def cerrar_sesion(self):
        self.Interfaz.destroy()
        InterfazWeb()
           
    def registrarse(self):
        self.Interfaz.destroy()
        from Pagina_Web.Ventanas_Web.Registro_Cliente import Registrar_Cliente
        Registrar_Cliente()
        
    def buscar_productos(self):
        buscarProductos.buscar_productos(self)
        
    def cargar_productos(self):   
        self.productos = Obtener_productos.ObtenerProductos()   
        CargarProducto.mostrar_productos(self, self.productos)
        
    def ver_categoria(self, categoria):
        self.productos_filtrados = {}
        for nombre, detalles in self.productos.items():
            if detalles['categoria'].lower() == categoria.lower():
                self.productos_filtrados[nombre] = detalles
        CargarProducto.mostrar_productos(self, self.productos_filtrados)
        
    def agregar_al_carrito(self, producto):
        if not isinstance(producto, dict):
            messagebox.showerror("Error", "El producto seleccionado no es válido.")
            return

        # Crear ventana emergente (popup)
        popup = Toplevel(self.Interfaz)
        popup.title("Agregar al Carrito")
        popup.geometry("300x250")
        popup.resizable(width=0, height=0)

        # Mostrar información del producto
        lbl_producto = Label(popup, text=f"Producto: {producto['descripcion']}", font=('Arial', 12, 'bold'))
        lbl_producto.pack(pady=10)

        # Procesar el precio para convertirlo en número
        try:
            precio_unitario = float(producto['precio'].replace('$', '').strip())
        except ValueError:
            messagebox.showerror("Error", f"Precio inválido: {producto['precio']}")
            popup.destroy()
            return

        lbl_precio = Label(popup, text=f"Precio: ${precio_unitario:.2f} x {producto['unidad']}", font=('Arial', 10))
        lbl_precio.pack()

        # Variable para la cantidad seleccionada
        cantidad_var = IntVar(value=1)

        lbl_cantidad = Label(popup, text="Cantidad:", font=('Arial', 10))
        lbl_cantidad.pack(pady=5)

        spinbox_cantidad = Spinbox(popup, from_=1, to=int(producto['cantidad']), textvariable=cantidad_var, width=5)
        spinbox_cantidad.pack()

        # Label para mostrar el total
        lbl_total = Label(popup, text=f"Total: ${precio_unitario * cantidad_var.get():.2f}", font=('Arial', 12, 'bold'), fg="blue")
        lbl_total.pack(pady=10)

        # Actualizar el total dinámicamente
        def actualizar_total(*args):
            cantidad = cantidad_var.get()
            try:
                cantidad = int(cantidad)
                total = precio_unitario * cantidad
                lbl_total.config(text=f"Total: ${total:.2f}")
            except ValueError:
                lbl_total.config(text="Total: $0.00")

        # Vincular el cambio de cantidad al cálculo del total
        cantidad_var.trace_add("write", actualizar_total)

        # Botón para confirmar
        btn_confirmar = Button(popup, text="Añadir al Carrito", command=lambda: self.confirmar_agregar_carrito(popup, producto, cantidad_var.get()))
        btn_confirmar.pack(pady=10)



    def confirmar_agregar_carrito(self, popup, producto, cantidad):
        popup.destroy()  # Cerrar la ventana emergente
        ActualizarProducto.actualizar_producto(self,producto,cantidad)
        messagebox.showinfo("Carrito", f"{cantidad} x {producto['descripcion']} se han agregado al carrito.")
        GuardarEnCarrito.guardar_en_carrito(self,producto,cantidad)
        self.cargar_productos()
        
    def ver_historial(self):
        if self.cliente is None:
            messagebox.showerror("Error", "Debes iniciar sesión para ver tu historial.")
            return

        # Crear ventana Toplevel
        historial_window = Toplevel(self.Interfaz)
        nombre_cliente = self.cliente[0]
        historial_window.title(f"Historial de Facturas de {nombre_cliente}")
        historial_window.geometry("600x400")
        historial_window.resizable(False, False)

        # Contenedor para mostrar el historial
        frame_historial = Frame(historial_window, bg="#B90518")  # Cambiar el fondo del frame principal
        frame_historial.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Etiqueta del título
        lbl_titulo = Label(frame_historial, text=f"Historial de Facturas de {nombre_cliente}", font=('Arial', 16, 'bold'), bg="#B90518")
        lbl_titulo.pack(pady=10)

        try:
            # Leer el archivo de facturas
            with open("Resources/facturas.txt", "r") as archivo_facturas:
                facturas = archivo_facturas.readlines()

            # Filtrar las facturas del cliente actual
            facturas_cliente = [factura for factura in facturas if factura.split(", ", 1)[0] == nombre_cliente]


            if not facturas_cliente:
                lbl_no_facturas = Label(frame_historial, text="No tienes facturas en el historial.", font=('Arial', 12), bg="#ffffff", fg="#555555")
                lbl_no_facturas.pack(pady=20)
            else:
                # Mostrar las facturas en un texto con scroll
                text_historial = Text(frame_historial, wrap=WORD, height=15, font=('Arial', 10), bg="#f5f5f5")
                text_historial.pack(fill=BOTH, expand=True)

                for factura in facturas_cliente:
                    # Remover el nombre del cliente y duplicado del total
                    partes_factura = factura.split(", ", 1)[1].rsplit("| Total: ", 1)
                    detalles = partes_factura[0].strip()
                    total = partes_factura[1].strip()

                    # Insertar detalles y total
                    text_historial.insert(END, f"{detalles}\n")
                    text_historial.insert(END, f"Total: {total}\n\n")

                text_historial.config(state=DISABLED)  # Hacer el texto de solo lectura
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo de facturas no se encontró.")



    
