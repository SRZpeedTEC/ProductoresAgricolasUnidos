from tkinter import *
from tkinter.font import Font
import Utiles.Genericos as gnr
from PIL import ImageTk, Image
from Utiles.Genericos import centrar_ventana
import Ventanas.Ventana_Fabricante.Procesar as Procesar

class VentanaPrincipalFabricante:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal - Fabricante')
        centrar_ventana(self.ventana, 700, 600)
        self.ventana.geometry("800x600")
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)

        # Cargar y mostrar el logo
        logo = gnr.leer_imagen("./Resources/logoProvisional.png", (200, 200))
        lblLogo = Label(self.ventana, image=logo, bg="#B6FFA1")
        lblLogo.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear botones de navegación específicos para productores
        self.crear_botones()

        self.ventana.mainloop()

    def crear_botones(self):
        frame_botones = Frame(self.ventana, bg="#A0D683")
        frame_botones.place(relx=0.5, rely=0.5, anchor=CENTER)

        btn_procesar = Button(frame_botones, text="Procesar", command=Procesar.Procesar, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_procesar.grid(row=0, column=0, padx=10, pady=10)

        btn_volver_login = Button(frame_botones, text="Volver al Login", command=self.volver_login, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_volver_login.grid(row=1, column=0, padx=10, pady=10)

    def volver_login(self):
        self.ventana.destroy()
        from Ventanas.login import Login  # Importación diferida para evitar el problema de importación circular
        Login()
