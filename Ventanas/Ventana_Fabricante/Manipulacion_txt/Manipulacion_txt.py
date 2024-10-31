from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox

class ManipulacionTXT:
    
    
    def __init__(self):
        self.path_materia_prima = "Resources/txt_informacion_productos/materia_prima.txt"
        self.path_productos = "Resources/txt_informacion_productos/materia_prima_items.txt"
        


    
    def leer_materia_prima(self):
        registros = {}
        if os.path.exists(self.path_materia_prima):
            with open(self.path_materia_prima, "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split(":")
                        if len(partes) == 2:
                            codigo = partes[0].strip()
                            cantidad_unidad = partes[1].strip()                          
                            cantidad, unidad = self.extraer_cantidad_unidad(cantidad_unidad)
                            try:
                                cantidad = float(cantidad)
                                registros[codigo] = (cantidad, unidad)
                            except ValueError:
                                messagebox.showwarning("Advertencia", f"La cantidad no es válida en la línea: {line}")
        return registros

    
    def escribir_materia_prima(self, registros):
        with open(self.path_materia_prima, "w") as file:
            for codigo_producto, (cantidad, unidad_medida) in registros.items():
                file.write(f"{codigo_producto}: {cantidad} {unidad_medida}\n")
                
                
              
    def escribir_nuevo_producto(self, codigo_producto, descripcion_producto, unidad_medida, ventana):
        with open(self.path_productos, "a") as file:
            file.write(f"{codigo_producto}|{descripcion_producto}|{unidad_medida}\n")
            ventana.destroy()
            
                
                
           
    def leer_productos(self):
        productos = {}
        try:
            with open(self.path_productos, "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split('|')
                        if len(partes) == 3:
                            codigo = partes[0].strip()
                            descripcion = partes[1].strip()
                            unidad_medida = partes[2].strip()
                            productos[codigo] = {
                                'descripcion': descripcion,
                                'unidadMedida': unidad_medida
                            }
                        else:
                            messagebox.showwarning("Advertencia", f"Línea inválida en productos.txt: {line}")
            return productos
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de productos.")
            return {}

    
    def extraer_cantidad_unidad(self, cantidad_unidad_str):
        partes = cantidad_unidad_str.strip().split()
        if len(partes) >= 2:
            cantidad = partes[0]
            unidad = ' '.join(partes[1:])
        else:
            cantidad = cantidad_unidad_str
            unidad = ""
        return cantidad, unidad