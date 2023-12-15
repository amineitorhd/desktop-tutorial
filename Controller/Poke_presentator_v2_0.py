from Model.Data_manager_v2_0 import Gestion_Data
from View.pok_GUI_v3_3 import GUI
from Filtre.Filtre_strategy import *


class Control_poke:
    def __init__(self,data_direction) :  
        self.DataBase= Gestion_Data(data_direction)
        self.filtres_info=self.DataBase.get_poke_filtres_data()
        self.poke_data=self.DataBase.get_poke_data()
        # print(self.poke_data.head(5))
        self.arbre_poke_noeuds=self.DataBase.reorganiser_colonnes()
        self.poke_data=self.DataBase.get_poke_data()
        # print(self.poke_data.head(5))

        self.poke_media=self.DataBase.get_poke_media()
        self.compteur_cartes_pokemons_affiches=30
        self.GUI_poke=GUI()

        
        self.initialisation_GUI()

    def ordre(self,filtre_ordre):
        if filtre_ordre!="":
            print("Je suis controller, filtre à ordonnée:",filtre_ordre)
    
    
    def initialisation_GUI(self):
        self.GUI_poke.filtres_avancee.configuration_initiale(self.filtres_info[1],self.filtres_info[2])
        self.GUI_poke.filtres_avancee.set_command(self.chercher_data_filtre)
        self.GUI_poke.filtres_avancee.bout_reset_set_command(self.reset_affichage)
        
        self.GUI_poke.zone_recherche.configuration_box_ordre(self.filtres_info[1])
        self.GUI_poke.zone_recherche.configuration_affichage_resultats(self.filtres_info[0])
        self.GUI_poke.zone_recherche.resultats.bind('<Double-1>', self.affichage_info_complete)  # Si double click
        self.GUI_poke.zone_recherche.resultats.bind('<Return>', self.affichage_info_complete)  # Ou si appuie sur enter)
        self.GUI_poke.zone_recherche.set_command(command_boutton_recherche=self.chercher_data,
                                                 command_boutton_ordre=self.ordre)
        self.GUI_poke.affichage_cartes_pokemons.initialisation_cartes_pokemons(self.poke_data,self.poke_media[0])
        self.GUI_poke.affichage_cartes_pokemons.bout_set_command(self.affichage_plus)
        self.GUI_poke.affichage_cartes_pokemons.set_command_poke_affichage(self.affichage_info_complete)
        self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(self.poke_data.iloc[:self.compteur_cartes_pokemons_affiches, 1],initialisation=True)
        # self.GUI_poke.affichage_cartes_pokemons.affichage_poke_liste(30)
        # self.GUI_poke.affichage_pokemons.initialisation_cartes_pokemons(self.poke_data)
        
        # self.compteur_pokemons_affiches=30
        # self.GUI_poke.affichage_pokemons.affichage_30pokemon(self.poke_data.head(self.compteur_pokemons_affiches),self.compteur_pokemons_affiches)
        # self.GUI_poke.affichage_pokemons.set_command(self.affichage_plus)
        self.GUI_poke.demarage()


    def affichage_info_complete(self,event,pokemon_carte=None):
        # fct pr creer infos pkm
        def creer_info_pkm(nom, donnees):
            if nom is not None:
                dir_gif = self.poke_media[1].get(nom, "View/error.gif")
                dir_img = self.poke_media[0].get(nom, "View/error.gif")
            else:
                dir_gif=dir_img=None
            return (nom, donnees, dir_gif, dir_img)
        
        # lst pr stocker infos pkm
        infos_pkm = []
        # obtenir idx des pkm sel ou pkm spec
        idxs = [0] if pokemon_carte else self.GUI_poke.zone_recherche.resultats.selection()
        
        # boucle pr traiter chq pkm
        for idx in idxs:
            if pokemon_carte:
                nom_pkm = pokemon_carte
            else:
                # obtenir ligne sel ds resultats recherche
                ligne_sel = self.GUI_poke.zone_recherche.resultats.item(idx)
                nom_pkm = ligne_sel["values"][1]
            
            # obtenir donnees pkm actuel
            donnees_pkm = self.poke_data.loc[self.poke_data.iloc[:, 1] == nom_pkm]
            idx_pkm = donnees_pkm.index[0]
            # ajouter infos pkm actuel
            infos_pkm.append(creer_info_pkm(nom_pkm, donnees_pkm))
            
            # traiter pkm prec et suiv
            for decalage in [-1, 1]:
                idx_voisin = idx_pkm + decalage
                if 0 <= idx_voisin < len(self.poke_data):
                    nom_voisin = self.poke_data.iloc[idx_voisin, 1]
                    donnees_voisin = self.poke_data.iloc[idx_voisin]
                    # ajouter infos pkm voisin
                    infos_pkm.append(creer_info_pkm(nom_voisin, donnees_voisin))
                else:
                # ajouter pas de pkm voisin
                    infos_pkm.append((None, None, None, None))

        # afficher infos pkm
        print(infos_pkm[0][0],infos_pkm[1][0],infos_pkm[2][0])
        # maj affichage avc infos compl pkm
        self.GUI_poke.affichage_info_complete_pok(infos_pkm)



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
                strategy=set_strategy(Strategie[0][0],Strategie[0][1][0],Strategie[0][1][1],trie=self.arbre_poke_noeuds)
            else:
                Strategie=list(id_nom[0])
                strategy=set_strategy(Strategie[0],Strategie[1][0],Strategie[1][1],trie=self.arbre_poke_noeuds)

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

        
    def chercher_data_filtre(self):  #hacer un excepcion si no hay filtros???
        print(self.GUI_poke.filtres_avancee.selections_filtres)
        self.poke_data=self.DataBase.get_poke_data()
        filtres_selectionnes=[]
        print("Controller application des filtres....")
        filtres_batailles=self.GUI_poke.filtres_avancee.dico_scales.items()
        filtres_categories=self.GUI_poke.filtres_avancee.bouttons_choisi
        for cle,valeur in filtres_batailles:
            # print(cle,valeur[0],valeur[1],type(valeur[0]))
            if not (valeur[0]==None and valeur[1]==None):
                filtres_selectionnes.append((cle,self.filtres_info[1][cle],valeur[0],valeur[1]))
        if len(filtres_categories)==2:
            filtre1=filtres_categories[0]
            filtre2=filtres_categories[1]
            print(filtre1[1],self.filtres_info[1][filtre1[1]],filtre1[0])
            print(filtre2[1],self.filtres_info[1][filtre2[1]],filtre2[0])

        # print("Filtres selectionnees:",filtres_selectionnes)

        for index,Filtre in enumerate(filtres_selectionnes):
            filtre, (test_num, type_filtre), valeur_min, valeur_max=Filtre
            strategie = set_strategy(filtre, test_num, type_filtre, strategie="Recherche_plage_de_valeurs")
            # print(filtre, (test_num, type_filtre), valeur_min, valeur_max)
            if index==0:
                print("initialisation_premiere plage")
                self.poke_data_filtree=strategie.application_filtre(strategie, self.poke_data, (valeur_min, valeur_max))
            # Aplicar el primer filtro a self.poke_data
            else:
                print(index)
                self.poke_data_filtree = strategie.application_filtre(strategie, self.poke_data_filtree, (valeur_min, valeur_max))
        
        print(self.poke_data_filtree)
        