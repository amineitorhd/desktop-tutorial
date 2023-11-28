from tkinter import ttk
import tkinter as tk
from functools import partial
from PIL import Image, ImageTk
import ctypes


class Fenetre_princiaple:
    def __init__(self,filtres_data):
        self.fenetre=tk.Tk()
        self.fenetre.title("Pokedex")
        self.fenetre.geometry("1000x600")
        self.definir_fond_ecran()


        # Charger l'image de fond
        image_fond = Image.open("pokedex_background.jpg")  # Remplacez "image.png" par le chemin de votre image
        image_fond = image_fond.resize((1000, 2000))
        self.image_fond = ImageTk.PhotoImage(image_fond)
#######################################################################################################
#demander pourquoi quand il ya un frame très difficile de mettre image de fond '''
        self.principal_frame = ttk.Frame(self.fenetre,width=1000, height=1800)
        self.principal_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Afficher l'image de fond dans un Label
        lbl = tk.Label(self.principal_frame, image=self.image_fond)
        lbl.image = self.image_fond  # Garder une référence pour éviter la collecte des déchets
        lbl.place(relx=0.5, rely=0.5, anchor='center')

        self.Gestion_recherche=Gestion_recherche(self.principal_frame)
        self.Gestion_Recherche_avancee=Gestion_Recherche_avancee(self.principal_frame,filtres_data)

        self.treeview_resultat = ttk.Treeview(self.principal_frame)
        self.treeview_resultat.grid(column=3, row=0, padx=10, pady=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    def definir_fond_ecran(self):
        # Charger l'image de fond pour le fond d'écran
        image_fond_ecran = Image.open("pokedex_background.jpg")
        image_fond_ecran = image_fond_ecran.resize((ctypes.windll.user32.GetSystemMetrics(0),
                                                     ctypes.windll.user32.GetSystemMetrics(1)))
        photo = ImageTk.PhotoImage(image_fond_ecran)

        # Créer un Canvas qui couvre toute la fenêtre pour afficher l'image en fond
        canvas = tk.Canvas(self.fenetre, width=ctypes.windll.user32.GetSystemMetrics(0),
                           height=ctypes.windll.user32.GetSystemMetrics(1),background="lightblue")
        canvas.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Afficher l'image en tant que fond d'écran
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # Garder une référence pour éviter la collecte des déchets

    
    
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






