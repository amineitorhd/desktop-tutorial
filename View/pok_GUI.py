import tkinter as tk
from functools import partial

class GUI:
    def __init__(self):
        self.fenetre=tk.Tk()
        self.fenetre.title("Pokedex")

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.fenetre, textvariable=self.entry_var)
        self.entry.pack(pady=10)

        # Botón de búsqueda
        self.search_button = tk.Button(self.fenetre, text="Buscar")
        self.search_button.pack(pady=5)

    def setCommand(self, command):
            # Utilisation de partial pour lier la commande au contrôleur
            self.search_button["command"] = partial(command, self.entry_var.get())

    def resultat_affichage(self,pok_output):
        print("Resultat:")
        for i,Pokemon in pok_output.iterrows():
            print (f'{i}  {Pokemon["Name"]}')

    def lanceur(self):
        self.fenetre.mainloop()