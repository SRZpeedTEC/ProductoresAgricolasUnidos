from tkinter import *
from tkinter import ttk
import os

class VerLotesProcesados:

    def __init__(self, parent_frame):
        # Limpiar el frame antes de agregar nuevos widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Etiqueta de título
        Label(parent_frame, text="Lotes Procesados", bg="#A0D683", font=("Arial", 18, "bold")).pack(pady=10)

        # Crear un Treeview para mostrar los lotes procesados con columnas detalladas
        columns = ("Lote", "Pequeños Verdes", "Pequeños Maduros", "Grandes Verdes", "Grandes Maduros", "Dañados")
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=15)
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        tree.heading("Lote", text="ID del Lote")
        tree.heading("Pequeños Verdes", text="Pequeños Verdes (kg)")
        tree.heading("Pequeños Maduros", text="Pequeños Maduros (kg)")
        tree.heading("Grandes Verdes", text="Grandes Verdes (kg)")
        tree.heading("Grandes Maduros", text="Grandes Maduros (kg)")
        tree.heading("Dañados", text="Dañados (kg)")

        # Ajustar el ancho de las columnas
        for col in columns:
            tree.column(col, width=150, anchor=CENTER)

        # Leer el archivo de lotes procesados y llenar el Treeview
        self.cargar_lotes_procesados(tree)

    def cargar_lotes_procesados(self, tree):
        # Leer los lotes procesados del archivo y mostrarlos en el Treeview
        if os.path.exists("lotes_procesados.txt"):
            with open("lotes_procesados.txt", "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split(':', 1)
                        if len(partes) == 2:
                            lote_id = partes[0]
                            detalles = partes[1].split(", ")

                            # Inicializar los valores para cada columna
                            detalle_dict = {
                                "Pequeños Verdes": 0,
                                "Pequeños Maduros": 0,
                                "Grandes Verdes": 0,
                                "Grandes Maduros": 0,
                                "Dañados": 0
                            }

                            # Parsear los detalles y asignar los valores correspondientes
                            for detalle in detalles:
                                key, value = detalle.split(": ")
                                key = key.strip()
                                value = int(value.strip().replace(" kg", ""))
                                if key in detalle_dict:
                                    detalle_dict[key] = value

                            # Insertar en el Treeview
                            tree.insert("", "end", values=(
                                lote_id,
                                detalle_dict["Pequeños Verdes"],
                                detalle_dict["Pequeños Maduros"],
                                detalle_dict["Grandes Verdes"],
                                detalle_dict["Grandes Maduros"],
                                detalle_dict["Dañados"]
                            ))
        else:
            Label(tree, text="No hay lotes procesados aún.", bg="#B6FFA1", font=("Arial", 12)).pack(pady=10)
