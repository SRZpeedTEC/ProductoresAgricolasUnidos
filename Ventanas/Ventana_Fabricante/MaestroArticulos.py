from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.Manipulacion_txt import ManipulacionTXT
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima import AgregarMateriaPrima, EditarMateriaPrima, EliminarMateriaPrima, nuevoProducto
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRegistros import ManipulacionRegistros

class GestionMateriaPrima:
    def __init__(self, frame):
             
        self.productos = ManipulacionTXT.leer_materia_prima()
        self.AgregarMateriaPrima = AgregarMateriaPrima.AgregarMateriaPrima(self.productos)
        self.EditarMateriaPrima = EditarMateriaPrima.EditarMateriaPrima(self.productos)
        self.EliminarMateriaPrima = EliminarMateriaPrima.EliminarMateriaPrima(self.productos)     
        
                                   
        Label(frame, text="Gestion Materias Primas", bg="white", font=("Times", 18, "bold")).pack(pady=10)
        
        
        controls_frame = Frame(frame, bg="white")
        controls_frame.pack(pady=10)
        
        # Botones de agregar, editar y eliminar
        btn_font = ("Times", 10)
        btn_agregar = Button(controls_frame, text="Agregar", command=self.agregar_materiaPrima, bg="#FCC509", font=btn_font, width=15)
        btn_agregar.grid(row=0, column=0, padx=5)
        
        btn_editar = Button(controls_frame, text="Editar", command=self.editar_materiaPrima, bg="#FCC509", font=btn_font, width=15)
        btn_editar.grid(row=0, column=1, padx=5)
        
        btn_eliminar = Button(controls_frame, text="Eliminar", command=self.eliminar_materiaPrima, bg="#FCC509", font=btn_font, width=15)
        btn_eliminar.grid(row=0, column=2, padx=5)
        
        btn_agregar_nuevo_producto = Button(controls_frame, text="Nuevo producto", command=lambda: self.nuevo_Producto(), bg="#FCC509", font=btn_font, width=15)
        btn_agregar_nuevo_producto.grid(row=0, column=3, padx=5)
        
        # Treeview para mostrar la materia prima
        columns = ("Código", "Descripción", "Cantidad", "Unidad")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=CENTER)
        
        # Cargar datos
        
        ManipulacionRegistros.cargar_materia_prima(self.tree)
           

    def agregar_materiaPrima(self):
        self.actualizar_materiaPrimaTXT()
        self.AgregarMateriaPrima.agregar_materia_prima(self.tree)
          
    def editar_materiaPrima(self):
        self.EditarMateriaPrima.editar_materia_prima(self.tree)
         
    def eliminar_materiaPrima(self):      
        self.EliminarMateriaPrima.eliminar_materia_prima(self.tree)
        
    def nuevo_Producto(self):
        nuevoProducto.AgregarNuevoProducto.agregar_nuevo_producto(self.tree)

    def actualizar_materiaPrima(self):
        ManipulacionRegistros.cargar_materia_prima(self.tree)
        
    def actualizar_materiaPrimaTXT(self):
        productos = ManipulacionTXT.leer_materia_prima()
        self.AgregarMateriaPrima = AgregarMateriaPrima.AgregarMateriaPrima(productos)
            
        
       
    
        


