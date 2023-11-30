from Model.Data_manager import Gestion_Data
from View.pok_GUI_v3_1 import GUI
from Filtre.Filtre_strategy import *
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time


class Control_poke:
    def __init__(self) :  #On indique qu'on veut un paramètre de type filtre
        self.DataBase= Gestion_Data()
        self.data=self.DataBase.get_pokeData()
        self.filtres_info=self.DataBase.get_data_filtrage()
        self.filtres=self.filtres_info[0]

        self.GUI_poke=GUI()
        self.GUI_poke.withdraw()


        self.fenetre_chargement=tk.Toplevel(self.GUI_poke)
        self.fenetre_chargement.geometry("200x200")
        message_chargement=tk.Label(self.fenetre_chargement,text="Chargement[*******]").pack()

        threading.Thread(target=self.init_GUI).start()

        self.GUI_poke.letsgoooo()

    def init_GUI(self):
        self.GUI_poke.Frame_affichage.initialisation(self.data.iloc[:, :3])
        self.GUI_poke.Frame_filtrage.set_command(self.cherche_par_nom_nombre)
        self.GUI_poke.configuration_filtres(self.filtres)
        time.sleep(3)
        self.fenetre_chargement.destroy()
        self.GUI_poke.deiconify()  # Muestra la ventana principal


    def cherche_par_nom_nombre(self,nom_numero):
        if nom_numero=="Nom ou numéro Pokemon":
            return

        filtrage=list(self.filtres.items())
        
        if nom_numero.isdigit():
            Strategie=filtrage[0]
        else:
            Strategie=filtrage[1]
        
        print("ta strategie est",Strategie[0],Strategie[1][0])  #fonction de strat sur class strat
        print(f"Ta strategie est caractérisé par: {Strategie[1][1]} et c'est un {type(Strategie[1][1])}")
        strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1])  #True pour dire qu'on traite les identifiants
        new_data=strategy.application_filtre(Filtre,self.data,nom_numero)

        if new_data is not None:
            principal_info_new_data = new_data.iloc[:, :3]
            self.GUI_poke.Frame_affichage.affichage_resultat_filtrage(principal_info_new_data)
        else:
            print("ups")
            print("your ups:   ", nom_numero)
