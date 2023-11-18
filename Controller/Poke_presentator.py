from Model.Data_manager import Gestion_Data
from View.pok_GUI import GUI
from Filtre.Filtre_strategy import Filtre

class Control_poke:
    def __init__(self) :  #On indique qu'on veut un paramètre de type filtre
        self.DataBase= Gestion_Data()
        self.data=self.DataBase.get_pokeData()

        self.affichage_data=GUI()
        self.affichage_data.setCommand(self.cherche_par_filtre)
        self.affichage_data.lanceur()

        self.filtres=self.DataBase.get_data_filtrage()
        liste_filtres=[]
        for filtre in self.filtres:
            liste_filtres.append(filtre+'()')

    def set_strategie_filtrage(self, strategie_filtrage:Filtre):
        self.filtrage=strategie_filtrage

    
    def cherche_par_filtre(self,filtre):
        print("ok",filtre)
        # result_filtre=self.filtrage.application_filtre(data,filtre)
        # print(result_filtre)
        # self.affichage_data.resultat_affichage(result_filtre)
