from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox

class GuardarMateriaPrima:
    
    def guardar_materia_prima(self, codigo, cantidad, unidad, sumar=True, ventana=None):
        if codigo and cantidad:
            try:
                cantidad = float(cantidad)
                if self.actualizar_registro(codigo, cantidad, unidad, sumar=sumar):
                    self.cargar_materia_prima()
                    if ventana:
                        ventana.destroy()
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos.")
            
    def guardar_nueva_materia_prima(self):
        codigo = self.codigo_var.get().strip()
        cantidad_nueva = self.cantidad_var.get().strip()
        unidad = self.unidad_var.get()

        self.guardar_materia_prima(
            codigo=codigo,
            cantidad=cantidad_nueva,
            unidad=unidad,
            sumar=True,
            ventana=self.ventana_agregar
        )
    
    def guardar_materia_prima_editada(self):
        codigo = self.codigo_var_editar.get().strip()
        nueva_cantidad = self.cantidad_var_editar.get().strip()
        unidad = self.productos.get(codigo, {}).get('unidadMedida', '')

        self.guardar_materia_prima(
            codigo=codigo,
            cantidad=nueva_cantidad,
            unidad=unidad,
            sumar=False,
            ventana=self.ventana_editar
        )