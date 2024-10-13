from tkinter import *
from tkinter.font import Font
import Utiles.Genericos as gnr
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox
import Ventanas.Ventana_Agricultor.formulario as formulario
import Ventanas.Ventana_Agricultor.ver_lote as ver_lote
import Ventanas.Ventana_Agricultor.editar_lote as editar_lote
from Utiles.Genericos import centrar_ventana

class VentanaPrincipal:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal')
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        centrar_ventana(self.ventana, 700, 600)

        self.ventana.geometry("800x600")
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)

        # Cargar y mostrar el logo
        logo = gnr.leer_imagen("./Resources/logoProvisional.png", (200, 200))
        lblLogo = Label(self.ventana, image=logo, bg="#B6FFA1")
        lblLogo.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear botones de navegación
        self.crear_botones()

        self.ventana.mainloop()

    def crear_botones(self):
        # Crear un contenedor para los botones
        frame_botones = Frame(self.ventana, bg="#A0D683")
        frame_botones.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Botón para registrar lotes
        btn_registrar_lote = Button(frame_botones, text="Registro de Lotes", command=lambda: formulario.crear_formulario(),bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_registrar_lote.grid(row=0, column=0, padx=10, pady=10)

        # Botón para monitorear inventarios
        btn_registrar_lote = Button(frame_botones, text="Editar Lote", command=lambda: editar_lote.editar_lote(self),bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_registrar_lote.grid(row=1, column=0, padx=10, pady=10)

        btn_ver_lote = Button(frame_botones, text="Ver Lote", command=lambda: ver_lote.ver_lote(self),bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_ver_lote.grid(row=2, column=0, padx=10, pady=10)

if __name__ == "__main__":
    app = VentanaPrincipal()
