import tkinter as tk
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk

class Fenetre_princiaple:
    def __init__(self,filtres):
        self.fenetre=tk.Tk()
        self.fenetre.title("Pokedex")
        self.fenetre.geometry("800x600")

        # Charger l'image de fond
        image_fond = Image.open("image.png")  # Remplacez "image.png" par le chemin de votre image
        image_fond = image_fond.resize((800, 600))
        self.image_fond = ImageTk.PhotoImage(image_fond)

        self.principal_frame = ttk.Frame(self.fenetre)
        self.principal_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Afficher l'image de fond dans un Label
        lbl = tk.Label(self.principal_frame, image=self.image_fond)
        lbl.image = self.image_fond  # Garder une référence pour éviter la collecte des déchets
        lbl.place(relx=0.5, rely=0.5, anchor='center')

        self.Gestion_recherche=Gestion_recherche(self.principal_frame)
        self.Gestion_Recherche_avancee=Gestion_Recherche_avancee(self.principal_frame,filtres)

    def lanceur(self):
        self.fenetre.mainloop()

class Gestion_recherche:
    def __init__(self,frame_pere):
        self.frame_pere=frame_pere

        self.nom_nombre=tk.StringVar()
        self.entree_nom_nombre=ttk.Entry(self.frame_pere, textvariable=self.nom_nombre, width=30)
        self.entree_nom_nombre.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        # Ajouter le texte initial dans l'entry
        self.entree_nom_nombre.insert(0, "Nom ou numéro Pokemon")

        # Liaison d'événement pour effacer le texte initial lorsqu'un clic est effectué sur l'entry
        self.entree_nom_nombre.bind("<FocusIn>", self.clear_placeholder_text)
        # Liaison d'événement pour restaurer le texte initial s'il n'y a pas de texte entré
        self.entree_nom_nombre.bind("<FocusOut>", self.restore_placeholder_text)

        self.boutton_recherche=ttk.Button(self.frame_pere, text="Rechercher")
        self.boutton_recherche.grid(column=2, row=0, padx=10, pady=10)
    
    def clear_placeholder_text(self, event):
        # Efface le texte initial lorsque l'utilisateur clique dans l'entry
        if self.nom_nombre.get() == "Nom ou numéro Pokemon":
            self.nom_nombre.set("")

        # Change la couleur du texte à noir lorsque l'utilisateur commence à taper
        self.entree_nom_nombre.config(foreground="black")

    def restore_placeholder_text(self, event):
        # Restaure le texte initial si l'entry est vide
        if not self.nom_nombre.get():
            self.nom_nombre.set("Nom ou numéro Pokemon")

            # Change la couleur du texte à gris si l'entry est vide
            self.entree_nom_nombre.config(foreground="grey")


    def set_command(self, command):
        self.boutton_recherche["command"] = lambda: command(self.entree_nom_nombre.get())

class Gestion_Recherche_avancee:
    def __init__(self, frame_pere,filtres):
        self.frame_pere = frame_pere
        self.liste_filtres=filtres
        self.frame_recherche_avancee = ttk.Frame(self.frame_pere)
        self.frame_recherche_avancee.grid(column=0, row=1, columnspan=3, pady=10)

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
            self.Gestion_filtres.affiche_filtre_avancee(self.liste_filtres)
            self.cadre_filtres_visible = True

class Gestion_Filtres_avancee:
    def __init__(self,frame_pere):
        self.frame_pere=frame_pere
        self.frame_filtres_gauche = None
        self.frame_filtres_droite = None

    def affiche_filtre_avancee(self,filtres):
        self.cacher_filtre_avancee()

        milieu = len(filtres) // 2
        filtres_gauche = filtres[:milieu]
        filtres_droite = filtres[milieu:]

        self.frame_filtres_gauche = ttk.Frame(self.frame_pere)
        self.frame_filtres_gauche.grid(column=0, row=2, pady=10, padx=10)

        for i, filtre in enumerate(filtres_gauche):
            boutton_filtre = ttk.Button(self.frame_filtres_gauche, text=filtre)
            boutton_filtre.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

        self.frame_filtres_droite = ttk.Frame(self.frame_pere)
        self.frame_filtres_droite.grid(column=1, row=2, pady=10, padx=10)

        for i, filtre in enumerate(filtres_droite):
            boutton_filtre= ttk.Button(self.frame_filtres_droite, text=filtre)
            boutton_filtre.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

    def cacher_filtre_avancee(self):
        if self.frame_filtres_gauche is not None:
            self.frame_filtres_gauche.grid_forget()

        if self.frame_filtres_droite is not None:
            self.frame_filtres_droite.grid_forget()





