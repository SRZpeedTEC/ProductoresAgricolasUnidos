from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from abc import ABC, abstractmethod

class Obtener_productos:
    @staticmethod
    def ObtenerProductos():
            
            productos = {}
            path_productos = "Resources/txt_pagina_web/productos.txt"
            
            if os.path.exists(path_productos):
                with open(path_productos, "r") as file:
                    for line in file:
                        if line.strip():
                            partes = line.strip().split("|")
                            if len(partes) == 7:
                                NombreProducto = partes[0].strip()
                                descripcion = partes[1].strip()                          
                                precio = partes[2].strip()
                                cantidad = partes[3].strip()
                                unidad = partes[4].strip()
                                imagen = partes[5].strip()    
                                categoria = partes[6].strip()    
                                                    
                                try:
                                    cantidad = float(cantidad)
                                    productos[NombreProducto] = {'descripcion': descripcion, 'precio': precio, 'cantidad': cantidad, 'unidad': unidad, 'imagen': imagen, 'categoria': categoria}                              
                                except ValueError:
                                    messagebox.showwarning("Advertencia", f"La cantidad no es válida en la línea: {line}")
            return productos