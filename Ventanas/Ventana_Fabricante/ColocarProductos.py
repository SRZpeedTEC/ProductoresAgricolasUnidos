from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from pathlib import Path
from tkinter import messagebox


class ColocarProductos:
    def __init__(self, parent):
        # Rutas a los archivos
        self.path_productos_listos = "Resources/txt_recetas/productos_listos.txt"
        self.path_productos_tienda = "Resources/txt_pagina_web/productos.txt"
        
        
        # Variables de descripción y categoría
        self.descripcion = None
        self.categoria = None

        # Título de la ventana
        Label(parent, text="Productos Disponibles en Tienda", font=("Times", 18, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar el contenido del archivo
        columns = ("ID", "Nombre", "Cantidad", "Unidad")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=8)  # Tamaño reducido
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")

        self.tree.column("ID", width=100, anchor=CENTER)
        self.tree.column("Nombre", width=200, anchor=W)
        self.tree.column("Cantidad", width=100, anchor=CENTER)
        self.tree.column("Unidad", width=100, anchor=CENTER)

        # Sección para ingresar precio
        frame_precio = Frame(parent, bg="white")
        frame_precio.pack(pady=10)

        Label(frame_precio, text="Precio por Unidad:", bg="white", font=("Times", 12)).grid(row=0, column=0, padx=5)
        self.entry_precio = Entry(frame_precio, width=15, font=("Times", 12))
        self.entry_precio.grid(row=0, column=1, padx=5)

        # Botón para agregar descripción
        Button(frame_precio, text="Agregar Descripción", command=self.agregar_descripcion, bg="#2196F3", font=("Times", 12), fg="white").grid(row=0, column=2, padx=10)

        # Botón para agregar categoría
        Button(frame_precio, text="Agregar Categoría", command=self.agregar_categoria, bg="#2196F3", font=("Times", 12), fg="white").grid(row=0, column=3, padx=10)

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

            # Agregar las líneas al Treeview
            for linea in lineas:
                partes = linea.strip().split("|")
                if len(partes) == 4:  # Formato: ID|Nombre|Cantidad|Unidad
                    self.tree.insert("", "end", values=(partes[0], partes[1], partes[2], partes[3]))

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

            # Obtener los datos del producto seleccionado
            item = self.tree.item(seleccion[0])
            valores = item["values"]  # ID, Nombre, Cantidad, Unidad
            producto_id, nombre, _, _ = valores

            # Solicitar la descripción
            self.descripcion = simpledialog.askstring(
                "Agregar Descripción",
                f"Ingrese la descripción para el producto '{nombre}':"
            )

            if self.descripcion:
                messagebox.showinfo("Descripción Agregada", f"Descripción guardada: {self.descripcion}")
            else:
                messagebox.showwarning("Advertencia", "No se ingresó ninguna descripción.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la descripción: {e}")

    def agregar_categoria(self):
        """
        Agrega una categoría al producto seleccionado.
        """
        try:
            # Verificar que se seleccionó un producto
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
                return

            # Solicitar la categoría
            self.categoria = simpledialog.askstring(
                "Agregar Categoría",
                "Ingrese la categoría para el producto:"
            )

            if self.categoria:
                messagebox.showinfo("Categoría Agregada", f"Categoría guardada: {self.categoria}")
            else:
                messagebox.showwarning("Advertencia", "No se ingresó ninguna categoría.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la categoría: {e}")

    def colocar_en_tienda(self):
        """
        Coloca el producto seleccionado en la tienda.
        """
        try:
            # Verificar que se seleccionó un producto
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un producto.")
                return

            # Verificar que todos los campos estén llenos
            if not self.descripcion or not self.categoria or not self.entry_precio.get().strip():
                messagebox.showwarning("Advertencia", "Debe completar la descripción, categoría y precio antes de continuar.")
                return

            # Obtener los datos del producto seleccionado
            item = self.tree.item(seleccion[0])
            valores = item["values"]  # ID, Nombre, Cantidad, Unidad
            producto_id, nombre, cantidad, unidad = valores

            # Obtener el precio
            precio = self.entry_precio.get().strip()
            if not precio.replace(".", "").isdigit():
                messagebox.showerror("Error", "Por favor, ingresa un precio válido.")
                return

            precio = float(precio)

            # Ruta de la foto (puedes cambiarla según el proyecto)
            foto = "./Resources/Imgs/logoProvisional.png"

            # Guardar en el archivo productos.txt
            with open(self.path_productos_tienda, "a", encoding="utf-8") as file:
                file.write(f"{nombre}|{self.descripcion}|{precio}|{cantidad}|{unidad}|{foto}|{self.categoria}\n")

            # Mostrar confirmación
            messagebox.showinfo("Éxito", f"El producto '{nombre}' fue colocado en la tienda correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo colocar el producto en tienda: {e}")
