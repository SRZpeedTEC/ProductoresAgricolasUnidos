from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.Manipulacion_txt import ManipulacionTXT

class ManipulacionRegistros:
    
    def __init__(self, productos):
        self.manipular_txt = ManipulacionTXT()
        self.productos = productos
        
    def cargar_materia_prima(self, tree):
    # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)        
        registros = self.manipular_txt.leer_materia_prima()            
        if registros:
            for codigo, (cantidad, unidad) in registros.items():
                producto = self.productos.get(codigo, {})
                descripcion = producto.get('descripcion', 'No disponible')
                tree.insert("", "end", values=(codigo, descripcion, cantidad, unidad))
    
        else:               
            Label(tree, text="No hay materia prima registrada.", bg="white", font=("Times", 12)).pack(pady=10)
    
    def actualizar_registro(self, codigo, cantidad_nueva, unidad, sumar=True):
        
        registros = self.manipular_txt.leer_materia_prima()

        if codigo in registros:
            cantidad_existente, unidad_existente = registros[codigo]         
            if sumar:
                registros[codigo] = (cantidad_existente + cantidad_nueva, unidad)
            else:
                registros[codigo] = (cantidad_nueva, unidad)
        else:
            registros[codigo] = (cantidad_nueva, unidad)
            
        self.manipular_txt.escribir_materia_prima(registros)  
             
    
    def eliminar_registro(self, codigo):
        registros = self.manipular_txt.leer_materia_prima()
        if codigo in registros:
            del registros[codigo]
            self.manipular_txt.escribir_materia_prima(registros)
            return True
        else:
            messagebox.showwarning("Advertencia", f"No se encontró el producto con código {codigo}.")
            return False