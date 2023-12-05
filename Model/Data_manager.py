import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import os
import re

class Gestion_Data:
    def __init__(self):
        self.poke_data=pd.read_csv("Model/pokemon.csv")
        # self.poke_data = self.poke_data.fillna('') #On remplace tous les nan par des 
        # self.conversion_Name_Number={row[1].replace("♀", "_f").replace("♂", "_m").replace("'", "").replace(":", "").replace(" ", "_").replace(".", "").replace("-", "").lower(): row[0] for _, row in self.poke_data.iterrows()}

    def get_pokeData(self):
        return self.poke_data
    
    def get_data_filtrage(self):
        Filtres_valeurs_possibles = {}
        type_filtres = {}
        for filtre in self.poke_data.columns:
            Filtres_valeurs_possibles[filtre] = self.poke_data[filtre].unique().tolist()
            
            # Numerique
            if np.issubdtype(self.poke_data[filtre].dtype, np.number):
                if len(Filtres_valeurs_possibles[filtre]) <= 220:
                    if len(Filtres_valeurs_possibles[filtre])<=10:
                        type_filtres[filtre] = True,"Categorique_Type"   #Le meme que abajo
                    else:
                        type_filtres[filtre] = True,"BatailleStat_Type"
                else:
                    type_filtres[filtre] = True, "Id_Type"
            # booleen
            elif self.poke_data[filtre].dtype == np.bool_:
                type_filtres[filtre] = False, "Booleen_Type"
            # categorique
            elif len(Filtres_valeurs_possibles[filtre]) < 15:
                type_filtres[filtre] = False, "Categorique_Type"
            # Texte
            elif self.poke_data[filtre].dtype == np.object_:
                if len(Filtres_valeurs_possibles[filtre])<=300:
                    type_filtres[filtre] = False, "Categorique_Type"
                else:
                    type_filtres[filtre] = False, "Id_Type"
            # Si no se cumple ninguna de las condiciones anteriores, la columna podría ser de otro tipo
            else:
                type_filtres[filtre] = False, "Otro_Type"
        
        Info_Filtres=(type_filtres,Filtres_valeurs_possibles)

        return Info_Filtres

                #Dico de forme:
                #  type_filtres={"filtre": (x,y),[....]}
                #       x=True---> Filtre numerico
                #       y=True---> Filtre avec quantités de valeurs uniques>220
    

    def test(self):
        ok=self.get_data_filtrage()
        print("tiens:")
        print(ok)
        
    def get_data_image(self):
        image_gif={}
        image_png={}
        
        for poke_gif in os.listdir("Model/GIF"):
            nom=(re.split('-|\.', poke_gif)[0]).lower()
            if nom=="mr":
                print((re.split('-', poke_gif)[0]).lower())
            # Manejar formas alternativas de Pokémon
            # if '_f' in nom:
            #     nom = nom.replace('_f', '♀').strip()
            #     print("\n")
            #     print(nom)
            
            if nom in self.conversion_Name_Number:
                # print("yes")
                nombre=self.conversion_Name_Number[nom]

                if nombre not in image_gif:
                    # print("ok")
                    image_gif[nombre]="Model/GIF"+"/"+poke_gif
            else:
                pass
                # print(nom,"ok")
        c=0
        for i in range (721):
            if i not in image_gif:
                c+=1
                if i>0 and i<721:
                    a=self.poke_data.loc[self.poke_data['Number'] == i, 'Name'].values[0]
                    print(f"on a un probleme avec{i}: {a}")
                else:
                    print(f"on a un probleme avec{i}")
        print("total:",c)

        for poke_photo in os.listdir("Model/Characters_image"):    
            # Obtener el número del Pokémon del nombre del archivo
            nmb = poke_photo.split('.')[0]

            # Agregar al diccionario
            image_png[nmb] = "Model/Characters_image"+"/"+poke_photo
        return image_png
            

        print(image_png)
        # print(image_gif)
                
        

                

# G=Gestion_Data()
# a=G.get_data_filtrage()
# print(G.conversion_Name_Number)
# G.get_data_image()
# G.data_image("Model/Characters_image","Model/GIF")
# a="Amine._AmineE"
# print(a.lower())

# for i in a:
#     li.append(i+"()")
# print(li)
# test=eval(li[0]).test()
