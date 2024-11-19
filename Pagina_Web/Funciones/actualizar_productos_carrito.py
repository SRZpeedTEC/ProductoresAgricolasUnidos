from tkinter import *
from tkinter import ttk
import os
from Pagina_Web.Funciones.cargar_productos import CargarProducto

class ActualizarProductoCarrito:
    def actualizar_producto_carrito(self, desc, cantidad_seleccionada):
        path_productos = "Resources/txt_pagina_web/productos.txt"
        productos = []

        # Leer el archivo y actualizar la cantidad
        if os.path.exists(path_productos):
            with open(path_productos, "r") as file:
                for line in file:
                    partes = line.strip().split("|")
                    if len(partes) == 7:
                        NombreProducto = partes[0].strip()
                        descripcion = partes[1].strip()
                        precio = partes[2].strip()
                        cantidad = float(partes[3].strip())
                        unidad = partes[4].strip()
                        imagen = partes[5].strip()
                        categoria = partes[6].strip()

                       
                        if desc == descripcion:

                            cantidad += cantidad_seleccionada
                        productos.append(f"{NombreProducto}|{descripcion}|{precio}|{cantidad}|{unidad}|{imagen}|{categoria}\n")

            # Sobrescribir el archivo con las cantidades actualizadas
            with open(path_productos, "w") as file:
                file.writelines(productos)
