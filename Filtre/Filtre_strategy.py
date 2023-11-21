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

def set_strategy(filtre,test_numerique,identificator):
    class strategy_filtrage(Filtre):
        def application_filtre(self,data,valeur_filtree):
            if test_numerique:
                if identificator:
                    return data[data[filtre].astype(str).str.startswith(str(valeur_filtree))]
                else:
                    return data[data[filtre] == int(valeur_filtree)]
            else:
                if identificator:
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



class Number(Filtre):
    def application_filtre(self, data, valeur_filtree):
        print(valeur_filtree)
        return data[data['Number'] == int(valeur_filtree)]

class Name(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Name'].str.lower().str.contains(valeur_filtree.lower())]

class Type_1(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Type_1'].str.lower() == valeur_filtree.lower()]

class Type_2(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Type_2'].str.lower() == valeur_filtree.lower()]

class Total(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Total'] == int(valeur_filtree)]

class HP(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['HP'] == int(valeur_filtree)]
    
class Attack(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Attack'] == int(valeur_filtree)]

class Defense(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Defense'] == int(valeur_filtree)]

class Sp_Atk(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Sp_Atk'] == int(valeur_filtree)]

class Sp_Def(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Sp_Def'] == int(valeur_filtree)]

class Speed(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Speed'] == int(valeur_filtree)]

class Generation(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Generation'] == int(valeur_filtree)]

class Legendary(Filtre):
    def application_filtre(self, data, valeur_filtree):
        return data[data['Legendary'] == int(valeur_filtree)]



