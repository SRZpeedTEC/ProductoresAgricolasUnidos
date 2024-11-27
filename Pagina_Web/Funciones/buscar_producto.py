from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
from Pagina_Web.Funciones.cargar_productos import CargarProducto

class buscarProductos:
    
    def buscar_productos(self):
        termino = self.buscar_var.get().lower()
        productos_a_buscar = self.productos_filtrados if hasattr(self, 'productos_filtrados') and self.productos_filtrados else self.productos
        productos_resultantes = {}
        for nombre, detalles in productos_a_buscar.items():
            if termino in nombre.lower() or termino in detalles['descripcion'].lower():
                productos_resultantes[nombre] = detalles               
        if productos_resultantes:
            CargarProducto.mostrar_productos(self, productos_resultantes)
        else:
            messagebox.showinfo("Búsqueda", f"No se encontraron productos que coincidan con: '{termino}'")