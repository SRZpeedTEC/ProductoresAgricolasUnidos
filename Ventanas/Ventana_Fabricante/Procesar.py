from tkinter import *
from tkinter import ttk
import os

class Procesar:

    def __init__(self):
        # Crear ventana para procesar
        self.ventana = Toplevel()
        self.ventana.title("Procesar Lote")
        self.ventana.geometry("800x600")
        self.ventana.config(bg="#A0D683")

        # Etiqueta de título
        Label(self.ventana, text="Procesamiento de Lotes", bg="#A0D683", font=("Arial", 20, "bold")).pack(pady=20)

        # Frame para botones de control
        frame_botones = Frame(self.ventana, bg="#A0D683")
        frame_botones.pack(pady=10)

        # Botón para iniciar la máquina
        btn_iniciar = Button(frame_botones, text="Iniciar Máquina", command=self.iniciar_maquina, bg="#B6FFA1", font=("Arial", 12), width=15)
        btn_iniciar.grid(row=0, column=0, padx=10, pady=5)

        # Botón para pausar la máquina
        btn_pausar = Button(frame_botones, text="Pausar Máquina", command=self.pausar_maquina, bg="#B6FFA1", font=("Arial", 12), width=15)
        btn_pausar.grid(row=0, column=1, padx=10, pady=5)

        # Botón para finalizar la máquina
        btn_finalizar = Button(frame_botones, text="Finalizar Máquina", command=self.finalizar_maquina, bg="#B6FFA1", font=("Arial", 12), width=15)
        btn_finalizar.grid(row=0, column=2, padx=10, pady=5)

        # Selector de lote a procesar
        frame_selector_lote = Frame(self.ventana, bg="#A0D683")
        frame_selector_lote.pack(pady=10)

        Label(frame_selector_lote, text="Seleccionar Lote:", bg="#A0D683", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        
        self.lote_var = StringVar()
        self.lote_selector = ttk.Combobox(frame_selector_lote, textvariable=self.lote_var, font=("Arial", 14), state="readonly")
        self.lote_selector.grid(row=0, column=1, padx=10, pady=5)

        # Llenar el Combobox con los lotes disponibles desde el archivo
        self.actualizar_lotes_disponibles()

        # Botón para confirmar el lote
        btn_confirmar_lote = Button(frame_selector_lote, text="Confirmar Lote", command=self.confirmar_lote, bg="#B6FFA1", font=("Arial", 12), width=15)
        btn_confirmar_lote.grid(row=0, column=2, padx=10, pady=5)

        # Área de texto para mostrar el registro de actividad
        self.text_area = Text(self.ventana, wrap=WORD, width=90, height=15, font=("Arial", 12))
        self.text_area.pack(pady=20)

        # Variable para almacenar el lote seleccionado
        self.lote_confirmado = None

    def actualizar_lotes_disponibles(self):
        # Leer el archivo de lotes y llenar el combobox con solo el identificador del lote
        lotes = []
        if os.path.exists("lotes.txt"):
            with open("lotes.txt", "r") as file:
                for line in file:
                    if line.strip():
                        partes = line.strip().split(',')
                        if len(partes) == 4:
                            lote_id = partes[3]  # Extraer solo el identificador del lote
                            lotes.append(lote_id)
        
        # Actualizar el combobox con los lotes encontrados
        self.lote_selector['values'] = lotes
        if lotes:
            self.lote_selector.set("Seleccione un lote")

    def actualizar_log(self, mensaje):
        # Función para mostrar mensajes en el área de texto
        self.text_area.insert(END, mensaje + "\n")
        self.text_area.see(END)  # Desplazar hacia el final para ver el último mensaje

    def iniciar_maquina(self):
        # Lógica para iniciar la máquina
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. Seleccione un lote antes de iniciar la máquina.")
        else:
            self.actualizar_log(f"Máquina iniciada. Procesando el lote {self.lote_confirmado}...")

    def pausar_maquina(self):
        # Lógica para pausar la máquina
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. No se puede pausar sin iniciar el procesamiento.")
        else:
            self.actualizar_log("Máquina pausada. Esperando para continuar...")

    def finalizar_maquina(self):
        # Lógica para finalizar la máquina
        if not self.lote_confirmado:
            self.actualizar_log("Error: No se ha confirmado ningún lote. No se puede finalizar sin iniciar el procesamiento.")
        else:
            self.actualizar_log("Máquina finalizada. Procesamiento completo.")
            self.lote_confirmado = None  # Resetear el lote confirmado

    def confirmar_lote(self):
        # Confirmar el lote que se quiere procesar
        lote = self.lote_var.get()
        if not lote or lote == "Seleccione un lote":
            self.actualizar_log("Error: Por favor, seleccione un lote válido.")
        else:
            self.lote_confirmado = lote
            self.actualizar_log(f"Lote {lote} confirmado para procesamiento.")
