from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from natsort import natsorted

def mostrar_editar_lote(content_frame):
    limpiar_frame_contenido(content_frame)

    Label(content_frame, text="Editar Lote", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

    lote_tree = crear_lote_treeview(content_frame)

    try:
        with open("Resources\\txt_lotes\\lotes.txt", "r") as file:
            lotes = file.readlines()
            lotes = natsorted(lotes, key=lambda x: (x.split(',')[0], x.split(',')[2]))  # Ordenar por tipo y fecha
            for lote in lotes:
                tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))
    except FileNotFoundError:
        messagebox.showerror("Error", "No hay lotes registrados aún.")

    tipo_var = StringVar()
    cantidad_var = StringVar()
    fecha_var = StringVar()
    lote_var = StringVar()

    def seleccionar_lote(event):
        selected_item = lote_tree.focus()
        if selected_item:
            values = lote_tree.item(selected_item, 'values')
            tipo_var.set(values[0])
            cantidad_var.set(values[1])
            fecha_var.set(values[2])
            lote_var.set(values[3])

    lote_tree.bind("<ButtonRelease-1>", seleccionar_lote)

    Label(content_frame, text="Tipo de Producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    tipo_entry = ttk.Combobox(content_frame, textvariable=tipo_var, values=["Tomate", "Papa"], state="readonly")
    tipo_entry.pack(pady=5)

    Label(content_frame, text="Cantidad (kg):", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    cantidad_entry = Entry(content_frame, textvariable=cantidad_var)
    cantidad_entry.pack(pady=5)

    btn_guardar = Button(content_frame, text="Guardar Cambios", command=lambda: guardar_cambios(lote_tree, tipo_var, cantidad_var, fecha_var, lote_var), bg="#4CAF50", font=("Arial", 12), fg="white")
    btn_guardar.pack(pady=20)

def guardar_cambios(lote_tree, tipo_var, cantidad_var, fecha_var, lote_var):
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

    if not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
        return

    lote_tree.item(selected_item, values=(tipo_producto, cantidad, fecha, lote_id))

    try:
        with open("Resources\\txt_lotes\\lotes.txt", "r") as file:
            lotes = file.readlines()

        with open("Resources\\txt_lotes\\lotes.txt", "w") as file:
            for lote in lotes:
                data = lote.strip().split(',')
                if data[3] == lote_id:
                    file.write(f"{tipo_producto},{cantidad},{fecha},{lote_id}\n")
                else:
                    file.write(lote)
        messagebox.showinfo("Confirmación", "Lote actualizado exitosamente.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Error al intentar acceder al archivo de lotes.")

def crear_lote_treeview(parent):
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

def limpiar_frame_contenido(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
