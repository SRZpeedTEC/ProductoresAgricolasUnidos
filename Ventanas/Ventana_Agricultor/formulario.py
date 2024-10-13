from tkinter import *
from tkinter.font import Font
import Utiles.Genericos as gnr
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import re
from Utiles.Genericos import centrar_ventana

def crear_formulario():
    nueva_ventana = Toplevel()
    nueva_ventana.title("Registro de Lotes")
    nueva_ventana.geometry("600x600")
    centrar_ventana(nueva_ventana, 700, 600)

    nueva_ventana.config(bg="#A0D683")

    # Etiqueta de Título
    Label(nueva_ventana, text="Registro de Lotes", bg="#A0D683", font=("Arial", 16)).place(x=50, y=50)

    # Tipo de producto
    Label(nueva_ventana, text="Tipo de producto:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=100)
    combo_tipo_producto = ttk.Combobox(nueva_ventana, values=["Tomate", "Papa"], state="readonly")
    combo_tipo_producto.place(x=250, y=100)

    # Cantidad cosechada
    Label(nueva_ventana, text="Cantidad cosechada (kg):", bg="#A0D683", font=("Arial", 12)).place(x=50, y=150)
    entry_cantidad = Entry(nueva_ventana)
    entry_cantidad.place(x=250, y=150)

    # Lote del producto (se llenará automáticamente)
    Label(nueva_ventana, text="Lote del producto:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=200)
    lote_entry = Entry(nueva_ventana, state="readonly")
    lote_entry.place(x=250, y=200)

    # Fecha de cosecha
    Label(nueva_ventana, text="Fecha de cosecha:", bg="#A0D683", font=("Arial", 12)).place(x=50, y=250)
    cal = Calendar(nueva_ventana, selectmode='day', date_pattern='y-mm-dd')
    cal.place(x=250, y=250)

    def actualizar_lote():
        tipo_producto = combo_tipo_producto.get()
        fecha = cal.get_date().replace("-", "")  # Fecha en formato AAAAMMDD
        
        if not tipo_producto:
            return

        # Definir prefijo según el tipo de producto
        if tipo_producto == "Tomate":
            prefijo = "T"
        elif tipo_producto == "Papa":
            prefijo = "P"
        else:
            return

        # Buscar en el archivo para obtener el número del siguiente lote
        contador = 1
        try:
            with open("lotes.txt", "r") as file:
                lotes = file.readlines()
                for lote in lotes:
                    # Cada línea tiene el formato: tipo_producto,cantidad,fecha,lote_id
                    _, _, lote_fecha, lote_id = lote.strip().split(',')
                    if lote_fecha.replace("-", "") == fecha and lote_id.startswith(prefijo):
                        # Extraer el número del lote y actualizar el contador
                        lote_numero = int(lote_id.split("_")[1])
                        contador = max(contador, lote_numero + 1)
        except FileNotFoundError:
            # Si el archivo no existe, es el primer lote
            contador = 1

        # Formar el ID del lote
        lote_id = f"{prefijo}{fecha}_{contador:02}"
        lote_entry.config(state="normal")
        lote_entry.delete(0, END)
        lote_entry.insert(0, lote_id)
        lote_entry.config(state="readonly")

    # Vincular la actualización del lote cuando cambie el tipo o la fecha
    combo_tipo_producto.bind("<<ComboboxSelected>>", lambda event: actualizar_lote())
    cal.bind("<<CalendarSelected>>", lambda event: actualizar_lote())

    # Función para registrar el lote
    def registrar_lote():
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

        # Validar el formato del lote usando expresiones regulares
        pattern = r"^[TP]\d{8}_[0-9]{2}$"
        if not re.match(pattern, lote):
            messagebox.showerror("Error", "El formato del lote es incorrecto. Debe seguir el patrón:\n"
                                          "Primera letra indicando el tipo (T para tomate, P para papa),\n"
                                          "seguido de la fecha en formato AAAAMMDD y un contador (_01, _02, ...).\n"
                                          "Ejemplo: T20240910_01")
            return

        # Guardar los datos en un archivo de texto
        with open("lotes.txt", "a") as file:
            file.write(f"{tipo_producto},{cantidad},{fecha},{lote}\n")

        messagebox.showinfo("Confirmación", f"Lote de {tipo_producto} registrado exitosamente\n"
                                            f"Cantidad: {cantidad}kg\n"
                                            f"Fecha de cosecha: {fecha}\n"
                                            f"Lote: {lote}")

        # Cerrar la ventana de registro de lote después de la confirmación
        nueva_ventana.destroy()

    # Botón para registrar lote
    btn_registrar = Button(nueva_ventana, text="Registrar Lote", command=registrar_lote, bg="#B6FFA1")
    btn_registrar.place(x=100, y=400)

