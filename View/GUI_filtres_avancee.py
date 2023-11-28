from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

class Gestion_Recherche_avancee:
    def __init__(self, frame_pere,filtres_data):
        self.frame_pere = frame_pere
        self.filtres_data=filtres_data
        
        image_fond=Image.open("View\image_recherche_avancee.jpg")
        self.image_fond=ImageTk.PhotoImage(image_fond)
        self.frame_recherche_avancee = ttk.Frame(self.frame_pere)
        self.frame_recherche_avancee.grid(column=0, row=1, columnspan=3, pady=10)
        
        lbl=tk.Label(self.frame_recherche_avancee,image=self.image_fond)
        lbl.image=self.image_fond
        lbl.place(relx=0.5,rely=0.5,anchor='center')

        self.recherche_avancee_button = ttk.Button(self.frame_recherche_avancee, 
                                                   text="Recherche avancée", 
                                                   command=self.affichage_recherche_avancee)
        
        self.recherche_avancee_button.grid(column=0, row=0, columnspan=3, pady=10)
        self.cadre_filtres_visible = False

        self.Gestion_filtres = Gestion_Filtres_avancee(self.frame_pere)

    def affichage_recherche_avancee(self):
        if self.cadre_filtres_visible:
            self.Gestion_filtres.cacher_filtre_avancee()
            self.cadre_filtres_visible = False
        else:
            self.Gestion_filtres.affiche_filtre_avancee(self.filtres_data)
            self.cadre_filtres_visible = True

class Gestion_Filtres_avancee:
    def __init__(self, frame_pere):
        self.frame_pere = frame_pere
        self.frame_filtres = None
        self.entries = {}

    def affiche_filtre_avancee(self, filtres):
        self.cacher_filtre_avancee()

        image_fond = Image.open("View/image_recherche_avancee.jpg")
        image_fond = ImageTk.PhotoImage(image_fond)
        self.frame_filtres = ttk.Frame(self.frame_pere)
        
        lbl = tk.Label(self.frame_filtres, image=image_fond)
        lbl.image = image_fond
        lbl.place(relx=0.5, rely=0.5, anchor='center')
        
        self.frame_filtres.grid(column=0, row=2, pady=10, padx=10)

# Afficher les Entry pour chaque type
        for i, filtre in enumerate(filtres[1]):
            row = i // 2
            col = i % 2

            if not (filtres[1][filtre][1]):
                print("ton filtre ",filtre,"peut etre en echelle!!!")

            label = ttk.Label(self.frame_filtres, text=filtre)
            label.grid(row=row, column=col * 2, padx=5, pady=5, sticky=tk.W)

            entry_var = tk.StringVar()
            entry = ttk.Entry(self.frame_filtres, textvariable=entry_var, width=8)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5, sticky=tk.W)

            # Stocker la référence à l'Entry dans le dictionnaire
            self.entries[filtre] = entry_var


    def cacher_filtre_avancee(self):
        if self.frame_filtres is not None:
            self.frame_filtres.grid_forget()