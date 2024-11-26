import os
from tkinter import messagebox

class EliminarReceta:
    def __init__(self, path_recetas):
        """
        Inicializa la clase EliminarReceta con la ruta al archivo de recetas.
        """
        self.path_recetas = os.path.abspath(path_recetas)

    def eliminar_receta(self, tree):
        """
        Elimina una receta seleccionada en el Treeview y la actualiza en el archivo.
        """
        # Verificar si hay una selección en el Treeview
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una receta para eliminar.")
            return

        # Obtener los valores del elemento seleccionado
        values = tree.item(selected_item[0])["values"]
        if not values or len(values) == 0:
            messagebox.showerror("Error", "No se pudo obtener los datos de la receta seleccionada.")
            return

        receta_id = str(values[0])  # El ID de la receta está en la primera columna

        # Confirmar la eliminación
        confirmar = messagebox.askyesno(
            "Confirmar", f"¿Estás seguro de que deseas eliminar la receta con ID '{receta_id}'?"
        )
        if not confirmar:
            return

        try:
            # Actualizar el archivo de recetas eliminando la receta seleccionada
            self._eliminar_receta_del_archivo(receta_id)

            # Eliminar la receta del Treeview
            tree.delete(selected_item[0])

            messagebox.showinfo("Éxito", f"Receta con ID '{receta_id}' eliminada correctamente.")
        except FileNotFoundError as fnf_error:
            messagebox.showerror("Error", f"No se encontró el archivo de recetas: {fnf_error}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la eliminación: {e}")

    def _eliminar_receta_del_archivo(self, receta_id):
        """
        Elimina una receta por su ID del archivo de recetas.
        """
        # Verificar si el archivo de recetas existe
        if not os.path.exists(self.path_recetas):
            raise FileNotFoundError(f"No se encontró el archivo de recetas en: {self.path_recetas}")

        try:
            # Leer todas las recetas del archivo
            with open(self.path_recetas, "r", encoding="utf-8") as file:
                recetas = file.readlines()

            # Filtrar las recetas para excluir la receta con el ID proporcionado
            recetas_actualizadas = [
                receta for receta in recetas if not receta.split("|", 1)[0] == receta_id
            ]

            # Verificar si realmente se eliminó alguna receta
            if len(recetas_actualizadas) == len(recetas):
                raise ValueError(f"No se encontró una receta con ID '{receta_id}' en el archivo.")

            # Escribir las recetas actualizadas en el archivo
            with open(self.path_recetas, "w", encoding="utf-8") as file:
                file.writelines(recetas_actualizadas)
                
        except FileNotFoundError as fnf_error:
            raise FileNotFoundError(f"No se encontró el archivo: {fnf_error}")
        except Exception as e:
            raise Exception(f"Error al actualizar el archivo de recetas: {e}")
