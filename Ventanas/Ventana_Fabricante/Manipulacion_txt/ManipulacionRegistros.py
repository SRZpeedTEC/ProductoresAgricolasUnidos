from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.Manipulacion_txt import ManipulacionTXT
class ManipulacionRegistros():
    
    registros = ManipulacionTXT.leer_materia_prima()
    
    @classmethod
    def cargar_materia_prima(cls, tree):
    # Limpiar el Treeview
        registros = cls.registros
        for item in tree.get_children():
            tree.delete(item)                        
        if registros:
            for codigo, (descripcion, cantidad, unidad) in registros.items():            
                tree.insert("", "end", values=(codigo, descripcion, cantidad, unidad))  
        else:               
            Label(tree, text="No hay materia prima registrada.", bg="white", font=("Times", 12)).pack(pady=10)
    
    @classmethod
    def actualizar_registro(cls, codigo, cantidad_nueva, sumar=True):
                
        registros = cls.registros
        if codigo in registros:
            descripcion, cantidad_existente, unidad = registros[codigo]  # CANTIDAD DE MATERIA Ej: Registros[TOM-001](descripcion, cantidad, unidad)   
            if sumar:
                registros[codigo] = (descripcion, cantidad_existente + cantidad_nueva, unidad)
            else:
                registros[codigo] = (descripcion, cantidad_nueva, unidad)
        else:
            registros[codigo] = (descripcion, cantidad_nueva, unidad)
            
        ManipulacionTXT.actualizar_materia_prima(registros)
    
    @classmethod
    def agregar_registro(cls, codigo, descripcion, cantidad, unidad, tree):
        
        registros = cls.registros
        if codigo in registros:
            return False               
        else:
            registros[codigo] = (descripcion, cantidad, unidad)
            ManipulacionTXT.escribir_nuevo_producto(codigo, descripcion, cantidad, unidad)
            ManipulacionRegistros.cargar_materia_prima(tree)
            return True
            
             
    @classmethod
    def eliminar_registro(cls, codigo):
        
        registros = cls.registros 
        
        if codigo in registros:
            del registros[codigo]
            ManipulacionTXT.actualizar_materia_prima(registros) 
            return True
        else:
            messagebox.showwarning("Advertencia", f"No se encontró el producto con código {codigo}.")
            return False