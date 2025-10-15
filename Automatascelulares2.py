# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:43:32 2025

@author: hilar
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================
# REGLAS DEL AUTÓMATA
# =========================
def regla_30(vecino):
    a, b, c = vecino
    return a ^ (b or c)

def regla_90(vecino):
    a, b, c = vecino
    return a ^ c

def regla_xor(vecino):
    # Regla personalizada: SI(B1<>D1;1;0)
    a, b, c = vecino
    return 1 if a != c else 0

# =========================
# SIGUIENTE FILA
# =========================
def siguiente_fila(fila_actual, regla):
    nueva_fila = np.zeros_like(fila_actual)
    # Borde se considera 0 (igual que en Excel cuando no hay valor)
    for j in range(len(fila_actual)):
        izquierda = fila_actual[j-1] if j > 0 else 0
        centro = fila_actual[j]
        derecha = fila_actual[j+1] if j < len(fila_actual)-1 else 0
        nueva_fila[j] = regla((izquierda, centro, derecha))
    return nueva_fila

# =========================
# ANIMACIÓN
# =========================
def animar(i):
    global filas, regla_func, ax, canvas
    if i >= len(filas)-1:
        return
    filas[i+1] = siguiente_fila(filas[i], regla_func)

    ax.clear()
    ax.imshow(filas[:i+2], cmap='binary', interpolation='nearest', origin='upper')
    ax.set_xticks([])
    ax.set_yticks([])
    canvas.draw()

    ventana.after(150, lambda: animar(i+1))

# =========================
# INICIAR SIMULACIÓN
# =========================
def iniciar():
    global filas, regla_func
    entrada = entry_binario.get().strip()
    if not entrada or not all(c in '01' for c in entrada):
        messagebox.showerror("Error", "Ingrese una cadena binaria válida (solo 0 y 1).")
        return
    
    try:
        num_filas = int(entry_filas.get())
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido de filas.")
        return
    
    n = len(entrada)
    filas = np.zeros((num_filas, n), dtype=int)
    filas[0] = [int(c) for c in entrada]

    regla = combo_regla.get()
    if regla == "Regla 30":
        regla_func = regla_30
    elif regla == "Regla 90":
        regla_func = regla_90
    else:
        regla_func = regla_xor

    animar(0)

# =========================
# INTERFAZ
# =========================
ventana = tk.Tk()
ventana.title("Autómatas Celulares Interactivos")
ventana.geometry("900x600")

ttk.Label(ventana, text="Fila inicial (binario, ej: 111111101111111):").pack()
entry_binario = ttk.Entry(ventana, width=60)
entry_binario.pack(pady=5)

ttk.Label(ventana, text="Número de filas a generar:").pack()
entry_filas = ttk.Entry(ventana, width=10)
entry_filas.insert(0, "50")
entry_filas.pack(pady=5)

ttk.Label(ventana, text="Seleccione regla:").pack()
combo_regla = ttk.Combobox(
    ventana,
    values=["Regla 30", "Regla 90", "Regla XOR (SI(B1<>D1;1;0))"]
)
combo_regla.current(2)
combo_regla.pack(pady=5)

boton_iniciar = ttk.Button(ventana, text="Iniciar simulación", command=iniciar)
boton_iniciar.pack(pady=5)

fig, ax = plt.subplots(figsize=(8,6))
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ventana.mainloop()
