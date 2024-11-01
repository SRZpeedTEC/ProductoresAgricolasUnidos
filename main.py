from Ventanas.VentanaAgricultor import VentanaPrincipalAgricultor
from Ventanas.VentanaFabricante import VentanaPrincipalFabricante
from Ventanas.Login.registro.login import Login
from Pagina_Web.InterfazPW import InterfazWeb
import os
from tkinter import messagebox

project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Login()
# InterfazWeb()
# VentanaPrincipalAgricultor()
VentanaPrincipalFabricante()


"""
with open("Resources/txt_informacion_productos/materia_prima_fabrica.txt", "r") as file:
    registros = {}
    for line in file:
        if line.strip():
            partes = line.strip().split("|")
            if len(partes) == 4:
                            codigo = partes[0].strip()
                            descripcion = partes[1].strip()                          
                            cantidad = partes[2].strip()
                            unidad = partes[3].strip()
                            try:
                                cantidad = float(cantidad)
                                registros[codigo] = (descripcion,  cantidad,  unidad)                               
                            except ValueError:
                                messagebox.showwarning("Advertencia", f"La cantidad no es válida en la línea: {line}")

print(registros["TOM-001"][1])               
"""