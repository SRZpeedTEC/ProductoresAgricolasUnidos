from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from abc import ABC, abstractmethod

class Obtener_productos_carrito:
    @staticmethod
    def ObtenerProductosCarrito(path_Carrito):
        productos = {}
        
        # Verificar si el archivo existe
        if os.path.exists(path_Carrito):
            with open(path_Carrito, "r") as file:
                for line in file:
                    if line.strip():  # Ignorar líneas vacías
                        partes = line.strip().split("|")
                        if len(partes) == 6:  # Ajustado a 6 partes
                            NombreProducto = partes[0].strip()
                            precio = partes[1].strip()
                            cantidad = partes[2].strip()
                            unidad = partes[3].strip()
                            imagen = partes[4].strip()
                            categoria = partes[5].strip()
                            
                            try:
                                cantidad = float(cantidad)  # Convertir cantidad a número
                                productos[NombreProducto] = {
                                    'precio': precio,
                                    'cantidad': cantidad,
                                    'unidad': unidad,
                                    'imagen': imagen,
                                    'categoria': categoria
                                }
                            except ValueError:
                                messagebox.showwarning("Advertencia", f"La cantidad no es válida en la línea: {line}")
        else:
            messagebox.showwarning("Archivo no encontrado", f"No se encontró el archivo: {path_Carrito}")
        
        return productos
