import pandas as pd
import numpy as np
from numpy.random import default_rng
import os,re




class Gestion_Data:
    def __init__(self,poke_data_direction):
        self.data=poke_data_direction
        self.poke_data=pd.read_csv(poke_data_direction)
                # Inicializar el diccionario para almacenar las rutas relativas de los GIFs
        self.dico_direction_gif = {}
        self.dico_direction_images={}



    def get_poke_data(self):
        return self.poke_data
    
    def get_poke_filtres_data(self):
        Filtres_valeurs_possibles = {} #Diccionaires contenant les valeurs possibles (uniques)
        type_filtres = {} #Contenant la classification des filtres
        for filtre in self.poke_data.columns: 
            Filtres_valeurs_possibles[filtre] = self.poke_data[filtre].unique().tolist()
            #On recupere les UNIQUES valeurs possibles
            
            #On fixera tout au long, des critères arbitraires
            # Numerique
            if np.issubdtype(self.poke_data[filtre].dtype, np.number):
                if len(Filtres_valeurs_possibles[filtre]) <= 600:
                    if len(Filtres_valeurs_possibles[filtre])<=10:
                        type_filtres[filtre] = True,"Categorique_Type_court"   
                    elif len(Filtres_valeurs_possibles[filtre])==2:
                        type_filtres[filtre]=True,"Booleen_Type"
                    else:
                        type_filtres[filtre] = True,"BatailleStat_Type"
                else:
                    type_filtres[filtre] = True, "Id_Type"
            # booleen
            elif self.poke_data[filtre].dtype == np.bool_  :
                type_filtres[filtre] = False, "Booleen_Type"
            # Texte
            elif self.poke_data[filtre].dtype == np.object_:
                if len(Filtres_valeurs_possibles[filtre])<=600:
                    type_filtres[filtre] = False, "Categorique_Type"
                else:
                    type_filtres[filtre] = False, "Id_Type"
            
            #Si aucun cas prévu:
            else:
                type_filtres[filtre] = False, "Autre_Type"

        # Liste avec tous les filtres qui sont des identifiants
        id_type_num = [(filtre) for filtre, info in type_filtres.items() if info[1] == 'Id_Type' and info[0]]
        id_type_nom = [(filtre) for filtre, info in type_filtres.items() if info[1] == 'Id_Type' and not info[0]]
        #Liste avec tous les filtres catégoriques
        categorique_type = [(filtre) for filtre, info in type_filtres.items() if info[1] == 'Categorique_Type']
        # for type in categorique_type:
        #     print("\n\n",Filtres_valeurs_possibles[type],"\n\n")

        #On combine les listes en prenant une valeur pour id_nom et num et 2 pour categorique
        filtres_affiches = id_type_num[:1] + id_type_nom[:1] + categorique_type[:2]
        #Filtres qui vont être affiches dans le treeview (pour pas trop le charger)

        Info_Filtres=(filtres_affiches,type_filtres,Filtres_valeurs_possibles)
        return Info_Filtres
    

    def reorganiser_colonnes(self):
        class Noeud():
            def __init__(self,caractere=None):
                #Initialisasion de la classe avec un caractère non existant d'abord
                self.enfants={} #Dictionnaire stockant les noeuds enfants
                self.mot_fini=False  #En début de recherche on l'initialise a faux


            """Methode qui prend des mots du dico_francais et les garde dans notre 
                                            arbre                 """
            def save(self,mot):
                #On prend un mot commençant par la racine de l'arbre
                node=self
                #On parcourt tous les caractère du mot
                for caract in mot:

                    #Si caract pas présent dans les enfants du Noeud
                    if caract not in node.enfants:
                        #On ajoute un nouveau Noeud pour ce caract
                        node.enfants[caract]=Noeud(caract)
                        #Les caract ici sont les clefs <=> uniques.
                    #Sinon on se déplace dans le Noeud associé au caractère suivant
                    node=node.enfants[caract]

                """Fin de la boucle for <=> fin du mot
                                        <=> dernier Noeud visité"""
                #On indique alors que le mot est fini
                node.mot_fini=True

            """    #fonction qui prend un mot et cherche s'il est présent dans l'arbre' 
                    fait précedement. Si mot présent ---> True, false sinon  """
            def cherche(self,mot):
                node=self
                #On regared tous les caract du mot
                for caract in mot:
                    if caract in node.enfants:
                        node = node.enfants[caract]
                        print(caract,"présent")
                    else:
                        print("pas de noeuds enfants",caract)
                        #S'il n'est pas dans les neuds enfants, alors ce n'est pas un mot valide
                        return False
                #On est arrivé au bout du mot
                #Verif si dernier Noeud visité correspond à la fin du mot
                return node.mot_fini
            
            def suggestions(self, prefix):
                # On commence par le noeud racine
                node = self
                # On parcourt chaque caractère du préfixe
                for caract in prefix:
                    # Si le caractère est présent dans les enfants du noeud actuel
                    if caract in node.enfants:
                        # On se déplace vers le noeud enfant correspondant
                        node = node.enfants[caract]
                    else:
                        # Si le préfixe n'est pas présent dans l'arbre, on retourne une liste vide
                        return None  # Pas de suggestions si le préfixe n'est pas trouvé
                # On appelle la fonction get_mots pour récupérer tous les mots qui commencent par le préfixe
                return self.get_mots(node, prefix)

            def get_mots(self, node, prefix):
                # Liste pour stocker les mots trouvés
                mots = []
                # Si le noeud actuel marque la fin d'un mot
                if node.mot_fini:
                    # On ajoute le préfixe à la liste des mots
                    mots.append(prefix)
                # On parcourt tous les enfants du noeud actuel
                for caract, enfant in node.enfants.items():
                    # On appelle récursivement get_mots sur les enfants pour trouver tous les mots
                    mots.extend(self.get_mots(enfant, prefix + caract))
                # On retourne la liste des mots trouvés
                return mots


        rng = default_rng()
        # Obtenez les informations de filtre
        _, type_filtres, _ = self.get_poke_filtres_data()
        
        # Sélectionnez les colonnes identifiant numérique et identifiant str
        id_num_col = [col for col, typ in type_filtres.items() if typ == (True, 'Id_Type')]
        id_str_col = [col for col, typ in type_filtres.items() if typ == (False, 'Id_Type')]
        
        # Sélectionnez deux colonnes avec (False, 'Categorique_Type')
        cat_type_cols = [col for col, typ in type_filtres.items() if typ == (False, 'Categorique_Type')][:2]
        
        # Mélangez les colonnes restantes au hasard
        autres_cols = [col for col in self.poke_data.columns if col not in (id_num_col + id_str_col + cat_type_cols)]
        rng.shuffle(autres_cols)
        
        # Réorganisez l'ordre des colonnes
        new_order = id_num_col[:1] + id_str_col[:1] + cat_type_cols + autres_cols
        self.poke_data = self.poke_data[new_order]
        
        self.arbre_poke_noms=Noeud()
        for poke_nom in self.poke_data.iloc[:,1].values:
            self.arbre_poke_noms.save(poke_nom.lower())
        return self.arbre_poke_noms


    def normalization(self, nom):
        # Verif si le fichier de donnees est celui des pokemons
        if self.data == "Model/pokemon.csv":
            # Rempl les caracteres speciaux par des symboles comprehensibles
            # Rempl les formes et les noms particuliers par des noms standards (par rpp a notre dossier media)
            remplacements = {
                "Normal Forme": "", "Plant Cloak": "", "Shield Forme": "",
                "Altered Forme": "", "Land Forme": "", "Standard Mode": "",
                "Mr. Mime": "mr._mime", "mr. mime": "mr._mime",
                "Mime Jr.": "mime_jr", "mime jr.": "mime_jr",
                "HoopaHoopa Confined": "hoopa", "Zygarde": "zygarde",
                "Flabébé": "flabebe", "'": "" , "♂": "_m", "♀": "_f"
            }
            for ancien, nouveau in remplacements.items():
                if ancien in nom:
                    nom = nom.replace(ancien, nouveau)
            if nom in remplacements:
                return remplacements[nom]

        # Conv les nombres en chaine de caracteres
        if isinstance(nom, (float, int)):
            nom = str(nom)
        # Separe le nom et prend la premiere partie
        nom_sep = nom.split()
        premier_mot = nom_sep[0]

        # Ajoute un tiret avant chaque majuscule qui n'est pas la premiere lettre
        nom_avec_tirets = re.sub(r'(?<!^)(?=[A-Z])', '-', premier_mot)
        # Conv en minuscules et rempl les caracteres speciaux par des tirets
        nom_normalise = re.sub(r'\W+', '-', nom_avec_tirets).lower()
        # Suppr les tirets a la fin si necessaire
        nom_normalise = re.sub(r'-+$', '', nom_normalise)

        # Gere les cas avec "X" ou "Y" a la fin du nom
        if len(nom_sep) > 2:
            if nom_sep[2].lower() == "x":
                return nom_normalise + "x"
            elif nom_sep[2].lower() == "y":
                return nom_normalise + "y"
        else:
            return nom_normalise


    def data_media(self,chemin_dossier_media,media_type):
        

        if self.data=="Model/pokemon.csv":
            self.dico_direction_images["CharizardMega Charizard X"]="Model/Characters_image/6-mega-x.png"
            self.dico_direction_images["CharizardMega Charizard Y"]="Model\Characters_image/6-mega-y.png"
            self.dico_direction_images["MewtwoMega Mewtwo X"]="Model/Characters_image/150-mega-y.png"
            self.dico_direction_images["MewtwoMega Mewtwo Y"]="Model/Characters_image/150-mega-y.png"
            self.dico_direction_images["HoopaHoopa Unbound"]="Model/Characters_image/720-unbound.png"
            self.dico_direction_gif["Mr. Mime"]="Model/GIF/mr._mime.gif"
            
            
            # Définir le chemin vers le dossier contenant les GIFs
        # Créer un dictionnaire avec les noms normalisés des Pokémon
        noms_normalises = {
            self.normalization(nom_pokemon): nom_pokemon
            for nom_pokemon in self.poke_data.iloc[:, 1].values
        }
        # Si le type de média est un GIF
        if media_type == ".gif":
            # Itérer sur tous les fichiers dans le dossier des GIFs
            for fichier in os.listdir(chemin_dossier_media):
                # Vérifier si le fichier est un GIF
                if fichier.endswith(media_type):
                    # Obtenir les parties du nom du fichier séparées par un tiret
                    parties_nom = fichier.split('-')
                    # Vérifier si le fichier n'a pas de numéro après le nom du Pokémon
                    if (len(parties_nom) == 1 or
                        (len(parties_nom) > 1 and not parties_nom[-1][0].isdigit())):
                        # Construire le chemin relatif et l'ajouter au dictionnaire si le nom est normalisé
                        chemin_relatif = os.path.join(chemin_dossier_media, fichier)
                        nom_normalise_gif = os.path.splitext(os.path.basename(chemin_relatif))[0]
                        if nom_normalise_gif in noms_normalises:
                            self.dico_direction_gif[noms_normalises[nom_normalise_gif]] = chemin_relatif
            i = 0
            # Vérifier l'existence des GIFs pour chaque Pokémon
            for nom in self.poke_data.iloc[:, 1].values:
                if nom not in self.dico_direction_gif:
                    self.dico_direction_gif[nom] = "Model/GIF/xd.gif"
                    i += 1
            print(f"{i} erreurs pour les gifs des Pokémon")
        # Si le type de média est un PNG
        if media_type == ".png":
            i = 0
            print("Traitement des fichiers PNG en cours...")
            for fichier in os.listdir(chemin_dossier_media):
                chemin_relatif = os.path.join(chemin_dossier_media, fichier)
                if fichier.endswith(media_type):
                    parties_nom = fichier.split("-")
                    # Ignorer le fichier 'xd.png'
                    if len(parties_nom) == 1 and parties_nom != ['xd.png']:
                        num_png = int(parties_nom[0].replace(".png", ""))
                        resultat_filtre = self.poke_data.loc[self.poke_data.iloc[:, 0] == num_png]
                        # Associer le nom du Pokémon à son image PNG
                        if not resultat_filtre.empty:
                            nom_pokemon = resultat_filtre.iloc[:, 1].values[0]
                            self.dico_direction_images[nom_pokemon] = chemin_relatif
                        else:
                            # Gérer le cas où aucun Pokémon n'est trouvé avec le numéro spécifié
                            print(f"Aucun Pokémon trouvé avec le numéro {num_png}.")
                        
                    if len(parties_nom) == 2:
                        mots_cles = ["Mega", "Attack", "Defense", "Speed", "Primal", "Sandy",
                                    "Trash", "Heat", "Wash", "Frost", "Fan", "Mow", "Female",
                                    "Origin", "Sky", "Therian", "Black", "White", "Resolute",
                                    "Pirouette", "Shield"]
                        # Vérifier si le deuxième élément contient un mot-clé
                        if any(mot_cle.lower() in parties_nom[1].lower() for mot_cle in mots_cles):
                            num_png = int(parties_nom[0].replace(".png", ""))
                            noms_pokemons = self.poke_data.loc[self.poke_data.iloc[:, 0] == num_png].iloc[:, 1]
                            # Associer l'image au Pokémon correspondant
                            for pokemon in noms_pokemons:
                                if parties_nom[1].replace(".png", "") in pokemon.lower():
                                    self.dico_direction_images[pokemon] = chemin_relatif
            
            # Vérifier l'existence des images pour chaque Pokémon
            for nom in self.poke_data.iloc[:, 1].values:
                if nom not in self.dico_direction_images:
                    self.dico_direction_images[nom] = "Model/Characters_image/xd.png"
                    i += 1
            print(f"{i} erreurs pour les images des Pokémon")
                        

    def get_poke_media(self):
        self.data_media("Model\\GIF",".gif")
        self.data_media("Model\\Characters_image",".png")
        return self.dico_direction_images,self.dico_direction_gif

