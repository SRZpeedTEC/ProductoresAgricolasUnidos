from tkinter import * 
from tkinter import ttk, filedialog
from tkinter import simpledialog
from tkinter import messagebox
import os

from tkinter import *
from tkinter import ttk, filedialog, messagebox

class EditarProductos:
    def __init__(self, parent):
        self.parent = parent
        self.path_productos_tienda = "Resources/txt_pagina_web/productos.txt"

        # Crear el frame principal dentro del parent (content_frame)
        self.frame = Frame(self.parent, bg="white")
        self.frame.pack(fill=BOTH, expand=True)

        # Crear el Treeview
        self.crear_treeview()

        # Cargar los productos en tienda
        self.cargar_productos_tienda()

        # Crear los botones para editar
        self.crear_botones()

    def crear_treeview(self):
        columns = ("Nombre", "Descripción", "Precio", "Cantidad", "Unidad", "Categoría")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=CENTER)

        self.tree.column("Nombre", width=150)
        self.tree.column("Descripción", width=200)
        self.tree.column("Precio", width=80)
        self.tree.column("Cantidad", width=80)
        self.tree.column("Unidad", width=80)
        self.tree.column("Categoría", width=100)

    def cargar_productos_tienda(self):
        try:
            # Limpiar el Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Leer el archivo de productos en tienda
            if os.path.exists(self.path_productos_tienda):
                with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                    for linea in file:
                        partes = linea.strip().split("|")
                        if len(partes) >= 7:
                            nombre = partes[0]
                            descripcion = partes[1]
                            precio = partes[2]
                            cantidad = partes[3]
                            unidad = partes[4]
                            imagen = partes[5]
                            categoria = partes[6]
                            self.tree.insert("", "end", values=(nombre, descripcion, precio, cantidad, unidad, categoria))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")

    def crear_botones(self):
        frame_botones = Frame(self.frame, bg="white")
        frame_botones.pack(pady=10)

        Button(frame_botones, text="Editar Producto", command=self.editar_producto, bg="#2196F3", font=("Times", 12), fg="white").grid(row=0, column=0, padx=10)
        Button(frame_botones, text="Cambiar Imagen", command=self.cambiar_imagen, bg="#4CAF50", font=("Times", 12), fg="white").grid(row=0, column=1, padx=10)
        Button(frame_botones, text="Eliminar Producto", command=self.eliminar_producto, bg="#F44336", font=("Times", 12), fg="white").grid(row=0, column=2, padx=10)

    def editar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para editar.")
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]  # Nombre, Descripción, Precio, Cantidad, Unidad, Categoría
        nombre_original = valores[0]
        descripcion_actual = valores[1]
        precio_actual = valores[2]
        categoria_actual = valores[5]

        # Crear frame para editar dentro de self.frame
        if hasattr(self, 'frame_editar'):
            self.frame_editar.destroy()

        self.frame_editar = Frame(self.frame, bg="white")
        self.frame_editar.pack(pady=10)

        Label(self.frame_editar, text="Descripción:", font=("Times", 12), bg="white").pack(pady=5, anchor=W)
        entry_descripcion = Text(self.frame_editar, height=2, width=50)
        entry_descripcion.pack()

        # Crear un frame para precio y categoría
        frame_precio_categoria = Frame(self.frame_editar, bg="white")
        frame_precio_categoria.pack(pady=5)

        # Campo de precio
        Label(frame_precio_categoria, text="Precio:", font=("Times", 12), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky=E)
        entry_precio = Entry(frame_precio_categoria, font=("Times", 12))
        entry_precio.grid(row=0, column=1, padx=5, pady=5)
        entry_precio.insert(0, precio_actual)

        # Combobox de categoría
        Label(frame_precio_categoria, text="Categoría:", font=("Times", 12), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky=E)
        categorias = ["Tomates", "Papas", "Chips", "Salsas", "Otros"]
        combobox_categoria = ttk.Combobox(frame_precio_categoria, values=categorias, state="readonly", font=("Times", 12), width=15)
        combobox_categoria.grid(row=0, column=3, padx=5, pady=5)
        combobox_categoria.set(categoria_actual)  # Establecer la categoría actual como seleccionada

        # Botón para guardar cambios
        Button(
            self.frame_editar,
            text="Guardar Cambios",
            command=lambda: self.guardar_cambios(
                nombre_original,
                entry_descripcion.get("1.0", END).strip(),
                entry_precio.get().strip(),
                combobox_categoria.get()
            ),
            bg="#4CAF50",
            font=("Times", 12),
            fg="white"
        ).pack(pady=10)


    def cambiar_imagen(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para cambiar la imagen.")
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]
        nombre_original = valores[0]

        # Seleccionar nueva imagen
        file_path = filedialog.askopenfilename(
            title="Seleccionar Nueva Imagen",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not file_path:
            return

        # Actualizar el archivo de productos
        try:
            productos_tienda = []
            with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                productos_tienda = file.readlines()

            # Actualizar la imagen del producto
            for i, linea in enumerate(productos_tienda):
                partes = linea.strip().split("|")
                if len(partes) >= 7 and partes[0].strip().lower() == nombre_original.lower():
                    partes[5] = file_path
                    productos_tienda[i] = "|".join(partes) + "\n"
                    break

            # Escribir los cambios
            with open(self.path_productos_tienda, "w", encoding="utf-8") as file:
                file.writelines(productos_tienda)

            messagebox.showinfo("Éxito", "La imagen del producto ha sido actualizada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la imagen: {e}")

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]
        nombre_original = valores[0]

        respuesta = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el producto '{nombre_original}' de la tienda?")
        if not respuesta:
            return

        # Eliminar el producto del archivo
        try:
            productos_tienda = []
            with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                productos_tienda = file.readlines()

            # Eliminar el producto
            productos_tienda = [linea for linea in productos_tienda if not linea.strip().split("|")[0].strip().lower() == nombre_original.lower()]

            # Escribir los cambios
            with open(self.path_productos_tienda, "w", encoding="utf-8") as file:
                file.writelines(productos_tienda)

            # Actualizar el Treeview
            self.cargar_productos_tienda()

            messagebox.showinfo("Éxito", f"El producto '{nombre_original}' ha sido eliminado de la tienda.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def guardar_cambios(self, nombre_original, nueva_descripcion, nuevo_precio, nueva_categoria):
        try:
            # Validar precio
            nuevo_precio = float(nuevo_precio)

            # Validar categoría
            if not nueva_categoria or nueva_categoria == "Seleccione":
                messagebox.showwarning("Advertencia", "Por favor, selecciona una categoría válida.")
                return

            # Leer productos de la tienda
            productos_tienda = []
            with open(self.path_productos_tienda, "r", encoding="utf-8") as file:
                productos_tienda = file.readlines()

            # Actualizar el producto
            for i, linea in enumerate(productos_tienda):
                partes = linea.strip().split("|")
                if len(partes) >= 7 and partes[0].strip().lower() == nombre_original.lower():
                    partes[1] = nueva_descripcion
                    partes[2] = str(nuevo_precio)
                    partes[6] = nueva_categoria
                    productos_tienda[i] = "|".join(partes) + "\n"
                    break

            # Escribir los cambios
            with open(self.path_productos_tienda, "w", encoding="utf-8") as file:
                file.writelines(productos_tienda)

            # Actualizar el Treeview
            self.cargar_productos_tienda()

            # Destruir el frame de edición
            self.frame_editar.destroy()

            messagebox.showinfo("Éxito", "El producto ha sido actualizado.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un precio válido.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")
