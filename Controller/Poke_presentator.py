from Model.Data_manager import Gestion_Data
from View.pok_GUI_v3_1 import GUI
from Filtre.Filtre_strategy import *

class Control_poke:
    def __init__(self) :  #On indique qu'on veut un paramètre de type filtre
        self.DataBase= Gestion_Data()
        self.data=self.DataBase.get_pokeData()
        self.filtres=self.DataBase.get_data_filtrage()
        
        self.GUI_poke=GUI(self.filtres)
        self.GUI_poke.Frame_affichage.initialisation(self.data.iloc[:, :3])
        self.GUI_poke.Frame_filtrage.set_command(self.cherche_par_nom_nombre)



        self.GUI_poke.letsgoooo()
    

    def cherche_par_nom_nombre(self,nom_numero):
        print("hiiiii")
        filtrage=list(self.filtres[1].items())
        if nom_numero.isdigit():
            Strategie=filtrage[0]
        else:
            Strategie=filtrage[1]
        
        print("ta strategie est",Strategie[0],Strategie[1])  #fonction de strat sur class strat
        strategy=set_strategy(Strategie[0],Strategie[1],True)  #True pour dire qu'on traite les identifiants
        new_data=strategy.application_filtre(Filtre,self.data,nom_numero)

        if new_data is not None:
            principal_info_new_data = new_data.iloc[:, :3]
            self.GUI_poke.Frame_affichage.affichage_resultat_filtrage(principal_info_new_data)
        else:
            print("ups")
            print("your ups:   ", nom_numero)
