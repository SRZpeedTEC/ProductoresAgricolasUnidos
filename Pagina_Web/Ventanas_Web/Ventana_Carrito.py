from tkinter import *
import os
from tkinter.font import Font, BOLD
from tkinter import messagebox
from Pagina_Web.Funciones.obtener_productos_carrito import Obtener_productos_carrito
from Pagina_Web.Funciones.actualizar_productos_carrito import ActualizarProductoCarrito

class VentanaCarrito:
    def __init__(self, parent, cliente, interfaz_principal):
        
        self.parent = parent  # Aquí, parent será self.Interfaz
        self.cliente = cliente
        self.interfaz_web = interfaz_principal

        # Determinar el archivo de carrito basándonos en el atributo 'cliente'
        if self.cliente:
            self.carrito_archivo = f"Resources/carritos/carrito_{self.cliente[0]}.txt"
        else:
            self.carrito_archivo = "Resources/carritos/carrito_anonimo.txt"

        # Crear la ventana
        self.ventana = Toplevel(parent)  # Pasar parent como el master
        self.ventana.title("Tu carrito de compras")
        self.ventana.geometry('800x600')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)

        self.crear_widgets()

    

    def crear_widgets(self):
        # Contenedor para la barra superior
        barra_superior = Frame(self.ventana, bg="#B90518", height=50)
        barra_superior.pack(side=TOP, fill=X)

        # Título en la barra superior
        lbl_titulo = Label(
            barra_superior, text="Tu carrito de compras",
            font=Font(family='Times', size=20, weight=BOLD),
            fg='white', bg="#B90518"
        )
        lbl_titulo.pack(pady=10)

        # Contenedor para los productos
        productos_frame = Frame(self.ventana, bg='#fcfcfc')
        productos_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Leer y mostrar productos
        self.carrito = Obtener_productos_carrito.ObtenerProductosCarrito(self.carrito_archivo)
        total_costo = 0
        if self.carrito:
            for idx, (descripcion, producto) in enumerate(self.carrito.items()):  # Iterar sobre los elementos del diccionario
                precio = float(producto['precio'].replace('$', '').strip())  # Convertir el precio
                cantidad = producto['cantidad']  # Obtener cantidad
                total_producto = precio * cantidad  # Calcular el total del producto
                total_costo += total_producto  # Sumar al total general

                lbl_producto = Label(
                    productos_frame,
                    text=f"{idx + 1}. {descripcion} - {cantidad} {producto['unidad']} x ${precio:.2f} = ${total_producto:.2f}",
                    font=Font(family='Arial', size=12), bg='#fcfcfc'
                )
                lbl_producto.pack(anchor='w', pady=5)
        else:
            lbl_producto = Label(
                productos_frame,
                text="Tu carrito está vacío.",
                font=Font(family='Arial', size=14, weight=BOLD), bg='#fcfcfc'
            )
            lbl_producto.pack(anchor='center', pady=10)

        # Mostrar total
        lbl_total = Label(
            self.ventana, text=f"Total: ${total_costo:.2f}",
            font=Font(family='Arial', size=16, weight=BOLD), fg='#B90518', bg='#fcfcfc'
        )
        lbl_total.pack(pady=10)

        # Botones de acción
        botones_frame = Frame(self.ventana, bg='#fcfcfc')
        botones_frame.pack(pady=20)

        btn_confirmar = Button(
            botones_frame, text="Confirmar Compra",
            font=Font(family='Arial', size=12), bg='#4CAF50', fg='white',
            command=self.confirmar_compra
        )
        btn_confirmar.pack(side=LEFT, padx=10)

        btn_cerrar = Button(
            botones_frame, text="Cerrar",
            font=Font(family='Arial', size=12), bg='#f44336', fg='white',
            command=self.ventana.destroy
        )
        btn_cerrar.pack(side=LEFT, padx=10)

        # Botón "Vaciar Carrito" en la esquina inferior izquierda
        btn_vaciar = Button(
            self.ventana, text="Vaciar Carrito",
            font=Font(family='Arial', size=12), bg='#FF5722', fg='white',
            command=self.vaciar_carrito
        )
        btn_vaciar.pack(side=LEFT, padx=10, pady=10, anchor='w')


    def vaciar_carrito(self):
        # Iterar sobre los productos del carrito antes de vaciarlo
        if self.carrito:
            for descripcion, producto in self.carrito.items():
                # Llamar a la función para actualizar los productos
                ActualizarProductoCarrito.actualizar_producto_carrito(self, descripcion, producto['cantidad'])

        # Vaciar el archivo del carrito
        with open(self.carrito_archivo, "w") as archivo:
            archivo.write("")

        # Actualizar la interfaz principal
        self.interfaz_web.cargar_productos()

        # Cerrar la ventana actual
        self.ventana.destroy()

    def confirmar_compra(self):
        if not self.carrito:
            messagebox.showinfo("Carrito", "Tu carrito está vacío.")
            return

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Compra Confirmada", "Tu compra ha sido confirmada con éxito.")
        
        # Vaciar el archivo del carrito
        with open(self.carrito_archivo, "w") as archivo:
            archivo.write("")
        
        # Cerrar la ventana
        self.ventana.destroy()
