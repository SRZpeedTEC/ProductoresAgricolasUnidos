from tkinter import messagebox
from pathlib import Path

class ManipulacionRecetasTXT:
    path_recetas = "Resources/txt_recetas/recetas.txt"



    @classmethod
    @classmethod
    def validar_ingredientes(cls, ingredientes):
        """
        Valida que los ingredientes tengan el formato correcto (código, cantidad).
        """
        for ingrediente in ingredientes:
            if len(ingrediente) != 2:
                return False
            codigo, cantidad = ingrediente
            if not codigo or not cantidad:
                return False
            try:
                # Asegurarse de que la cantidad sea un número entero o flotante
                float(cantidad)
            except ValueError:
                return False
        return True


    @classmethod
    def leer_recetas(cls):
        """
        Lee las recetas desde el archivo.
        """
        recetas = []
        try:
            with open(cls.path_recetas, "r", encoding="utf-8") as file:
                for line in file:
                    partes = line.strip().split("|")
                    if len(partes) >= 5:
                        id_receta = partes[0]
                        nombre = partes[1]
                        cantidad = int(partes[2])  # Asegúrate de convertir cantidades a entero
                        unidad = partes[3]
                        ingredientes = [tuple(ing.split(":")) for ing in partes[4].split(";") if ":" in ing]
                        recetas.append((id_receta, nombre, cantidad, unidad, ingredientes))
        except FileNotFoundError:
            # Si el archivo no existe, devuelve una lista vacía
            return []
        except Exception as e:
            raise Exception(f"Error al leer recetas: {e}")
        return recetas

    @classmethod
    def agregar_receta(cls, receta_id, nombre, cantidad_producir, unidad, ingredientes):
        """
        Agrega una nueva receta al archivo.
        """
        
        
        # Validar los ingredientes
        if not cls.validar_ingredientes(ingredientes):
            raise ValueError("Los ingredientes deben tener el formato 'codigo:cantidad'. La cantidad debe ser un número entero.")
        
        recetas_existentes = cls.leer_recetas()

        # Verificar duplicados por ID
        if any(receta[0] == receta_id for receta in recetas_existentes):
            raise ValueError(f"El ID '{receta_id}' ya existe. Usa otro ID.")

        # Añadir la nueva receta
        ingredientes_str = ";".join([f"{codigo}:{cantidad}" for codigo, cantidad in ingredientes])
        nueva_receta = f"{receta_id}|{nombre}|{cantidad_producir}|{unidad}|{ingredientes_str}\n"
        
        try:
            with open(cls.path_recetas, "a", encoding="utf-8") as file:
                file.write(nueva_receta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo escribir en el archivo: {e}")

    @classmethod
    def escribir_recetas(cls, recetas):
        """
        Sobrescribe el archivo con las recetas proporcionadas.
        """
        
        try:
            with open(cls.path_recetas, "w", encoding="utf-8") as file:
                for receta in recetas:
                    id_receta, nombre, cantidad_producir, unidad, ingredientes = receta
                    ingredientes_str = ";".join([f"{codigo}:{cantidad}" for codigo, cantidad in ingredientes])
                    file.write(f"{id_receta}|{nombre}|{cantidad_producir}|{unidad}|{ingredientes_str}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo escribir en el archivo: {e}")

    @classmethod
    def eliminar_receta(cls, receta_id):
        """
        Elimina una receta por su ID.
        """
        recetas = cls.leer_recetas()
        recetas_filtradas = [receta for receta in recetas if receta[0] != receta_id]

        if len(recetas) == len(recetas_filtradas):
            messagebox.showinfo("Información", f"No se encontró una receta con ID '{receta_id}'.")
            return

        cls.escribir_recetas(recetas_filtradas)

    @classmethod
    def actualizar_receta(cls, receta_id, nuevo_nombre, nueva_cantidad_producir, nueva_unidad, nuevos_ingredientes):
        """
        Actualiza una receta existente.
        """
        # Validar los ingredientes
        if not cls.validar_ingredientes(nuevos_ingredientes):
            raise ValueError("Los ingredientes deben tener el formato 'codigo:cantidad'. La cantidad debe ser un número entero.")
        
        recetas = cls.leer_recetas()
        for i, receta in enumerate(recetas):
            if receta[0] == receta_id:
                recetas[i] = (receta_id, nuevo_nombre, nueva_cantidad_producir, nueva_unidad, nuevos_ingredientes)
                cls.escribir_recetas(recetas)
                return

        messagebox.showinfo("Información", f"No se encontró una receta con ID '{receta_id}'.")

    @classmethod
    def eliminar_ingrediente(cls, receta_id, codigo_ingrediente):
        """
        Elimina un ingrediente específico de una receta por su código.
        """
        recetas = cls.leer_recetas()
        for i, receta in enumerate(recetas):
            if receta[0] == receta_id:
                ingredientes = receta[4]
                ingredientes_filtrados = [ingrediente for ingrediente in ingredientes if ingrediente[0] != codigo_ingrediente]
                if len(ingredientes) == len(ingredientes_filtrados):
                    messagebox.showinfo("Información", f"No se encontró el ingrediente con código '{codigo_ingrediente}' en la receta '{receta_id}'.")
                else:
                    recetas[i] = (receta_id, receta[1], receta[2], receta[3], ingredientes_filtrados)
                    cls.escribir_recetas(recetas)
                    messagebox.showinfo("Información", f"Ingrediente con código '{codigo_ingrediente}' eliminado.")
                return
        messagebox.showinfo("Información", f"No se encontró una receta con ID '{receta_id}'.")
