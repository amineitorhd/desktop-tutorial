from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
import ctypes
from View.GUI_recherche import Gestion_Recherche
from View.GUI_filtres_avancee import Gestion_Recherche_avancee

class Fenetre_princiaple:
    def __init__(self,filtres_data):
        self.fenetre=tk.Tk()
        self.fenetre.title("Pokedex")
        self.fenetre.geometry("1000x600")
        self.fenetre.minsize(400,300)
        # self.fenetre.columnconfigure((0,1), weight = 1, uniform = 'a')
        # self.fenetre.rowconfigure((0,1,2,3), weight = 1)
        self.image_test=Image.open("pokedex_background.jpg")
        self.ratio=self.image_test.size[0]/self.image_test.size[1]
        self.image_tk=ImageTk.PhotoImage(self.image_test)

        self.principal_frame=ttk.Frame(self.fenetre)
        self.principal_frame.place(x=0,y=0,relwidth=0.5,relheight=1)
        
        # self.principal_frame.pack_propagate(False)
        # self.principal_frame.grid(column=0,sticky="nw")
        


        self.support_resultat=tk.Canvas(self.fenetre,background="black",bd=0,highlightthickness=0,relief="ridge")
        self.support_resultat.place(relx=0.5,y=0,relwidth=0.5,relheight=1)

        self.support_resultat.columnconfigure((0,1,2,3,4,5,6,7,8,9,10),weight=1,uniform="a")
        self.support_resultat.rowconfigure((0,1,2,3),weight=1,uniform="a")
        # self.support_resultat.grid(column=1,sticky="nw")


        self.support_resultat.bind('<Configure>', self.remplir_image)

        self.Gestion_recherche=Gestion_Recherche(self.principal_frame)
        self.Gestion_Recherche_avancee=Gestion_Recherche_avancee(self.principal_frame,filtres_data)

        self.treeview_resultat = ttk.Treeview(self.support_resultat,show='headings')
        self.treeview_resultat.grid(column=2,columnspan=6,row=1,rowspan=2)


    def remplir_image(self,event):
        global resized_tk
        
        largeur=event.width
        hauteur=event.height
        resized_image=self.image_test.resize((largeur,hauteur))
        resized_tk=ImageTk.PhotoImage(resized_image)
        self.support_resultat.create_image(0,0,image=resized_tk,anchor="nw")
        
        
        
        # current ratio 
        print("okk")
        # canvas_ratio = event.width / event.height

        # # get coordinates 
        # if canvas_ratio < self.ratio: # canvas is wider than the image
        #     hauteur = int(event.height)
        #     largeur = int(hauteur * self.ratio) 
        # else: # canvas is narrower than the image
        #     largeur = int(event.width) 
        #     hauteur = int(largeur / self.ratio)



        # self.resized_image = self.image_test.resize((largeur, hauteur))
        # resized_tk = ImageTk.PhotoImage(self.resized_image)
        # self.support_resultat.create_image(
        #     int(event.width / 2),
        #     int(event.height / 2),
        #     anchor = 'center',
        #     image = resized_tk)
        
    
    def affiche_resultat(self, data):
        colonnes=data.columns
        self.treeview_resultat["columns"] = tuple(colonnes)

        for col in colonnes:
            self.treeview_resultat.heading(col, text=col)
            self.treeview_resultat.column(col, anchor=tk.CENTER, width=100)  # Ajustez la largeur selon vos besoins
        # Efface toutes les lignes existantes dans le Treeview
        print("Je suis GUI et je connais le résultat:::::   ",data)
        for row in self.treeview_resultat.get_children():
            self.treeview_resultat.delete(row)

        # Insère les nouvelles données dans le Treeview
        for index, row_data in data.iterrows():
            self.treeview_resultat.insert("", "end", values=tuple(row_data))
    
    def lanceur(self):
        self.fenetre.mainloop()

