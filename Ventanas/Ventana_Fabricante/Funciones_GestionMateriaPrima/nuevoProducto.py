from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima.GuardarMateriaPrima import GuardarMateriaPrima
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRegistros import ManipulacionTXT


class AgregarNuevoProducto:
    
    
    
    @staticmethod      
    def agregar_nuevo_producto():
        manipulador_txt = ManipulacionTXT()
        ventana_agregar = Toplevel()
        ventana_agregar.title("Agregar Materia Prima")
        ventana_agregar.geometry("300x400")       
                   
        lbl_codigo = Label(ventana_agregar, text=f"Digite el codigo para su producto")
        lbl_codigo.pack(pady=5)        
        ent_codigo = Entry(ventana_agregar)
        ent_codigo.pack(pady=5)

        # Etiqueta para mostrar la descripción del producto
        lbl_descripcion = Label(ventana_agregar, text=f"Digite la descripción del producto")
        lbl_descripcion.pack(pady=5)                 
        ent_descripcion = Entry(ventana_agregar)
        ent_descripcion.pack(pady=5)
        
        # Campo para ingresar la cantidad  
        lbl_unidad = Label(ventana_agregar, text=f"digite la unidad de medida de su producto")
        lbl_unidad.pack(pady=5)               
        ent_unidad = Entry(ventana_agregar)
        ent_unidad.pack(pady=5)

        Button(ventana_agregar, text="Guardar", command=lambda: manipulador_txt.escribir_nuevo_producto(ent_codigo.get() ,ent_descripcion.get(), ent_unidad.get(), ventana_agregar)).pack(pady=10)
        
        
    