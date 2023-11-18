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
    def test(self):
        print("ok")
        

G=Gestion_Data()
a=G.get_data_filtrage()
li=['Gestion_Data()']
for i in a:
    li.append(i+"()")
print(li)
test=eval(li[0]).test()
