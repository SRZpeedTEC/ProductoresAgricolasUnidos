from Ventanas.VentanaPrincipalAgricultor import VentanaPrincipalAgricultor
from Ventanas.VentanaPrincipalFabricante import VentanaPrincipalFabricante
from Ventanas.login import Login
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

Login()
