from Model.Data_manager_v2_0 import Gestion_Data
from View.pok_GUI_v3_3 import GUI
from Filtre.Filtre_strategy import *

print("Ok")

class Control_poke:
    def __init__(self,data_direction) :  
        self.DataBase= Gestion_Data(data_direction)
        self.poke_data=self.DataBase.get_poke_data()
        self.filtres_info=self.DataBase.get_poke_filtres_data()
        self.compteur_cartes_pokemons_affiches=30
        self.GUI_poke=GUI()
        self.initialisation_GUI()
    
    def initialisation_GUI(self):
        self.GUI_poke.filtres_avancee.configuration_initiale(self.filtres_info[-2:])
        self.GUI_poke.zone_recherche.configuration_affichage_resultats(self.filtres_info[0])
        self.GUI_poke.zone_recherche.resultats.bind('<Double-1>', self.affichage_info_complete)  # Si double click
        self.GUI_poke.zone_recherche.resultats.bind('<Return>', self.affichage_info_complete)  # Ou si appuie sur enter)
        self.GUI_poke.zone_recherche.set_command(self.chercher_data)
        self.GUI_poke.affichage_cartes_pokemons.initialisation_cartes_pokemons(self.poke_data)
        self.GUI_poke.affichage_cartes_pokemons.bout_set_command(self.affichage_plus)
        self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(self.poke_data.iloc[:self.compteur_cartes_pokemons_affiches, 1],initialisation=True)
        # self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(30)
        # self.GUI_poke.affichage_pokemons.initialisation_cartes_pokemons(self.poke_data)
        
        # self.compteur_pokemons_affiches=30
        # self.GUI_poke.affichage_pokemons.affichage_30pokemon(self.poke_data.head(self.compteur_pokemons_affiches),self.compteur_pokemons_affiches)
        # self.GUI_poke.affichage_pokemons.set_command(self.affichage_plus)
        self.GUI_poke.demarage()

    def affichage_info_complete(self,event):
        for pokemon in self.GUI_poke.zone_recherche.resultats.selection():
            ligne_selection=self.GUI_poke.zone_recherche.resultats.item(pokemon)
            pokemon=self.poke_data[self.poke_data["Name"]== ligne_selection["values"][1]].iloc[0]
            self.GUI_poke.affichage_info_complete_pok(pokemon)




    def affichage_plus(self):
        print("transfer des données à GUI:")
        new_data=self.poke_data.iloc[self.compteur_cartes_pokemons_affiches:self.compteur_cartes_pokemons_affiches+30
                                     , 1]
        self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(new_data)
        self.compteur_cartes_pokemons_affiches+=30

    def chercher_data(self,entree,pack_resultats=False):
        
        Strategies_filtrage=self.filtres_info[1]

        id_nombre=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(True,'Id_Type')]
        id_nom=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(False,'Id_Type')]

        print("\n tes id_nombre sont:",id_nombre)
        print("\n tes id_nom sont:",id_nom)

        #Si rien écrit encore
        if entree=="Nom ou numéro Pokemon" or entree=="":
            return
        
        if entree.isdigit():
            if len(id_nombre)==1:
                Strategie=id_nombre
                strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1])
            else:
                Strategie=list(id_nombre[0])
                strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1])
        else: #('japanese_name', (False, 'Id_Type')) [('Name', (False, 'Id_Type'))]
                                                    #['japanese_name', (False, 'Id_Type')]
            if len(id_nom)==1:
                Strategie=id_nom
                strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1])
            else:
                Strategie=list(id_nom[0])
                strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1])
        print(Strategie)


        data_filtree=strategy.application_filtre(Filtre,self.poke_data,entree)
        data_pour_afficher=data_filtree[self.filtres_info[0]]
                                                            #On utilise la structure d¡une liste car ordre importe
        if pack_resultats:
            self.GUI_poke.zone_recherche.affichage_temps_reel(list(tuple(pokemon) for pokemon in data_pour_afficher.values))
        
        
