from tkinter import *
from tkinter import ttk
import os
import Utiles.Genericos as gnr
from PIL import ImageTk, Image
from Utiles.Genericos import centrar_ventana
import Ventanas.Ventana_Fabricante.Procesar as Procesar

class VentanaPrincipalFabricante:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal - Fabricante')
        centrar_ventana(self.ventana, 700, 600)
        self.ventana.geometry("1000x600")
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)

        # Frame principal para los botones y contenido
        self.main_frame = Frame(self.ventana, bg="#A0D683")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Frame para los botones de navegación (lado izquierdo)
        self.nav_frame = Frame(self.main_frame, bg="#A0D683", width=180)
        self.nav_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

        # Frame para mostrar el contenido (lado derecho)
        self.content_frame = Frame(self.main_frame, bg="#B6FFA1")
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Crear botones de navegación
        self.crear_botones()

        # Mostrar logo en el content frame
        self.mostrar_logo()

        self.ventana.mainloop()

    def crear_botones(self):
        # Crear los botones en el frame de navegación
        btn_font = ("Arial", 11)
        btn_procesar = Button(self.nav_frame, text="Procesar", command=self.mostrar_procesar, bg="#B6FFA1", font=btn_font, width=20)
        btn_procesar.pack(pady=5)

        btn_ver_procesados = Button(self.nav_frame, text="Ver Lotes Procesados", command=self.mostrar_lotes_procesados, bg="#B6FFA1", font=btn_font, width=20)
        btn_ver_procesados.pack(pady=5)

        btn_volver_login = Button(self.nav_frame, text="Volver al Login", command=self.volver_login, bg="#B6FFA1", font=btn_font, width=20)
        btn_volver_login.pack(pady=5)

    def limpiar_frame_contenido(self):
        # Limpiar el frame de contenido antes de mostrar algo nuevo
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_logo(self):
        # Mostrar el logo en el content frame
        self.limpiar_frame_contenido()
        logo = gnr.leer_imagen("./Resources/logoProvisional.png", (150, 150))
        lblLogo = Label(self.content_frame, image=logo, bg="#B6FFA1")
        lblLogo.image = logo  # Guardar una referencia para evitar que la imagen se borre
        lblLogo.pack(expand=True)

    def mostrar_procesar(self):
        # Crear la vista de procesar en el content_frame
        self.limpiar_frame_contenido()
        Procesar.Procesar(self.content_frame, btn_width=15)

    def mostrar_lotes_procesados(self):
        # Mostrar los lotes procesados en el content_frame
        self.limpiar_frame_contenido()

        # Crear un Treeview para mostrar los lotes procesados con columnas detalladas
        columns = ("Lote", "Pequeños Verdes", "Pequeños Maduros", "Grandes Verdes", "Grandes Maduros", "Dañados")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=15)
        tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Definir encabezados
        tree.heading("Lote", text="ID del Lote")
        tree.heading("Pequeños Verdes", text="Pequeños Verdes (kg)")
        tree.heading("Pequeños Maduros", text="Pequeños Maduros (kg)")
        tree.heading("Grandes Verdes", text="Grandes Verdes (kg)")
        tree.heading("Grandes Maduros", text="Grandes Maduros (kg)")
        tree.heading("Dañados", text="Dañados (kg)")

        # Ajustar el ancho de las columnas
        for col in columns:
            tree.column(col, width=150, anchor=CENTER)

        # Leer el archivo de lotes procesados y llenar el Treeview
        if os.path.exists("lotes_procesados.txt"):
            with open("lotes_procesados.txt", "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split(':', 1)
                        if len(partes) == 2:
                            lote_id = partes[0]
                            detalles = partes[1].split(", ")

                            # Inicializar los valores para cada columna de detalles
                            detalle_dict = {
                                "Pequeños Verdes": 0,
                                "Pequeños Maduros": 0,
                                "Grandes Verdes": 0,
                                "Grandes Maduros": 0,
                                "Dañados": 0
                            }

                            # Parsear los detalles y llenar el diccionario
                            for detalle in detalles:
                                key, value = detalle.split(": ")
                                detalle_dict[key.strip()] = int(value.strip().replace(" kg", ""))

                            # Insertar en el Treeview
                            tree.insert("", "end", values=(lote_id,
                                                           detalle_dict["Pequeños Verdes"],
                                                           detalle_dict["Pequeños Maduros"],
                                                           detalle_dict["Grandes Verdes"],
                                                           detalle_dict["Grandes Maduros"],
                                                           detalle_dict["Dañados"]))
        else:
            # Si no hay lotes procesados, mostrar un mensaje
            Label(self.content_frame, text="No hay lotes procesados aún.", bg="#B6FFA1", font=("Arial", 12)).pack(pady=10)

    def volver_login(self):
        # Volver a la pantalla de login
        self.ventana.destroy()
        from Ventanas.login import Login  # Importación diferida para evitar el problema de importación circular
        Login()
