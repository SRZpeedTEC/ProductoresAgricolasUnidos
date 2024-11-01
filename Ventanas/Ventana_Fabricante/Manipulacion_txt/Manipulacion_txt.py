from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from abc import ABC, abstractmethod


class ManipulacionTXT(ABC):
    
    path_materia_prima_fabrica = "Resources/txt_informacion_productos/materia_prima_fabrica.txt"
    @classmethod
    def leer_materia_prima(cls):
        registros = {}
        path_materia_prima = cls.path_materia_prima_fabrica
        
        if os.path.exists(path_materia_prima):
            with open(path_materia_prima, "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split("|")
                        if len(partes) == 4:
                            codigo = partes[0].strip()
                            descripcion = partes[1].strip()                          
                            cantidad = partes[2].strip()
                            unidad = partes[3].strip()
                            try:
                                cantidad = float(cantidad)
                                registros[codigo] = (descripcion,  cantidad,  unidad)                               
                            except ValueError:
                                messagebox.showwarning("Advertencia", f"La cantidad no es válida en la línea: {line}")
        return registros

    @classmethod
    def actualizar_materia_prima(cls, registros):
        
        path_materia_prima = cls.path_materia_prima_fabrica
        
        with open(path_materia_prima, "w") as file:
            for codigo_producto, (descripcion, cantidad, unidad_medida) in registros.items():
                file.write(f"{codigo_producto}|{descripcion}|{cantidad}|{unidad_medida}\n")
                
                
    @classmethod        
    def escribir_nuevo_producto(cls, codigo_producto, descripcion_producto, cantidad, unidad_medida, ventana):
        path_materia_prima = cls.path_materia_prima_fabrica
        
        with open(path_materia_prima, "a") as file:
            try:    
                file.write(f"{codigo_producto}|{descripcion_producto}|{cantidad}|{unidad_medida}\n")
                ventana.destroy()
            
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar el producto: {e}")
                
                
        
                          
