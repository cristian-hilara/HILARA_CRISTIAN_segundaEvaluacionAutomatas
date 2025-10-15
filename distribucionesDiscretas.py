# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 09:45:51 2025

@author: hilar
"""
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# === Funciones para generar distribuciones ===
def generar_distribucion(nombre, params, n=1000):
    if nombre == "Uniforme":
        a = int(params["a"].get())
        b = int(params["b"].get())
        data = np.random.randint(a, b + 1, n)
        titulo = f"UNIFORME DISCRETA (a={a}, b={b})"
    
    elif nombre == "Bernoulli":
        p = float(params["p"].get())
        data = np.random.binomial(1, p, n)
        titulo = f"BERNOULLI (p={p})"
    
    elif nombre == "Binomial":
        n_ensayos = int(params["n"].get())
        p = float(params["p"].get())
        data = np.random.binomial(n_ensayos, p, n)
        titulo = f"BINOMIAL (n={n_ensayos}, p={p})"
    
    elif nombre == "Poisson":
        lam = float(params["lam"].get())
        data = np.random.poisson(lam, n)
        titulo = f"POISSON (λ={lam})"
    
    else:
        data, titulo = np.array([]), ""
    
    return data, titulo


# === Actualizar campos según la distribución seleccionada ===
def actualizar_parametros(event=None):
    for widget in frame_params.winfo_children():
        widget.destroy()

    distrib = combo.get()
    global parametros
    parametros = {}

    if distrib == "Uniforme":
        tk.Label(frame_params, text="a:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        parametros["a"] = tk.Entry(frame_params, width=8)
        parametros["a"].insert(0, "1")
        parametros["a"].grid(row=0, column=1, padx=5)

        tk.Label(frame_params, text="b:", bg="#1e1e1e", fg="white").grid(row=0, column=2)
        parametros["b"] = tk.Entry(frame_params, width=8)
        parametros["b"].insert(0, "6")
        parametros["b"].grid(row=0, column=3, padx=5)

    elif distrib == "Bernoulli":
        tk.Label(frame_params, text="p:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        parametros["p"] = tk.Entry(frame_params, width=8)
        parametros["p"].insert(0, "0.6")
        parametros["p"].grid(row=0, column=1, padx=5)

    elif distrib == "Binomial":
        tk.Label(frame_params, text="n:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        parametros["n"] = tk.Entry(frame_params, width=8)
        parametros["n"].insert(0, "10")
        parametros["n"].grid(row=0, column=1, padx=5)

        tk.Label(frame_params, text="p:", bg="#1e1e1e", fg="white").grid(row=0, column=2)
        parametros["p"] = tk.Entry(frame_params, width=8)
        parametros["p"].insert(0, "0.5")
        parametros["p"].grid(row=0, column=3, padx=5)

    elif distrib == "Poisson":
        tk.Label(frame_params, text="λ:", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        parametros["lam"] = tk.Entry(frame_params, width=8)
        parametros["lam"].insert(0, "3")
        parametros["lam"].grid(row=0, column=1, padx=5)


# === Función para graficar ===
def graficar():
    distrib = combo.get()
    data, titulo = generar_distribucion(distrib, parametros)
    if data.size == 0:
        return

    fig.clear()
    ax = fig.add_subplot(111)

    valores, conteo = np.unique(data, return_counts=True)
    ax.bar(valores, conteo, color='dodgerblue', edgecolor='black', width=0.6)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel("Valores")
    ax.set_ylabel("Frecuencia")
    ax.grid(True, linestyle='--', alpha=0.6)
    canvas.draw()


# === Interfaz principal ===
ventana = tk.Tk()
ventana.title("Distribuciones Discretas")
ventana.geometry("760x580")
ventana.config(bg="#1e1e1e")

# Título principal
tk.Label(ventana, text="Simulador de Distribuciones Discretas", bg="#1e1e1e", fg="white",
         font=("Arial", 15, "bold")).pack(pady=10)

# ComboBox
frame_superior = tk.Frame(ventana, bg="#1e1e1e")
frame_superior.pack(pady=5)
tk.Label(frame_superior, text="Distribución:", bg="#1e1e1e", fg="white", font=("Arial", 11)).pack(side="left", padx=5)
combo = ttk.Combobox(frame_superior, values=["Uniforme", "Bernoulli", "Binomial", "Poisson"],
                     state="readonly", font=("Arial", 11))
combo.set("Uniforme")
combo.pack(side="left", padx=5)
combo.bind("<<ComboboxSelected>>", actualizar_parametros)

# Parámetros
frame_params = tk.Frame(ventana, bg="#1e1e1e")
frame_params.pack(pady=10)
parametros = {}
actualizar_parametros()

# Botón
boton = tk.Button(ventana, text="Generar y Graficar", command=graficar, bg="#0078D7", fg="white",
                  font=("Arial", 11, "bold"), padx=10, pady=5)
boton.pack(pady=10)

# Figura Matplotlib
fig = plt.Figure(figsize=(6.5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(padx=10, pady=10)

ventana.mainloop()
