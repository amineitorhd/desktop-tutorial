import pandas as pd
import numpy as np
from numpy.random import default_rng
import os,re




class Gestion_Data:
    def __init__(self,poke_data_direction):
        self.data=poke_data_direction
        self.poke_data=pd.read_csv(poke_data_direction)
                # Inicializar el diccionario para almacenar las rutas relativas de los GIFs
        self.diccionario_gifs = {}
        self.diccionario_imagenes={}



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
        filtres_affiches, type_filtres, _ = self.get_poke_filtres_data()
        
        # Sélectionnez les colonnes identifiant numérique et identifiant str
        id_num_col = [col for col, typ in type_filtres.items() if typ == (True, 'Id_Type')]
        id_str_col = [col for col, typ in type_filtres.items() if typ == (False, 'Id_Type')]
        
        # Sélectionnez deux colonnes avec (False, 'Categorique_Type')
        cat_type_cols = [col for col, typ in type_filtres.items() if typ == (False, 'Categorique_Type')][:2]
        
        # Mélangez les colonnes restantes au hasard
        autres_cols = [col for col in self.poke_data.columns if col not in id_num_col + id_str_col + cat_type_cols]
        rng.shuffle(autres_cols)
        
        # Réorganisez l'ordre des colonnes
        new_order = id_num_col[:1] + id_str_col[:1] + cat_type_cols + autres_cols
        self.poke_data = self.poke_data[new_order]
        
        self.arbre_poke_noms=Noeud()
        for poke_nom in self.poke_data.iloc[:,1].values:
            self.arbre_poke_noms.save(poke_nom.lower())
        return self.arbre_poke_noms


    def normalizar_nombre(self,nombre):
        if self.data=="Model/pokemon.csv":
            # Primero, dividimos el nombre por espacios y tomamos la primera palabra
            if '♀' in nombre:
                nombre = nombre.replace('♀', '_f')
            elif '♂' in nombre:
                nombre = nombre.replace('♂', '_m')
            elif "'" in nombre:
                nombre=nombre.replace("'","")
            elif "Normal Forme" in nombre:
                nombre=nombre.replace("Normal Forme","")
            elif "Plant Cloak" in nombre:
                nombre=nombre.replace("Plant Cloak","")
            elif "Shield Forme" in nombre:
                nombre=nombre.replace("Shield Forme","")
            elif "Altered Forme" in nombre:
                nombre=nombre.replace("Altered Forme","")
            elif "Land Forme" in nombre:
                nombre=nombre.replace("Land Forme","")
            elif "Standard Mode" in nombre:
                nombre=nombre.replace("Standard Mode","")
            if nombre == 'Mr. Mime' or nombre=="mr. mime":
                return 'mr._mime'
            elif nombre=="Mime Jr." or nombre == "mime jr.":
                return "mime_jr"
            elif "HoopaHoopa Confined" in nombre:
                return "hoopa"
            elif "Zygarde" in nombre:
                return "zygarde"
            elif "Flabébé"==nombre or "flabébé"==nombre:
                return "flabebe"

        if isinstance(nombre, (float, int)):
            nombre=str(nombre)
        nombre_dividido = nombre.split()
        primera_palabra = nombre_dividido[0]
        # Luego, buscamos si hay una segunda palabra que comienza con "Mega"
        # y la concatenamos con la primera palabra sin espacios
        
        nombre=primera_palabra
        # Insertar un guión antes de cada letra mayúscula que no sea la primera letra
        nombre_con_guiones = re.sub(r'(?<!^)(?=[A-Z])', '-', nombre)
        # Convertir a minúsculas y reemplazar caracteres especiales con guiones
        nombre_normalizado = re.sub(r'\W+', '-', nombre_con_guiones).lower()
        # Eliminar posibles guiones al final
        nombre_normalizado = re.sub(r'-+$', '', nombre_normalizado)
        if len(nombre_dividido)>2:
            if nombre_dividido[2].lower()=="X".lower():
                return nombre_normalizado+"x"
            elif nombre_dividido[2].lower()=="Y".lower():
                return nombre_normalizado+"y"
        else:
            return nombre_normalizado

    def data_media(self,ruta_carpeta_media,media_type):
        

        if self.data=="Model/pokemon.csv":
            self.diccionario_imagenes["CharizardMega Charizard X"]="Model/Characters_image/6-mega-x.png"
            self.diccionario_imagenes["CharizardMega Charizard Y"]="Model\Characters_image/6-mega-y.png"
            self.diccionario_imagenes["MewtwoMega Mewtwo X"]="Model/Characters_image/150-mega-y.png"
            self.diccionario_imagenes["MewtwoMega Mewtwo Y"]="Model/Characters_image/150-mega-y.png"
            self.diccionario_imagenes["HoopaHoopa Unbound"]="Model/Characters_image/720-unbound.png"

            
            
        # Definir la ruta a la carpeta donde se encuentran los GIFs
        # Crear un diccionario con nombres normalizados de los pokémon
        nombres_normalizados = {
            self.normalizar_nombre(pokemon_name): pokemon_name
            for pokemon_name in self.poke_data.iloc[:, 1].values
        }
        if media_type==".gif":
            # Iterar sobre todos los archivos en la carpeta de GIFs
            for archivo in os.listdir(ruta_carpeta_media):
                # Comprobar si el archivo es un GIF
                if archivo.endswith(media_type):
                    # Obtener las partes del nombre del archivo separadas por guión
                    partes_nombre = archivo.split('-')
                    # Comprobar si el archivo no tiene un número después del nombre del pokémon
                    if (len(partes_nombre) == 1 or
                        (len(partes_nombre) > 1 and not partes_nombre[-1][0].isdigit())):
                        # Construir la ruta relativa y añadirla al diccionario si el nombre está normalizado
                        relative_path = os.path.join(ruta_carpeta_media, archivo)
                        nombre_normalizado_gif = os.path.splitext(os.path.basename(relative_path))[0]
                        if nombre_normalizado_gif in nombres_normalizados:
                            self.diccionario_gifs[nombres_normalizados[nombre_normalizado_gif]] = relative_path
            i=0
            for nom in self.poke_data.iloc[:,1].values:
                if nom not in self.diccionario_gifs:
                    self.diccionario_gifs[nom]="Model/GIF/xd.gif"
                    i+=1
            print(f"{i} erreur pour les gifs des pokemons")
            
        if media_type==".png":
            i=0
            print("111111111111111111111111111ok")
            for archivo in os.listdir(ruta_carpeta_media):
                relative_path = os.path.join(ruta_carpeta_media, archivo)
                if archivo.endswith(media_type):
                    partes_nombre=archivo.split("-")
                    # partes_nombre.remove("xd")
                    if len(partes_nombre)==1 and partes_nombre!=['xd.png']:
                        
                        num_png=int(partes_nombre[0].replace(".png",""))
                        resultat_filtre = self.poke_data.loc[self.poke_data.iloc[:, 0] == num_png]
                        if not resultat_filtre.empty:
                            nom_pokemon = resultat_filtre.iloc[:, 1].values[0]
                            self.diccionario_imagenes[nom_pokemon]=relative_path
                        else:
                            # Gérez le cas où aucun résultat n'est trouvé
                            print(f"Aucun Pokémon trouvé avec le numéro {num_png}.")
                        
                    if len(partes_nombre)==2:
                        if any(keyword.lower() in partes_nombre[1].lower() for keyword in ["Mega","Attack", "Defense","Speed", "Primal", "Sandy",
                                                                                           "Trash", "Heat", "Wash", "Frost", "Fan", 
                                                                                           "Mow", "Female","Origin","Sky","Therian",
                                                                                           "Black","White","Resolute","Pirouette","Shield",]):
                            # Condition for other keywords
                            num_png = int(partes_nombre[0].replace(".png", ""))
                            noms_pokemons = self.poke_data.loc[self.poke_data.iloc[:, 0] == num_png].iloc[:, 1]
                            for pokemon in noms_pokemons:
                                if partes_nombre[1].replace(".png","") in pokemon.lower():
                                    self.diccionario_imagenes[pokemon] = relative_path
            j=0
            for nom in self.poke_data.iloc[:,1].values:
                if nom not in self.diccionario_imagenes:
                        self.diccionario_imagenes[nom]="Model/Characters_image/xd.png"
                        j+=1
                        print(nom)
            print(f"{j} erreur pour les images des pokemons")

    def get_poke_media(self):
        self.data_media("Model\\GIF",".gif")
        self.data_media("Model\\Characters_image",".png")
        return self.diccionario_imagenes,self.diccionario_gifs

