from tkinter import Toplevel, Label, Listbox, Scrollbar, Button, Entry, END, Frame
from tkinter import ttk
from tkinter import messagebox
from Ventanas.Ventana_Fabricante.Manipulacion_txt.Manipulacion_txt import ManipulacionTXT
from Ventanas.Ventana_Fabricante.Manipulacion_txt.ManipulacionRecetasTXT import ManipulacionRecetasTXT

def agregar_receta(self):
    # Crear una nueva ventana para agregar recetas
    ventana_receta = Toplevel()
    ventana_receta.title("Agregar Receta")
    ventana_receta.geometry("1100x800")
    ventana_receta.configure(bg="#e6f2ff")
    ventana_receta.resizable(False, False)

    # Frame para la sección de información de la receta
    frame_info = Frame(ventana_receta, bg="#e6f2ff")
    frame_info.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    Label(frame_info, text="ID Receta:", font=("Helvetica", 12), bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    id_receta = Entry(frame_info, width=40, font=("Helvetica", 12))
    id_receta.grid(row=0, column=1, padx=10, pady=10)

    Label(frame_info, text="Nombre Receta:", font=("Helvetica", 12), bg="#e6f2ff").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    nombre_receta = Entry(frame_info, width=40, font=("Helvetica", 12))
    nombre_receta.grid(row=1, column=1, padx=10, pady=10)

    # Frame para seleccionar la unidad de producción y la cantidad a producir
    frame_produccion = Frame(ventana_receta, bg="#e6f2ff")
    frame_produccion.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    Label(frame_produccion, text="Unidad de Producción:", font=("Helvetica", 12), bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    unidad_produccion = ttk.Combobox(frame_produccion, values=["Kilogramos", "Gramos", "Unidad","Litro"], font=("Helvetica", 12))
    unidad_produccion.grid(row=0, column=1, padx=10, pady=10)
    unidad_produccion.current(0)  # Seleccionar "Kilogramos" por defecto

    Label(frame_produccion, text="Cantidad a Producir:", font=("Helvetica", 12), bg="#e6f2ff").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    cantidad_producir = Entry(frame_produccion, width=20, font=("Helvetica", 12))
    cantidad_producir.grid(row=1, column=1, padx=10, pady=10)
  

    # Frame para la lista de Materia Prima Disponible
    frame_materia_prima = Frame(ventana_receta, bg="#e6f2ff")
    frame_materia_prima.grid(row=2, column=0, padx=20, pady=10, sticky="nw")

    Label(frame_materia_prima, text="Materia Prima Disponible:", font=("Helvetica", 12, "bold"), bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=10, sticky="w")

    listbox = Listbox(frame_materia_prima, width=60, height=15, selectmode="single", font=("Helvetica", 10))
    scrollbar = Scrollbar(frame_materia_prima, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)

    # Llenar el Listbox con la materia prima
    materia_prima = ManipulacionTXT.leer_materia_prima_recetas()
    for item in materia_prima:
        listbox.insert(END, f"{item[0]} - {item[1]} ({item[2]} {item[3]})")

    listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    scrollbar.grid(row=1, column=1, padx=5, pady=10, sticky="ns")

    # Mostrar cantidad disponible
    cantidad_disponible_label = Label(frame_materia_prima, text="Disponible: -", font=("Helvetica", 10), fg="blue", bg="#e6f2ff")
    cantidad_disponible_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    def mostrar_cantidad_disponible(event):
        seleccion = listbox.curselection()
        if seleccion:
            index = seleccion[0]
            _, nombre, disponible, unidad = materia_prima[index]
            cantidad_disponible_label.config(text=f"Disponible: {disponible} {unidad}")

    listbox.bind("<<ListboxSelect>>", mostrar_cantidad_disponible)

    # Frame para la tabla de Ingredientes Seleccionados
    frame_ingredientes = Frame(ventana_receta, bg="#e6f2ff")
    frame_ingredientes.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

    Label(frame_ingredientes, text="Ingredientes Seleccionados:", font=("Helvetica", 12, "bold"), bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=10, sticky="w")

    ingredientes_tree = ttk.Treeview(frame_ingredientes, columns=("Código", "Nombre", "Cantidad", "Unidad"), show="headings")
    ingredientes_tree.heading("Código", text="Código")
    ingredientes_tree.heading("Nombre", text="Nombre")
    ingredientes_tree.heading("Cantidad", text="Cantidad")
    ingredientes_tree.heading("Unidad", text="Unidad")
    ingredientes_tree.column("Código", width=100)
    ingredientes_tree.column("Nombre", width=150)
    ingredientes_tree.column("Cantidad", width=100)
    ingredientes_tree.column("Unidad", width=100)
    ingredientes_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Frame para la cantidad y los botones de acciones
    frame_acciones = Frame(ventana_receta, bg="#e6f2ff")
    frame_acciones.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    Label(frame_acciones, text="Cantidad:", font=("Helvetica", 12), bg="#e6f2ff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    cantidad = Entry(frame_acciones, width=15, font=("Helvetica", 12))
    cantidad.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    def agregar_ingrediente():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un ingrediente de la lista.")
            return
        index = seleccion[0]

        # Obtener datos del Listbox basados en `materia_prima`
        codigo, nombre, disponible, unidad = materia_prima[index]
        cantidad_ingresada = cantidad.get()

        cantidad_ingresada = float(cantidad_ingresada)

        if cantidad_ingresada > int(disponible):
            messagebox.showwarning("Advertencia", "La cantidad ingresada excede la disponible.")
            return

        # Insertar ingrediente en el Treeview
        ingredientes_tree.insert("", "end", values=(codigo, nombre, cantidad_ingresada, unidad))
        cantidad.delete(0, END)

    Button(frame_acciones, text="Agregar Ingrediente", command=agregar_ingrediente, font=("Helvetica", 10), bg="#4CAF50", fg="white", padx=15, pady=10).grid(row=1, column=0, padx=10, pady=10)

    def eliminar_ingrediente():
        seleccion = ingredientes_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un ingrediente para eliminar.")
            return
        for item in seleccion:
            ingredientes_tree.delete(item)

    Button(frame_acciones, text="Eliminar Ingrediente", command=eliminar_ingrediente, font=("Helvetica", 10), bg="#f44336", fg="white", padx=15, pady=10).grid(row=1, column=1, padx=10, pady=10)

    def guardar_receta():
        # Validar que todos los campos estén completos
        if not id_receta.get().strip():
            messagebox.showwarning("Advertencia", "El ID de la receta es obligatorio.")
            return
        if not nombre_receta.get().strip():
            messagebox.showwarning("Advertencia", "El nombre de la receta es obligatorio.")
            return
        if not cantidad_producir.get().strip():
            messagebox.showwarning("Advertencia", "La cantidad a producir es obligatoria.")
            return

        # Validar que la cantidad a producir sea un entero
        if not cantidad_producir.get().isdigit():
            messagebox.showwarning("Advertencia", "La cantidad a producir debe ser un número entero.")
            return

        # Obtener los ingredientes seleccionados del Treeview
        ingredientes = []
        for item in ingredientes_tree.get_children():
            valores = ingredientes_tree.item(item, "values")
            try:
                codigo = valores[0]
                cantidad = valores[2]
                ingredientes.append((codigo, cantidad))
            except ValueError:
                messagebox.showwarning(
                    "Error de Formato",
                    f"El ingrediente '{valores[1]}' tiene una cantidad inválida. Asegúrate de que sea un número entero."
                )
                return

        # Verificar que se haya agregado al menos un ingrediente
        if not ingredientes:
            messagebox.showwarning("Advertencia", "Debes agregar al menos un ingrediente.")
            return

        # Guardar la receta
        try:
            ManipulacionRecetasTXT.agregar_receta(
                id_receta.get().strip(),
                nombre_receta.get().strip(),
                int(cantidad_producir.get().strip()),  # Convertir cantidad a entero
                unidad_produccion.get().strip(),
                ingredientes
            )
            messagebox.showinfo("Éxito", "Receta guardada correctamente.")
            ventana_receta.destroy()
        except ValueError as e:
            messagebox.showerror("Error al guardar receta", f"{e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error al guardar la receta: {e}")


    Button(ventana_receta, text="Guardar Receta", command=guardar_receta, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10).grid(row=4, column=0, columnspan=2, pady=20)

    ventana_receta.mainloop()
