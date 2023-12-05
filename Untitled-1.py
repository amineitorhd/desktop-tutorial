import tkinter as tk
from tkinter import ttk

class Frame_personalizado(ttk.Frame):
    def __init__(self, parent=None, width=100, height=100, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        
        self['borderwidth'] = 2
        self['relief'] = 'groove'
        
        self.label_nombre = ttk.Label(self, text="0001 Bulbasaur")
        self.label_nombre.pack()
        
        self.canvas = tk.Canvas(self, width=width, height=height, bg='blue')
        self.canvas.pack()
        
        self.label_tipo = ttk.Label(self, text="Grass\nPoison")
        self.label_tipo.pack()

root = tk.Tk()
  # Establece el tamaño mínimo de la ventana
cv = tk.Canvas(root, bg="magenta")
cv.pack(fill="both", expand=1)

frames=[]
for i in range(5):
    for j in range(2):
        frame = Frame_personalizado(cv, width=300, height=300)
        frame.place(x=j*360, y=i*500)
        frames.append(frame)

def deplacement():
    frames[3].pack(side="right")

www=ttk.Frame(cv)
lab=tk.Canvas(www,bg="blue",width=200,height=200).pack(side="left")
lab2=tk.Canvas(www,bg="yellow",width=200,height=200).pack(side="right",padx=100)
www.pack(side="right")
ttk.Button(cv,text="waow",command=deplacement).pack()




root.mainloop()

if 5 !=None:
    print("ok")




