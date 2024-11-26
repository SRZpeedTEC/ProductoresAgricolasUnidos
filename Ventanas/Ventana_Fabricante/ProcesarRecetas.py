from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from Ventanas.Ventana_Fabricante.Funciones_ProcesarRecetas.VentanaProcesarRecetas import VentanaProcesarRecetas

class ProcesarRecetas:
    def __init__(self, frame):
        self.path_recetas = "Resources/txt_recetas/recetas.txt"
        self.path_productos_listos = "Resources/txt_recetas/productos_para_vender.txt"
        self.path_materia_prima = "Resources/txt_informacion_productos/materia_prima_fabrica.txt"

        Label(frame, text="Gestión de Recetas", bg="white", font=("Times", 18, "bold")).pack(pady=10)

        controls_frame = Frame(frame, bg="white")
        controls_frame.pack(pady=10)

        # Botón para procesar las recetas
        btn_font = ("Times", 10)
        btn_procesar = Button(controls_frame, text="Procesar Recetas", command=self.abrir_ventana_procesar_recetas, bg="#FCC509", font=btn_font, width=20)
        btn_procesar.grid(row=0, column=0, padx=5)

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
            # Leer las recetas desde el archivo
            if self.path_recetas != None:
                with open(self.path_recetas, "r", encoding="utf-8") as file:
                    recetas = file.readlines()

                # Insertar las recetas en el Treeview
                for receta in recetas:
                    partes = receta.strip().split("|")
                    if len(partes) == 5:  # ID, Nombre, Cantidad, Unidad, Ingredientes
                        id_receta, nombre_receta, cantidad, unidad, _ = partes

                        # Validar que la cantidad sea un entero
                        if not cantidad.isdigit():
                            messagebox.showwarning("Advertencia", f"La cantidad '{cantidad}' en la receta '{id_receta}' no es un número entero. Será omitida.")
                            continue

                        self.tree.insert("", "end", values=(id_receta, nombre_receta, int(cantidad), unidad))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar las recetas: {e}")

    def abrir_ventana_procesar_recetas(self):
        """
        Abre la ventana para procesar la receta seleccionada.
        """
        try:
            # Verificar si hay una selección en el Treeview
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una receta para procesar.")
                return

            # Obtener los valores de la fila seleccionada
            valores = self.tree.item(seleccion[0])["values"]
            receta_id = str(valores[0])
            nombre_receta = str(valores[1])

            # Verificar que la cantidad sea un número entero
            try:
                cantidad_procesada = int(valores[2])
            except ValueError:
                messagebox.showerror("Error", f"La cantidad '{valores[2]}' no es válida. Debe ser un número entero.")
                return

            unidad = str(valores[3])

            # Crear una nueva ventana emergente
            nueva_ventana = Toplevel()
            VentanaProcesarRecetas(nueva_ventana, receta_id, nombre_receta, cantidad_procesada, unidad)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de procesamiento: {e}")
