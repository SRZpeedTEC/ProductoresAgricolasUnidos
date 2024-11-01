from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRegistros import ManipulacionRegistros

class GuardarMateriaPrima:
    
    def __init__(self, productos):
         
        self.productos = productos
        ManipulacionRegistros()
    
    def guardar_materia_prima(self, codigo, cantidad, ventana, tree, sumar=True):
        if codigo and cantidad:
            try:
                cantidad = float(cantidad)
                ManipulacionRegistros.actualizar_registro(codigo, cantidad, sumar=sumar)                   
                if ventana:
                    ventana.destroy()
                ManipulacionRegistros.cargar_materia_prima(tree)
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            
    def guardar_nueva_materia_prima(self, codigo_var, cantidad_var, ventana_toplvl, treeProductos):
        codigo = codigo_var.get().strip()
        cantidad_nueva = cantidad_var.get().strip()
        ventana = ventana_toplvl
        treeProductos = treeProductos
        

        self.guardar_materia_prima(
            codigo,
            cantidad_nueva,
            ventana,
            treeProductos,
            sumar=True        
        )
    
    def guardar_materia_prima_editada(self, codigo_var_editar, cantidad_var_editar, ventana_toplvl, treeProductos):
        codigo = codigo_var_editar.get().strip()
        nueva_cantidad = cantidad_var_editar.get().strip()
        ventana = ventana_toplvl
        treeProductos = treeProductos

        self.guardar_materia_prima(
            codigo,
            nueva_cantidad,
            ventana,
            treeProductos,
            sumar=False            
        )