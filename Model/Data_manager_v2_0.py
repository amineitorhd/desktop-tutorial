import pandas as pd
import numpy as np


class Gestion_Data:
    def __init__(self,poke_data_direction):
        self.poke_data=pd.read_csv(poke_data_direction)
    
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
    


