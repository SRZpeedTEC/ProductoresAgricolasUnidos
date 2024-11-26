from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

class VentanaProcesarRecetas:
    def __init__(self, root, receta_id, nombre_receta, cantidad_procesada, unidad):
        self.root = root
        self.root.title("Procesar Receta")
        self.root.geometry("700x600")
        self.root.configure(bg="white")

        self.receta_id = receta_id
        self.nombre_receta = nombre_receta
        self.cantidad_procesada = cantidad_procesada
        self.unidad = unidad
        self.path_recetas = "Resources/txt_recetas/recetas.txt"
        self.path_materia_prima = "Resources/txt_informacion_productos/materia_prima_fabrica.txt"
        self.path_productos_listos = "Resources/txt_recetas/productos_listos.txt"
   

        # Título de la ventana
        Label(self.root, text=f"Procesar Receta ID: {receta_id}", bg="white", font=("Times", 16, "bold")).pack(pady=10)

        # Entrada para la cantidad de recetas a procesar
        Label(self.root, text="Cantidad a procesar:", bg="white", font=("Times", 12)).pack()
        self.cantidad_a_procesar_entry = Entry(self.root, width=10, font=("Times", 12), justify=CENTER)
        self.cantidad_a_procesar_entry.insert(0, "1")  # Valor inicial
        self.cantidad_a_procesar_entry.pack(pady=5)

        Button(self.root, text="Aplicar Cantidad", command=self.aplicar_cantidad, bg="#2196F3", font=("Times", 12), fg="white").pack(pady=5)

        # Treeview para mostrar los ingredientes
        columns = ("Ingrediente", "Cantidad Necesaria", "Cantidad Disponible")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        self.tree.heading("Ingrediente", text="Ingrediente")
        self.tree.heading("Cantidad Necesaria", text="Cantidad Necesaria")
        self.tree.heading("Cantidad Disponible", text="Cantidad Disponible")
        self.tree.column("Ingrediente", width=200, anchor=CENTER)
        self.tree.column("Cantidad Necesaria", width=150, anchor=CENTER)
        self.tree.column("Cantidad Disponible", width=150, anchor=CENTER)

        # Botón para procesar la receta
        Button(self.root, text="Procesar", command=self.procesar_receta, bg="#FCC509", font=("Times", 12), width=15).pack(pady=10)

        # Cargar datos de los ingredientes
        self.cargar_ingredientes()

    def cargar_ingredientes(self):
        """
        Carga los datos de los ingredientes desde la receta y verifica la cantidad disponible.
        """
        try:
            # Verificar si el archivo de recetas existe
            if self.path_recetas == None:
                messagebox.showwarning("Advertencia", "El archivo de recetas no existe.")
                return

            # Leer las recetas desde el archivo
            with open(self.path_recetas, "r", encoding="utf-8") as file:
                recetas = file.readlines()

            # Buscar la receta correspondiente
            receta_encontrada = None
            for receta in recetas:
                partes = receta.strip().split("|")
                if len(partes) >= 5 and partes[0].strip() == self.receta_id:
                    receta_encontrada = partes
                    break

            if not receta_encontrada:
                messagebox.showerror("Error", f"No se pudo encontrar la receta con ID '{self.receta_id}' en el archivo.")
                return

            _, _, _, _, ingredientes_str = receta_encontrada

            ingredientes = []
            for ing in ingredientes_str.split(";"):
                partes_ingrediente = ing.split(":")
                if len(partes_ingrediente) == 2:
                    try:
                        codigo = partes_ingrediente[0].strip()
                        cantidad = float(partes_ingrediente[1].strip()) # Validar solo enteros
                        ingredientes.append((codigo, cantidad))
                    except ValueError:
                        messagebox.showwarning("Advertencia", f"Ingrediente '{ing}' tiene un formato incorrecto.")

            # Verificar si el archivo de materia prima existe
            if self.path_materia_prima == None:
                messagebox.showwarning("Advertencia", "El archivo de materia prima no existe.")
                return

            # Leer la materia prima desde el archivo
            with open(self.path_materia_prima, "r", encoding="utf-8") as file:
                materia_prima = {}
                materia_prima_info = {}
                for line in file:
                    partes = line.strip().split("|")
                    if len(partes) == 4:
                        codigo = partes[0].strip()
                        descripcion = partes[1].strip()
                        cantidad = float(partes[2].strip())  # Convertir a entero
                        unidad = partes[3].strip()
                        materia_prima[codigo] = cantidad
                        materia_prima_info[codigo] = (descripcion, unidad)

            self.ingredientes_base = ingredientes
            self.materia_prima = materia_prima
            self.materia_prima_info = materia_prima_info

            self.aplicar_cantidad()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los ingredientes: {e}")

    def aplicar_cantidad(self):
        """
        Recalcula las cantidades necesarias en función de la cantidad a procesar.
        """
        try:
            cantidad_a_procesar = self.cantidad_a_procesar_entry.get()
            if not cantidad_a_procesar.isdigit():
                raise ValueError("Solo se permiten números enteros.")

            cantidad_a_procesar = int(cantidad_a_procesar)

            if cantidad_a_procesar <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            # Limpiar Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Calcular nuevas cantidades y actualizar el Treeview
            for codigo, cantidad_base in self.ingredientes_base:
                cantidad_necesaria = cantidad_base * cantidad_a_procesar
                cantidad_disponible = self.materia_prima.get(codigo, 0)

                # Agregar al Treeview con colores
                tag = "suficiente" if cantidad_disponible >= cantidad_necesaria else "insuficiente"
                self.tree.insert("", "end", values=(codigo, cantidad_necesaria, cantidad_disponible), tags=(tag,))

            # Estilo del Treeview
            self.tree.tag_configure("suficiente", background="lightgreen")
            self.tree.tag_configure("insuficiente", background="lightcoral")

        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida: {e}")

    def procesar_receta(self):
        """
        Procesa la receta verificando si hay suficientes ingredientes y actualizando la materia prima.
        """
        try:
            cantidad_a_procesar = self.cantidad_a_procesar_entry.get()
            if not cantidad_a_procesar.isdigit():
                raise ValueError("Solo se permiten números enteros.")

            cantidad_a_procesar = int(cantidad_a_procesar)

            insuficientes = []

            # Verificar ingredientes
            for codigo, cantidad_base in self.ingredientes_base:
                cantidad_necesaria = cantidad_base * cantidad_a_procesar
                cantidad_disponible = self.materia_prima.get(codigo, 0)
                if cantidad_disponible < cantidad_necesaria:
                    insuficientes.append((codigo, cantidad_necesaria, cantidad_disponible))
                else:
                    self.materia_prima[codigo] -= cantidad_necesaria

            # Mostrar advertencia si hay insuficientes
            if insuficientes:
                faltantes = "\n".join([f"{codigo}: Necesario {necesario}, Disponible {disponible}" for codigo, necesario, disponible in insuficientes])
                messagebox.showerror("Error", f"No hay suficiente materia prima para los siguientes ingredientes:\n{faltantes}")
                return

            # Actualizar materia prima
            with open(self.path_materia_prima, "w", encoding="utf-8") as file:
                for codigo, cantidad in self.materia_prima.items():
                    descripcion, unidad = self.materia_prima_info[codigo]
                    file.write(f"{codigo}|{descripcion}|{cantidad}|{unidad}\n")

            # Guardar receta procesada
            self.guardar_producto_listo()

            messagebox.showinfo("Éxito", "La receta ha sido procesada correctamente.")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Cantidad inválida para procesar: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la receta: {e}")

    def guardar_producto_listo(self):
        """
        Guarda los datos de la receta procesada en el archivo de productos listos.
        Si el producto ya existe, actualiza su cantidad.
        """
        try:
            cantidad_a_procesar = int(self.cantidad_a_procesar_entry.get())
            cantidad_total = self.cantidad_procesada * cantidad_a_procesar  # Cantidad total procesada

            # Leer productos existentes
            productos_existentes = {}
            if os.path.exists(self.path_productos_listos):
                with open(self.path_productos_listos, "r", encoding="utf-8") as file:
                    for line in file:
                        partes = line.strip().split("|")
                        if len(partes) >= 4:
                            id_producto = partes[0]
                            nombre_producto = partes[1]
                            cantidad_producto = float(partes[2])  # Puede ser decimal
                            unidad_producto = partes[3]
                            productos_existentes[id_producto] = {
                                'nombre': nombre_producto,
                                'cantidad': cantidad_producto,
                                'unidad': unidad_producto
                            }

            # Actualizar o agregar producto
            if self.receta_id in productos_existentes:
                # Actualizar cantidad
                productos_existentes[self.receta_id]['cantidad'] += cantidad_total
            else:
                # Agregar nuevo producto
                productos_existentes[self.receta_id] = {
                    'nombre': self.nombre_receta,
                    'cantidad': cantidad_total,
                    'unidad': self.unidad
                }

            # Escribir productos actualizados en el archivo
            with open(self.path_productos_listos, "w", encoding="utf-8") as file:
                for id_producto, datos in productos_existentes.items():
                    file.write(f"{id_producto}|{datos['nombre']}|{datos['cantidad']}|{datos['unidad']}\n")

            messagebox.showinfo("Éxito", f"Receta procesada: {cantidad_total} {self.unidad} de {self.nombre_receta}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la receta procesada: {e}")

