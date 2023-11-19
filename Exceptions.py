class PokedexError(Exception):
    """Classe de base pour les exceptions du Pokedex."""

class DataError(PokedexError):
    """Exception liée aux erreurs de données du Pokedex."""

class FilterError(PokedexError):
    """Exception liée aux erreurs de filtrage du Pokedex."""

class SearchError(PokedexError):
    """Exception liée aux erreurs de recherche du Pokedex."""


""""La gestion des exceptions dans un Pokedex pourrait couvrir 
un large éventail de scénarios. Voici quelques exemples potentiels 
d'exceptions que tu pourrais envisager de gérer, en fonction des
 fonctionnalités spécifiques de ton Pokedex :

1. **Erreur de chargement des données** : Si le chargement des 
données depuis la source échoue, cela pourrait déclencher une 
exception.

2. **Erreur de filtrage** : Si une erreur se produit lors de 
l'application d'un filtre aux données (par exemple, le filtre 
spécifié par l'utilisateur n'est pas valide), tu pourrais gérer
 cette situation avec une exception.

3. **Erreur de recherche** : Lorsque l'utilisateur effectue une 
recherche, des erreurs peuvent survenir si la recherche est mal
 formulée ou si aucun résultat n'est trouvé.

4. **Problèmes d'accès à la base de données** : Si tu stockes 
les données du Pokedex dans une base de données, tu pourrais gérer
 des exceptions liées à des problèmes d'accès à la base de données.

5. **Erreurs de saisie utilisateur** : Les utilisateurs peuvent 
entrer des données incorrectes ou mal formatées. La gestion des 
erreurs de saisie peut aider à fournir des retours d'informations
 clairs.

6. **Erreurs de configuration** : Si des configurations nécessaires ne
 sont pas correctement définies, cela peut déclencher des exceptions.

7. **Problèmes de connexion réseau** : Si ton Pokedex nécessite des
 requêtes réseau pour obtenir des données, tu pourrais gérer des 
 exceptions liées à des problèmes de connexion.

8. **Problèmes de mémoire** : Dans des cas exceptionnels, tu pourrais 
gérer des erreurs liées à des problèmes de mémoire insuffisante.

Il est essentiel de déterminer les situations qui pourraient causer 
des erreurs dans ton application spécifique et de planifier la gestion
 des exceptions en conséquence. Cela contribuera à rendre ton Pokedex
   plus robuste et à améliorer l'expérience utilisateur en fournissant
     des messages d'erreur significatifs.
                                                        
                                                        
                                                        """