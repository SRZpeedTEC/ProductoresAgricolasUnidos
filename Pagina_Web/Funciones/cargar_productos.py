from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from PIL import ImageTk, Image
from abc import ABC, abstractmethod
from Pagina_Web.Funciones.obtener_productos import Obtener_productos


class CargarProducto:
    
    
    
            
    def mostrar_productos(self, productos):
        
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        for idx, producto in enumerate(productos):
            frame_producto = Frame(self.product_frame, bd=2, relief=RIDGE)
            frame_producto.grid(row=idx // 4, column=idx % 4, padx=20, pady=10)

            # Cargar imagen del producto
            try:
                img = ImageTk.PhotoImage(Image.open(productos[producto]['imagen']).resize((150, 150)))
            except:
                img = ImageTk.PhotoImage(Image.new('RGB', (150, 150), color='gray'))

            lbl_imagen = Label(frame_producto, image=img)
            lbl_imagen.image = img  # Mantener referencia
            lbl_imagen.pack()

            lbl_nombre = Label(frame_producto, text=producto)
            lbl_nombre.pack()

            lbl_precio = Label(frame_producto, text=productos[producto]['precio'], fg="green")
            lbl_precio.pack()
            
            lbl_cantidad = Label(frame_producto, text=f"Disponible: {productos[producto]['cantidad']} {productos[producto]['unidad']}")
            lbl_cantidad.pack()            

            btn_agregar = Button(frame_producto, text="Agregar al Carrito", command=lambda p=producto: self.agregar_al_carrito(p))
            btn_agregar.pack(pady=5)
    
    
    