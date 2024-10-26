from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima.GuardarMateriaPrima import GuardarMateriaPrima

class EditarMateriaPrima:
    
    def __init__(self, productos):
        
        self.productos = productos
        self.guardar_materia_prima = GuardarMateriaPrima(self.productos)
        
    def editar_materia_prima(self, treeProductos):
    # Obtener el item seleccionado
        selected_item = treeProductos.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un elemento para editar.")
            return
    
        # Obtener los valores
        values = treeProductos.item(selected_item, 'values')
        codigo_seleccionado = values[0]
        descripcion = values[1]
        cantidad_actual = values[2]
        unidad = values[3]
    
        # Crear una nueva ventana para editar
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Materia Prima")
        self.ventana_editar.geometry("350x250")
    
        # Campos de entrada
        Label(self.ventana_editar, text="Código:").pack(pady=5)
        self.codigo_var_editar = StringVar(value=codigo_seleccionado)
        Entry(self.ventana_editar, textvariable=self.codigo_var_editar, state='readonly').pack(pady=5)
    
        Label(self.ventana_editar, text="Descripción:").pack(pady=5)
        Label(self.ventana_editar, text=descripcion).pack(pady=5)
    
        Label(self.ventana_editar, text="Unidad de Medida:").pack(pady=5)
        Label(self.ventana_editar, text=unidad).pack(pady=5)
    
        Label(self.ventana_editar, text="Cantidad:").pack(pady=5)
        self.cantidad_var_editar = StringVar(value=cantidad_actual)
        Entry(self.ventana_editar, textvariable=self.cantidad_var_editar).pack(pady=5)
    
        Button(self.ventana_editar, text="Guardar", command=lambda: self.guardar_materia_prima.guardar_materia_prima_editada(self.codigo_var_editar, self.cantidad_var_editar, self.ventana_editar, treeProductos)).pack(pady=10)