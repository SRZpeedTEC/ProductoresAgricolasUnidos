from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
from tkinter import ttk
import Utiles.Genericos as genericos
from Ventanas.Login.registro import login
from PIL import ImageTk, Image
import os

class Registrar:

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Registro de Usuario')
        self.ventana.geometry('900x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        genericos.centrar_ventana(self.ventana, 900, 500)

        # Cargar logo
<<<<<<< Updated upstream:Ventanas/registro.py
        logo = genericos.leer_imagen("./Resources/logoProvisional.png", (200, 200))
        frame_logo = Frame(self.ventana, bd=0, width=300, relief=SOLID, padx=10, pady=10, bg='#A0D683')
=======
        logo = genericos.leer_imagen("./Resources/Imgs/logoProvisional.png", (100, 100))
        frame_logo = Frame(self.ventana, bd=0, width=150, relief=SOLID, padx=10, pady=10, bg='#A0D683')
>>>>>>> Stashed changes:Ventanas/Login/registro/registro.py
        frame_logo.pack(side="left", expand=NO, fill=BOTH)
        lbllogo = Label(frame_logo, image=logo, bg='#A0D683')
        lbllogo.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame derecho para el formulario
        frame_form = Frame(self.ventana, bd=0, relief=SOLID, bg='white')
        frame_form.pack(side="right", expand=YES, fill=BOTH, padx=20, pady=20)

        # Título del formulario
        frame_form_title = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='white')
        frame_form_title.pack(side="top", fill=X)
        titulo = Label(frame_form_title, text='Registrarse', font=Font(family='Times', size=30), fg="#666a88", bg='white', pady=10)
        titulo.pack(expand=YES, fill=BOTH)

        # Formulario de registro
        frame_form_fill = Frame(frame_form, height=50, bd=0, relief=SOLID, bg='white')
        frame_form_fill.pack(side="bottom", expand=YES, fill=BOTH)

        etiqueta_usuario = Label(frame_form_fill, text="Usuario", font=('Times', 14), fg="#666a88", bg='white', anchor="w")
        etiqueta_usuario.pack(fill=X, padx=20, pady=5)
        self.usuario = Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=X, padx=20, pady=5)

        etiqueta_password = Label(frame_form_fill, text="Contraseña", font=('Times', 14), fg="#666a88", bg='white', anchor="w")
        etiqueta_password.pack(fill=X, padx=20, pady=5)
        self.password = Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=X, padx=20, pady=5)
        self.password.config(show="*")

        etiqueta_rol = Label(frame_form_fill, text="Rol", font=('Times', 14), fg="#666a88", bg='white', anchor="w")
        etiqueta_rol.pack(fill=X, padx=20, pady=5)
        self.rol = ttk.Combobox(frame_form_fill, values=["Agricultor", "Fabricante"], state="readonly", font=('Times', 14))
        self.rol.pack(fill=X, padx=20, pady=5)
        self.rol.set("Seleccione su rol")  # Placeholder para la lista desplegable

        # Botones
        frame_botones = Frame(frame_form_fill, bd=0, relief=SOLID, bg='white')
        frame_botones.pack(fill=X, padx=20, pady=20)

        crear = Button(frame_botones, text="Crear Usuario", font=('Times', 15, BOLD), bg='#A0D683', bd=0, fg="#fff", command=self.registrar_usuario)
        crear.grid(row=0, column=0, padx=5, pady=10)

        volver_login = Button(frame_botones, text="Volver al Login", font=('Times', 15, BOLD), bg='#A0D683', bd=0, fg="#fff", command=self.volver_al_login)
        volver_login.grid(row=0, column=1, padx=5, pady=10)

        self.ventana.mainloop()

    def registrar_usuario(self):
        usuario_nuevo = self.usuario.get()
        contrasena_nueva = self.password.get()
        rol_seleccionado = self.rol.get()

        if not usuario_nuevo or not contrasena_nueva or rol_seleccionado == "Seleccione su rol":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Verificar si el archivo de usuarios ya existe
            if os.path.exists('./Resources/usuarios.txt'):
                with open('./Resources/usuarios.txt', 'r', encoding='utf-8') as file:
                    usuarios = file.readlines()

                # Verificar si el usuario ya existe
                usuarios_existentes = [linea.strip().split(',', 1)[0] for linea in usuarios]
                if usuario_nuevo in usuarios_existentes:
                    messagebox.showerror("Error", "El usuario ya existe")
                    return

            # Agregar el nuevo usuario al archivo
            with open('./Resources/usuarios.txt', 'a', encoding='utf-8', newline='') as archivo:
                archivo.write(f"{usuario_nuevo},{contrasena_nueva},{rol_seleccionado}\n")

            messagebox.showinfo("Éxito", "El usuario ha sido creado exitosamente")
            # Limpiar los campos de entrada
            self.usuario.delete(0, END)
            self.password.delete(0, END)
            self.rol.set("Seleccione su rol")

        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al crear el usuario: {e}")

    def volver_al_login(self):
        self.ventana.destroy()
        login.Login()
