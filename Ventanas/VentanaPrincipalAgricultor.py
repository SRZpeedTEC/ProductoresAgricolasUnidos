from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from Ventanas.Ventana_Agricultor.registro_lote import mostrar_registro_lote
from Ventanas.Ventana_Agricultor.editar_lote import mostrar_editar_lote
from Ventanas.Ventana_Agricultor.ver_lote import mostrar_ver_lote
from Ventanas.login import Login

class VentanaPrincipalAgricultor:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal Agricultor')
        self.ventana.geometry("900x600")
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)

        # Frame principal para los botones y contenido
        self.main_frame = Frame(self.ventana, bg="#A0D683")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Frame para los botones de navegación (lado izquierdo)
        self.nav_frame = Frame(self.main_frame, bg="#A0D683", width=200)
        self.nav_frame.pack(side=LEFT, fill=Y, padx=20, pady=20)

        # Frame para mostrar el contenido (lado derecho)
        self.content_frame = Frame(self.main_frame, bg="#B6FFA1")
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        # Crear botones de navegación
        self.crear_botones()

        self.ventana.mainloop()

    def crear_botones(self):
        # Crear los botones en el frame de navegación
        btn_registrar_lote = Button(self.nav_frame, text="Registro de Lotes", command=lambda: mostrar_registro_lote(self.content_frame), bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_registrar_lote.pack(pady=10)

        btn_editar_lote = Button(self.nav_frame, text="Editar Lote", command=lambda: mostrar_editar_lote(self.content_frame), bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_editar_lote.pack(pady=10)

        btn_ver_lote = Button(self.nav_frame, text="Ver Lotes", command=lambda: mostrar_ver_lote(self.content_frame), bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_ver_lote.pack(pady=10)

        btn_volver_login = Button(self.nav_frame, text="Volver al Login", command=self.volver_login, bg="#B6FFA1", font=("Arial", 12), width=20)
        btn_volver_login.pack(pady=10)

    def limpiar_frame_contenido(self):
        # Limpiar el frame de contenido antes de mostrar algo nuevo
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def volver_login(self):
        self.ventana.destroy()
        Login()
