from tkinter import Toplevel, Label, ttk, messagebox

def ver_ingredientes(receta):
    """
    Muestra los ingredientes de la receta seleccionada en una nueva ventana.

    :param receta: La receta seleccionada (tupla con ID, Nombre, Ingredientes).
    """
    _, nombre_receta, ingredientes_list = receta  # Los ingredientes ya son una lista de tuplas (código, cantidad)

    # Crear ventana emergente para mostrar los ingredientes
    ventana_ingredientes = Toplevel()
    ventana_ingredientes.title(f"Ingredientes de la Receta: {nombre_receta}")
    ventana_ingredientes.geometry("450x350")
    ventana_ingredientes.resizable(False, False)

    # Etiqueta del título de la ventana
    Label(
        ventana_ingredientes,
        text=f"Ingredientes de la Receta: {nombre_receta}",
        font=("Helvetica", 16, "bold"),
        pady=10,
    ).pack()

    # Configurar Treeview para mostrar ingredientes
    tree_ingredientes = ttk.Treeview(ventana_ingredientes, columns=("Código", "Cantidad"), show="headings", height=10)
    tree_ingredientes.pack(fill="both", expand=True, padx=10, pady=10)
    tree_ingredientes.heading("Código", text="Código")
    tree_ingredientes.heading("Cantidad", text="Cantidad")
    tree_ingredientes.column("Código", width=200, anchor="center")
    tree_ingredientes.column("Cantidad", width=200, anchor="center")

    # Mostrar los ingredientes en el Treeview
    for ingrediente in ingredientes_list:
        if isinstance(ingrediente, tuple) and len(ingrediente) == 2:
            codigo, cantidad = ingrediente
            tree_ingredientes.insert("", "end", values=(codigo.strip(), cantidad.strip()))
        else:
            messagebox.showwarning("Advertencia", f"Formato inválido para el ingrediente: {ingrediente}")

    # Botón para cerrar la ventana
    ttk.Button(ventana_ingredientes, text="Cerrar", command=ventana_ingredientes.destroy).pack(pady=10)
