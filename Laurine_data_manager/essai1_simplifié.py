#projet long pokémon
#sur cette version : peut seulement tester les critères un par un

from tkinter import *
import pandas as pds
from functools import partial



fichier=pds.read_csv("pokemon.csv",index_col="#")   #pour lire le fichier en DataFrame


#interface graphique
def recherchePokemon(lbl,texte):
    resultat=fichier[fichier["Name"]==texte.get()] 
    lbl.config(text=resultat)
    #faire 2 cas, pokemon existe ou non
    
def rechercheLeg(lbl,legend):
    resultat=fichier[fichier["Legendary"]==legend.get() ]    
    lbl.config(text=resultat)    
    
def rechercheVit(lbl,vitesse):
    resultat=fichier[fichier["Speed"]>=vitesse.get() ]    
    lbl.config(text=resultat) 
    
def rechercheGen(lbl,generation):
    resultat=fichier[fichier["Generation"]==generation.get() ]    
    lbl.config(text=resultat) 
    
def rechercheHP(lbl,hp):
    resultat=fichier[fichier["HP"]>=hp.get() ]    
    lbl.config(text=resultat) 
    
    
        

def fenetre():
    root=Tk()
    root.title("pokedex")
    
    
    # Recherche par le nom
    f1 = Frame(root, bd=1, relief='solid')
    
    nom = Label(f1, text="Nom : ")
    nom.grid(row=0,column=0)
   
    text=StringVar(root)    #que fait cette ligne déjà?
    entry=Entry(f1,textvariable=text)
    entry.grid(row=0,column=1)
   
    bouton=Button(f1,text="rechercher")
    bouton.grid(row=0,column=2)
    
    f1.grid(row=0,column=0)
    
    recherche = Label(root, text="")
    recherche.grid(row=1)
    
    
    bouton.config(command=partial(recherchePokemon,lbl=recherche,texte=entry))
    
    
    
    #critère 1 : légendaire
    frameLeg=Frame(root, bd=1, relief='solid')
    
    legendaire = Label(frameLeg, text="Légendaire : ")
    legendaire.grid()
    
    choixLeg = BooleanVar(frameLeg)
    
    oui = Radiobutton(frameLeg, text="oui", variable=choixLeg, value="True")
    oui.grid(row=1,column=0)
    
    non = Radiobutton(frameLeg, text="non", variable=choixLeg, value="False")
    non.grid(row = 2, column = 0)
    
    frameLeg.grid()  
    
    bouton2=Button(root,text="rechercher")
    bouton2.grid()
    
    bouton2.config(command=partial(rechercheLeg,lbl=recherche,legend=choixLeg))
    
    
    #critère 2 : vitesse
    # c'est un entry
    frameVit=Frame(root, bd=1, relief='solid')
    
    vitesse = Label(frameVit, text="Vitesse supérieure ou égale à : ")
    vitesse.grid(row=0,column=0)
    
    choixVit = IntVar(frameVit)
    
    vitessemin=Entry(frameVit,textvariable=choixVit)
    vitessemin.grid(row=0,column=1)
    
    frameVit.grid()
    
    bouton3=Button(root,text="rechercher")
    bouton3.grid()
    
    bouton3.config(command=partial(rechercheVit,lbl=recherche,vitesse=choixVit))
    
    
    
    #critère 3 : generation
    frameGen=Frame(root, bd=1, relief='solid')
    
    gener = Label(frameGen, text="génération : ")
    gener.grid()
    
    choixGen = IntVar(frameGen)
    
    gen1 = Radiobutton(frameGen, text="1", variable=choixGen, value="1")
    gen1.grid(row=1,column=0)
    
    gen2 = Radiobutton(frameGen, text="2", variable=choixGen, value="2")
    gen2.grid(row = 1, column = 1)
    
    gen3 = Radiobutton(frameGen, text="3", variable=choixGen, value="3")
    gen3.grid(row=1,column=2)
    
    gen4 = Radiobutton(frameGen, text="4", variable=choixGen, value="4")
    gen4.grid(row = 1, column = 3)
    
    gen5 = Radiobutton(frameGen, text="5", variable=choixGen, value="5")
    gen5.grid(row = 1, column = 4)
    
    gen6 = Radiobutton(frameGen, text="6", variable=choixGen, value="6")
    gen6.grid(row=1,column=5)

    frameGen.grid()  
    
    bouton4=Button(root,text="rechercher")
    bouton4.grid()
    
    bouton4.config(command=partial(rechercheGen,lbl=recherche,generation=choixGen))
    
    
    #critère 2 : HP
    frameHP=Frame(root, bd=1, relief='solid')
    
    HP = Label(frameHP, text="HP supérieur ou égal à : ")
    HP.grid(row=0,column=0)
    
    choixHP = IntVar(frameHP)
    
    HPmin=Entry(frameHP,textvariable=choixHP)
    HPmin.grid(row=0,column=1)
    
    frameHP.grid()
    
    bouton5=Button(root,text="rechercher")
    bouton5.grid()
    
    bouton5.config(command=partial(rechercheHP,lbl=recherche,hp=choixHP))
    

    
    
    
    root.mainloop()
    
#vérifie si valeurs manquantes :
#print(fichier[fichier["Legendary"]=="NaN"])
#print(fichier[fichier["Speed"]=="NaN"])
   
   
fenetre()