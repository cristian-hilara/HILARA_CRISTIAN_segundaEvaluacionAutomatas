# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:53:41 2025

@author: hilar
"""
import tkinter as tk
from tkinter import ttk
import time

class GameOfLife:
    def __init__(self, root, rows=20, cols=20, cell_size=25):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.running = False

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self.canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size, bg="white")
        self.canvas.pack()

        # Dibujar la cuadrícula
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

        # Click para encender/apagar celdas
        self.canvas.bind("<Button-1>", self.toggle_cell)

        # Botones
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        self.start_btn = ttk.Button(frame, text="Iniciar simulación", command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(frame, text="Detener", command=self.stop)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.clear_btn = ttk.Button(frame, text="Limpiar", command=self.clear)
        self.clear_btn.grid(row=0, column=2, padx=5)

    def toggle_cell(self, event):
        if self.running:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.grid[row][col] = 1 - self.grid[row][col]
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("cell")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", tags="cell")

    def start(self):
        if not self.running:
            self.running = True
            self.run()

    def stop(self):
        self.running = False

    def clear(self):
        self.running = False
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def run(self):
        if not self.running:
            return

        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    # Soledad o superpoblación
                    if alive_neighbors <= 1 or alive_neighbors >= 4:
                        new_grid[i][j] = 0
                    elif alive_neighbors in [2, 3]:
                        new_grid[i][j] = 1  # Sobrevive
                else:
                    # Nacimiento
                    if alive_neighbors == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        self.draw_grid()

        # Llamar de nuevo a run después de 300ms
        self.root.after(300, self.run)

    def count_neighbors(self, i, j):
        count = 0
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                ni, nj = i + x, j + y
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    count += self.grid[ni][nj]
        return count


# --- Ejecución principal ---
root = tk.Tk()
root.title("Autómata Celular - Juego de la Vida")
app = GameOfLife(root)
root.mainloop()
