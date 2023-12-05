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
                if len(Filtres_valeurs_possibles[filtre]) <= 220:
                    if len(Filtres_valeurs_possibles[filtre])<=10:
                        type_filtres[filtre] = True,"Categorique_Type"   
                    else:
                        type_filtres[filtre] = True,"BatailleStat_Type"
                else:
                    type_filtres[filtre] = True, "Id_Type"
            # booleen
            elif self.poke_data[filtre].dtype == np.bool_:
                type_filtres[filtre] = False, "Booleen_Type"
            
            elif len(Filtres_valeurs_possibles[filtre]) < 15:
                type_filtres[filtre] = False, "Categorique_Type"
            # Texte
            elif self.poke_data[filtre].dtype == np.object_:
                if len(Filtres_valeurs_possibles[filtre])<=300:
                    type_filtres[filtre] = False, "Categorique_Type"
                else:
                    type_filtres[filtre] = False, "Id_Type"
            
            #Si aucun cas prévu:
            else:
                type_filtres[filtre] = False, "Autre_Type"
        
        Info_Filtres=(type_filtres,Filtres_valeurs_possibles)

        return Info_Filtres