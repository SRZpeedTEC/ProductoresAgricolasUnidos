from tkinter import *
from tkinter import ttk
import os
import random
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.Manipulacion_txt import ManipulacionTXT
from Ventanas.Ventana_Fabricante.Funciones_GestionMateriaPrima import GuardarMateriaPrima

class GestionMateriaPrima:
    def __init__(self, frame):
        
        self.manipular_txt = ManipulacionTXT()
        self.productos = self.cargar_productos()
               
                     
        Label(frame, text="Gestion Materias Primas", bg="white", font=("Times", 18, "bold")).pack(pady=10)
        
        
        controls_frame = Frame(frame, bg="white")
        controls_frame.pack(pady=10)
        
        # Botones de agregar, editar y eliminar
        btn_font = ("Times", 10)
        btn_agregar = Button(controls_frame, text="Agregar", command=self.agregar_materia_prima, bg="#FCC509", font=btn_font, width=15)
        btn_agregar.grid(row=0, column=0, padx=5)
        
        btn_editar = Button(controls_frame, text="Editar", command=self.editar_materia_prima, bg="#FCC509", font=btn_font, width=15)
        btn_editar.grid(row=0, column=1, padx=5)
        
        btn_eliminar = Button(controls_frame, text="Eliminar", command=self.eliminar_materia_prima, bg="#FCC509", font=btn_font, width=15)
        btn_eliminar.grid(row=0, column=2, padx=5)
        
        # Treeview para mostrar la materia prima
        columns = ("Código", "Descripción", "Cantidad")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=CENTER)
        
        # Cargar datos
        self.cargar_materia_prima()
        
    def cargar_productos(self):
        productos = {}
        try:
            with open("Resources/txt_informacion_productos/materia_prima_items.txt", "r") as file:
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
        
    def cargar_materia_prima(self):
    # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        registros = self.manipular_txt.leer_materia_prima()
        if registros:
            for codigo, (cantidad, unidad) in registros.items():
                producto = self.productos.get(codigo, {})
                descripcion = producto.get('descripcion', 'No disponible')
                self.tree.insert("", "end", values=(codigo, descripcion, cantidad, unidad))
    
        else:               
            Label(self.tree, text="No hay materia prima registrada.", bg="white", font=("Times", 12)).pack(pady=10)
            
    def actualizar_registro(self, codigo, cantidad_nueva, unidad, sumar=True):
        
        registros = self.manipular_txt.leer_materia_prima()

        if codigo in registros:
            cantidad_existente, unidad_existente = registros[codigo]
            if unidad_existente != unidad:
                messagebox.showerror("Error", f"La unidad de medida no coincide para el producto {codigo}.")
                return False
            if sumar:
                registros[codigo] = (cantidad_existente + cantidad_nueva, unidad)
            else:
                registros[codigo] = (cantidad_nueva, unidad)
        else:
            registros[codigo] = (cantidad_nueva, unidad)

        self.manipular_txt.escribir_materia_prima(registros)
        return True
    
    def eliminar_registro(self, codigo):
        registros = self.manipular_txt.leer_materia_prima()
        if codigo in registros:
            del registros[codigo]
            self.manipular_txt.escribir_materia_prima(registros)
            return True
        else:
            messagebox.showwarning("Advertencia", f"No se encontró el producto con código {codigo}.")
            return False


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

    
    
    def agregar_materia_prima(self):
        self.ventana_agregar = Toplevel()
        self.ventana_agregar.title("Agregar Materia Prima")
        self.ventana_agregar.geometry("300x400")       
        
        Label(self.ventana_agregar, text="Código del Producto:").pack(pady=5)
        self.codigo_var = StringVar()
        codigos_producto = list(self.productos.keys())
        self.codigo_selector = ttk.Combobox(self.ventana_agregar, textvariable=self.codigo_var, values=codigos_producto, state="readonly")
        self.codigo_selector.pack(pady=5)
        self.codigo_selector.bind("<<ComboboxSelected>>", self.actualizar_descripcion_producto)

        # Etiqueta para mostrar la descripción del producto
        Label(self.ventana_agregar, text="Descripción:").pack(pady=5)
        self.descripcion_var = StringVar()
        self.lbl_descripcion = Label(self.ventana_agregar, textvariable=self.descripcion_var)
        self.lbl_descripcion.pack(pady=5)
        
        # Campo para ingresar la cantidad  
        self.unidad_var = StringVar(self.ventana_agregar, value = "")     
        self.lbl_unidad = Label(self.ventana_agregar, text=f"cantidad en: {self.unidad_var.get()}")
        self.lbl_unidad.pack(pady=5) 
        self.cantidad_var = StringVar()
        Entry(self.ventana_agregar, textvariable=self.cantidad_var).pack(pady=5)

        Button(self.ventana_agregar, text="Guardar", command=self.guardar_nueva_materia_prima).pack(pady=10)
    
    def actualizar_descripcion_producto(self, event):
        codigo = self.codigo_var.get()
        producto = self.productos.get(codigo, {})
        descripcion = producto.get('descripcion', 'No disponible')
        unidad = producto.get('unidadMedida', 'No disponible')        
        self.descripcion_var.set(descripcion)
        self.unidad_var.set(unidad)
        self.lbl_unidad.config(text=f"cantidad en: {self.unidad_var.get()}")
        
    
    def extraer_cantidad_unidad(self, cantidad_unidad_str):
        # Asumiendo que el formato es "cantidad unidad"
        partes = cantidad_unidad_str.strip().split()
        if len(partes) >= 2:
            cantidad = partes[0]
            unidad = ' '.join(partes[1:])
        else:
            cantidad = cantidad_unidad_str
            unidad = ""
        return cantidad, unidad
           
        
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



        
    
    def editar_materia_prima(self):
    # Obtener el item seleccionado
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un elemento para editar.")
            return
    
        # Obtener los valores
        values = self.tree.item(selected_item, 'values')
        codigo_seleccionado = values[0]
        descripcion = values[1]
        cantidad_actual = values[2]
        unidad = values[3]
    
        # Crear una nueva ventana para editar
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Materia Prima")
        self.ventana_editar.geometry("350x250")
    
        # Campos de entrada
        Label(self.ventana_editar, text="Código:").pack(pady=5)
        self.codigo_var_editar = StringVar(value=codigo_seleccionado)
        Entry(self.ventana_editar, textvariable=self.codigo_var_editar, state='readonly').pack(pady=5)
    
        Label(self.ventana_editar, text="Descripción:").pack(pady=5)
        Label(self.ventana_editar, text=descripcion).pack(pady=5)
    
        Label(self.ventana_editar, text="Unidad de Medida:").pack(pady=5)
        Label(self.ventana_editar, text=unidad).pack(pady=5)
    
        Label(self.ventana_editar, text="Cantidad:").pack(pady=5)
        self.cantidad_var_editar = StringVar(value=cantidad_actual)
        Entry(self.ventana_editar, textvariable=self.cantidad_var_editar).pack(pady=5)
    
        Button(self.ventana_editar, text="Guardar", command=self.guardar_materia_prima_editada).pack(pady=10)
        
    def eliminar_materia_prima(self):
        # Obtener el item seleccionado
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un elemento para eliminar.")
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este registro?")
        if respuesta:
            # Obtener el código
            values = self.tree.item(selected_item, 'values')
            codigo_seleccionado = values[0]

            if self.eliminar_registro(codigo_seleccionado):
                self.cargar_materia_prima()

    
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



