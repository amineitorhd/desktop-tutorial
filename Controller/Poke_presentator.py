from Model.Data_manager import Gestion_Data
from View.pok_GUI import GUI

class Control_poke:
    def __init__(self) :
        self.chercheur_data= Gestion_Data()
        self.affichage_data=GUI()
    
    def filtre_type(self,poke_type):
        result_filtre=self.chercheur_data.filtre_type(poke_type)
        self.affichage_data.resultat_affichage(result_filtre)
