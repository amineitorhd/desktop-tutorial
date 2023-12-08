from abc import ABC, abstractmethod


class Filtre(ABC):
    @abstractmethod
    def application_filtre(self,data,valeur_filtree):
        pass

"""""
        La razón para tener esta clase madre abstracta es doble:

Establecer una interfaz común: Proporciona una interfaz común que todas las estrategias 
                                de filtrado deben seguir. Esto facilita la sustitución de 
                                estrategias y la extensión del sistema con nuevas estrategias 
                                sin tener que cambiar el código existente.

Hacer cumplir la estructura: Al declarar FilterStrategy como una clase abstracta, se asegura de
                                que cualquier clase que quiera actuar como una estrategia de 
                                filtrado deba proporcionar una implementación concreta del 
                                método apply_filter. Si una clase no lo hace, el intérprete 
                                de Python generará un error en tiempo de ejecución.
                                """




def set_strategy(filtre,test_numerique,Type,strategie="Recherche_Simple"):
    class Filtrage_Simple(Filtre):
            def application_filtre(self,data,valeur_filtree):
                if test_numerique:
                    if Type=="Id_Type":
                        print("identifiant nominale detecté")
                        return data[data[filtre].astype(str).str.startswith(str(valeur_filtree))]
                    else:
                        return data[data[filtre] == int(valeur_filtree)]
                else:
                    if Type=="Id_Type":
                        print("identifiant numerique detecté")
                        return data[data[filtre].str.lower().str.contains(valeur_filtree.lower())]
                    else:
                        return data[data[filtre].str.lower() == valeur_filtree.lower()]
                    #Demander laurine si pour identificator afficher slment ce qui commence par la chaine de charact
                    #ou comme j'ai fais ceux que contiennent tous la chaine
    

    class Filtrage_Plage(Filtre):
            def application_filtre(self, data, valeur_filtree):
                if test_numerique:
                    if Type=="BatailleStat_Type":
                        return data[(data[filtre] >= valeur_filtree[0]) & (data[filtre] <= valeur_filtree[1])]
    

    class Random(Filtre):
            def application_filtre(self, data, valeur_filtree):
                num_pokemons = int(valeur_filtree)
                return data.sample(n=num_pokemons)

    
    class Ordre_Filtre(Filtre):
        def application_filtre(self, data, valeur_filtree=True):
            if valeur_filtree is True:
                return data.sort_values(filtre, ascending=True)
            else:
                return data.sort_values(filtre, ascending=False)    


    class AndStrategy(Filtre):
        def __init__(self, *strategies):
            self.strategies = strategies

        def application_filtre(self, data, valeur_filtree):
            for strategy in self.strategies:
                data = strategy.application_filtre(data, valeur_filtree)
            return data

    def combine_strategies(*strategies):
        return AndStrategy(*strategies)   

    if strategie=="Recherche_Simple":
        return Filtrage_Simple
    elif strategie=="Recherche_plage_de_valeurs":
        return Filtrage_Plage
    elif strategie=="Random":
        return Random
    elif strategie=="Ordre":
        return Ordre_Filtre
    elif isinstance(strategie, list):
        # Si 'strategie' es una lista, combinar las estrategias
        strategy_instances = []
        for strat in strategie:
            strategy_class = set_strategy(filtre, test_numerique, Type, strat)
            strategy_instances.append(strategy_class())
        return combine_strategies(*strategy_instances)        


    




