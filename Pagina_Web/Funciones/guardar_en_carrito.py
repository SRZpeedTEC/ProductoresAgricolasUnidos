from tkinter import *
from tkinter import ttk
import os


class GuardarEnCarrito:
    def guardar_en_carrito(self, producto, cantidad_seleccionada):
        # Determinar el archivo de carrito basándonos en el atributo 'cliente'
        if self.cliente:  # Si 'cliente' tiene un valor, usamos el nombre del cliente
            path_carrito = f"Resources/carritos/carrito_{self.cliente[0]}.txt"
        else:  # Si 'cliente' está vacío, usamos el archivo para clientes anónimos
            path_carrito = "Resources/carritos/carrito_anonimo.txt"
        
        # Crear un diccionario para almacenar los productos del carrito
        carrito = {}

        # Leer el contenido del archivo si existe
        if os.path.exists(path_carrito):
            with open(path_carrito, "r") as file:
                for line in file:
                    partes = line.strip().split("|")
                    descripcion = partes[0]
                    precio = partes[1]
                    cantidad = float(partes[2])
                    unidad = partes[3]
                    imagen = partes[4]
                    categoria = partes[5]

                    carrito[descripcion] = {
                        "precio": precio,
                        "cantidad": cantidad,
                        "unidad": unidad,
                        "imagen": imagen,
                        "categoria": categoria,
                    }
        
        # Actualizar la cantidad del producto si ya existe, o agregarlo si no está
        if producto['descripcion'] in carrito:
            carrito[producto['descripcion']]['cantidad'] += cantidad_seleccionada
        else:
            carrito[producto['descripcion']] = {
                "precio": producto['precio'],
                "cantidad": cantidad_seleccionada,
                "unidad": producto['unidad'],
                "imagen": producto['imagen'],
                "categoria": producto['categoria'],
            }

        # Reescribir el archivo con los cambios
        with open(path_carrito, "w") as file:
            for descripcion, datos in carrito.items():
                file.write(f"{descripcion}|{datos['precio']}|{datos['cantidad']}|{datos['unidad']}|{datos['imagen']}|{datos['categoria']}\n")
