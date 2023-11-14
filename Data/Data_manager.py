import pandas as pd

class Gestion_Data:
    def __init__(self):
        self.data=pd.read_csv("Data\pokemon.csv")
        print(self.data)