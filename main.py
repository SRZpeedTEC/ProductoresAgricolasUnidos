from Ventanas.VentanaAgricultor import VentanaPrincipalAgricultor
from Ventanas.VentanaFabricante import VentanaPrincipalFabricante
from Ventanas.Login.registro.login import Login
from Pagina_Web.InterfazPW import InterfazWeb
import os
from tkinter import messagebox

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Login()
#InterfazWeb()
#VentanaPrincipalAgricultor()
VentanaPrincipalFabricante()    