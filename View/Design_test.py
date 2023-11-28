import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from random import choice

def test1():
    window=tk.Tk()
    window.geometry("1300x1100")
    window.columnconfigure((0,1),weight=1)
    window.rowconfigure((0,1),weight=1)

    image=tk.Canvas(window,background="red")
    image.grid(row=0,column=1,sticky="nsew")
    case=ttk.Frame(image)


    label1=ttk.Label(case,text="asdas")
    label1.place(relx=0.1, rely=0.1,relheight=0.7,relwidth=0.15)
    # label2=ttk.Label(case,text="asdasdsdas")
    # label2.pack()
    case.grid(row=0)


    window.mainloop()
def test2():
        
    window2=tk.Tk()
    window2.geometry("1300x600")
    window2.title("second")

    frame=ttk.Frame(window2)
    frame.pack(fill="both",expand=1)
    ttk.Label(frame,text="hello",background="green").pack()

    canvas=tk.Canvas(frame,bg="red")
    canvas.pack(side="left",fill="both",expand=1)

    scroll=ttk.Scrollbar(frame,orient="vertical",command=canvas.yview)
    scroll.pack(side="right",fill="y")

    canvas.configure(yscrollcommand=scroll)
    canvas.bind("<Configure>",lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

    deuxieme_frame=ttk.Frame(canvas)
    canvas.create_window((0,0),window=deuxieme_frame,anchor="nw")

    for chose in range (100):
        fr=ttk.Frame(deuxieme_frame)
        cv=tk.Canvas(fr,bg="grey")
        cv.pack(fill="both",expand=1)

        label_pokemon_nom=ttk.Label(cv,text=f"Pikachu{chose}")
        label_pokemon_nom.place(relx=0.35,rely=0,relheight=0.3,relwidth=0.4)
        
        label_pokemon_numero=ttk.Label(cv,text=f"#{chose}")
        label_pokemon_numero.place(relx=0.7,rely=0.3,relheight=0.7,relwidth=0.28)
        
        image_pokemon=tk.Canvas(cv,bg="black")
        image_pokemon.place(relx=0,rely=0,relheight=1,relwidth=0.31)
        
        image_type1=tk.Canvas(cv,bg="green")
        image_type1.place(relx=0.35,relwidth=0.1,rely=0.35,relheight=0.1)

        image_type2=tk.Canvas(cv,bg="yellow")
        image_type2.place(relx=0.46,relwidth=0.1,rely=0.35,relheight=0.1)
        
        fr.grid(row=chose,rowspan=1,column=0)



    window2.mainloop()

class Filtres (ttk.Frame):
    def __init__(self,pere,pos_initial,pos_final):
        super().__init__(master=pere)
        self.start=pos_initial+0.04
        self.end=pos_final-0.04
        self.largeur=abs(pos_initial-pos_final)
        
        self.position=pos_initial
        self.home=True

        self.place(relx=self.start,rely=0,relheight=1,relwidth=self.largeur)

    def animation(self):
        if self.home:
            self.animation_palante()
        else:
            self.animation_patras()

    def animation_palante(self):
        if self.position>self.end:
            self.position-=0.008
            self.place(relx=self.position,rely=0,relheight=1,relwidth=self.largeur)
            self.after(10,self.animation_palante)
        else:
            self.home=False

    def animation_patras(self):
        if self.position<self.start:
            self.position+=0.008
            self.place(relx=self.position,rely=0,relheight=1,relwidth=self.largeur)
            self.after(10,self.animation_patras)
        else:
            self.home=True

def mouvement():
    global button_x
    button_x+=0.05
    button.place(relx=button_x,rely=0.5,relheight=button_x,anchor="center")

def infinit():
    global button_x
    print("mouveeeeement")
    button_x+=0.05
    print(button_x)
    if button_x<1:
        window.after(100,infinit)

def combin():
    global button_x
    button_x+=0.01
    button.place(relx=button_x,rely=0.5,relheight=0.5,anchor="center")
    if button_x<0.98:
        window.after(10,combin)


window=tk.Tk()
window.title("filtrageAnimé")
window.geometry("600x400")



filtres=Filtres(window,1.0,0.7)
tk.Canvas(filtres,bg="red").pack(fill="both",expand=1)
button_x=0.5
button=ttk.Button(window,text="vzy",command=filtres.animation)
button.place(relx=button_x,rely=0.5,relheight=0.5,anchor="center")

window.mainloop()