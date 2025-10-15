# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 09:40:58 2025

@author: hilar
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def generar():
    try:
        dist = combo_tipo.get()
        cantidad = int(entry_cant.get())
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
            return

        valores = []

        # --- UNIFORME ---
        if dist == "Uniforme":
            a = float(entry_param1.get())
            b = float(entry_param2.get())
            if a >= b:
                messagebox.showerror("Error", "El mínimo debe ser menor que el máximo.")
                return
            valores = [round(random.uniform(a, b), 2) for _ in range(cantidad)]

        # --- K-ERLANG (Gamma con forma=k, escala=θ/k) ---
        elif dist == "k-Erlang":
            k = float(entry_param1.get())
            theta = float(entry_param2.get())
            valores = [round(random.gammavariate(k, theta / k), 2) for _ in range(cantidad)]

        # --- EXPONENCIAL (Gamma con forma=1, escala=λ) ---
        elif dist == "Exponencial":
            lambd = float(entry_param1.get())
            valores = [round(random.gammavariate(1, lambd), 2) for _ in range(cantidad)]

        # --- GAMMA (forma=(μ²/σ²), escala=(σ²/μ)) ---
        elif dist == "Gamma":
            media = float(entry_param1.get())
            varianza = float(entry_param2.get())
            forma = (media ** 2) / varianza
            escala = varianza / media
            valores = [round(random.gammavariate(forma, escala), 2) for _ in range(cantidad)]

        # --- NORMAL ---
        elif dist == "Normal":
            media = float(entry_param1.get())
            varianza = float(entry_param2.get())
            valores = [round(random.normalvariate(media, np.sqrt(varianza)), 2) for _ in range(cantidad)]

        # --- WEIBULL ---
        elif dist == "Weibull":
            forma = float(entry_param1.get())
            escala = float(entry_param2.get())
            desplaz = float(entry_param3.get()) if entry_param3.get() != "" else 0
            valores = [round(desplaz + (escala ** 2) * ((-np.log(1 - random.random())) ** (1 / forma)), 2)
                       for _ in range(cantidad)]

        # Limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        # Insertar nuevos valores
        for i, v in enumerate(valores, start=1):
            tabla.insert("", "end", values=(i, v))

        # Mostrar gráfico
        mostrar_grafico(valores, dist)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

def mostrar_grafico(valores, titulo):
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 3.5))
    n, bins, patches = ax.hist(valores, bins=10, color="#5DADE2", edgecolor="black", rwidth=0.9)

    for i in range(len(n)):
        ax.text(bins[i] + (bins[i+1]-bins[i])/2, n[i] + 0.3, str(int(n[i])),
                ha='center', va='bottom', fontsize=8)

    ax.set_title(f"Distribución {titulo}", fontsize=12, weight="bold")
    ax.set_xlabel("Valores")
    ax.set_ylabel("Frecuencia")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack()

def actualizar_campos(event=None):
    dist = combo_tipo.get()
    for w in [lbl_p1, lbl_p2, lbl_p3, entry_param1, entry_param2, entry_param3]:
        w.pack_forget()

    if dist == "Uniforme":
        lbl_p1.config(text="Mínimo (a):"); lbl_p2.config(text="Máximo (b):")
        lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack()

    elif dist == "k-Erlang":
        lbl_p1.config(text="Forma (k):"); lbl_p2.config(text="Escala (θ):")
        lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack()

    elif dist == "Exponencial":
        lbl_p1.config(text="Escala (λ):")
        lbl_p1.pack(); entry_param1.pack()

    elif dist == "Gamma":
        lbl_p1.config(text="Media (μ):"); lbl_p2.config(text="Varianza (σ²):")
        lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack()

    elif dist == "Normal":
        lbl_p1.config(text="Media (μ):"); lbl_p2.config(text="Varianza (σ²):")
        lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack()

    elif dist == "Weibull":
        lbl_p1.config(text="Forma (β):"); lbl_p2.config(text="Escala (η):"); lbl_p3.config(text="Desplazamiento (opcional):")
        lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack(); lbl_p3.pack(); entry_param3.pack()

# ---------------- INTERFAZ ----------------
ventana = tk.Tk()
ventana.title("Simulador de Distribuciones")
ventana.geometry("500x750")
ventana.resizable(False, False)

tk.Label(ventana, text="Tipo de Distribución:").pack(pady=5)
combo_tipo = ttk.Combobox(ventana, values=["Uniforme", "k-Erlang", "Exponencial", "Gamma", "Normal", "Weibull"])
combo_tipo.current(0)
combo_tipo.pack()
combo_tipo.bind("<<ComboboxSelected>>", actualizar_campos)

# Campos de parámetros
lbl_p1 = tk.Label(ventana, text="Mínimo (a):")
entry_param1 = tk.Entry(ventana)
lbl_p2 = tk.Label(ventana, text="Máximo (b):")
entry_param2 = tk.Entry(ventana)
lbl_p3 = tk.Label(ventana, text="Desplazamiento:")
entry_param3 = tk.Entry(ventana)

lbl_p1.pack(); entry_param1.pack(); lbl_p2.pack(); entry_param2.pack()

tk.Label(ventana, text="Cantidad de valores:").pack(pady=5)
entry_cant = tk.Entry(ventana)
entry_cant.pack()

tk.Button(ventana, text="Generar", command=generar, bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).pack(pady=10)

# Tabla
tabla = ttk.Treeview(ventana, columns=("N°", "Valor"), show="headings", height=10)
tabla.heading("N°", text="N°")
tabla.heading("Valor", text="Valor")
tabla.column("N°", width=50, anchor="center")
tabla.column("Valor", width=100, anchor="center")
tabla.pack(pady=10)

# Frame para el gráfico
frame_grafico = tk.Frame(ventana)
frame_grafico.pack(pady=10)

ventana.mainloop()

