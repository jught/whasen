import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pandas as pd
import json
from dotenv import load_dotenv
from utils import leer_excel
from templates import generar_mensaje

load_dotenv()

TEMPLATE_PATH = './app/templates/mensajes.plantilla'
TEST_MODE = False

def importar_fichero():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("Text files", "*.txt"), ("CSV files", "*.csv")])
    if filepath:
        try:
            df = leer_excel(filepath)
            columnas = list(df.columns)

            columna_var.set(', '.join(columnas))
            messagebox.showinfo("Importado", f"Archivo cargado con columnas: {', '.join(columnas)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

def generar_plantilla():
    ventana_plantilla = tk.Toplevel(root)
    ventana_plantilla.title("Generar Plantilla de Mensajes")
    
    texto = tk.Text(ventana_plantilla, height=10, width=60)
    texto.pack(pady=10)
    
    tk.Button(ventana_plantilla, text="Nombre", command=lambda: insertar_variable(texto, "<nombre>")).pack(side=tk.LEFT, padx=5)
    tk.Button(ventana_plantilla, text="Teléfono", command=lambda: insertar_variable(texto, "<telefono>")).pack(side=tk.LEFT, padx=5)
    tk.Button(ventana_plantilla, text="Guardar Plantilla", command=lambda: guardar_plantilla(texto)).pack(side=tk.LEFT, padx=5)

def insertar_variable(widget, variable):
    widget.insert(tk.INSERT, variable)

def guardar_plantilla(texto_widget):
    contenido = texto_widget.get("1.0", tk.END)
    plantilla = {
        "plantilla": contenido.strip(),
        "variables": ["<nombre>", "<telefono>"]
    }
    try:
        with open(TEMPLATE_PATH, 'w') as f:
            json.dump(plantilla, f, indent=4)
        messagebox.showinfo("Guardado", "Plantilla guardada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def alternar_modo():
    global TEST_MODE
    TEST_MODE = not TEST_MODE
    color = "#333333" if TEST_MODE else "white"
    root.configure(bg=color)
    modo_boton.config(text="Modo Test" if TEST_MODE else "Modo Normal")

root = tk.Tk()
root.title("Sistema de Mensajes WhatsApp")

columna_var = tk.StringVar()

tk.Button(root, text="Importar Fichero", command=importar_fichero).pack(pady=10)
tk.Label(root, text="Columnas detectadas:").pack()
tk.Label(root, textvariable=columna_var).pack(pady=5)

tk.Button(root, text="Generar Plantilla", command=generar_plantilla).pack(pady=10)
modo_boton = tk.Button(root, text="Modo Normal", command=alternar_modo)
modo_boton.pack(pady=20)

root.mainloop()
