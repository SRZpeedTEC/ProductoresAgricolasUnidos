from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
import Utiles.Genericos as genericos
from Ventanas.Login.registro import registro
from PIL import ImageTk, Image

from Ventanas.Ventana_Agricultor import VentanaPrincipalAgricultor
from Ventanas.Ventana_Fabricante import VentanaPrincipalFabricante

class Login:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Inicio de sesión')
        self.ventana.geometry('700x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        genericos.centrar_ventana(self.ventana, 700, 500)

        # Cargar logo
        logo = genericos.leer_imagen("./Resources/Imgs/logoProvisional.png", (200, 200))
        frame_logo = Frame(self.ventana, bd=0, width=300, relief=SOLID, padx=10, pady=10, bg='#A0D683')
        frame_logo.pack(side="left", fill=BOTH)
        lbllogo = Label(frame_logo, image=logo, bg='#A0D683')
        lbllogo.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame derecho para el formulario
        frame_form = Frame(self.ventana, bd=0, relief=SOLID, bg='white')
        frame_form.pack(side="right", expand=YES, fill=BOTH, padx=20, pady=20)

        # Título del formulario
        frame_form_title = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='white')
        frame_form_title.pack(side="top", fill=X)
        titulo = Label(frame_form_title, text='Inicio de sesión', font=Font(family='Times', size=30), fg="#666a88", bg='white', pady=10)
        titulo.pack(expand=YES, fill=BOTH)

        # Formulario de registro
        frame_form_fill = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='white')
        frame_form_fill.pack(side="bottom", expand=YES, fill=BOTH)

        etiqueta_usuario = Label(frame_form_fill, text="Usuario", font=('Times', 14), fg="#666a88", bg='white', anchor="w")
        etiqueta_usuario.pack(fill=X, padx=20, pady=5)
        self.usuario = Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=X, padx=20, pady=10)

        etiqueta_password = Label(frame_form_fill, text="Contraseña", font=('Times', 14), fg="#666a88", bg='white', anchor="w")
        etiqueta_password.pack(fill=X, padx=20, pady=5)
        self.password = Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=X, padx=20, pady=10)
        self.password.config(show="*")

        # Botón de inicio de sesión
        inicio = Button(frame_form_fill, text="Iniciar sesión", font=('Times', 15, BOLD), bg='#A0D683', bd=0, fg="#fff", command=self.verificar_datos)
        inicio.pack(fill=X, padx=20, pady=10)

        # Botón para registrar usuario
        registrarse = Button(frame_form_fill, text="Registrar Usuario", font=('Times', 15, BOLD), bg='#A0D683', bd=0, fg="#fff", command=self.ventana_registro)
        registrarse.pack(fill=X, padx=20, pady=10)

        self.ventana.mainloop()

    def verificar_datos(self):
        usuario = self.usuario.get()
        contrasena = self.password.get()

        try:
            with open('./Resources/usuarios.txt', 'r', encoding='utf-8') as archivo:
                usuarios = archivo.readlines()

            # Eliminar caracteres de nueva línea y espacios
            usuarios = [linea.strip() for linea in usuarios]

            credenciales_validas = False
            rol = None
            for linea in usuarios:
                if ',' in linea:
                    datos = linea.split(',')
                    if len(datos) == 3:
                        usuario_archivo, contrasena_archivo, rol_archivo = datos
                        if usuario == usuario_archivo and contrasena == contrasena_archivo:
                            credenciales_validas = True
                            rol = rol_archivo
                            break

            if credenciales_validas:
                self.ventana.destroy()
                # Determinar si abrir Ventana de Productor o Fabricante según el rol almacenado
                if rol == "Fabricante":
                    VentanaPrincipalFabricante.VentanaPrincipalFabricante()
                elif rol == "Agricultor":
                    VentanaPrincipalAgricultor.VentanaPrincipalAgricultor()
            else:
                messagebox.showerror("Error", "Credenciales inválidas")

        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo de usuarios")

    def ventana_registro(self):
        self.ventana.destroy()
        registro.Registrar()
