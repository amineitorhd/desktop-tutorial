from tkinter import ttk
import tkinter as tk

class Gestion_Recherche:
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