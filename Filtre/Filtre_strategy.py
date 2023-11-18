from abc import ABC, abstractmethod

class Filtre(ABC):

    
    def application_filtre(self,filtres):
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
class Type_filtre(Filtre):
    def application_filtre(self, data, valeur_filtree):
        print("ok")
        return data[data["Type 1"]==valeur_filtree]