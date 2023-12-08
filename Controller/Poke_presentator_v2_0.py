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
        
        self.test=True
        self.GUI_poke.sort_command(self.ordre)
        
        self.initialisation_GUI()

    def ordre(self):
        strat=set_strategy("#",True,"Id_Type",strategie="Ordre")
        result=strat.application_filtre(strat,self.poke_data,self.test)
        print(result)
        self.test=False
    def initialisation_GUI(self):
        self.GUI_poke.filtres_avancee.configuration_initiale(self.filtres_info[-2:])
        self.GUI_poke.filtres_avancee.set_command(self.chercher_data_filtre)
        self.GUI_poke.filtres_avancee.bout_reset_set_command(self.reset_affichage)
        
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
        print(self.GUI_poke.zone_recherche.resultats.selection())
        for pokemon in self.GUI_poke.zone_recherche.resultats.selection():
            ligne_selection=self.GUI_poke.zone_recherche.resultats.item(pokemon)
            pokemon=self.poke_data[self.poke_data["Name"]== ligne_selection["values"][1]].iloc[0]
            self.GUI_poke.affichage_info_complete_pok(pokemon)




    def affichage_plus(self,affichage_par_30):
        print("transfer des données à GUI:")
        if affichage_par_30:
            new_data=self.poke_data.iloc[self.compteur_cartes_pokemons_affiches:self.compteur_cartes_pokemons_affiches+30
                                         , 1]
            
            self.compteur_cartes_pokemons_affiches+=30
        else:
            print("affichage par 30 non disponible")
        self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(new_data)

    def reset_affichage(self):
        for cartes_affiches in self.GUI_poke.affichage_cartes_pokemons.poke_cartes_affichees:
            cartes_affiches.pack_forget()
        self.GUI_poke.affichage_cartes_pokemons.poke_cartes_affichees.clear()
        self.compteur_cartes_pokemons_affiches=30
        self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(self.poke_data.iloc[:self.compteur_cartes_pokemons_affiches,1],True)
        self.GUI_poke.affichage_cartes_pokemons.affichage_par30=True
        self.GUI_poke.affichage_cartes_pokemons.configuration_affichage(None)

    def chercher_data(self,entree,pack_resultats=False):
        
        Strategies_filtrage=self.filtres_info[1]  #On recupere les filtres avec leurs types
                                                        #Exemple : {'#': (True, 'Id_Type'), 
                                                        # 'Name': (False, 'Id_Type'), 
                                                        # 'Type_1': (False, 'Categorique_Type'),

        #Avec la base de données du prof c'est pas trop utile ça.
        #Mais dans dautres dataframe il ya plusuieurs identifiants (exemple:nom en japonais)
        # Alors dans deux listes je mets tous les filtres identifiants (un pour numérique et autre pour str)
        id_nombre=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(True,'Id_Type')]
        id_nom=[(filtre,info_filtre) for filtre,info_filtre in Strategies_filtrage.items() if info_filtre==(False,'Id_Type')]

        #Si rien écrit encore
        if entree=="Nom ou numéro Pokemon" or entree=="":
            return
        
        if entree.isdigit():
            if len(id_nombre)==1:
                Strategie=id_nombre
                strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1])
                        #EXEMPLE:    (  "Name"     ,numerique ou pas:"True"  ,       "Id_type" )
                        #Cette methode nous retourne une classe, stocké dans la variable strategy
            else:
                Strategie=list(id_nombre[0])
                strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1])
        else: 
            if len(id_nom)==1:
                Strategie=id_nom
                strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1])
            else:
                Strategie=list(id_nom[0])
                strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1])

        #Comme strategy c'est une classe
            #On accède à la fonction aaplication_filtre() qui nous retourne les données filtrés
        data_filtree=strategy.application_filtre(strategy,self.poke_data,entree)
        data_pour_afficher=data_filtree[self.filtres_info[0]]
                                                            #On utilise la structure d¡une liste car ordre important
        if pack_resultats:
            print("Affichage des frames:")
            poke_nom=[pokemon[1] for pokemon in data_pour_afficher.values]
            self.GUI_poke.affichage_cartes_pokemons.nb_poke_resultats=len(poke_nom)
            self.GUI_poke.affichage_cartes_pokemons.affichage_par30=False
            self.GUI_poke.affichage_cartes_pokemons.configuration_affichage(None)
            self.GUI_poke.affichage_cartes_pokemons.affichage_poke_specifique(poke_nom)
        else:
            self.GUI_poke.zone_recherche.affichage_temps_reel(list(tuple(pokemon) for pokemon in data_pour_afficher.values))

        
    def chercher_data_filtre(self):
        self.poke_data=self.DataBase.get_poke_data()
        filtres_selectionnes=[]
        print("Controller application des filtres....")
        for cle,valeur in self.GUI_poke.filtres_avancee.dico_scales.items():
            print(cle,valeur[0],valeur[1],type(valeur[0]))
            if not (valeur[0]==None and valeur[1]==None):
                filtres_selectionnes.append((cle,self.filtres_info[1][cle],valeur[0],valeur[1]))
        print("Filtres selectionnees:",filtres_selectionnes)

        for filtre, (test_num, type_filtre), valeur_min, valeur_max in filtres_selectionnes:
            strategie = set_strategy(filtre, test_num, type_filtre, strategie="Recherche_plage_de_valeurs")
            print(filtre, (test_num, type_filtre), valeur_min, valeur_max)

            # Aplicar el primer filtro a self.poke_data
            self.poke_data = strategie.application_filtre(strategie, self.poke_data, (valeur_min, valeur_max))
        
        print(self.poke_data)
        