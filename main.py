from Ventanas.Ventana_Agricultor.VentanaPrincipalAgricultor import VentanaPrincipalAgricultor
from Ventanas.Ventana_Fabricante.VentanaPrincipalFabricante import VentanaPrincipalFabricante
from Ventanas.Login.registro.login import Login
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

Login()
