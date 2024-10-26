from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima.GuardarMateriaPrima import GuardarMateriaPrima

class AgregarMateriaPrima:
    
    def __init__(self, productos):
              
        self.productos = productos
        self.guardar_materia_prima = GuardarMateriaPrima(self.productos)
            
    def agregar_materia_prima(self, tree):
        self.ventana_agregar = Toplevel()
        self.ventana_agregar.title("Agregar Materia Prima")
        self.ventana_agregar.geometry("300x400")       
        
        Label(self.ventana_agregar, text="Código del Producto:").pack(pady=5)
        self.codigo_var = StringVar()
        codigos_producto = list(self.productos.keys())
        self.codigo_selector = ttk.Combobox(self.ventana_agregar, textvariable=self.codigo_var, values=codigos_producto, state="readonly")
        self.codigo_selector.pack(pady=5)
        self.codigo_selector.bind("<<ComboboxSelected>>", self.actualizar_descripcion_producto)

        # Etiqueta para mostrar la descripción del producto
        Label(self.ventana_agregar, text="Descripción:").pack(pady=5)
        self.descripcion_var = StringVar()
        self.lbl_descripcion = Label(self.ventana_agregar, textvariable=self.descripcion_var)
        self.lbl_descripcion.pack(pady=5)
        
        # Campo para ingresar la cantidad  
        self.unidad_var = StringVar(self.ventana_agregar, value = "")     
        self.lbl_unidad = Label(self.ventana_agregar, text=f"cantidad en: {self.unidad_var.get()}")
        self.lbl_unidad.pack(pady=5) 
        self.cantidad_var = StringVar()
        Entry(self.ventana_agregar, textvariable=self.cantidad_var).pack(pady=5)

        Button(self.ventana_agregar, text="Guardar", command=lambda: self.guardar_materia_prima.guardar_nueva_materia_prima(self.codigo_var, self.cantidad_var, self.unidad_var, self.ventana_agregar, tree)).pack(pady=10)
        
    def actualizar_descripcion_producto(self, event):
        codigo = self.codigo_var.get()
        producto = self.productos.get(codigo, {})
        descripcion = producto.get('descripcion', 'No disponible')
        unidad = producto.get('unidadMedida', 'No disponible')        
        self.descripcion_var.set(descripcion)
        self.unidad_var.set(unidad)
        self.lbl_unidad.config(text=f"cantidad en: {self.unidad_var.get()}")
        
    