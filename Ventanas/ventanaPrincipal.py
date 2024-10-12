from tkinter import *
from tkinter.font import Font
import Utiles.Genericos as gnr
from PIL import ImageTk, Image

class VentanaPrincipal:
    
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title('Ventana Principal')
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg="#A0D683")
        self.ventana.resizable(0, 0)
        
        logo = gnr.leer_imagen("./Resources/logoProvisional.png", (200, 200))
        lblLogo = Label(self.ventana, image=logo, bg="#B6FFA1")
        lblLogo.place(x=0, y=0, relwidth=1, relheight=1)  
        self.ventana.mainloop()   
           