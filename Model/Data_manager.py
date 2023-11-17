import pandas as pd

class Gestion_Data:
    def __init__(self):
        self.poke_data=pd.read_csv("Model\pokemon.csv")
        
    def get_pokeData(self):
        return self.poke_data
    
    def filtre_type(self,poke_type):
        return self.poke_data[self.poke_data["Type 1"]==poke_type]
        