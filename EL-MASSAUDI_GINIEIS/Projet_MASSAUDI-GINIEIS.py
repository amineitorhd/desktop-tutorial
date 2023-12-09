# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 15:40:48 2023

@author: amine
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 13:05:11 2023

@author: amine
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 06:56:43 2023

@author: amine
"""

#Bibliotheque fournie permettant de gerer des graph de tkinter plus simplement.
from tkiteasy import *
# import openpyxl
#Pour gerer des fichier xl (excel)
import csv
import time
import pandas as pd

import random



class jeu():
    "On initialise nos variables"
    def __init__(self,):

        #Set contenant les mots trouvés
        self.set_de_mots_trouves_etape3=set()
        
        #Set contenant les mots français du diccionaire 
        self.words_french=set()
        self.lecture()
        self.lettres = {
            "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 8, "G": 3, "H": 2,
            "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2,
            "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1,
            "Y": 2, "Z": 1
                       }
        #Diccionaire contenant lettres du damier avec ces coordonnées
        self.lettres_damier={}
        #Dictionnaire contenant les coordonnés de chaque rectangle associé à chaque case
        self.cellules_damier={}
        self.couleur_case="Blue"
   ############### Paramètres d'affichage graphique ##########################     
        self.taille_damier=4
   ############### Variables divers pour le code     ##########################     
        '''Variable permettant de paramétrer les transitions du jeu.
            Si on fixe à 0, on aura transitions ultra rapides'''
        self.temps_transition=0.8
        self.temps_de_jeu=120
        self.score=0
        self.score_joueur2=0
        self.joueur_nom=""
        self.joueur2_nom=""
        self.joueur2=False
        self.premier_indice=True
        self.cases_selected=[]
        self.mot_saisie=""
        self.liste_j1=[]
        self.liste_j2=[]
  
        
  

    """"On ajoute les mots du dictionnaire dans un set"""
    def lecture(self):
        #On ouvre le fichier en mode lecture ("r")
        with open ("EL-MASSAUDI_GINIEIS\dictionnaire_francais.txt","r") as file:

            #Sur chaque ligne du fichier On ajoute un mot sur notre set words_french

            for line in file:
                self.words_french.add(line.strip())
     
                      #Strip pour effacer espace entre début/fin de ligne
 
    
 
    
    """On fait la lecture du dictionnaire pour construire l'arbre"""
    def lecture_trie(self):
        with open ("EL-MASSAUDI_GINIEIS\dictionnaire_francais.txt","r") as file:
            self.words_french_Trie=Noeud()
            for line in file:
                self.words_french_Trie.save(line.strip().lower())
            return self.words_french_Trie






    """Premiere fenetre où l'on selectionne notre mode de jeu"""
    def menu(self):
        #On ouvre une fenetre
        self.menu=ouvrirFenetre(500,500)
        self.menu.afficherTexte("Jeu De Mots", 250, 100,"white",22)
        #Créations des boutons du menu
        self.menu.dessinerRectangle(150, 130, 190, 40, "blue")
        self.menu.afficherTexte("Mode 1 joueur", 250, 150)
        self.menu.dessinerRectangle(150, 190, 190, 40, "blue")
        self.menu.afficherTexte("Mode 2 joueurs", 250, 210)
        self.menu.afficherImage(0, 0,"EL-MASSAUDI_GINIEIS\exit_bottom_icon.png")
        self.menu.dessinerRectangle(150, 250, 190, 40, "blue")
        self.menu.afficherTexte("Cherche",250 , 270)
        self.menu.afficherImage(440,440,"EL-MASSAUDI_GINIEIS\settings_icon.png")
        self.menu.actualiser()

        while True:

            clic_menu=self.menu.attendreClic()
            
            #Bouton de fermeture
            if 0<clic_menu.x<40 and 0<clic_menu.y<40:
                self.menu.fermerFenetre()
                break
            #Premier mode de jeu
            if 150<clic_menu.x<340 and 130<clic_menu.y<170:
                #On ouvre la fenetre pseudo
                self.joueur_nom=self.saisir_nom_joueur(1)
                self.menu.actualiser()
                self.menu.fermerFenetre()
                #On lance affichage graphique avec  mode multijoueur en False
                self.affichage_graphique(False)
                #Bouton d'aide
                self.help_boutton=self.g.afficherImage(0, 50,"EL-MASSAUDI_GINIEIS\help.png")
                #On affiche le score et le pseudo une premeire fois
                self.score1=self.g.afficherTexte("0 point",self.maxLimitx_damier+150,150)           
                self.g.afficherTexte(f"{self.joueur_nom}",self.maxLimitx_damier+150,80,"orange")
                #On lance play avec multijoueur en False 
                self.play(False)
                self.score_enregistres()
                break
            #Deuxieme mode de jeu
            if 150<clic_menu.x<340 and 190<clic_menu.y<230:
                #On lance la fentre saisir nom joueur deux fois
                self.joueur_nom=self.saisir_nom_joueur(1)
                self.joueur2_nom=self.saisir_nom_joueur(2)
                self.menu.actualiser()
                self.menu.fermerFenetre()
                #On lance affichage graphique et play avec multijoueur en True 
                self.affichage_graphique(True)
                self.play(True)
                self.score_enregistres(True)
                break
                #Plus tard faire mode deux joueurs
            #Ouvre le menu secondaire pour les étapes 1 et 2
            if 150<clic_menu.x<340 and 250<clic_menu.y<290:
                self.menu.fermerFenetre()
                self.menu_secondaire()
                
                break
            #Ouvre la fenetre réglage
            if 440<clic_menu.x<490 and 440<clic_menu.y<490:
                self.setting()





    """"menu pour selectionner les étapes une ou deux """
    def menu_secondaire(self):
        #On ouvre une deuxieme fenetre
        self.menu2=ouvrirFenetre(450,250)
        #On dessine nos boutons et nos textes
        self.menu2.afficherTexte("Choisi la methode recherche", 220, 50,"white",20)
        self.menu2.dessinerRectangle(70, 90, 150, 40, "red")
        self.menu2.afficherTexte("Etape 2", 140, 109)
        self.menu2.dessinerRectangle(250, 90, 150, 40, "blue")
        self.menu2.afficherTexte("Etape 3", 320, 109)
        
        while True:
            menu2_clic=self.menu2.attendreClic()
            #On lance l'étape 2
            if 70<menu2_clic.x<220 and 90<menu2_clic.y<130:
                self.menu2.fermerFenetre()
                #On lance affichage graphique avec multijoueur en False
                self.affichage_graphique(False)
                self.search_mots_etape2()
                self.g.attendreTouche()
                self.g.fermerFenetre()
                break
            #On lance étape 3
            if 250<menu2_clic.x<400 and 90<menu2_clic.y<130:
                self.menu2.fermerFenetre()
                self.arbre=self.lecture_trie() #On le met là pour temps de charge de l'ordi
                self.affichage_graphique(False)
                self.search_mots_etape3()
                while True:    
                    clic=self.g.attendreClic()
                    if 0<clic.x<40 and 0<clic.y<40:        
                        self.g.fermerFenetre()
                        break
                break
    
    """"Fenetre de réglage"""
    def setting(self):
         #On ouvre une nouvelle fenetre
        setting_fenetre=ouvrirFenetre(400,400) 
        #On dessine nos bouttons                    
        setting_fenetre.dessinerRectangle(120, 100, 50, 50, "blue")
        setting_fenetre.afficherTexte("+", 145, 125,"white",22)
        setting_fenetre.dessinerRectangle(230, 100, 50, 50, "blue")
        setting_fenetre.afficherTexte("-", 255, 125,"white",22)
        taille=setting_fenetre.afficherTexte(f"{self.taille_damier}", 200, 125,"white",22)
        setting_fenetre.afficherTexte("Réglage de la taille du damier", 200, 75)
        setting_fenetre.dessinerRectangle(140, 350, 120, 40, "blue")
        setting_fenetre.afficherTexte("Valider",200,370)
        setting_fenetre.afficherTexte("Réglage du chronometre(en seconde)", 200, 195)
        setting_fenetre.dessinerRectangle(120, 220, 50, 50, "blue")
        setting_fenetre.afficherTexte("+", 145, 245,"white",52)
        setting_fenetre.dessinerRectangle(230, 220, 50, 50, "blue")
        setting_fenetre.afficherTexte("-", 255, 245,"white",52)
        temps_de_jeu=setting_fenetre.afficherTexte(f"{self.temps_de_jeu}", 200, 245,"white",22)
        setting_fenetre.dessinerRectangle(150, 300, 100, 40, "blue")
        temps=setting_fenetre.afficherTexte("temps infini",200,320)
      
        while True:   
            clic_setting=setting_fenetre.attendreClic() 
            #On supprime taille et temps_de_jeu pour l'actualiser par la suite 
            setting_fenetre.supprimer(taille)
            setting_fenetre.supprimer(temps_de_jeu)
            #On augmente de 1 la taille du damier 
            if 120<clic_setting.x<170 and 100<clic_setting.y<150:
                self.taille_damier+=1
            #On diminue de 1 la taille du damier 
            #On met une condition pour ne pas avoir un damier trop petit
            if 230<clic_setting.x<280 and 100<clic_setting.y<150 and self.taille_damier>3:
                self.taille_damier-=1
            #On augmente de 5 le temps de jeu
            if 120<clic_setting.x<170 and 220<clic_setting.y<270:
                self.temps_de_jeu+=5
            #On diminue de 5 le temps de jeu
            if 230<clic_setting.x<280 and 220<clic_setting.y<270 and self.temps_de_jeu>1:
                self.temps_de_jeu-=5   
            #On met le temps en infini ou en fini
            if 150<clic_setting.x<300 and 300<clic_setting.y<340:
                #On met le temps en infini
                if self.temps_de_jeu<900000:                               
                    self.temps_de_jeu=999999
                    #On change le bouton
                    setting_fenetre.supprimer(temps)
                    temps=setting_fenetre.afficherTexte("temps fini",200,320)
                else:
                    #On met le temps en fini
                    self.temps_de_jeu=60
                    #On change le bouton
                    setting_fenetre.supprimer(temps)
                    temps=setting_fenetre.afficherTexte("temps infini",200,320)
                    
            #Si on valide alors la fenetre se ferme et on revient au menu   
            if 140<clic_setting.x<270 and 350<clic_setting.y<390:
                setting_fenetre.fermerFenetre()
                break
            #On actualise les valeurs de taille et temps de jeu
            taille=setting_fenetre.afficherTexte(f"{self.taille_damier}", 200, 125,"white",22)
            temps_de_jeu=setting_fenetre.afficherTexte(f"{self.temps_de_jeu}", 200, 245,"white",22)
    


    
    """Fenetre pour saisir son pseudo avec la variable numero pour l'affichage si il y a plusieur joueur"""
    def saisir_nom_joueur(self,numero):
        user_fenetre=ouvrirFenetre(450,250)  #On ouvre une nouvelle fenetre
        user_fenetre.afficherTexte(f"Indique ton pseudo joueur numero {numero}", 225, 70,"blue",22)    
        user_fenetre.actualiser()
        #set contenant l'alphabet
        alphabet=set([lettre.lower() for lettre in self.lettres.keys()])
        pseudo=None
        nom=""
        while True:
                        
            touche=user_fenetre.attendreTouche()
            #On supprime tout pour pas que ça ne superpose par la suite
            if pseudo is not None:
                user_fenetre.supprimer(pseudo)
            
            #On supprime
            if touche=="BackSpace":
                nom=nom[:-1]
            #On met un espace avec un _
            if touche=="space":
                nom+="_"
            #Pour qu'il ne detecte que l'alphabet
            if touche in alphabet:
                nom+=touche
            #On valide
            if touche=="Return":
                break

            pseudo=user_fenetre.afficherTexte(f"{nom}", 200, 90)
        #On ferme la fenêtre et on commence par la suite la partie
        user_fenetre.fermerFenetre()
        return nom
        #On retourne le nom du joueur




    def affichage_graphique(self,multijoueur):
        if self.taille_damier<4:
            self.RESX,self.RESY= 400,600
            #Déplacement du damier dans la fenêtre graphique
            if not(multijoueur):
                self.OFX,self.OFY=40,60
            else:
                self.OFX,self.OFY=90,60
                
    
            #Taille des cases
            self.CASE=45
            self.g=ouvrirFenetre(self.RESX,self.RESY)
        else:
            
            self.RESX,self.RESY= self.taille_damier*100+600,self.taille_damier*200
            
            if not(multijoueur):
                self.g=ouvrirFenetre(self.RESX,self.RESY)
                x=0
            else:
                self.g=ouvrirFenetre(self.RESX,self.RESY)
                x=self.RESX//9
                
            #Déplacement du damier dans la fenêtre graphique
            self.OFX,self.OFY=800//self.taille_damier+x,300//self.taille_damier
            #Taille des cases
            self.CASE=400//self.taille_damier            
            
            #Tailles des lettres
        self.taille_lettre=self.CASE//3
        #Coordonnés des coins du damier
        self.minLimitx_damier=self.OFX+2
        self.minLimity_damier= self.OFY+2
        self.maxLimitx_damier=self.minLimitx_damier+(self.taille_damier)*self.CASE
        self.maxLimity_damier=self.minLimity_damier+(self.taille_damier)*self.CASE

        lettres_copy= dict(self.lettres)  #On fait une copie du dictionnaire
        lettres_poids_tuples=[]
        for lettre,poids in lettres_copy.items():
            lettres_poids_tuples+= [lettre]*poids
        
        if multijoueur:
                self.g.afficherTexte("Le joueur 1 commence ", self.minLimitx_damier+200,self.maxLimity_damier+80)
                self.g.afficherTexte("Vous jouez chacun votre tour ", self.minLimitx_damier+200,self.maxLimity_damier+100)
                self.g.afficherTexte(f"{self.joueur2_nom}",830,90,"orange")
                self.score2=self.g.afficherTexte("0 point",830,150)                
                self.score1=self.g.afficherTexte("0 point",130,150)           
                self.g.afficherTexte(f"{self.joueur_nom}",130,90,"orange")
        
        
    ############# Création/affichage du damier ################################
        for i in range (self.taille_damier):
            for j in range (self.taille_damier):

                #On affiche la case
                cellule=self.g.dessinerRectangle(self.OFX+j*self.CASE+2,self.OFY+i*self.CASE+2, self.CASE-4, self.CASE-4,self.couleur_case)
                self.cellules_damier[(i,j)]=cellule
                #On génère une lettre "aléatoirement" prenant compte son poids (valeur dans le dictionnaire (self.lettres))
                lettre=random.choice(lettres_poids_tuples)
                lettres_copy[lettre] -=1 #On enlève une fréquence/poids à la lettre choisie

                #On définit les clefs du diccionaire comme les coordonnées (uniques)
                #Par conséquent, les valeurs associées sont les lettres (pas uniques forcément)
                self.lettres_damier[(i,j)]=lettre.lower()

                #On centre les coordonnés de l'affichage de la lettre
                x = self.OFX + j * self.CASE + self.CASE / 2
                y = self.OFY + i * self.CASE + self.CASE / 2
                #Et on affiche la lettre

                self.g.afficherTexte(lettre, x, y,"orange",self.taille_lettre)
        self.exit_boutton=self.g.afficherImage(0, 0,"EL-MASSAUDI_GINIEIS\exit_bottom_icon.png")
        self.g.actualiser()
 
        
 
    
    "Methode qui nous permet de supprimer tous les changements de couleurs et lignes lorsqu'on clique sur des cases"
             
    def supprimer_trace(self):
  
        #Efface les lignes
        for lignes in self.lignes_dessinees:
            self.g.supprimer(lignes)

        #Effaces le changement de couleur
        for cases in self.cases_selectionnees:
            self.g.changerCouleur(cases,self.couleur_case)
     
 
    
        """Boucle principale du jeu etape1/multijoeur"""
    def play(self,multijoueur):
        #On enregistre le temps auquel le jeu a commencé
        time_debut=time.time()
        temps_ecoule=0
        #Ensemble des lignes dessiné entre les cases
        self.lignes_dessinees=set()
        #Ensemble d'objet avec couleur changée
        self.cases_selectionnees=set()
            
        while temps_ecoule<self.temps_de_jeu:
            #Affichage du temps restant
            self.g.afficherTexte("Temps Restant:", self.minLimitx_damier+200, self.maxLimity_damier+150,"white",20)
            chrono=self.g.afficherTexte(f"{self.temps_de_jeu-int(temps_ecoule)} ", self.minLimitx_damier+200, self.maxLimity_damier+200,"red",40)
            self.g.actualiser()
            self.g.pause(0.2)
            self.g.supprimer(chrono)
            self.g.actualiser()
            
            clic=self.g.recupererClic()
            #Tant qu'on clique sur rien, on recalcule le temps
            if clic==None:
                temps_ecoule=time.time()-time_debut
                continue
            #On determine les coord de la lettre/case cliquee par rapport
            #au damier. Exemple: premiere case coord=(0,0)   
            x_case=( clic.y - self.OFY) // self.CASE
            y_case= (clic.x - self.OFX) // self.CASE
            coord_case=x_case,y_case
            
            #Si on clique sur le damier
            if  0<=x_case<self.taille_damier and 0<=y_case<self.taille_damier:
                #Si case déjà sélectionné
                if coord_case in self.cases_selected:
                    continue
                #On ajoute la case au cases selectionnées
                self.cases_selected.append(coord_case)
                
                #On traite le cas de la première case
                    #Pour avoir un affichage différent
                if len(self.cases_selected)==1:
                    #La lettre est obtenue à partir des coord de la case
                    lettre=self.lettres_damier.get(coord_case)
                    self.mot_saisie+=lettre.lower()
                    for case in self.cellules_damier.keys():
                        #Si les coord d'une case du diccionaire est égale
                            #à celle de notre case selectionnées
                        if case == coord_case:
                            first_case=self.cellules_damier.get(case)
                            self.g.changerCouleur(first_case, "magenta")
                            self.cases_selectionnees.add(first_case)
                    #Emplacement du bouton verification dépendant du mode de jeu
                    if multijoueur:
                        vx,vy=-180,self.maxLimity_damier
                    else:
                        vx,vy=0,0
                    self.bouton_verification=self.g.afficherImage( self.maxLimitx_damier+120+vx , vy , "EL-MASSAUDI_GINIEIS/test_word_bottom_icon.png" )
                    
                    continue 
                   
                if not (self.voisins_etape1(self.cases_selected[-1], self.cases_selected[-2])):
                    #Si ils sont pas voisins on le retire de la liste
                    self.cases_selected.pop()
                    continue
                else:
                    for coord_lettres in self.lettres_damier:
                        #Même fonctionnement que pour la première case
                        lettres=self.lettres_damier.get(coord_lettres)
                        if coord_case==coord_lettres:
                            self.mot_saisie+=lettres.lower()
                            for case in self.cellules_damier.keys():
                                if case==coord_case:
                                    case_cliquee=self.cellules_damier.get(case)
                                    self.g.changerCouleur(case_cliquee, "green")
                                    self.cases_selectionnees.add(case_cliquee)
                        #Affichage de lignes entre les cases cliqués
                        if len(self.cases_selected)>1:
                            for i in range (len(self.cases_selected)-1):
                                coord_premiere_case=self.cases_selected[i]
                                coord_deuxieme_case=self.cases_selected[i+1]
                                centre_premiere_case=self.OFX + (coord_premiere_case[1] + 0.5) * self.CASE, self.OFY + (coord_premiere_case[0] + 0.5) * self.CASE
                                centre_deuxieme_case=self.OFX + (coord_deuxieme_case[1] + 0.5) * self.CASE, self.OFY + (coord_deuxieme_case[0] + 0.5) * self.CASE
                                lignes_dessinnees=self.g.dessinerLigne(centre_premiere_case[0], centre_premiere_case[1] , centre_deuxieme_case[0], centre_deuxieme_case[1], "red")
                                self.lignes_dessinees.add(lignes_dessinnees)                                   
            #Si on clique hors du damier
            else:
                #En cas d'avoir déjà selectionné au moins une case
                #On peut verifier le mot en cours
                if len(self.cases_selected)>0:
                    if self.bouton_verification.x<clic.x<self.bouton_verification.x+50 and self.bouton_verification.y<clic.y<self.bouton_verification.y+50:
                        self.verification(multijoueur)
                        continue
                #Si on veut quitter le jeu
                if self.exit_boutton.x<clic.x<self.exit_boutton.x+40 and self.exit_boutton.y<clic.y<self.exit_boutton.y+40:
                    self.g.fermerFenetre()
                    break
                if not multijoueur:
                    if self.help_boutton.x<clic.x<self.help_boutton.x+70 and self.help_boutton.y<clic.y<self.help_boutton.y+70:
                        #On initialise à nouveau
                        self.cases_selected=[]
                        self.mot_saisie=""
                        self.supprimer_trace()
                        self.g.actualiser()
                        self.cases_selectionnees=set()
                        self.lignes_dessinees=set()
                        #on lance la methode qui fourni des indices aleatoirement
                        self.aide_joueur(self.premier_indice)
                        self.premier_indice=False
                        #On le met a faux pour pas crée l'arbre tout le temps
                        self.g.actualiser()
                        self.g.pause(self.temps_transition)
                        self.supprimer_trace()
                        self.lignes_dessinees=set()
                        self.cases_selectionnees=set()
                        self.lignes_dessinees=set()
        if temps_ecoule>=self.temps_de_jeu:
            self.g.fermerFenetre()
            print("temps écoulé!!!")
  

  
 
    """"Compare la derniere case cliqué avec la case actuelement cliqué"""
    def voisins_etape1(self,last_click,click):
        return abs(last_click[0]-click[0])<=1 and abs(last_click[1]-click[1])<=1 and not (last_click==click)
        # On calcule la valeur absolue de la différence entre les coordonnées         
        # Si ils sont inférieur ou égale à 1, alors ils sont voisins
        # Et on regarde si l'on a pas cliqué sur la même case
        # Retourne True ou False   
 
    
 
            
    """"Vérifie si le mot saisie est correct pour l'étape 1/mode multijoueur avec la variable multijoueur qui indique si l'on joue seul ou non"""
    def verification(self,multijoueur):
       
        if self.mot_saisie in self.words_french:          
            #Si c'est vrai c'est au tour du joueur 2
            if self.joueur2:
                        #Si un des deux joueurs a trouvé le mot 
                        if (self.mot_saisie in self.liste_j1) or (self.mot_saisie in self.liste_j2):
                            #On affiche un message
                            message=self.g.afficherTexte("Le mot avait déjà était trouvé", self.OFX+(self.taille_damier*self.CASE)//2,self.OFY+self.taille_damier*self.CASE+50)
                        #Si personne l'a trouvé 
                        else:
                            message=self.g.afficherTexte(f"Ton mot <{self.mot_saisie}> est valide", self.OFX+(self.taille_damier*self.CASE)//2,self.OFY+self.taille_damier*self.CASE+50)
                            #On ajoute ajoute le mot dans la liste joueur 2
                            self.liste_j2.append(self.mot_saisie)
                            self.score_joueur2+=10
                            #On actualise le score
                            self.g.supprimer(self.score2)
                            self.score2=self.g.afficherTexte(f" {self.score_joueur2} points",830,150)
                            #On la lance la fonction affichage_mots_trouves_etape1 pour actualisé la liste des mots trouvé
                            self.affichage_mots_trouves_etape1(multijoueur)
                        #C'est au tour du joueur 1
                        self.joueur2=False
                        
            #Le joueur 1 joue   
            else:                
                  if  (self.mot_saisie in self.liste_j1) or (self.mot_saisie in self.liste_j2):                           
                            message=self.g.afficherTexte("Le mot avait déjà était trouvé", self.OFX+(self.taille_damier*self.CASE)//2,self.OFY+self.taille_damier*self.CASE+50)
                            #On change de tour 
                            if multijoueur:    
                                self.joueur2=True
                  else:
                            message=self.g.afficherTexte(f"Ton mot <{self.mot_saisie}> est valide", self.OFX+(self.taille_damier*self.CASE)//2,self.OFY+self.taille_damier*self.CASE+50)
                            self.liste_j1.append(self.mot_saisie)
                            self.score+=10
                            self.g.supprimer(self.score1)                     
                            #Actualise la liste des mots trouvés
                            self.affichage_mots_trouves_etape1(multijoueur)
                            #Si c'est en mode seul
                            if not multijoueur:
                                            #On affiche le score ailleur que lorsque l'on joue a deux 
                                            self.score1=self.g.afficherTexte(f"{self.score} points",self.maxLimitx_damier+150,150)
                                            
                            else:
                                #On affiche le score ailleur que lorque l'on joue seul
                                    self.score1=self.g.afficherTexte(f"{self.score} points",150,150)
                                    #On change de tour 
                                    self.joueur2=True
        #Si le mot n'est pas dans le dictionnaire
        else:
                message=self.g.afficherTexte(f"Ton mot <{self.mot_saisie}> n'est pas valide", self.OFX+(self.taille_damier*self.CASE)//2,self.OFY+self.taille_damier*self.CASE+50)                 
    
        #On met une pause en fonction du temps qu'on a initié dans le init
        self.g.pause(self.temps_transition)        
        #On supprime les messages, les traces et bouton de vérification
        self.g.supprimer(message)
        self.supprimer_trace()
        self.g.supprimer(self.bouton_verification)
        #On remet a zéro les variables pour le prochain tour 
        self.mot_saisie=""
        self.cases_selected=[]
        self.lignes_dessinees=set()
        self.cases_selectionnees=set()
        self.g.actualiser()



        
    """"Affiche les mots trouvés pour l'étape 1/mode multijoueur en fonction de si l'on joue seul ou non """
    def affichage_mots_trouves_etape1(self,multijoueur):
        #Si on joue a deux
        if multijoueur:
             #Si c'est le tour du joueur 2
             if self.joueur2:
                #On affiche le dernier mot de sa liste 
                self.g.afficherTexte(f"{self.liste_j2[-1]}", self.maxLimitx_damier+120 , 40*len(self.liste_j2)+150,"red",18)
             #Si c'est le tour du joueur 1 
             else:
                #On affiche le dernier mot de sa lite
                self.g.afficherTexte(f"{self.liste_j1[-1]}", self.minLimitx_damier-180 , 40*len(self.liste_j1)+150,"red",18)
        #Si on joue seul les mots toruvé ne sont pas affiché au même endroit     
        else:
            self.g.afficherTexte(f"{self.liste_j1[-1]}", self.maxLimitx_damier+100 , 40*len(self.liste_j1)+150,"red",18) 




    """Fonction donnant un coup de pouce à l'utilisateur"""
    def aide_joueur(self, premier_indice):
        #On distingue les cas pour ne pas charger plusieurs fois l'arbre
        if premier_indice:
            self.arbre = self.lecture_trie()
            #On le met a vrai pour indiquer qu'on veut pas d'affichage des mots
            self.search_mots_etape3(True)
        
        
        def trouver_mot_trier(dictionnaire, mot):
            def recherche(x,y, mot_trier, visite):
                #On verifie si le mot formé/trié est le mot donné par l'arbre
                if len(mot_trier) == len(mot):
                    return mot_trier
                
                for voisin in voisins(x,y):
                    #On vérifie si son voisin a la lettre correspondante au mot
                    if voisin not in visite and dictionnaire[voisin] == mot[len(mot_trier)]:
                        visite.add(voisin)
                        #appel recursif avec le voisin en ajoutant la lettre du voisin au mot trier
                        parcours= recherche(voisin[0],voisin[1], mot_trier + [voisin], visite)
                        if parcours:
                            return parcours
                        #Si le mot trie ne correspond pas au mot/mauvais chemin
                        #On enlève le voisin
                        visite.remove(voisin)
            
            def voisins(x, y):
                # Parcourt toutes les coordonnées voisines de la case (x, y)
                for dx, dy in [(i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]:
                    # Calcule les coordonnées du voisin
                    voisin = (x + dx, y + dy)
                    # Si le voisin est présent dans le dictionnaire de cases valides
                    if voisin in dictionnaire:
                        # Yield permet de renvoyer le voisin comme résultat de la fonction, sans arrêter la boucle for
                        yield voisin

            #On parcours toutes les lettres du dictionnaire
            #Sans oublier que ce dictionnaire contient tous les couples
            #clefs/valeurs (coord,lettre) des caractères du mot qu'on souhaite trouver
            for (x,y) in dictionnaire:
                if dictionnaire[(x,y)] == mot[0]:
                    #ajout de la case vistées 
                    visite = {(x,y)}
                    #et on lance la fonction qui cherche le chemin/trie
                    parcours= recherche(x,y, [(x,y)], visite)
                    if parcours:
                        return parcours
            #Si le mot n'est pas dans le damier
            #Ok car arbre bien construit
            return "¿mot pas dans le damier?"
        mot_hazard = ""
        while len(mot_hazard) < 3:
            mot_hazard = random.choice(list(self.set_de_mots_trouves_etape3))
        print(mot_hazard)
        coord_cases = {}
        #Parcourt toutes les lettres du mot aleatoire
        for i, lettre in enumerate(mot_hazard):
            #en parcourant toutes les cases du damier
            for coord in self.lettres_damier:
                if self.lettres_damier[coord].lower() == lettre.lower():
                    coord_cases[coord] = lettre
        #Là on a un dictionnaire avec toutes les cases possibles
        #On cherche donc la combinaison "correccte" abouttissant au mot
        cases_formant_le_mot=trouver_mot_trier(coord_cases,mot_hazard)
        #On enlève deux dernières case pour que ça reste un indice et pas une reponse
        cases_indice=cases_formant_le_mot[:-2]
        
        #Affichage graphique comme dans play()
        if cases_indice[0] in self.cellules_damier:
            print("premiere cellule ok")
            premiere_cellule=self.cellules_damier[cases_indice[0]]
            self.g.changerCouleur(premiere_cellule, "magenta")
            self.cases_selectionnees.add(premiere_cellule)
        for cases in cases_indice[1:]:
            if cases in self.cellules_damier:
                cellule=self.cellules_damier[cases]
                self.g.changerCouleur(cellule, "pink")
                self.cases_selectionnees.add(cellule)
        for i in range (len(cases_indice)-1):
            coord_premiere_case=cases_indice[i]
            coord_deuxieme_case=cases_indice[i+1]
            centre_premiere_case=self.OFX + (coord_premiere_case[1] + 0.5) * self.CASE, self.OFY + (coord_premiere_case[0] + 0.5) * self.CASE
            centre_deuxieme_case=self.OFX + (coord_deuxieme_case[1] + 0.5) * self.CASE, self.OFY + (coord_deuxieme_case[0] + 0.5) * self.CASE
            lignes_dessinnees=self.g.dessinerLigne(centre_premiere_case[0], centre_premiere_case[1] , centre_deuxieme_case[0], centre_deuxieme_case[1], "red")
            self.lignes_dessinees.add(lignes_dessinnees)



    
    """Recherche tous les mots avec les lettres du damier qui sont présents dans le dictionnaire 
    en utilisant la méthode de recherche en profondeur à travers des recursions. 
    Cette méthode stocke les mots trouvés dans un set et retourne le set à la fin de la fonction.
    """
    def search_mots_etape2(self):
        
        def recherche_profondeur(line, column, actuel_mot, cell_visited):
            
            # Si la case a déjà été visitée, on arrête cette étape
            if (line, column) in cell_visited:
                return

            # On ajoute la lettre au mot qu'on fait
            actuel_mot += self.lettres_damier[line, column]
            if actuel_mot.lower() not in set_de_mot_etape2:
                    
                # Si le mot est dans notre liste de mots français
                if actuel_mot.lower() in self.words_french:
                    # On l'ajoute à notre set de mots trouvés
                    set_de_mot_etape2.add(actuel_mot.lower())
                    #Affichage des mots trouvés
                    if (len(set_de_mot_etape2))<30:
                        
                        self.g.afficherTexte(f"{actuel_mot.lower()}", self.maxLimitx_damier+150, 100+(len(set_de_mot_etape2))*15,"red",14)
                        self.g.actualiser()
                    elif (len(set_de_mot_etape2))<60:
                        self.g.afficherTexte(f"{actuel_mot.lower()}", self.maxLimitx_damier+190, 100+((len(set_de_mot_etape2))-29)*15,"red",14)
                        self.g.actualiser()
                    elif (len(set_de_mot_etape2))<90:
                            
                        self.g.afficherTexte(f"{actuel_mot.lower()}", self.maxLimitx_damier+190, 100+((len(set_de_mot_etape2))-59)*15,"red",14)
                        self.g.actualiser()
                    else:
                        self.g.afficherTexte(f"{actuel_mot.lower()}", self.maxLimitx_damier+190, 100+((len(set_de_mot_etape2))-89)*15,"red",14)
                        self.g.actualiser()
            # Il faut regarder les cases du voisinage non visitées encore
            cell_visited.add((line, column))
            # On regarde chaque voisin parmi la liste des voisins_etape2_3 (voisinage de la case)
            for voisin in self.voisins_etape2_3(line, column):
                # Si on n'a pas visité le voisin
                if voisin not in cell_visited:
                    # On relance la recherche à partir de la position du voisin
                    recherche_profondeur(voisin[0], voisin[1], actuel_mot, cell_visited)
            # On enlève la lettre du mot en création
            actuel_mot = actuel_mot[:-1]
            # Et on l'enlève de la liste des cases visitées
            cell_visited.remove((line, column))
        
        set_de_mot_etape2=set()
        for line in range(self.taille_damier):
            for column in range(self.taille_damier):
                recherche_profondeur(line, column, "", set())
        return(set_de_mot_etape2)




    """Fonction récursive de recherche similaire mais en utilisant un arbre du
    dictionnaire français
    Elle stocke les mots trouvés dans le set_de_mots_trouves_etape3
    """               
    def recursion_etape3(self, ligne, colonne, mot_actuel, noeud_actuel,visite):
        if noeud_actuel.mot_fini:
            self.set_de_mots_trouves_etape3.add(mot_actuel)
        
        #On regarde les voisins non visités du noeud_Actuel
        for voisin in self.voisins_etape2_3(ligne, colonne):
            if voisin not in visite:
                nouveau_mot = mot_actuel + (self.lettres_damier[voisin[0], voisin[1]]).lower()
                #On recupere le noeud correspondant au nouveau mot formé
                nouveau_noeud = noeud_actuel.enfants.get(nouveau_mot[-1])
                if nouveau_noeud:
                    #Si le nouveau_Noeud existe dans l'arbre
                    visite.append(voisin)
                    #On fait une visite récursive
                    self.recursion_etape3(voisin[0], voisin[1], nouveau_mot, nouveau_noeud,visite)
                    visite.pop()
  
        
        """Le booléen etape1 est vrai lorsque on utilise les indices dans l'etape1
            on utilise la recherche de l'etape 3 qui est beacoup plus rapides"""
    def search_mots_etape3(self,etape1=False):
        racine = self.arbre
        for ligne in range(self.taille_damier):
            for colonne in range(self.taille_damier):
                cases_visitees=[]
                cases_visitees.append((ligne,colonne))
                mot = (self.lettres_damier[ligne, colonne]).lower()
                #On récupère le noeud correspondant au mot
                noeud = racine.enfants.get(mot)
                if noeud:
                    self.recursion_etape3(ligne, colonne, mot, noeud,cases_visitees)
        #Si etape1 (<=> mode indice) alors on recupère les mots trouvés
        if etape1:
            return
        else:    
            self.affichage_etape3()
        
   
    """ affichage des mots de l'étape 3"""
    def affichage_etape3(self):
        
        #On fixe un pas pour
            #Séparer les colonnes de mots affichés
            #Le nombre de cases par colonnes
        pas = 50
        nb_cases = (len(self.set_de_mots_trouves_etape3) - 1) // 40 + 1  
        #Liste des lignes pour chaque colonne
        liste = [50 + i * pas for i in range(nb_cases)]
        y_position = 80
        y_pas = 15
        self.g.afficherTexte("Les mots trouvés par l'etape 3 sont:",1.30*self.maxLimitx_damier , 20,"White",15)
        for i, mot in enumerate(self.set_de_mots_trouves_etape3):
            #On change de colonne tous les 40 mots
            x = liste[i // 40]
            #Position verticale en fonction de la liste des lignes
            y = y_position + (i % 40) * y_pas
            self.g.afficherTexte(f"{mot}", self.maxLimitx_damier + x, y, "red", 10)
            self.g.pause(0.002)
            self.g.actualiser()

            
       
    """Crée un liste avec les voisins d'une case"""
    def voisins_etape2_3(self,x,y):
        voisins=[]
        for ligne in range (max(0,x-1),min(self.taille_damier,x+2)): #On ne veut pas sortir du damier
            for colonne in range (max(0,y-1),min(self.taille_damier,y+2)):
                if ligne!=x or colonne!=y:  #On ne comte pas la case elle même
                    voisins.append((ligne,colonne))
        return voisins
        #Retourne la liste des voisins
    
    #Dépendant du mode de jeu on sauvegarde les scores des joueurs
    def score_enregistres(self,deuxiemejoueur=False):
        #On ouvre un exel ou l'on note les scores avec le nom
        with open ("base_de_donees.csv","a",newline="") as file:
             writer = csv.writer(file, delimiter=',')
              # Ajout d'un nouvel enregistrement de jeu
             writer.writerow([self.joueur_nom, self.score])
        if deuxiemejoueur:
            with open ("base_de_donees.csv","a",newline="") as file:
                 writer = csv.writer(file, delimiter=',')
                  # Ajout d'un nouvel enregistrement de jeu
                 writer.writerow([self.joueur2_nom, self.score_joueur2])
    def classement(self):

        #On modifie le fichier csv et on le stocke dans un dataframe pandas
        datafframe = pd.read_csv("EL-MASSAUDI_GINIEIS/base_de_donees.csv", header=None, names=["Joueur", "Score"])
                                                        #Pas d'entête sur notre fichier
        datafframe['Score'] = datafframe['Score'].astype(int)
        #On convertis les scores en nombre
        # Grouper les scores par joueur
        classement = datafframe.groupby("Joueur").sum()
                                #Et on somme tous ses scores
        # Trier le classement par ordre décroissant de score
        classement = classement.sort_values("Score", ascending=False)
                #Méthode sort.values de panda en spécifiant la colonne Score
                
        print("le classement des meilleurs joueurs est:")
        print(classement)
        print("merci d'avoir joué!")
"""le but de cette classe est de stocker le diccionaire français sous la forme
    d'un arbre qui stocke chaque caractère des mots dans des noeuds enfants
                                                    """
class Noeud():
    def __init__(self,caractere=None):
        #Initialisasion de la classe avec un caractère non existant d'abord
        self.enfants={} #Dictionnaire stockant les noeuds enfants
        self.mot_fini=False  #En début de recherche on l'initialise a faux


    """Methode qui prend des mots du dico_francais et les garde dans notre 
                                    arbre                 """
    def save(self,mot):
        #On prend un mot commençant par la racine de l'arbre
        node=self
        #On parcourt tous les caractère du mot
        for caract in mot:

            #Si caract pas présent dans les enfants du Noeud
            if caract not in node.enfants:
                #On ajoute un nouveau Noeud pour ce caract
                node.enfants[caract]=Noeud(caract)
                #Les caract ici sont les clefs <=> uniques.
            #Sinon on se déplace dans le Noeud associé au caractère suivant
            node=node.enfants[caract]

        """Fin de la boucle for <=> fin du mot
                                <=> dernier Noeud visité"""
        #On indique alors que le mot est fini
        node.mot_fini=True

    """    #fonction qui prend un mot et cherche s'il est présent dans l'arbre' 
            fait précedement. Si mot présent ---> True, false sinon  """
    def cherche(self,mot):
        node=self
        #On regared tous les caract du mot
        for caract in mot:
            if caract in node.enfants:
                node = node.enfants[caract]
            else:
                #S'il n'est pas dans les neuds enfants, alors ce n'est pas un mot valide
             return False
        #On est arrivé au bout du mot
        #Verif si dernier Noeud visité correspond à la fin du mot
        return node.mot_fini






j=jeu()
j.menu()
j.classement()


#On essaye déroulement normal du jeu
# try :
#     print("////////////////////////////////////////////////////////////////")
#     j.menu()

# #Si erreur on affiche le traceback(message d'erreur sur la console)
# except Exception as error:
#     # j.menu.fermerFenetre()
#     j.g.fermerFenetre()
#     import traceback
#     trace=traceback.format_exc()
#     print("La ligne:")
#     print(trace)
#     print("tas une erreur")
#     print(error)
# except KeyboardInterrupt:
#     # j.menu.fermerFenetre()
#     j.g.fermerFenetre()
