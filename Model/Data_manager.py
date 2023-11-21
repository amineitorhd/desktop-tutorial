import pandas as pd

class Gestion_Data:
    def __init__(self):
        self.poke_data=pd.read_csv("Model\pokemon.csv")
        
    def get_pokeData(self):
        return self.poke_data
    
    def get_data_filtrage(self):
        Filtres_valeurs_possibles={}
        type_filtres={}
        for filtre in self.poke_data.columns:
        # if filtre not in ["Number", "Name"]:
            Filtres_valeurs_possibles[filtre]=self.poke_data[filtre].unique().tolist()
            if isinstance(Filtres_valeurs_possibles[filtre][0],int):
                type_filtres[filtre]=True
            else:
                type_filtres[filtre]=False

                # Filtres_valeurs_possibles
        return Filtres_valeurs_possibles,type_filtres

    def test(self):
        ok=self.get_data_filtrage()
        print("tiens:")
        print(ok)
        

G=Gestion_Data()
a=G.get_data_filtrage()



# for i in a:
#     li.append(i+"()")
# print(li)
# test=eval(li[0]).test()
