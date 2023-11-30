import pandas as pd
import numpy as np
from os import walk


class Gestion_Data:
    def __init__(self):
        self.poke_data=pd.read_csv("Model\pokemon.csv")
        
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
        
    def data_image(self,direction_image,direction_gif):
        image_gif=[]
        image_gif_direction_codifie={}
        for direction in (direction_image,direction_gif):
            for _,__, image_data in walk(direction):
                image_gif.append(image_data)
        
        dic_image={}
        for image in image_gif[0]:
            parties=image.split("-")
            id=parties[0]
            mega="mega" in parties
            X= "x" in parties
            Y= "y" in parties
            dic_image[id]={"Mega":mega, "X":X, "Y":Y}
        
        print(len(dic_image))

                

# G=Gestion_Data()
# a=G.get_data_filtrage()
# b=list(a.items())
# print(b[0][0],b[0][1][0])

# G.data_image("Model/Characters_image","Model/GIF")



# for i in a:
#     li.append(i+"()")
# print(li)
# test=eval(li[0]).test()
