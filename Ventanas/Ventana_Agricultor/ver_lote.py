from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from natsort import natsorted

def mostrar_ver_lote(content_frame):
    limpiar_frame_contenido(content_frame)

    Label(content_frame, text="Ver Lotes Registrados", bg="#B6FFA1", font=("Arial", 16, "bold")).pack(pady=10)

    lote_tree = crear_lote_treeview(content_frame)

    try:
        with open("Resources\\txt_lotes\\lotes.txt", "r") as file:
            lotes = file.readlines()
            lotes = natsorted(lotes, key=lambda x: (x.split(',')[0], x.split(',')[2]))
            for lote in lotes:
                tipo_producto, cantidad, fecha, lote_id = lote.strip().split(',')
                lote_tree.insert("", "end", values=(tipo_producto, cantidad, fecha, lote_id))
    except FileNotFoundError:
        messagebox.showerror("Error", "No hay lotes registrados aún.")

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