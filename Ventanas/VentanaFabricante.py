from tkinter import *
from tkinter import ttk
import os
import Utiles.Genericos as gnr
from PIL import ImageTk, Image
from Utiles.Genericos import centrar_ventana
from Ventanas.Ventana_Fabricante import Procesar, Ver_lotesprocesados, MaestroArticulos

class VentanaPrincipalFabricante:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal - Fabricante')   
        self.ventana.geometry("1100x600")
        centrar_ventana(self.ventana, 1100, 600)
        self.ventana.config(bg="#B6FFA1")
        self.ventana.resizable(0, 0)

        # Frame principal para los botones y contenido
        self.main_frame = Frame(self.ventana, bg="#FCC509")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Frame para los botones de navegación (lado izquierdo)
        self.nav_frame = Frame(self.main_frame, bg="#FCC509", width=200)
        self.nav_frame.pack(side=LEFT, fill=Y, padx=20, pady=20)

        # Frame para mostrar el contenido (lado derecho)
        self.content_frame = Frame(self.main_frame, bg="white")
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Crear botones de navegación
        self.crear_botones()

        # Mostrar logo en el content frame
        self.mostrar_logo()

        self.ventana.mainloop()

    def crear_botones(self):
        # Crear los botones en el frame de navegación
        btn_font = ("Times", 11)
        btn_procesar = Button(self.nav_frame, text="Procesar", command=self.mostrar_procesar, bg="#eeeaea", font=btn_font, width=20)
        btn_procesar.pack(pady=10)

        btn_ver_procesados = Button(self.nav_frame, text="Ver Lotes Procesados", command=self.mostrar_lotes_procesados, bg="#eeeaea", font=btn_font, width=20)
        btn_ver_procesados.pack(pady=10)
        
        btn_maestro_articulos = Button(self.nav_frame, text="Gestionar Inventario", command=self.mostrar_maestro_articulos, bg="#eeeaea", font=btn_font, width=20)
        btn_maestro_articulos.pack(pady=10)

        btn_volver_login = Button(self.nav_frame, text="Volver al Login", command=self.volver_login, bg="#eeeaea", font=btn_font, width=20)
        btn_volver_login.pack(pady=10)
        
        
    def limpiar_frame_contenido(self):
        # Limpiar el frame de contenido antes de mostrar algo nuevo
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_logo(self):
        # Mostrar el logo en el content frame
        self.limpiar_frame_contenido()
        logo = gnr.leer_imagen("./Resources/Imgs/logoProvisional.png", (150, 150))
        lblLogo = Label(self.content_frame, image=logo, bg="white")
        lblLogo.image = logo  # Guardar una referencia para evitar que la imagen se borre
        lblLogo.pack(expand=True)

    def mostrar_procesar(self):
        # Crear la vista de procesar en el content_frame
        self.limpiar_frame_contenido()
        Procesar.Procesar(self.content_frame, btn_width=15)

    def mostrar_lotes_procesados(self):
        # Mostrar los lotes procesados en el content_frame
        self.limpiar_frame_contenido()
        Ver_lotesprocesados.VerLotesProcesados(self.content_frame)
            
    def mostrar_maestro_articulos(self):
        # Crear la vista de maestro de artículos en el content_frame
        self.limpiar_frame_contenido()
        MaestroArticulos.GestionMateriaPrima(self.content_frame)

    def volver_login(self):
        # Volver a la pantalla de login
        self.ventana.destroy()
        from Ventanas.Login.registro.login import Login  # Importación diferida para evitar el problema de importación circular
        Login()