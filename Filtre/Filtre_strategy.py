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


    




import re

def normalizar_nombre(nombre):
    # Primero, dividimos el nombre por espacios y tomamos la primera palabra
    nombre_dividido = nombre.split()
    primera_palabra = nombre_dividido[0]
    # Luego, buscamos si hay una segunda palabra que comienza con "Mega"
    # y la concatenamos con la primera palabra sin espacios
    
    

    nombre=primera_palabra
    # Insertar un guión antes de cada letra mayúscula que no sea la primera letra
    nombre_con_guiones = re.sub(r'(?<!^)(?=[A-Z])', '-', nombre)
    # Convertir a minúsculas y reemplazar caracteres especiales con guiones
    nombre_normalizado = re.sub(r'\W+', '-', nombre_con_guiones).lower()
    # Eliminar posibles guiones al final
    nombre_normalizado = re.sub(r'-+$', '', nombre_normalizado)
    if len(nombre_dividido)>2:
        if nombre_dividido[2].lower()=="X".lower():
            return nombre_normalizado+"x"
        elif nombre_dividido[2].lower()=="Y".lower():
            return nombre_normalizado+"y"
    else:
        return nombre_normalizado

# Ejemplo de uso
print(normalizar_nombre("CharizardMega Charizard X"))  # Debería imprimir 'charizard-megax'
print(normalizar_nombre("BlastoiseMega Blastoise"))   # Debería imprimir 'blastoise-mega'


print( "charizard-megax" in normalizar_nombre("Charizard"))