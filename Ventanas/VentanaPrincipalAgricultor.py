from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font, BOLD
from tkcalendar import Calendar
from natsort import natsorted

class VentanaPrincipalAgricultor:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal Agricultor')
        self.ventana.geometry("900x600")
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)

        # Frame principal para los botones y contenido
        self.main_frame = Frame(self.ventana, bg="#A0D683")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Frame para los botones de navegación (lado izquierdo)
        self.nav_frame = Frame(self.main_frame, bg="#A0D683", width=200)
        self.nav_frame.pack(side=LEFT, fill=Y, padx=20, pady=20)

        # Frame para mostrar el contenido (lado derecho)
        self.content_frame = Frame(self.main_frame, bg="#B6FFA1")
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        # Crear botones de navegación
        self.crear_botones()

        self.ventana.mainloop()

    def crear_botones(self):
        # Crear los botones en el frame de navegación
        btn_registrar_lote = Button(self.nav_frame, text="Registro de Lotes", command=self.mostrar_registro_lote, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_registrar_lote.pack(pady=10)

        btn_editar_lote = Button(self.nav_frame, text="Editar Lote", command=self.mostrar_editar_lote, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_editar_lote.pack(pady=10)

        btn_ver_lote = Button(self.nav_frame, text="Ver Lotes", command=self.mostrar_ver_lote, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_ver_lote.pack(pady=10)

        btn_volver_login = Button(self.nav_frame, text="Volver al Login", command=self.volver_login, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_volver_login.pack(pady=10)

    def limpiar_frame_contenido(self):
        # Limpiar el frame de contenido antes de mostrar algo nuevo
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_registro_lote(self):
        self.limpiar_frame_contenido()

        Label(self.content_frame, text="Registro de Lotes", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

        # Tipo de producto
        Label(self.content_frame, text="Tipo de producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        combo_tipo_producto = ttk.Combobox(self.content_frame, values=["Tomate", "Papa"], state="readonly")
        combo_tipo_producto.pack(pady=5)

        # Cantidad cosechada
        Label(self.content_frame, text="Cantidad cosechada (kg):", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        entry_cantidad = Entry(self.content_frame)
        entry_cantidad.pack(pady=5)

        # Lote del producto (se llenará automáticamente)
        Label(self.content_frame, text="Lote del producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        lote_entry = Entry(self.content_frame, state="readonly")
        lote_entry.pack(pady=5)

        # Fecha de cosecha
        Label(self.content_frame, text="Fecha de cosecha:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        cal = Calendar(self.content_frame, selectmode='day', date_pattern='y-mm-dd')
        cal.pack(pady=10)

        # Función para actualizar el lote ID
        def actualizar_lote():
            tipo_producto = combo_tipo_producto.get()
            fecha = cal.get_date().replace("-", "")  # Fecha en formato AAAAMMDD

            if not tipo_producto:
                return

            # Definir prefijo según el tipo de producto
            prefijo = "T" if tipo_producto == "Tomate" else "P"

            # Buscar en el archivo para obtener el número del siguiente lote
            contador = 1
            try:
                with open("lotes.txt", "r") as file:
                    lotes = file.readlines()
                    for lote in lotes:
                        _, _, lote_fecha, lote_id = lote.strip().split(',')
                        if lote_fecha.replace("-", "") == fecha and lote_id.startswith(prefijo):
                            # Extraer el número del lote y actualizar el contador
                            lote_numero = int(lote_id.split("_")[1])
                            contador = max(contador, lote_numero + 1)
            except FileNotFoundError:
                pass

            # Formar el ID del lote
            lote_id = f"{prefijo}{fecha}_{contador:02}"
            lote_entry.config(state="normal")
            lote_entry.delete(0, END)
            lote_entry.insert(0, lote_id)
            lote_entry.config(state="readonly")

        # Vincular la actualización del lote cuando cambie el tipo o la fecha
        combo_tipo_producto.bind("<<ComboboxSelected>>", lambda event: actualizar_lote())
        cal.bind("<<CalendarSelected>>", lambda event: actualizar_lote())

        # Botón para registrar lote
        btn_registrar = Button(self.content_frame, text="Registrar Lote", command=lambda: self.registrar_lote(combo_tipo_producto, entry_cantidad, cal, lote_entry), bg="#4CAF50", font=("Arial", 12, BOLD), fg="white", padx=20)
        btn_registrar.pack(pady=20)

    def mostrar_editar_lote(self):
        self.limpiar_frame_contenido()

        Label(self.content_frame, text="Editar Lote", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

        lote_tree = self.crear_lote_treeview(self.content_frame)

        # Leer y mostrar los lotes del archivo
        try:
            with open("lotes.txt", "r") as file:
                lotes = file.readlines()
                lotes = natsorted(lotes, key=lambda x: (x.split(',')[0], x.split(',')[2]))  # Ordenar por tipo y fecha

                for lote in lotes:
                    tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                    lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))
        except FileNotFoundError:
            messagebox.showerror("Error", "No hay lotes registrados aún.")

        # Variables para los campos de edición
        tipo_var = StringVar()
        cantidad_var = StringVar()
        fecha_var = StringVar()
        lote_var = StringVar()

        # Selección del Treeview
        def seleccionar_lote(event):
            selected_item = lote_tree.focus()
            if selected_item:
                values = lote_tree.item(selected_item, 'values')
                tipo_var.set(values[0])
                cantidad_var.set(values[1])
                fecha_var.set(values[2])
                lote_var.set(values[3])

        lote_tree.bind("<ButtonRelease-1>", seleccionar_lote)

        # Área para editar los valores seleccionados
        Label(self.content_frame, text="Tipo de Producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        tipo_entry = ttk.Combobox(self.content_frame, textvariable=tipo_var, values=["Tomate", "Papa"], state="readonly")
        tipo_entry.pack(pady=5)

        Label(self.content_frame, text="Cantidad (kg):", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
        cantidad_entry = Entry(self.content_frame, textvariable=cantidad_var)
        cantidad_entry.pack(pady=5)

        # Función para guardar cambios
        def guardar_cambios():
            selected_item = lote_tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "No se ha seleccionado ningún lote para editar.")
                return

            tipo_producto = tipo_var.get()
            cantidad = cantidad_var.get()
            fecha = fecha_var.get()
            lote_id = lote_var.get()

            if not tipo_producto or not cantidad or not fecha or not lote_id:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Validar que la cantidad sea un número positivo
            if not cantidad.isdigit() or int(cantidad) <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
                return

            # Actualizar los datos en el Treeview
            lote_tree.item(selected_item, values=(tipo_producto, cantidad, fecha, lote_id))

            # Actualizar el archivo lotes.txt
            try:
                with open("lotes.txt", "r") as file:
                    lotes = file.readlines()

                # Actualizar la línea correspondiente en el archivo
                with open("lotes.txt", "w") as file:
                    for lote in lotes:
                        data = lote.strip().split(',')
                        if data[3] == lote_id:  # Comparar por el Lote ID
                            file.write(f"{tipo_producto},{cantidad},{fecha},{lote_id}\n")
                        else:
                            file.write(lote)
                messagebox.showinfo("Confirmación", "Lote actualizado exitosamente.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Error al intentar acceder al archivo de lotes.")

        # Botón para guardar cambios
        btn_guardar = Button(self.content_frame, text="Guardar Cambios", command=guardar_cambios, bg="#4CAF50", font=("Arial", 12), fg="white")
        btn_guardar.pack(pady=20)

    def mostrar_ver_lote(self):
        self.limpiar_frame_contenido()

        Label(self.content_frame, text="Ver Lotes Registrados", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

        lote_tree = self.crear_lote_treeview(self.content_frame)

        # Leer y mostrar los lotes del archivo
        try:
            with open("lotes.txt", "r") as file:
                lotes = file.readlines()
                lotes = natsorted(lotes, key=lambda x: (x.split(',')[0], x.split(',')[2]))  # Ordenar por tipo y fecha

                for lote in lotes:
                    tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                    lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))
        except FileNotFoundError:
            messagebox.showerror("Error", "No hay lotes registrados aún.")

    def crear_lote_treeview(self, parent):
        lote_tree = ttk.Treeview(parent, columns=("Tipo", "Cantidad", "Fecha", "Lote"), show="headings", height=8)
        lote_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        lote_tree.heading("Tipo", text="Tipo de Producto")
        lote_tree.heading("Cantidad", text="Cantidad (kg)")
        lote_tree.heading("Fecha", text="Fecha de Cosecha")
        lote_tree.heading("Lote", text="Lote ID")

        lote_tree.column("Tipo", width=100, anchor=CENTER)
        lote_tree.column("Cantidad", width=80, anchor=CENTER)
        lote_tree.column("Fecha", width=100, anchor=CENTER)
        lote_tree.column("Lote", width=130, anchor=CENTER)

        return lote_tree

    def volver_login(self):
        self.ventana.destroy()

    def registrar_lote(self, combo_tipo_producto, entry_cantidad, cal, lote_entry):
        # Validar y registrar los lotes
        tipo_producto = combo_tipo_producto.get()
        cantidad = entry_cantidad.get()
        fecha = cal.get_date()
        lote = lote_entry.get()

        # Validar los campos obligatorios
        if not tipo_producto or not cantidad or not lote:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Validar que la cantidad sea un número válido
        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "La cantidad cosechada debe ser un número positivo.")
            return

        # Guardar los datos en un archivo de texto
        with open("lotes.txt", "a") as file:
            file.write(f"{tipo_producto},{cantidad},{fecha},{lote}\n")

        messagebox.showinfo("Registro Exitoso", f"Lote de {tipo_producto} registrado exitosamente.")
        # Actualizar el formulario
        lote_entry.config(state="normal")
        lote_entry.delete(0, END)
        lote_entry.config(state="readonly")
        combo_tipo_producto.set('')
        entry_cantidad.delete(0, END)


