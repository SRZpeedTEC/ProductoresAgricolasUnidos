from tkinter import *
from tkinter import ttk
import os
import random
from .Ver_lotesprocesados import VerLotesProcesados

class Procesar:

    def __init__(self, parent_frame, btn_width=15):
        # Inicializar los lotes procesados
        self.lotes_procesados = self.leer_lotes_procesados()
        self.lote_confirmado = None

        # Limpiar el frame pasado antes de agregar nuevos widgets
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Etiqueta de título
        Label(parent_frame, text="Procesamiento de Lotes", bg="#A0D683", font=("Arial", 18, "bold")).pack(pady=10)

        # Frame para botones de control
        frame_botones = Frame(parent_frame, bg="#A0D683")
        frame_botones.pack(pady=5)

        # Botón para iniciar la máquina
        btn_iniciar = Button(frame_botones, text="Iniciar Máquina", command=self.iniciar_maquina, bg="#B6FFA1", font=("Arial", 10), width=btn_width)
        btn_iniciar.grid(row=0, column=0, padx=5, pady=5)

        # Botón para pausar la máquina
        btn_pausar = Button(frame_botones, text="Pausar Máquina", command=self.pausar_maquina, bg="#B6FFA1", font=("Arial", 10), width=btn_width)
        btn_pausar.grid(row=0, column=1, padx=5, pady=5)

        # Botón para finalizar la máquina
        btn_finalizar = Button(frame_botones, text="Finalizar Máquina", command=self.finalizar_maquina, bg="#B6FFA1", font=("Arial", 10), width=btn_width)
        btn_finalizar.grid(row=0, column=2, padx=5, pady=5)

        # Selector de lote a procesar
        frame_selector_lote = Frame(parent_frame, bg="#A0D683")
        frame_selector_lote.pack(pady=5)

        Label(frame_selector_lote, text="Seleccionar Lote:", bg="#A0D683", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)

        self.lote_var = StringVar()
        self.lote_selector = ttk.Combobox(frame_selector_lote, textvariable=self.lote_var, font=("Arial", 12), state="readonly")
        self.lote_selector.grid(row=0, column=1, padx=5, pady=5)

        # Llenar el Combobox con los lotes disponibles desde el archivo
        self.actualizar_lotes_disponibles()

        # Botón para confirmar el lote
        btn_confirmar_lote = Button(frame_selector_lote, text="Confirmar Lote", command=self.confirmar_lote, bg="#B6FFA1", font=("Arial", 10), width=btn_width)
        btn_confirmar_lote.grid(row=0, column=2, padx=5, pady=5)

        # Área de texto para mostrar el registro de actividad
        self.text_area = Text(parent_frame, wrap=WORD, width=80, height=10, font=("Arial", 10))
        self.text_area.pack(pady=10)

    def leer_lotes_procesados(self):
        # Leer el archivo de lotes procesados y devolver un conjunto de lotes ya procesados
        lotes_procesados = set()
        # Cambiar la ruta a la nueva ubicación de los lotes procesados
        path = "Resources/txt_lotes/lotes_procesados.txt"
        if os.path.exists(path):
            with open(path, "r") as file:
                for line in file:
                    partes = line.strip().split(':')
                    if len(partes) > 0:
                        lotes_procesados.add(partes[0])
        return lotes_procesados

    def actualizar_lotes_disponibles(self):
        # Leer el archivo de lotes y llenar el combobox con solo el identificador del lote
        lotes = []
        path = "Resources/txt_lotes/lotes.txt"  # Cambiar esta ruta si también moviste el archivo de lotes
        if os.path.exists(path):
            with open(path, "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split(',')
                        if len(partes) == 4:
                            lote_id = partes[3]  # Extraer solo el identificador del lote
                            if lote_id not in self.lotes_procesados:
                                lotes.append(lote_id)
        
        # Actualizar el combobox con los lotes encontrados
        self.lote_selector['values'] = lotes
        if lotes:
            self.lote_selector.set("Seleccione un lote")
        else:
            self.lote_selector.set("No hay lotes disponibles")

    def actualizar_log(self, mensaje):
        # Función para mostrar mensajes en el área de texto
        self.text_area.insert(END, mensaje + "\n")
        self.text_area.see(END)  # Desplazar hacia el final para ver el último mensaje

    def iniciar_maquina(self):
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. Seleccione un lote antes de iniciar la máquina.")
        elif self.lote_confirmado in self.lotes_procesados:
            self.actualizar_log(f"Error: El lote {self.lote_confirmado} ya ha sido procesado. Seleccione un lote diferente.")
        else:
            self.actualizar_log(f"Máquina iniciada. Procesando el lote {self.lote_confirmado}...")

    def pausar_maquina(self):
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. No se puede pausar sin iniciar el procesamiento.")
        else:
            self.actualizar_log("Máquina pausada. Esperando para continuar...")

    def finalizar_maquina(self):
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. No se puede finalizar sin iniciar el procesamiento.")
        else:
            # Simular el procesamiento del lote
            self.simular_procesamiento()

            # Añadir el lote confirmado a la lista de lotes procesados y registrarlo en el archivo
            self.lotes_procesados.add(self.lote_confirmado)
            with open("Resources/txt_lotes/lotes_procesados.txt", "a") as file:  # Actualizar la ruta
                file.write(f"{self.lote_confirmado}: {self.resultado_procesamiento}\n")

            # Actualizar la lista de lotes disponibles
            self.actualizar_lotes_disponibles()
            # Resetear el lote confirmado
            self.lote_confirmado = None

    def confirmar_lote(self):
        lote = self.lote_var.get()
        if not lote or lote == "Seleccione un lote":
            self.actualizar_log("Error: Por favor, seleccione un lote válido.")
        elif lote in self.lotes_procesados:
            self.actualizar_log(f"Error: El lote {lote} ya ha sido procesado. Seleccione un lote diferente.")
        else:
            self.lote_confirmado = lote
            self.actualizar_log(f"Lote {lote} confirmado para procesamiento.")

    def simular_procesamiento(self):
        # Simular el procesamiento de un lote, dividiendo en categorías específicas
        categorias = ['Pequeños Verdes', 'Pequeños Maduros', 'Grandes Verdes', 'Grandes Maduros', 'Dañados']
        resultado = {}

        # Generar aleatoriamente la cantidad de kilogramos para cada categoría
        for categoria in categorias:
            cantidad_kg = random.randint(10, 50)  # Simulando entre 10 y 50 kg
            resultado[categoria] = cantidad_kg

        # Actualizar el log con los detalles del procesamiento
        self.actualizar_log("Resultado del procesamiento:")
        for key, value in resultado.items():
            self.actualizar_log(f"  {key}: {value} kg")

        # Guardar el resultado para registrar en el archivo
        self.resultado_procesamiento = ", ".join([f"{key}: {value} kg" for key, value in resultado.items()])

    def mostrar_lotes_procesados(self, parent_frame):
        # Llamar a la clase VerLotesProcesados para cargar los lotes procesados
        VerLotesProcesados(parent_frame)
