from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter.font import BOLD
import Utiles.Genericos as genericos
from Ventanas import ventanaPrincipal, registro
import tkinter.simpledialog as simpledialog
from PIL import ImageTk, Image
import time
import sys
from natsort import natsorted

class Login:
    
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Inicio de sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        self.admin_password = "pau123"
        genericos.centrar_ventana(self.ventana, 800, 500)
        
        
        logo = genericos.leer_imagen("./Resources/logoProvisional.png", (200, 200))
        
        frame_logo = Frame(self.ventana, bd=0, width=300, relief=SOLID, padx=10, pady=10, bg='#A0D683')
        frame_logo.pack(side="left", expand=NO, fill=BOTH)
        lbllogo = Label(frame_logo, image=logo, bg='#A0D683')
        lbllogo.place(x=0, y=0, relwidth=1, relheight=1)
        
        frame_form = Frame(self.ventana, bd=0, relief=SOLID, bg='white')
        frame_form.pack(side="right", expand=YES, fill=BOTH)
        
        
        frame_form_title = Frame(frame_form, height=50, bd=0,  relief=SOLID, bg='black')
        frame_form_title.pack(side="top", fill=X)
        titulo = Label(frame_form_title, text='Inicio de sesion', font=Font(family='Times', size=30), fg="#666a88", bg='white', pady=50)
        titulo.pack(expand=YES, fill=BOTH)
        
        frame_form_fill = Frame(frame_form, height=50, bd=0,  relief=SOLID, bg='white')
        frame_form_fill.pack(side="bottom", expand=YES, fill=BOTH)
        
        etiqueta_usuario = Label(frame_form_fill, text="Usuario", font=('Times', 14) ,fg="#666a88",bg='white', anchor="w")
        etiqueta_usuario.pack(fill=X, padx=20,pady=5)
        self.usuario = Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=X, padx=20,pady=10)

        etiqueta_password = Label(frame_form_fill, text="Contraseña", font=('Times', 14),fg="#666a88",bg='white' , anchor="w")
        etiqueta_password.pack(fill=X, padx=20,pady=5)
        self.password = Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=X, padx=20,pady=10)
        self.password.config(show="*")

        inicio = Button(frame_form_fill,text="Iniciar sesion",font=('Times', 15, BOLD),bg='#A0D683', bd=0,fg="#fff", command=self.verificar_datos)
        inicio.pack(fill=X, padx=20,pady=20)  
        
        registrarse = Button(frame_form_fill,text="Registrar Usuario",font=('Times', 15, BOLD),bg='#A0D683', bd=0,fg="#fff", command=self.ventanaRegistro)
        registrarse.pack(fill=X, padx=20,pady=20) 
        
        self.ventana.mainloop()
                  
        #end frame_form_fill
        
        
    def verificar_datos(self):
        usuario = self.usuario.get()
        contrasena = self.password.get()
            
        try: 
            with open('./Resources/usuarios.txt', 'r') as archivo:
                usuarios = archivo.readlines()
            
            # Eliminar caracteres de nueva linea y espacios
            usuarios = [linea.strip() for linea in usuarios]
            
            credenciales_validas = False
            for linea in usuarios:
                usuario_archivo, contrasena_archivo = linea.split(',')
                if usuario == usuario_archivo and contrasena == contrasena_archivo:
                    credenciales_validas = True
                    break
            if credenciales_validas:
                self.ventana.destroy()
                ventanaPrincipal.VentanaPrincipal()
                
            
            else:
                messagebox.showerror("Error", "Credenciales invalidas")
                
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontro el archivo de usuarios")
            
    def ventanaRegistro(self):
        contrasena_admin = simpledialog.askstring("Contraseña de administrador",
                                              "Ingrese la contraseña de administrador:",
                                              show='*', parent=self.ventana)
        if contrasena_admin == self.admin_password:
            self.ventana.destroy()
            registro.Registrar()
        elif contrasena_admin is None:
            # El usuario canceló el diálogo
            messagebox.showerror("Error", "Contraseña de administrador requerida")
        else:
            messagebox.showerror("Error", "Contraseña de administrador incorrecta")
        self.mostrar_mensaje("Contraseña de administrador incorrecta", "red")
        
        
            
        