import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex Python App")
        self.geometry("1000x600")
        self.minsize(500,300)
        lim=(0,0,2000,6000)
        self.fond_ecran=Fond_Ecran(self,lim,"red")


        self.Menu_filtre=Menu_Filtre(self.fond_ecran)


        self.mainloop()

class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,a,fond="red"):
        super().__init__(mere,bg=fond,scrollregion=a)
        # self.rowconfigure(0,weight=4,uniform="a")
        # self.rowconfigure(1,weight=5,uniform="a")
        # # self.columnconfigure((0,1),weight=1,uniform="a")
        # self.columnconfigure((0,1,2,3),weight=1,uniform="a")
        
        self.pack(expand=True,fill="both")
        self.set_fond_ecran()
        self.bind('<Configure>', self.config_fond_ecran)
        # self.menu=Menu_Filtre(self)
        print("first:",self.winfo_width(),self.winfo_height())
        
        
        self.Affichage_pokemon=Affichage_Pokemon(self)
        print("second:",self.winfo_width(),self.winfo_height())

    def set_fond_ecran(self):
        self.image_fond_ecran=Image.open("View/fond_ecran_pokedex.jpeg")
        self.ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
        image_fond_ecran_tk=ImageTk.PhotoImage(self.image_fond_ecran)

    def config_fond_ecran(self,event):

        largeur=self.winfo_width()
        hauteur=self.winfo_height()

        ecran_ratio=largeur/hauteur

        if self.ratio_image<ecran_ratio:
            x=int(largeur)
            y=int(x/self.ratio_image)
        else:
            y=int(hauteur)
            x=int(y*self.ratio_image)


        updated_ecran=self.image_fond_ecran.resize((x,y))
        self.updated_ecran_tk=ImageTk.PhotoImage(updated_ecran)
        self.create_image(int(largeur/2),
                          int(hauteur/2),
                          image=self.updated_ecran_tk,
                          anchor="center")
        
class Affichage_Pokemon(ttk.Frame):
    def __init__(self,mere):
        super().__init__(mere)
        self.pack(fill="both")
        # canvas=tk.Canvas(self)
        # canvas.pack(side="left",fill="both",expand=1)

        scroll=ttk.Scrollbar(self,orient="vertical",command=mere.yview)
        scroll.pack(side="right",fill="y")

        mere.configure(yscrollcommand=scroll)
        mere.bind("<Configure>",lambda e: mere.configure(scrollregion= mere.bbox("all")))

        deuxieme_frame=ttk.Frame(mere)
        mere.create_window((0,0),window=deuxieme_frame,anchor="nw")

        for chose in range (50):
            Segment_Pokemon_Affichage(deuxieme_frame,None,None,None,None,f"{chose}").grid(row=chose,column=2,pady=10)

    


class Menu_Filtre(ttk.Frame):
    def __init__(self, mere):
        super().__init__(mere)
        # tk.Canvas(self,bg="red").pack(side="top",fill="x")
        self.nom_nombre=tk.StringVar()
        self.entree_nom_nombre=ttk.Entry(self, textvariable=self.nom_nombre, width=30)
        self.entree_nom_nombre.pack(side="top",fill="x",pady=10)
        # self.grid(column=1,row=0,columnspan=2,sticky="nsew")
        self.place(relx=0.2,y=0,relwidth=0.65)

class Segment_Pokemon_Affichage(ttk.Frame):
    def __init__(self,mere,pokemon_nom,pokemon_numero,pokemon_image,pokemon_type,texte,y=int):
        super().__init__(mere)
        style=ttk.Style()
        style.configure('TFrame',background="#ADD8E6")
        
        def shit():

            # self.rowconfigure(0,weight=2,uniform="a")
            # self.rowconfigure(1,weight=1,uniform="a")
            # self.rowconfigure(2,weight=4,uniform="a")
            # self.columnconfigure(0,weight=1,uniform="a")
            # self.columnconfigure(0,weight=4,uniform="a")
            # self.columnconfigure(0,weight=2,uniform="a")

            # Label1=ttk.Label(self,text="1").grid(row=0,rowspan=3,column=0)
            # Label2=ttk.Label(self,text="2").grid(row=0,column=1)
            # Label3=ttk.Label(self,text="3").grid(row=1,column=1)
            # Label4=ttk.Label(self,text="4").grid(row=2,column=2)
            pass
        
        Label1 = ttk.Label(self, text=texte,background="red")
        # Label1.place(relx=0.1, rely=0.1,relheight=0.7,relwidth=0.15)
        Label1.pack(side="left")

        Label2 = ttk.Label(self, text="2")
        # Label2.place(relx=0.5, rely=0.1)
        Label2.pack(side="left")

        Label3 = ttk.Label(self, text="3")
        # Label3.place(relx=0.5, rely=0.5)
        Label3.pack(side="left")

        Label4 = ttk.Label(self, text="4")
        # Label4.place(relx=0.9, rely=0.9)
        Label4.pack(side="left")



Gui=GUI()

