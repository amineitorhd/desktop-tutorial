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

def set_strategy(filtre,test_numerique,Type):
    # print("filtre:",filtre)
    # print("test numerique:",test_numerique)
    # print(f"Type:{Type}:{type(Type)}")
    class strategy_filtrage(Filtre):
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
    return strategy_filtrage

class Random(Filtre):
    def application_filtre(self, data, valeur_filtree):
        num_pokemons = int(valeur_filtree)
        return data.sample(n=num_pokemons)
    
class AndStrategy(Filtre):
    def __init__(self, *strategies):
        self.strategies = strategies

    def application_filtre(self, data, valeur_filtree):
        for strategy in self.strategies:
            data = strategy.application_filtre(data, valeur_filtree)
        return data

class SortByIDStrategy(Filtre):
    def application_filtre(self, data, valeur_filtree=None):
        return data.sort_values('Number')

# Luego puedes crear una instancia de AndStrategy con tus estrategias
strategy = AndStrategy(set_strategy('Type_1', False, 'Text_Type')(), SortByIDStrategy())
# Ahora puedes usar strategy.application_filtre(data, valeur_filtree) para filtrar y ordenar tus datos
