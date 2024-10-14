from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import tkinter.messagebox as messagebox

def mostrar_registro_lote(content_frame):
    limpiar_frame_contenido(content_frame)

    Label(content_frame, text="Registro de Lotes", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

    # Tipo de producto
    Label(content_frame, text="Tipo de producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    combo_tipo_producto = ttk.Combobox(content_frame, values=["Tomate", "Papa"], state="readonly")
    combo_tipo_producto.pack(pady=5)

    # Cantidad cosechada
    Label(content_frame, text="Cantidad cosechada (kg):", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    entry_cantidad = Entry(content_frame)
    entry_cantidad.pack(pady=5)

    # Lote del producto (se llenará automáticamente)
    Label(content_frame, text="Lote del producto:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    lote_entry = Entry(content_frame, state="readonly")
    lote_entry.pack(pady=5)

    # Fecha de cosecha
    Label(content_frame, text="Fecha de cosecha:", bg="#B6FFA1", font=("Arial", 12)).pack(pady=5)
    cal = Calendar(content_frame, selectmode='day', date_pattern='y-mm-dd')
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
    btn_registrar = Button(content_frame, text="Registrar Lote", command=lambda: registrar_lote(combo_tipo_producto, entry_cantidad, cal, lote_entry), bg="#4CAF50", font=("Arial", 12, "bold"), fg="white", padx=20)
    btn_registrar.pack(pady=20)

def registrar_lote(combo_tipo_producto, entry_cantidad, cal, lote_entry):
    tipo_producto = combo_tipo_producto.get()
    cantidad = entry_cantidad.get()
    fecha = cal.get_date()
    lote = lote_entry.get()

    if not tipo_producto or not cantidad or not lote:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not cantidad.isdigit() or int(cantidad) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
        return

    with open("lotes.txt", "a") as file:
        file.write(f"{tipo_producto},{cantidad},{fecha},{lote}\n")

    messagebox.showinfo("Registro Exitoso", f"Lote de {tipo_producto} registrado exitosamente.")
    lote_entry.config(state="normal")
    lote_entry.delete(0, END)
    lote_entry.config(state="readonly")
    combo_tipo_producto.set('')
    entry_cantidad.delete(0, END)

def limpiar_frame_contenido(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
