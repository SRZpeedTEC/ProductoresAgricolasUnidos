from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from natsort import natsorted
from Utiles.Genericos import centrar_ventana

def ver_lote(self):
    nueva_ventana = Toplevel(self.ventana)
    nueva_ventana.title("Visualización de Lotes")
    nueva_ventana.geometry("700x600")
    centrar_ventana(nueva_ventana, 700, 600)
    nueva_ventana.config(bg="#A0D683")

    # Contenedor principal de la ventana
    main_frame = Frame(nueva_ventana, bg="#A0D683", bd=2, relief=SOLID)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Etiqueta de título
    Label(main_frame, text="Lotes Registrados", bg="#A0D683", font=("Arial", 20, "bold")).pack(pady=10)

    # Crear el Treeview para mostrar los lotes en forma de tabla
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 12))  # Cambiar el estilo de la fuente
    style.configure("mystyle.Treeview.Heading", font=('Arial', 13, 'bold'))  # Cambiar el estilo de la cabecera
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminar los bordes

    tree_frame = Frame(main_frame, bg="#A0D683")
    tree_frame.pack(fill=BOTH, expand=True)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    lote_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("Tipo", "Cantidad", "Fecha", "Lote"), style="mystyle.Treeview")
    tree_scroll.config(command=lote_tree.yview)

    lote_tree.heading("#0", text="", anchor=W)
    lote_tree.heading("Tipo", text="Tipo de Producto", anchor=CENTER)
    lote_tree.heading("Cantidad", text="Cantidad (kg)", anchor=CENTER)
    lote_tree.heading("Fecha", text="Fecha de Cosecha", anchor=CENTER)
    lote_tree.heading("Lote", text="Lote", anchor=CENTER)

    lote_tree.column("#0", width=0, stretch=NO)
    lote_tree.column("Tipo", anchor=CENTER, width=150)
    lote_tree.column("Cantidad", anchor=CENTER, width=150)
    lote_tree.column("Fecha", anchor=CENTER, width=150)
    lote_tree.column("Lote", anchor=CENTER, width=150)

    lote_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Leer el archivo de lotes y mostrar todos los datos en la tabla al inicio
    def cargar_todos_lotes():
        try:
            with open("lotes.txt", "r") as file:
                lotes = file.readlines()

            # Ordenar los lotes para una mejor visualización
            lotes = natsorted(lotes)

            # Insertar todos los lotes en el Treeview
            for lote in lotes:
                tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))

        except FileNotFoundError:
            messagebox.showerror("Error", "No hay lotes registrados aún.")

    # Llamar a la función para cargar todos los lotes al inicio
    cargar_todos_lotes()

    # Área para el filtro de fecha
    filter_frame = Frame(main_frame, bg="#A0D683")
    filter_frame.pack(fill=X, padx=10, pady=10)

    Label(filter_frame, text="Filtrar por Fecha:", bg="#A0D683", font=("Arial", 12)).pack(side=LEFT, padx=5)

    cal = Calendar(filter_frame, selectmode='day', date_pattern='y-mm-dd')
    cal.pack(side=LEFT, padx=5)

    # Función para filtrar lotes por fecha
    def filtrar_lotes():
        fecha_seleccionada = cal.get_date()

        # Limpiar el Treeview antes de insertar nuevos datos
        for item in lote_tree.get_children():
            lote_tree.delete(item)

        try:
            with open("lotes.txt", "r") as file:
                lotes = file.readlines()

            # Ordenar los lotes para una mejor visualización
            lotes = natsorted(lotes)

            # Insertar en el Treeview los lotes que coincidan con la fecha seleccionada
            for lote in lotes:
                tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                if fecha == fecha_seleccionada:
                    lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))

            if not lote_tree.get_children():
                messagebox.showinfo("Información", f"No hay lotes registrados para la fecha: {fecha_seleccionada}")

        except FileNotFoundError:
            messagebox.showerror("Error", "No hay lotes registrados aún.")

    # Botón para aplicar el filtro de fecha
    btn_filtrar = Button(filter_frame, text="Aplicar Filtro", command=filtrar_lotes, bg="#B6FFA1", font=("Arial", 12))
    btn_filtrar.pack(side=LEFT, padx=10)

    # Botón para cerrar la ventana
    btn_cerrar = Button(main_frame, text="Cerrar", command=nueva_ventana.destroy, bg="#B6FFA1", font=("Arial", 12))
    btn_cerrar.pack(pady=10)

