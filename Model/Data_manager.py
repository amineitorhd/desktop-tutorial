import pandas as pd

class Gestion_Data:
    def __init__(self):
        self.poke_data=pd.read_csv("Model\pokemon.csv")
        
    def get_pokeData(self):
        return self.poke_data
    
    def get_data_filtrage(self):
        Filtres={}
        for filtre in self.poke_data.columns:
            Filtres[filtre]=self.poke_data[filtre].unique().tolist()
        return Filtres
        

G=Gestion_Data()
a=G.get_data_filtrage()
for element in a:
    print (a[element])

