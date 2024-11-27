from tkinter import * 
from tkinter import ttk, filedialog
from tkinter import simpledialog
from tkinter import messagebox
import os

class ColocarProductos:
    def __init__(self, parent):
        # Rutas a los archivos
        self.path_productos_listos = "Resources/txt_recetas/productos_listos.txt"
        self.path_productos_tienda = "Resources/txt_pagina_web/productos.txt"
        self.default_image_path = "./Resources/Imgs/logoProvisional.png"  # Imagen predeterminada
             

        # Variables de descripción, categoría y ruta de imagen
        self.descripcion = None
        self.image_path = self.default_image_path

        # Título de la ventana
        Label(parent, text="Productos Disponibles en Tienda", font=("Times", 18, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar el contenido del archivo
        columns = ("ID", "Nombre", "Cantidad", "Unidad", "En Tienda")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)  # Tamaño reducido
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("En Tienda", text="En Tienda")

        self.tree.column("ID", width=100, anchor=CENTER)
        self.tree.column("Nombre", width=200, anchor=W)
        self.tree.column("Cantidad", width=100, anchor=CENTER)
        self.tree.column("Unidad", width=100, anchor=CENTER)
        self.tree.column("En Tienda", width=100, anchor=CENTER)

        # Sección para ingresar precio
        frame_precio = Frame(parent, bg="white")
        frame_precio.pack(pady=10)

        Label(frame_precio, text="Precio por Unidad:", bg="white", font=("Times", 12)).grid(row=0, column=0, padx=5)
        self.entry_precio = Entry(frame_precio, width=15, font=("Times", 12))
        self.entry_precio.grid(row=0, column=1, padx=5)

        # Botón para agregar descripción
        Button(frame_precio, text="Agregar Descripción", command=self.agregar_descripcion, bg="#2196F3", font=("Times", 12), fg="white").grid(row=0, column=2, padx=10)

        # Categoría mediante Combobox
        Label(frame_precio, text="Categoría:", bg="white", font=("Times", 12)).grid(row=0, column=3, padx=5)
        self.categoria_combobox = ttk.Combobox(
            frame_precio,
            values=["Tomates", "Papas", "Chips", "Salsas", "Otros"],
            font=("Times", 12),
            state="readonly",
            width=12
        )
        self.categoria_combobox.grid(row=0, column=4, padx=5)
        self.categoria_combobox.set("Seleccione")  # Valor inicial

        # Sección para cargar imagen
        frame_imagen = Frame(parent, bg="white")
        frame_imagen.pack(pady=10)

        Label(frame_imagen, text="Imagen del Producto:", bg="white", font=("Times", 12)).grid(row=0, column=0, padx=5)
        self.image_label = Label(frame_imagen, text="Imagen predeterminada", bg="white", font=("Times", 10), fg="gray")
        self.image_label.grid(row=0, column=1, padx=5)

        Button(frame_imagen, text="Seleccionar Imagen", command=self.cargar_imagen, bg="#2196F3", font=("Times", 12), fg="white").grid(row=0, column=2, padx=10)

        # Botón para colocar en tienda
        Button(parent, text="Colocar en Tienda", command=self.colocar_en_tienda, bg="#4CAF50", font=("Times", 12), fg="white").pack(pady=10)

        # Cargar datos iniciales
        self.cargar_productos()

    def cargar_productos(self):
        """
        Carga el contenido del archivo productos_listos.txt en el Treeview.
        """
        try:
            # Limpiar el Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Leer el archivo de productos listos
            with open(self.path_productos_listos, "r", encoding="utf-8") as file:
                lineas = file.readlines()

            # Leer los productos en tienda
            productos_en_tienda = set()
            if os.path.exists(self.path_productos_tienda):
                with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                    for linea in file:
                        partes = linea.strip().split("|")
                        if len(partes) >= 1:
                            nombre_producto = partes[0].strip().lower()  # Usamos el nombre como identificador
                            productos_en_tienda.add(nombre_producto)

            # Agregar las líneas al Treeview
            for linea in lineas:
                partes = linea.strip().split("|")
                if len(partes) >= 4:  # Formato: ID|Nombre|Cantidad|Unidad
                    producto_id = partes[0]
                    nombre = partes[1]
                    cantidad = partes[2]
                    unidad = partes[3]
                    en_tienda = "Sí" if nombre.lower() in productos_en_tienda else "No"
                    self.tree.insert("", "end", values=(producto_id, nombre, cantidad, unidad, en_tienda))

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo productos_listos.txt no se encontró.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")



    def agregar_descripcion(self):
        """
        Agrega una descripción al producto seleccionado.
        """
        try:
            # Verificar que se seleccionó un producto
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
                return

            # Solicitar la descripción
            self.descripcion = simpledialog.askstring(
                "Agregar Descripción",
                "Ingrese la descripción para el producto seleccionado:"
            )

            if self.descripcion:
                messagebox.showinfo("Descripción Agregada", f"Descripción guardada: {self.descripcion}")
            else:
                messagebox.showwarning("Advertencia", "No se ingresó ninguna descripción.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la descripción: {e}")

    def cargar_imagen(self):
        """
        Permite seleccionar una imagen desde el explorador de archivos.
        """
        try:
            file_path = filedialog.askopenfilename(
                title="Seleccionar Imagen",
                filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp")]
            )

            if file_path:
                self.image_path = file_path
                self.image_label.config(text=os.path.basename(file_path), fg="black")
            else:
                self.image_path = self.default_image_path
                self.image_label.config(text="Imagen predeterminada", fg="gray")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def colocar_en_tienda(self):
        try:
            # Verificar que se seleccionó un producto
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
                return

            # Obtener los datos del producto seleccionado
            item = self.tree.item(seleccion[0])
            valores = item["values"]  # ID, Nombre, Cantidad, Unidad, En Tienda
            producto_id, nombre, cantidad_disponible, unidad, en_tienda = valores
            cantidad_disponible = int(float(cantidad_disponible))  # Convertir a entero

            # Leer el archivo de productos tienda
            productos_tienda = []
            if os.path.exists(self.path_productos_tienda):
                with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                    productos_tienda = file.readlines()

            # Verificar si el producto ya existe en la tienda
            producto_encontrado = None
            for i, linea in enumerate(productos_tienda):
                partes = linea.strip().split("|")
                if len(partes) >= 1 and partes[0].strip().lower() == nombre.lower():  # Comparar por nombre del producto
                    producto_encontrado = (i, partes)
                    break

            if producto_encontrado:
                # Si el producto ya existe, solo pedir la cantidad a agregar
                indice, datos_producto = producto_encontrado
                cantidad_actual = int(float(datos_producto[3]))  # Convertir a entero

                # Pedir la cantidad a agregar
                cantidad_a_agregar = simpledialog.askinteger(
                    "Agregar Cantidad",
                    f"El producto '{nombre}' ya existe en la tienda con {cantidad_actual} {unidad}. "
                    "Ingrese la cantidad adicional que desea publicar:",
                    minvalue=1,
                    maxvalue=cantidad_disponible
                )

                if cantidad_a_agregar is None:
                    return

                # Actualizar cantidad en el producto existente
                datos_producto[3] = str(cantidad_actual + cantidad_a_agregar)
                productos_tienda[indice] = "|".join(datos_producto) + "\n"

                # Restar la cantidad publicada de productos listos
                cantidad_disponible -= cantidad_a_agregar

            else:
                # Si el producto no existe, solicitar los campos adicionales
                if not self.descripcion or self.categoria_combobox.get() == "Seleccione" or not self.entry_precio.get().strip():
                    messagebox.showwarning("Advertencia", "Debe completar la descripción, categoría y precio antes de continuar.")
                    return

                # Verificar precio
                try:
                    precio = float(self.entry_precio.get().strip())
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingresa un precio válido.")
                    return

                # Pedir la cantidad a publicar
                cantidad_a_publicar = simpledialog.askinteger(
                    "Cantidad a Publicar",
                    f"El producto '{nombre}' no está en la tienda. Ingrese la cantidad a publicar:",
                    minvalue=1,
                    maxvalue=cantidad_disponible
                )

                if cantidad_a_publicar is None:
                    return

                productos_tienda.append(
                    f"{nombre}|{self.descripcion}|{precio}|{cantidad_a_publicar}|{unidad}|{self.image_path}|{self.categoria_combobox.get()}\n"
                )

                # Restar la cantidad publicada de productos listos
                cantidad_disponible -= cantidad_a_publicar

            # Guardar los cambios en productos tienda
            with open(self.path_productos_tienda, "w", encoding="utf-8") as file:
                file.writelines(productos_tienda)

            # Actualizar o eliminar el producto en productos_listos.txt
            self.actualizar_productos_listos(producto_id, cantidad_disponible)

            # Actualizar el Treeview
            self.cargar_productos()

            # Resetear campos si es necesario
            if not producto_encontrado:
                self.descripcion = None
                self.image_path = self.default_image_path
                self.image_label.config(text="Imagen predeterminada", fg="gray")
                self.entry_precio.delete(0, END)
                self.categoria_combobox.set("Seleccione")

            # Mostrar confirmación
            messagebox.showinfo("Éxito", f"El producto '{nombre}' fue actualizado en la tienda correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo colocar el producto en tienda: {e}")




    def actualizar_productos_listos(self, producto_id, cantidad_disponible):
        """
        Actualiza la cantidad disponible del producto en productos_listos.txt,
        o lo elimina si la cantidad es cero.
        """
        # Leer productos_listos.txt
        with open(self.path_productos_listos, "r", encoding="utf-8") as file:
            productos_listos = file.readlines()

        with open(self.path_productos_listos, "w", encoding="utf-8") as file:
            for linea in productos_listos:
                if linea.startswith(f"{producto_id}|"):
                    if cantidad_disponible > 0:
                        # Actualizar la cantidad
                        partes = linea.strip().split("|")
                        partes[2] = str(cantidad_disponible)
                        file.write("|".join(partes) + "\n")
                    # Si la cantidad es cero, no escribimos el producto (lo eliminamos)
                else:
                    file.write(linea)

