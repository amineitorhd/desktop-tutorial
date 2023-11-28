#projet long pokémon

from tkinter import *
import pandas as pds
from functools import partial



fichier=pds.read_csv("Laurine_data_manager/pokemon.csv",index_col="#")   #pour lire le fichier en DataFrame


#interface graphique
def recherchePokemon(lbl,texte):
    resultat=fichier[fichier["Name"]==texte.get()] 
    lbl.config(text=resultat)
    #faire 2 cas, pokemon existe ou non
    
def rechercheCriteres(lbl,legend, vitesse):
    print (legend.get())
    resultat=fichier[(fichier["Legendary"]==legend.get()) & (fichier["Speed"]>=vitesse.get()) ]    
    lbl.config(text=resultat)    
    #réussir à faire un seul bouton et une seule fonction
    #marche pas si il y a que la vitesse de rensaignée
    #si on met rien, legend==False, peut pas initialiser à vrai et faux
    # faire en sorte que si rien n'est entré, on face aussi avec les true
    
    
        

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
    
      
    
    #critère 2 : vitesse
    # c'est un entry
    frameVit=Frame(root, bd=1, relief='solid')
    
    vitesse = Label(frameVit, text="Vitesse supérieure ou égale à : ")
    vitesse.grid(row=0,column=0)
    
    choixVit = IntVar(frameVit)
    
    vitessemin=Entry(frameVit,textvariable=choixVit)
    vitessemin.grid(row=0,column=1)
    
    frameVit.grid()
    
    
    #critère 3 : génération
    frameGen=Frame(root, bd=1, relief='solid')
    
    generation = Label(frameGen, text="Génération : ")
    generation.grid()
    
    choixGen1 = IntVar(frameGen)
    gen1 = Checkbutton(frameGen, text="1", variable=choixGen1, offvalue=0, onvalue=1)  #offvalue quand c'est décoché
    gen1.grid(row=0,column=1)
    
    choixGen2 = IntVar(frameGen)
    gen2 = Checkbutton(frameGen, text="2", variable=choixGen2, offvalue=0, onvalue=2)
    gen2.grid(row=0,column=2)
    
    choixGen3 = IntVar(frameGen)
    gen3 = Checkbutton(frameGen, text="3", variable=choixGen3, offvalue=0, onvalue=3)
    gen3.grid(row=0,column=3)
    
    choixGen4 = IntVar(frameGen)
    gen4 = Checkbutton(frameGen, text="4", variable=choixGen4, offvalue=0, onvalue=4)
    gen4.grid(row=0,column=4)
    
    choixGen5 = IntVar(frameGen)
    gen5 = Checkbutton(frameGen, text="5", variable=choixGen5, offvalue=0, onvalue=5)
    gen5.grid(row=0,column=5)
    
    choixGen6 = IntVar(frameGen)
    gen6 = Checkbutton(frameGen, text="6", variable=choixGen6, offvalue=0, onvalue=1)
    gen6.grid(row=0,column=6)
    
    
    
    frameGen.grid()
    
    
    
    
    bouton2=Button(root,text="rechercher")
    bouton2.grid()
    
    bouton2.config(command=partial(rechercheCriteres,lbl=recherche,legend=choixLeg, vitesse=choixVit))
    
    root.mainloop()
    
#vérifie si valeurs manquantes :
#print(fichier[fichier["Legendary"]=="NaN"])
#print(fichier[fichier["Speed"]=="NaN"])
   
   
fenetre()