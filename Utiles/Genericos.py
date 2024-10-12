from PIL import ImageTk, Image


def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

def centrar_ventana(ventana, ancho, largo):
    pantalla_Ancho = ventana.winfo_screenwidth()
    pantalla_Alto = ventana.winfo_screenheight()
    x = int((pantalla_Ancho / 2) - (ancho / 2))
    y = int((pantalla_Alto / 2) - (largo / 2))
    return ventana.geometry(f"{ancho}x{largo}+{x}+{y}")
    

