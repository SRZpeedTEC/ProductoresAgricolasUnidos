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
        factura_texto = ""  # Aquí almacenaremos el texto de la factura

        if self.carrito:
            for idx, (descripcion, producto) in enumerate(self.carrito.items()):  # Iterar sobre los elementos del diccionario
                precio = float(producto['precio'].replace('$', '').strip())  # Convertir el precio
                cantidad = producto['cantidad']  # Obtener cantidad
                total_producto = precio * cantidad  # Calcular el total del producto
                total_costo += total_producto  # Sumar al total general

                # Crear el texto de la factura
                factura_texto += f"{idx + 1}. {descripcion} - {cantidad} {producto['unidad']} x ${precio:.2f} = ${total_producto:.2f}\n"

            # Agregar el total
            factura_texto += f"\nTotal: ${total_costo:.2f}\n"
        else:
            factura_texto = "Tu carrito está vacío.\n"

        # Crear área de texto para mostrar la factura
        lbl_factura = Label(
            self.ventana,
            text=factura_texto,
            font=Font(family='Arial', size=12), bg='#fcfcfc', justify=CENTER, anchor=N
        )
        lbl_factura.pack(padx=10, pady=10, fill=X)

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
        # Verificar si el carrito está vacío
        if not self.carrito:
            messagebox.showinfo("Carrito", "Tu carrito está vacío.")
            return

        # Crear la factura y calcular el total
        try:
            factura_texto, total_costo = self.generar_factura()

            # Mostrar mensaje de confirmación al usuario
            messagebox.showinfo(
                "Compra Confirmada",
                f"Tu compra ha sido confirmada con éxito.\n¡Gracias por tu compra!\n\nTotal: ${total_costo:.2f}"
            )

            # Guardar la factura
            self.guardar_factura(factura_texto, total_costo)

            # Vaciar el carrito
            self.vaciar_carrito()

            # Cerrar la ventana actual
            self.ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al confirmar la compra:\n{str(e)}")

    def generar_factura(self):
        """Genera el texto de la factura y calcula el costo total."""
        factura_texto = ""
        total_costo = 0

        for idx, (descripcion, producto) in enumerate(self.carrito.items()):
            try:
                precio = float(producto['precio'].replace('$', '').strip())
                cantidad = producto['cantidad']
                total_producto = precio * cantidad
                total_costo += total_producto

                factura_texto += (
                    f"{idx + 1}. {descripcion} - {cantidad} {producto['unidad']} x "
                    f"${precio:.2f} = ${total_producto:.2f}\n"
                )
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error procesando el producto '{descripcion}': {e}")

        factura_texto += f"\nTotal: ${total_costo:.2f}"
        return factura_texto, total_costo

    def guardar_factura(self, factura_texto, total_costo):
        """Guarda la factura en el archivo correspondiente."""
        try:
            cliente_nombre = self.cliente[0] if self.cliente else 'Anonimo'
            factura_guardada = f"{cliente_nombre}, {factura_texto.replace(chr(10), ' | ')} | Total: ${total_costo:.2f}\n"

            with open("Resources/facturas.txt", "a", encoding="utf-8") as archivo_facturas:
                archivo_facturas.write(factura_guardada)

        except IOError as e:
            raise IOError(f"No se pudo guardar la factura: {e}")

    def vaciar_carrito(self):
        """Vacía el contenido del carrito y limpia el archivo correspondiente."""
        try:
            with open(self.carrito_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("")
            self.carrito.clear()
        except IOError as e:
            raise IOError(f"No se pudo vaciar el carrito: {e}")
