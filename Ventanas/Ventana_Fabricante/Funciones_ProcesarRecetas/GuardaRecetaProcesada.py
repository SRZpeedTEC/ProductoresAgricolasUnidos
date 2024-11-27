from pathlib import Path

def guardar_receta_procesada(receta_id, nombre_receta):
    path_productos_listos = "Resources/txt_recetas/productos_listos.txt"
    try:
        # Crear el archivo si no existe
        if not path_productos_listos.exists():
            path_productos_listos.touch()

        # Guardar la receta procesada en el archivo
        with open(path_productos_listos, "a") as file:
            file.write(f"{receta_id}|{nombre_receta}|Procesado\n")
        print("Receta procesada guardada con éxito.")
    except Exception as e:
        print(f"Error al guardar la receta procesada: {e}")
