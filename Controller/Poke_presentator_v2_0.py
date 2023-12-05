from Model.Data_manager_v2_0 import Gestion_Data
from View.pok_GUI_v3_3 import GUI
from Filtre.Filtre_strategy import *

print("Ok")

class Control_poke:
    def __init__(self,data_direction) :  
        self.DataBase= Gestion_Data(data_direction)
        self.poke_data=self.DataBase.get_poke_data()
        self.filtres_info=self.DataBase.get_poke_filtres_data()
        print("Ok")

        self.GUI_poke=GUI()
        self.initialisation_GUI()
    
    def initialisation_GUI(self):
        self.GUI_poke.filtres_avancee.configuration_initiale(self.filtres_info)
        self.GUI_poke.zone_recherche.configuration_affichage_resultats(list((self.filtres_info[0]).keys())[:4])
        self.GUI_poke.zone_recherche.set_command(self.chercher_data)
        self.GUI_poke.demarage()


    def chercher_data(self,entree,pack_resultats=False):
        print("Je suis Controller et j'ai reçue cette entree:",
              entree)
        Strategies_filtrage=self.filtres_info[0]

        id_nombre=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(True,'Id_Type')]
        id_nom=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(False,'Id_Type')]

        #Si rien écrit encore
        if entree=="Nom ou numéro Pokemon" or entree=="":
            return
        
        if entree.isdigit():
            if len(id_nombre)==1:
                Strategie=id_nombre
        else:
            if len(id_nom)==1:
                Strategie=id_nom

        print("tes strats sont:")
        print("\nfiltre:",Strategie[0][0],
              "\ntest_numerique",Strategie[0][1][0],
              "\nType:",Strategie[0][1][1])

        strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1])
        data_filtree=strategy.application_filtre(Filtre,self.poke_data,entree)
        data_pour_afficher=data_filtree.iloc[:, :4]
                                                            #On utilise la structure d¡une liste car ordre importe
        if pack_resultats:
            self.GUI_poke.zone_recherche.affichage_temps_reel(list(tuple(pokemon) for pokemon in data_pour_afficher.values))
        
        self.GUI_poke.recup_data_apres_filtrage(data_pour_afficher)
