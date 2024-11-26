import os
from tkinter import Toplevel, Label, Entry, Button, messagebox, END
from tkinter import ttk

class EditarReceta:
    def __init__(self, path_recetas, receta, tree):
        """
        Inicializa la clase EditarReceta con la ruta al archivo de recetas y la receta seleccionada.
        
        :param path_recetas: Ruta al archivo de recetas.
        :param receta: Receta seleccionada (tupla con ID, Nombre, Cantidad, Unidad, Ingredientes).
        :param tree: Treeview que muestra las recetas.
        """
        self.path_recetas = os.path.abspath(path_recetas)
        self.receta = receta
        self.tree = tree
        self.ventana_editar = None
        self.id_receta_entry = None
        self.nombre_receta_entry = None
        self.cantidad_producir_entry = None
        self.unidad_produccion_combobox = None
        self.ingredientes_tree = None
        self.codigo_entry = None
        self.cantidad_entry = None

        self._crear_ventana_editar()

    def _crear_ventana_editar(self):
        """
        Crea la ventana para editar la receta seleccionada.
        """
        receta_id, nombre_receta, cantidad_producir, unidad_produccion, ingredientes_str = self.receta
        ingredientes_list = [tuple(ingrediente.split(":")) for ingrediente in ingredientes_str.split(";")]

        # Crear ventana para editar la receta
        self.ventana_editar = Toplevel()
        self.ventana_editar.title(f"Editar Receta: {nombre_receta}")
        self.ventana_editar.geometry("600x700")
        self.ventana_editar.resizable(False, False)
        self.ventana_editar.configure(bg="#f0f0f5")  # Fondo de ventana

        # Widgets para el formulario
        Label(self.ventana_editar, text="ID Receta:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.id_receta_entry = Entry(self.ventana_editar, width=30, bg="#ffffff", fg="#000000", font=("Arial", 11))
        self.id_receta_entry.insert(0, receta_id)
        self.id_receta_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.ventana_editar, text="Nombre Receta:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.nombre_receta_entry = Entry(self.ventana_editar, width=30, bg="#ffffff", fg="#000000", font=("Arial", 11))
        self.nombre_receta_entry.insert(0, nombre_receta)
        self.nombre_receta_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.ventana_editar, text="Cantidad a Producir:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_producir_entry = Entry(self.ventana_editar, width=30, bg="#ffffff", fg="#000000", font=("Arial", 11))
        self.cantidad_producir_entry.insert(0, cantidad_producir)
        self.cantidad_producir_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.ventana_editar, text="Unidad de Producción:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.unidad_produccion_combobox = ttk.Combobox(self.ventana_editar, width=27, state="readonly", font=("Arial", 11))
        self.unidad_produccion_combobox["values"] = ["Unidad", "Kilogramos", "Litros"]
        self.unidad_produccion_combobox.set(unidad_produccion)  # Establecer valor inicial
        self.unidad_produccion_combobox.grid(row=3, column=1, padx=10, pady=5)

        # Tabla de Ingredientes Seleccionados
        Label(self.ventana_editar, text="Ingredientes:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.ingredientes_tree = ttk.Treeview(self.ventana_editar, columns=("Código", "Cantidad"), show="headings")
        self.ingredientes_tree.heading("Código", text="Código")
        self.ingredientes_tree.heading("Cantidad", text="Cantidad")
        self.ingredientes_tree.column("Código", width=200, anchor="center")
        self.ingredientes_tree.column("Cantidad", width=150, anchor="center")
        self.ingredientes_tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew", rowspan=4)

        # Llenar el Treeview con los ingredientes actuales
        for codigo, cantidad in ingredientes_list:
            self.ingredientes_tree.insert("", "end", values=(codigo.strip(), cantidad.strip()))

        # Entradas para agregar un ingrediente nuevo
        Label(self.ventana_editar, text="Código Ingrediente:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.codigo_entry = Entry(self.ventana_editar, width=20, bg="#ffffff", fg="#000000", font=("Arial", 11))
        self.codigo_entry.grid(row=9, column=1, padx=10, pady=5)

        Label(self.ventana_editar, text="Cantidad:", bg="#f0f0f5", font=("Arial", 12, "bold")).grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.cantidad_entry = Entry(self.ventana_editar, width=20, bg="#ffffff", fg="#000000", font=("Arial", 11))
        self.cantidad_entry.grid(row=10, column=1, padx=10, pady=5)

        # Botón para agregar ingrediente
        Button(self.ventana_editar, text="Agregar Ingrediente", command=self.agregar_ingrediente, bg="#28a745", fg="#ffffff", font=("Arial", 11, "bold")).grid(row=11, column=0, padx=10, pady=10)

        # Botón para eliminar ingrediente
        Button(self.ventana_editar, text="Eliminar Ingrediente", command=self.eliminar_ingrediente, bg="#dc3545", fg="#ffffff", font=("Arial", 11, "bold")).grid(row=11, column=1, padx=10, pady=10)

        # Botón para guardar cambios
        Button(self.ventana_editar, text="Guardar Cambios", command=self.guardar_cambios, bg="#007bff", fg="#ffffff", font=("Arial", 12, "bold")).grid(row=12, column=1, padx=10, pady=20)

    def agregar_ingrediente(self):
        """
        Agrega un nuevo ingrediente al Treeview.
        """
        codigo = self.codigo_entry.get().strip()
        cantidad = self.cantidad_entry.get().strip()

        if not codigo or not cantidad:
            messagebox.showwarning("Advertencia", "Por favor, ingresa tanto el código como la cantidad del ingrediente.")
            return

        try:
            # Verificar que la cantidad sea numérica
            float(cantidad)
        except ValueError:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una cantidad válida (número).")
            return

        # Insertar el nuevo ingrediente en el Treeview
        self.ingredientes_tree.insert("", "end", values=(codigo, cantidad))
        self.codigo_entry.delete(0, END)
        self.cantidad_entry.delete(0, END)

    def eliminar_ingrediente(self):
        """
        Elimina el ingrediente seleccionado del Treeview.
        """
        seleccion = self.ingredientes_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un ingrediente para eliminar.")
            return

        for item in seleccion:
            self.ingredientes_tree.delete(item)

    def guardar_cambios(self):
        """
        Guarda los cambios realizados en la receta.
        """
        nuevo_id = self.id_receta_entry.get().strip()
        nuevo_nombre = self.nombre_receta_entry.get().strip()
        nueva_cantidad = self.cantidad_producir_entry.get().strip()
        nueva_unidad = self.unidad_produccion_combobox.get().strip()

        if not nuevo_id or not nuevo_nombre or not nueva_cantidad or not nueva_unidad:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Obtener los ingredientes del Treeview
        nuevos_ingredientes = []
        for item in self.ingredientes_tree.get_children():
            valores = self.ingredientes_tree.item(item)["values"]
            nuevos_ingredientes.append(f"{valores[0]}:{valores[1]}")

        # Formatear los ingredientes para el archivo
        ingredientes_str = ";".join(nuevos_ingredientes)

        # Actualizar el archivo
        try:
            # Leer todas las recetas del archivo
            with open(self.path_recetas, "r", encoding="utf-8") as file:
                recetas = file.readlines()

            # Actualizar la receta correspondiente
            for i in range(len(recetas)):
                partes = recetas[i].strip().split("|")
                if len(partes) >= 5 and partes[0] == self.receta[0]:
                    recetas[i] = f"{nuevo_id}|{nuevo_nombre}|{nueva_cantidad}|{nueva_unidad}|{ingredientes_str}\n"
                    break

            # Escribir las recetas actualizadas en el archivo
            with open(self.path_recetas, "w", encoding="utf-8") as file:
                file.writelines(recetas)

            # Actualizar el Treeview en la ventana principal
            self.tree.item(self.tree.selection()[0], values=(nuevo_id, nuevo_nombre, nueva_cantidad, nueva_unidad))

            # Mostrar mensaje de éxito y cerrar la ventana de edición
            messagebox.showinfo("Éxito", "Receta actualizada con éxito.")
            self.ventana_editar.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
