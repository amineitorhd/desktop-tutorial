import tkinter as tk

class GUI:
    def __init__(self):
        pass

    def resultat_affichage(self,pok_output):
        print("Resultat:")
        for i,Pokemon in pok_output.iterrows():
            print (f'{i}  {Pokemon["Name"]}')