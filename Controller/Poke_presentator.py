from Model.Data_manager import Gestion_Data
from View.pok_GUI import Fenetre_princiaple
from Filtre.Filtre_strategy import *

class Control_poke:
    def __init__(self) :  #On indique qu'on veut un paramètre de type filtre
        self.DataBase= Gestion_Data()
        self.data=self.DataBase.get_pokeData()
        self.filtres=self.DataBase.get_data_filtrage()
        liste_filtres_fonction=[]
        liste_filtres=[]
        for filtre in self.filtres:
            liste_filtres_fonction.append(filtre+'()')
            liste_filtres.append(filtre)
        


        self.GUI=Fenetre_princiaple(liste_filtres)
        self.GUI.Gestion_recherche.set_command(self.cherche_par_nom_nombre)
        # self.GUI.setFiltres(liste_filtres)
        
        self.GUI.lanceur()

        



    def set_strategie_filtrage(self, strategie_filtrage:Filtre):
        resultat=strategie_filtrage.application_filtre(self.data)
        print(resultat)

    
    def cherche_par_nom_nombre(self,nom_numero):
        if nom_numero.isdigit():
            new_data=Number.application_filtre(Filtre,self.data,nom_numero)
        else:
            new_data=Name.application_filtre(Filtre,self.data,nom_numero)

        if new_data.empty:
            print("ups")
        else:
            print(new_data)



        #     def cherche_par_filtre(self,nom_numero):
        # new_data=Number.application_filtre(Filtre,self.data,nom_numero)
        # print(new_data)