from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima.GuardarMateriaPrima import GuardarMateriaPrima
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRegistros import ManipulacionRegistros

class EliminarMateriaPrima:
    
    def __init__(self, productos):
        
        self.productos = productos
        self.guardar_materia_prima = GuardarMateriaPrima(self.productos)
        self.manipular_registros = ManipulacionRegistros(self.productos)
        
    def eliminar_materia_prima(self, tree):
        # Obtener el item seleccionado
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un elemento para eliminar.")
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este registro?")
        if respuesta:
            # Obtener el código
            values = tree.item(selected_item, 'values')
            codigo_seleccionado = values[0]

            if self.manipular_registros.eliminar_registro(codigo_seleccionado):
                self.manipular_registros.cargar_materia_prima(tree)
                
    