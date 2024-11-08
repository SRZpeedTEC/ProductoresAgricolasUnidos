from tkinter import *
from tkinter import ttk
import os

class VerLotesProcesados:

    def __init__(self, frame_adjunto):
        for widget in frame_adjunto.winfo_children():
            widget.destroy()

        # Etiqueta de título
        Label(frame_adjunto, text="Lotes Procesados", bg="white", font=("Times", 18, "bold")).pack(pady=10)

        # Crear un Frame para contener el Treeview y las Scrollbars
        frame_tree = Frame(frame_adjunto)
        frame_tree.pack(fill=BOTH, expand=True)

        # Definir las columnas del Treeview
        column = ("Lote") # , "TOM-001", "TOM-002", "TOM-003", "PAP-001"

        # Crear el Treeview
        tree = ttk.Treeview(frame_tree, columns=column, show="headings", height=15)

        
        tree.heading("Lote", text="ID del Lote")
        '''
        tree.heading("TOM-001", text="Tomates Frescos kg")
        tree.heading("TOM-002", text="Tomates Frescos Grande kg")
        tree.heading("TOM-003", text="Tomates Frescos Pequeño kg")
        tree.heading("PAP-001", text="Papas Frescas")
        '''
       
        tree.column(column, width=150, anchor=CENTER)

        # Crear una Scrollbar vertical y asociarla al Treeview
        scrollbar_vertical = Scrollbar(frame_tree, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)

        # Crear una Scrollbar horizontal y asociarla al Treeview
        scrollbar_horizontal = Scrollbar(frame_tree, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side=BOTTOM, fill=X)

        # Empaquetar el Treeview
        tree.pack(fill=BOTH, expand=True)

    # Leer el archivo de lotes procesados y llenar el Treeview
        self.cargar_lotes_procesados(tree)

    def cargar_lotes_procesados(self, tree):
        # Leer los lotes procesados del archivo y mostrarlos en el Treeview
        if os.path.exists("Resources/txt_lotes/lotes_procesados.txt"):
            with open("Resources/txt_lotes/lotes_procesados.txt", "r") as file:
                for line in file:
                    if line.strip():                       
                        lote_id = line.strip()                                                    
                        tree.insert("", "end", values=(lote_id)) # detalles_columna["TOM-001"], detalles_columna["TOM-002"], detalles_columna["TOM-003"], detalles_columna["PAP-001"]
        else:
            Label(tree, text="No hay lotes procesados aún.", bg="white", font=("Times", 12)).pack(pady=10)
