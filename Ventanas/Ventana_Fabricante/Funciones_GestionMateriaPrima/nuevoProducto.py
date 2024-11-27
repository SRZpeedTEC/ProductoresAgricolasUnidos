from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRegistros import ManipulacionRegistros


class AgregarNuevoProducto:
    
    
    
    @staticmethod      
    def agregar_nuevo_producto(tree):       
        ventana_agregar = Toplevel()
        ventana_agregar.title("Agregar Materia Prima")
        ventana_agregar.geometry("300x400")       
                   
        lbl_codigo = Label(ventana_agregar, text=f"Digite el codigo para su producto")
        lbl_codigo.pack(pady=5)        
        ent_codigo = Entry(ventana_agregar)
        ent_codigo.pack(pady=5)

        # Etiqueta para mostrar la descripción del producto
        lbl_descripcion = Label(ventana_agregar, text=f"Digite la descripción del producto")
        lbl_descripcion.pack(pady=5)                 
        ent_descripcion = Entry(ventana_agregar)
        ent_descripcion.pack(pady=5)
        
        # Campo para ingresar la cantidad  
        lbl_unidad = Label(ventana_agregar, text=f"digite la unidad de medida de su producto")
        lbl_unidad.pack(pady=5)               
        ent_unidad = Entry(ventana_agregar)
        ent_unidad.pack(pady=5)

        Button(ventana_agregar, text="Guardar", command=lambda: guardar()).pack(pady=10)
        
        def guardar():
            if not ent_codigo.get() or not ent_descripcion.get() or not ent_unidad.get():
                messagebox.showerror("Error", "Todos los campos deben estar llenos")
            elif len(ent_codigo.get()) > 10:
                messagebox.showerror("Error", "El código no puede tener más de 10 caracteres")
            else:
                if ManipulacionRegistros.agregar_registro(ent_codigo.get(), ent_descripcion.get(), 0.0, ent_unidad.get(), tree):                            
                    messagebox.showinfo("Exito", "Producto agregado correctamente")
                    ventana_agregar.destroy()
                else:
                    messagebox.showerror("Error", "El producto ya existe")
                
    