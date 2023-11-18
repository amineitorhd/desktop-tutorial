from Model.Data_manager import Gestion_Data
from View.pok_GUI import GUI
from Filtre.Filtre_strategy import Filtre

class Control_poke:
    def __init__(self,strategie_filtrage:Filtre) :  #On indique qu'on veut un paramètre de type filtre
        self.chercheur_data= Gestion_Data()
        self.affichage_data=GUI()
        self.filtrage=strategie_filtrage
    
    def set_strategie_filtrage(self, strategie_filtrage:Filtre):
        self.filtrage=strategie_filtrage
    
    def application_filtre(self,filtrage):
        data=self.chercheur_data.get_pokeData()
        result_filtre=self.filtrage.application_filtre(data,filtrage)
        print(result_filtre)
        self.affichage_data.resultat_affichage(result_filtre)
