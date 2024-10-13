from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from natsort import natsorted
from Utiles.Genericos import centrar_ventana

def editar_lote(self):
    nueva_ventana = Toplevel(self.ventana)
    nueva_ventana.title("Edición de Lotes")
    nueva_ventana.geometry("700x500")
    centrar_ventana(nueva_ventana, 700, 500)
    nueva_ventana.config(bg="#A0D683")

    # Etiqueta de Título
    Label(nueva_ventana, text="Edición de Lotes", bg="#A0D683", font=("Arial", 20, "bold")).pack(pady=10)

    # Contenedor principal
    frame = Frame(nueva_ventana, bg="#A0D683")
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Crear el Treeview para mostrar los lotes
    lote_tree = ttk.Treeview(frame, columns=("Tipo", "Cantidad", "Fecha", "Lote"), show="headings", height=8)
    lote_tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar para el Treeview
    scroll_y = Scrollbar(frame, orient=VERTICAL, command=lote_tree.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    lote_tree.configure(yscrollcommand=scroll_y.set)

    # Configuración de columnas
    lote_tree.heading("Tipo", text="Tipo de Producto")
    lote_tree.heading("Cantidad", text="Cantidad (kg)")
    lote_tree.heading("Fecha", text="Fecha de Cosecha")
    lote_tree.heading("Lote", text="Lote ID")

    lote_tree.column("Tipo", width=150, anchor=CENTER)
    lote_tree.column("Cantidad", width=100, anchor=CENTER)
    lote_tree.column("Fecha", width=150, anchor=CENTER)
    lote_tree.column("Lote", width=150, anchor=CENTER)

    # Leer los lotes del archivo
    try:
        with open("lotes.txt", "r") as file:
            lotes = file.readlines()
            lotes = natsorted(lotes)  # Ordenar de forma natural

            for lote in lotes:
                tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))
    except FileNotFoundError:
        messagebox.showerror("Error", "No hay lotes registrados aún.")
        return

    # Variables para editar
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
    Label(nueva_ventana, text="Tipo de Producto:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=300)
    tipo_entry = ttk.Combobox(nueva_ventana, textvariable=tipo_var, values=["Tomate", "Papa"], state="readonly")
    tipo_entry.place(x=200, y=300)

    Label(nueva_ventana, text="Cantidad (kg):", bg="#A0D683", font=("Arial", 12)).place(x=50, y=350)
    cantidad_entry = Entry(nueva_ventana, textvariable=cantidad_var)
    cantidad_entry.place(x=200, y=350)

    Label(nueva_ventana, text="Fecha de Cosecha:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=400)
    fecha_entry = Entry(nueva_ventana, textvariable=fecha_var, state="readonly")
    fecha_entry.place(x=200, y=400)

    Label(nueva_ventana, text="Lote ID:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=450)
    lote_entry = Entry(nueva_ventana, textvariable=lote_var, state="readonly")
    lote_entry.place(x=200, y=450)

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
    btn_guardar = Button(nueva_ventana, text="Guardar Cambios", command=guardar_cambios, bg="#B6FFA1", font=("Arial", 12))
    btn_guardar.place(x=450, y=450)

