import tkinter as tk
from tkinter import ttk
from functools import partial

class GUI:
    def __init__(self):
        self.fenetre=tk.Tk()
        self.fenetre.title("Pokedex")

         # Cadre principal
        main_frame = ttk.Frame(self.fenetre, padding=(10, 10))
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Entrée de recherche
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(main_frame, textvariable=self.entry_var, width=30)
        self.entry.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        # Bouton de recherche
        self.search_button = ttk.Button(main_frame, text="Rechercher")
        self.search_button.grid(column=2, row=0, padx=10, pady=10)

       # Cadre pour recherche avancée
        self.advanced_frame = ttk.Frame(main_frame)
        self.advanced_frame.grid(column=0, row=1, columnspan=3, pady=10)

        # Bouton pour recherche avancée
        self.advanced_search_button = ttk.Button(self.advanced_frame, text="Recherche avancée", command=self.recherche_avancee)
        self.advanced_search_button.grid(column=0, row=0, columnspan=3, pady=10)

        self.filter_frame_left = ttk.Frame(main_frame)
        self.filter_frame_left.grid(column=0, row=2, pady=10, padx=10)

        self.filter_frame_right = ttk.Frame(main_frame)
        self.filter_frame_right.grid(column=1, row=2, pady=10, padx=10)

        
    def setFiltres(self,liste_filtres):
         self.liste_filtres=liste_filtres

    def setCommand(self, command):
            # Utilisation de partial pour lier la commande au contrôleur
            self.search_button["command"] = lambda: command(self.entry_var.get())

    def resultat_affichage(self,pok_apres_filtrage):
        pass

    def recherche_avancee(self):
        # Supprimer les anciens boutons de filtre
        for widget in self.filter_frame_left.winfo_children():
            widget.destroy()

        for widget in self.filter_frame_right.winfo_children():
            widget.destroy()

        # Diviser la liste de filtres en deux
        middle_index = len(self.liste_filtres) // 2
        left_filters = self.liste_filtres[:middle_index]
        right_filters = self.liste_filtres[middle_index:]

        # Créer un bouton pour chaque filtre dans la première colonne
        for i, filtre in enumerate(left_filters):
            btn = ttk.Button(self.filter_frame_left, text=filtre)
            btn.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

        # Créer un bouton pour chaque filtre dans la deuxième colonne
        for i, filtre in enumerate(right_filters):
            btn = ttk.Button(self.filter_frame_right, text=filtre)
            btn.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)

    def lanceur(self):
        self.fenetre.mainloop()