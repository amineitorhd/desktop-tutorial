import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from random import choice




class DoubleSlider(tk.Canvas):
    def __init__(self, master=None, min_val=0, max_val=160, **kwargs):
        super().__init__(master, bg="#2992B0", **kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.first_thumb_val = min_val  # Valor del pulgar azul
        self.second_thumb_val = max_val  # Valor del pulgar rojo

        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)

        # Crear elementos de texto para los valores mínimo y máximo
        self.canvas_max=tk.Canvas(self,bg="red")
        self.canvas_max.place(relx=0.6,rely=0.3,relwidth=0.2,relheight=0.1)
        self.canvas_min=tk.Canvas(self,bg="blue")
        self.canvas_min.place(relx=0.05,rely=0.3,relwidth=0.2,relheight=0.1)
        self.text_min = self.create_text(50, 20, text=str(self.min_val), anchor="w", fill="white")
        self.text_max = self.create_text(0, 0, text=str(self.max_val), anchor="e", fill="white")

        self.dessin_slider(500,100)

    def dessin_slider(self, largeur_relative, hauteur_relative):
        self.width = largeur_relative  # Ancho solicitado del Canvas
        self.height = hauteur_relative  # Altura solicitada del Canvas

        self.margin = 20  # Margen para los pulgares
        self.line_y = self.height // 2  # Posición y para la línea

        self.delete("all")
        self.create_line(self.margin, self.line_y, self.width - self.margin, self.line_y, fill="lightgray", width=10)
        self.first_thumb = self.create_oval(self.margin - 10, self.line_y - 5, self.margin + 10, self.line_y + 5, fill="blue", outline="blue", tags="thumb")
        self.second_thumb = self.create_oval(self.width - self.margin - 10, self.line_y - 5, self.width - self.margin + 10, self.line_y + 5, fill="red", outline="red", tags="thumb")

        # Actualizar la posición de los elementos de texto
        self.coords(self.text_min, self.margin, self.line_y - 20)
        self.coords(self.text_max, self.width - self.margin, self.line_y - 20)

    def click(self, event):
        closest = self.find_closest(event.x, event.y)[0]
        if closest == self.first_thumb:
            self.active_thumb = self.first_thumb
        elif closest == self.second_thumb:
            self.active_thumb = self.second_thumb

    def drag(self, event):
        if hasattr(self, 'active_thumb'):
            x = min(max(event.x, self.margin), self.width - self.margin)
            val = int(((x - self.margin) / (self.width - 2 * self.margin)) * (self.max_val - self.min_val) + self.min_val)
            if self.active_thumb == self.first_thumb:
                if val <= self.second_thumb_val:  # Condición para el pulgar azul
                    self.first_thumb_val = val
                    self.coords(self.active_thumb, x - 10, self.line_y - 5, x + 10, self.line_y + 5)
                    self.itemconfig(self.text_min, text=str(val))  # Actualizar texto del valor mínimo
                    print(str(val))
            else:
                if val >= self.first_thumb_val:  # Condición para el pulgar rojo
                    self.second_thumb_val = val
                    self.coords(self.active_thumb, x - 10, self.line_y - 5, x + 10, self.line_y + 5)
                    self.itemconfig(self.text_max, text=str(val))  # Actualizar texto del valor máximo
                    print(str(val))
window=tk.Tk()
window.title("filtrageAnimé")
window.geometry("600x400")
DoubleSlider(window).place(relx=0,rely=0.2,relwidth=1)

window.mainloop()