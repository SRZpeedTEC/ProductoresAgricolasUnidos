from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRecetasTXT import ManipulacionRecetasTXT
from Ventanas.Ventana_Fabricante.Funciones_GestionRecetas.AgregarReceta import agregar_receta
from Ventanas.Ventana_Fabricante.Funciones_GestionRecetas.EditarReceta import EditarReceta
from Ventanas.Ventana_Fabricante.Funciones_GestionRecetas.EliminarReceta import EliminarReceta
from Ventanas.Ventana_Fabricante.Funciones_GestionRecetas.VerIngredientes import ver_ingredientes
from pathlib import Path

class GestionRecetas:
    def __init__(self, frame):
        self.path_recetas = "Resources/txt_recetas/recetas.txt"

        self.eliminar_receta_helper = EliminarReceta(self.path_recetas)

        Label(frame, text="Gestión de Recetas", bg="white", font=("Times", 18, "bold")).pack(pady=10)

        controls_frame = Frame(frame, bg="white")
        controls_frame.pack(pady=10)

        # Botones para agregar, editar, eliminar y ver ingredientes
        btn_font = ("Times", 10)
        btn_agregar = Button(controls_frame, text="Agregar", command=self.agregar_receta, bg="#FCC509", font=btn_font, width=15)
        btn_agregar.grid(row=0, column=0, padx=5)

        btn_editar = Button(controls_frame, text="Editar", command=self.editar_receta, bg="#FCC509", font=btn_font, width=15)
        btn_editar.grid(row=0, column=1, padx=5)

        btn_eliminar = Button(controls_frame, text="Eliminar", command=self.eliminar_receta, bg="#FCC509", font=btn_font, width=15)
        btn_eliminar.grid(row=0, column=2, padx=5)

        btn_ver_ingredientes = Button(controls_frame, text="Ver Ingredientes", command=self.ver_ingredientes, bg="#FCC509", font=btn_font, width=15)
        btn_ver_ingredientes.grid(row=0, column=3, padx=5)

        # Treeview para mostrar las recetas
        columns = ("ID", "Nombre", "Cantidad", "Unidad")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.column("ID", width=100, anchor=CENTER)
        self.tree.column("Nombre", width=200, anchor=CENTER)
        self.tree.column("Cantidad", width=100, anchor=CENTER)
        self.tree.column("Unidad", width=100, anchor=CENTER)

        # Cargar datos iniciales
        self.actualizar_recetas()

    def actualizar_recetas(self):
        """
        Actualiza las recetas mostradas en el Treeview.
        """
        # Limpia el Treeview antes de cargar
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Recarga las recetas desde el archivo
            self.recetas = ManipulacionRecetasTXT.leer_recetas()

            # Insertar las recetas en el Treeview
            for receta in self.recetas:
                # Mostrar ID, Nombre, Cantidad a producir y Unidad
                id_receta, nombre_receta, cantidad, unidad, _ = receta
                self.tree.insert("", "end", values=(id_receta, nombre_receta, cantidad, unidad))
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo de recetas en: {self.path_recetas}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al actualizar las recetas: {e}")


    def agregar_receta(self):
        agregar_receta(self, self.actualizar_recetas)
        

    def editar_receta(self):
        """
        Abre una ventana para editar una receta seleccionada en el Treeview.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una receta para editar.")
            return

        valores = self.tree.item(seleccion[0])["values"]
        if not valores or len(valores) < 4:
            messagebox.showerror("Error", "No se pudo obtener los datos completos de la receta seleccionada.")
            return

        receta_id = str(valores[0])
        nombre_receta = str(valores[1])
        cantidad = str(valores[2])
        unidad = str(valores[3])

        # Obtener la receta actual desde el archivo
        try:
            recetas = ManipulacionRecetasTXT.leer_recetas()
            receta_encontrada = next((receta for receta in recetas if receta[0] == receta_id), None)

            if not receta_encontrada:
                messagebox.showerror("Error", f"No se pudo encontrar la receta con ID '{receta_id}'.")
                return

            # Abrir ventana para editar la receta
            
            editar_receta_window = EditarReceta(self.path_recetas, receta_encontrada, self.tree)
            editar_receta_window.guardar_cambios_callback = self.actualizar_recetas

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al editar la receta: {e}")


    def eliminar_receta(self):
        self.eliminar_receta_helper.eliminar_receta(self.tree)
        self.actualizar_recetas()

    def ver_ingredientes(self):
        """
        Llama a la función para mostrar los ingredientes de la receta seleccionada.
        """
        # Validar que se haya seleccionado una receta en el Treeview
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una receta para ver sus ingredientes.")
            return

        # Obtener los valores de la fila seleccionada
        valores = self.tree.item(seleccion[0])["values"]

        # Validar que se obtuvieron los datos completos
        if not valores or len(valores) < 4:
            messagebox.showerror("Error", "No se pudo obtener los datos completos de la receta seleccionada.")
            return

        # Extraer el ID de la receta
        receta_id = str(valores[0])

        # Leer las recetas desde el archivo para obtener los ingredientes más recientes
        try:
            recetas = ManipulacionRecetasTXT.leer_recetas()

            # Buscar la receta con el ID seleccionado
            receta_encontrada = next((receta for receta in recetas if receta[0] == receta_id), None)

            if not receta_encontrada:
                messagebox.showerror("Error", f"No se pudo encontrar la receta con ID '{receta_id}' en el archivo.")
                return

            # Obtener el nombre y los ingredientes de la receta encontrada
            _, nombre_receta, _, _, ingredientes_list = receta_encontrada

            # Llamar a la función `ver_ingredientes` pasando la lista de ingredientes
            receta = (receta_id, nombre_receta, ingredientes_list)
            ver_ingredientes(receta)

        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo de recetas en: {self.path_recetas}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al leer el archivo de recetas: {e}")
