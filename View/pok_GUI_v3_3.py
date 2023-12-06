import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex Python GUI")
        #Initialisation taille du pokedex_GUI
        ecran_largeur = self.winfo_screenwidth()
        ecran_longeur = self.winfo_screenheight()
        self.geometry(f"{ecran_largeur-(ecran_largeur//2)}x{ecran_longeur-(ecran_longeur//2)}")
        self.minsize(500,300)


        #Initialisation fond d'ecran (avec son mode obscure)
        #On configure leur taille selon la taille de l'ecran du pc
        self.ecran=Image.open("View/fond_ecran_pokedex.jpeg").resize((ecran_largeur+20,
                                                                      ecran_longeur+25))
        self.ecran_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png").resize((ecran_largeur+20,
                                                                                        ecran_longeur+15))
        self.ecran_actuel=self.ecran  #Variable qui va permettre de switch les ecrans

        #Initialisation du fond d'ecran 
        region_scroll=(0,0,ecran_largeur,ecran_longeur)
        self.fond_ecran=Fond_Ecran(self,self.ecran,"red",True,region_de_scroll=region_scroll)
        self.fond_ecran.pack(expand=True,fill="both")




        self.filtres_avancee=Frame_dynamique_filtres(self,1.5,0.35,0.0502,True,0.4,0.80,2,teleport=(True,0.95))
        
        self.boutton_filtres_avancee=ttk.Button(self,text="Filtres",
                                              command=lambda:self.filtres_avancee.animation(self.boutton_filtres_avancee))
        self.boutton_filtres_avancee.place(relx=0.0502,rely=0.95,relwidth=0.4)

#Ordre d'initialisation important!!!
        #Initialisation de la barre de recherche
        self.zone_recherche=Frame_Recherche_simple(self,size=ecran_longeur//60)
        self.zone_recherche.place(relx=0.005,relwidth=0.4,y=0)

        #Initialisation des réglages du Pokedex_GUI
        self.configuration=Frame_dynamique_configuration(self,-0.4,0.035,0.50,False,0.4,0.2,5)
        self.config_configuration()

        #Initialisation des affichages graphiques des pokemons
        # self.affichage_pokemons=Frame_Affichage_Pokemons(self) #Frame_Affichage_Pokemons(self)
        # self.bind("<Configure>",self.gestion_fenetre)
        # self.fond_ecran.bind_all('<MouseWheel>',lambda event: self.fond_ecran.yview_scroll(-int(event.delta/60),"units"))

        self.affichage_cartes_pokemons=Frame_poke_affichage_v2(self,self.ecran)

    def config_configuration(self):
        self.image_configuration=Image.open("View/Back1.jpeg")
        self.image_configuration_obscure=Image.open("View/Back_obscure.jpeg")
        self.ecran_actuel_configuration=self.image_configuration
        self.fond_ecran_configuration=Fond_Ecran(self.configuration,self.image_configuration,"yellow")
        self.fond_ecran_configuration.pack(fill="both",expand=1)
        self.boutton_configuration=ttk.Button(self,text="Configuration",
                                                    command=self.configuration.animation).place(relx=0,
                                                    rely=0.9,relheight=0.1,relwidth=0.05)
        #Boutton permettant de switch entre mode obscure ou pas
        boutton_obscur=ttk.Button(self.fond_ecran_configuration,text="Obscure Mode",
                                command=self.actualisation_mode_obscur).pack(side="top",anchor="nw")
            
    def gestion_fenetre(self,event):
        self.fond_ecran.create_window(((self.winfo_width()//2)*0.95,0),window=self.affichage_pokemons,
                                      anchor="nw",width=(self.winfo_width()//2*1.0499))

    def actualisation_mode_obscur(self):
        if self.ecran_actuel==self.ecran:
            self.ecran_actuel=self.ecran_obscur #On swich d'ecran
        else:
            self.ecran_actuel=self.ecran
        
        if self.ecran_actuel_configuration==self.image_configuration:
            self.ecran_actuel_configuration=self.image_configuration_obscure
        else:
            self.ecran_actuel_configuration=self.image_configuration

        # if self.squirtel_actuel==self.squirtels:
        #     self.squirtel_actuel=self.squirtels_obscur
        # else:
        #     self.squirtel_actuel=self.squirtels
            
        self.fond_ecran.switch_mode_ecran(self.ecran_actuel) #On met a jour le nouveau ecran
        self.fond_ecran_configuration.switch_mode_ecran(self.ecran_actuel_configuration)
        # self.cv.switch_mode_ecran(self.squirtel_actuel)


    def affichage_info_pokemon(self,pokemon):
        print(f"tu veux plus d'info de: {pokemon}")


    def affichage_info_complete_pok(self,pokemon):
        nom=pokemon.iloc[1]
        poke_info_window=Poke_Details_Window(nom,"Model/GIF/pikachu-5.gif","Model/Characters_image/25-belle.png")
        for info in pokemon:
            ttk.Label(poke_info_window,text=f"{info}").pack(side="right")
        # Si on ferme le window, on indique d'arrêter lethred
        poke_info_window.protocol("WM_DELETE_WINDOW", poke_info_window.fermer_and_stop_thread)
        
        threading.Thread(target=poke_info_window.configuration_gif).start()  #On le traite à part pour pas perturber le fonctionnement de notre GUI.


    def demarage(self):
        self.mainloop()


class Frame_poke_affichage_v2(ttk.Frame):
    def __init__(self,mere,fond_ecran):
        super().__init__(mere)
        self.pokemons_affiches=30
        self.dico_pokemon_carte={}
        self.poke_cartes_affichees=[]


        self.place(relx=0.5,rely=0.005,relwidth=0.48,relheight=1)
        self.canvas=tk.Canvas(self,bg="magenta",scrollregion=(0,0,self.winfo_width(),self.pokemons_affiches*330))
        self.canvas.pack(fill="both",expand=1)
        
        self.frame=ttk.Frame(self)
        self.boutton_afficher_plus=ttk.Button(self.frame,text="Afficher plus")
        # self.fond_ecran=Fond_Ecran(self.frame,fond_ecran,expand_ecran=True,region_de_scroll=(0,0,500,800))
        # self.fond_ecran.pack(fill="both",expand=1)

        

        self.scroll_bar=ttk.Scrollbar(self,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.place(relx=1,rely=0,relheight=1,anchor="ne")
        self.canvas.bind_all("<MouseWheel>",lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
        self.bind("<Configure>",self.configuration_affichage)

    def affichage_poke_liste(self,poke_nom_data,initialisation=False):
        # for carte in self.poke_cartes_affichees:
        #     carte.pack_forget()
        if not initialisation:
            self.boutton_afficher_plus.pack_forget()
            self.pokemons_affiches+=30
            self.configuration_affichage(None)

        for poke_nom in poke_nom_data:
            carte=self.dico_pokemon_carte[poke_nom][0]
            carte.pack(fill="both",padx=(0,15))
            self.poke_cartes_affichees.append(carte)
        self.boutton_afficher_plus.pack(fill="both",expand=1)


    def configuration_affichage(self,_):
        if self.pokemons_affiches*330>=self.winfo_height():
            hauteur_fenetre_scroll=self.pokemons_affiches*330
            self.canvas.bind_all("<MouseWheel>",lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
            self.scroll_bar.place(relx=1,rely=0,relheight=1,anchor="ne")

        else:
            hauteur_fenetre_scroll=self.winfo_height()
            self.canvas.unbind_all("<MouseWheel>")
            self.scroll_bar.place_forget()

        self.canvas.config(scrollregion=(0,0,self.winfo_width(),hauteur_fenetre_scroll))
        self.canvas.create_window((0,0),window=self.frame,
                            width=self.winfo_width(),
                            height=hauteur_fenetre_scroll,
                            anchor="nw")

    def creation_poke_carte(self, nom, numero,image_tk=None):
        self.carte_pokemon = ttk.Frame(self.frame)
  
        
        self.fond_carte_pokemon = tk.Canvas(self.carte_pokemon, bg="#2992B0")
        self.fond_carte_pokemon.pack(fill="both",expand=True)
        self.fond_carte_pokemon.rowconfigure((0,1,2),weight=2,uniform="a")
        self.fond_carte_pokemon.rowconfigure((3),weight=1)
        self.fond_carte_pokemon.columnconfigure((0,1,2),weight=2,uniform="a")
        self.fond_carte_pokemon.columnconfigure((4,5,6,7),weight=1,uniform="a")

        # Canvas où il y aura limage du  Pokemon
        self.canvas_pokemon = tk.Canvas(self.fond_carte_pokemon, bg="black")
        if image_tk is not None:
            self.canvas_pokemon.create_image(40,40,image=image_tk,anchor="center")
            self.carte_pokemon.image_tk = image_tk #On le garde en instance pour pas qu'il se fasse elim
        self.canvas_pokemon.grid(row=0,rowspan=4,column=0,columnspan=2,sticky="nsew")


        # Labels pour nom et numero
        label_pokemon_nom = ttk.Label(self.fond_carte_pokemon, text=f"{nom}",font=("Helvetica",20),background="red")
        label_pokemon_nom.grid(row=0,rowspan=2,column=2,columnspan=2,sticky="ew")

        label_pokemon_numero = ttk.Label(self.fond_carte_pokemon, text=f"#{numero}")
        label_pokemon_numero.grid(row=2,rowspan=1,column=2,columnspan=1,sticky="nsw")


        # Canvas où il yaura les types de pkemon (en icone)
        canvas_type1 = tk.Canvas(self.fond_carte_pokemon, bg="green")
        canvas_type1.grid(row=3,column=6,columnspan=1,sticky="s")

        canvas_type2 = tk.Canvas(self.fond_carte_pokemon, bg="yellow")
        canvas_type2.grid(row=3,column=7,columnspan=1,sticky="s")

        return self.carte_pokemon,self.canvas_pokemon


    def initialisation_cartes_pokemons(self,data_pokemons):
        print("initialisation cartes:")
        for index,pokemon_info in data_pokemons.iterrows():
            poke_nom=pokemon_info.iloc[1]
            poke_numero=pokemon_info.iloc[0]
            pokemon_carte=self.creation_poke_carte(poke_nom,poke_numero)
            self.dico_pokemon_carte[poke_nom]=pokemon_carte
        print("fin initialisation")


    def bout_set_command(self,command):
        self.boutton_afficher_plus["command"]=command



#Création objet Canvas pour gerer l'affichage du fond d'ecran
#Aussi pour gerer les regions de scroll possibles
class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,ecran,fond="magenta",expand_ecran=False,affichage_pokemon=None,region_de_scroll=(0,0,500,900)):
        super().__init__(mere,bg=fond,scrollregion=region_de_scroll)
        self.image_fond_ecran=ecran

        #Si il faut afficher plus de pokemons, il faut agrandir la fenêtre
        self.expandir_ecran=expand_ecran

        #Si le canvas change de taille (<=> si fenetre change de taille (car canvas occupant toute la fenêtre))
        self.bind('<Configure>', self.config_fond_ecran)
        self.affichage_pokemon=affichage_pokemon
        #attribut affichage_pokemon: On l'utilise que pour notre fenêtre top_level


    def config_fond_ecran(self,event=None,numb_pokemons=40): #valeur arbitraire (numb de pokemons par ecran)
        #On utilise pas l'argument event fournie par "bind"    
        
        #On va ajuster le fond d'ecran selon la taille de la fenêtre
        largeur=self.winfo_width()
        hauteur=self.winfo_height()
        
        #ratio du fond d'ecran et celui de la fenêtre:
        ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
        ecran_ratio=largeur/hauteur

        if ratio_image<ecran_ratio:
            x=int(largeur)
            y=int(x/ratio_image)
        else:
            y=int(hauteur)
            x=int(y*ratio_image)

        #On actualise alors la taille de l'ecran:
        ecran_actualisee=self.image_fond_ecran.resize((x,y))
        self.ecran_actualisee_tk=ImageTk.PhotoImage(ecran_actualisee)
        #Et on la recentre pour l'expandir
        self.create_image(int(largeur/2),
                          int(hauteur/2),
                          image=self.ecran_actualisee_tk,
                          anchor="center")
        
        # if self.expandir_ecran:
        #     num_lignes=int(numb_pokemons//7) #Calculs arbitraires

        #     #On prefère cree une image en dessous l'autre pour garder la visibilité
        #     #Au lieu de redimensioner l'hauteur
        #     for i in range(num_lignes):
        #         self.create_image(0,i*y, image=self.ecran_actualisee_tk, anchor="nw")
            
        #     #On ajuste le scroll_region à chaque actualisation de l'ecran.
        #     self.config(scrollregion=(0,0,largeur,num_lignes*x-750)) #750: choisie arbitrairement

        if self.affichage_pokemon is not None:
            self.image_tk = ImageTk.PhotoImage(self.affichage_pokemon.resize((100,200)))

            # Obtenir les dimensions du Canvas
            largeur_canvas = self.winfo_width()
            hauteur_canvas = self.winfo_height()

            # Afficher l'image au centre du Canvas
            self.create_image(largeur_canvas // 2, hauteur_canvas // 2, image=self.image_tk, anchor="center")
    

    def switch_mode_ecran(self,ecran):
        self.image_fond_ecran=ecran #On change d'ecran
        self.config_fond_ecran() #on actualise le fond d'ecran


#Frame personnalisée représentant la barre de recherche
class Frame_Recherche_simple(ttk.Frame):
    def __init__(self,mere,size):
        super().__init__(mere)
        self.mere=mere

        #Initialisation de la barre de recherche
        self.nom_nombre=tk.StringVar()  #Variable des entrees
        self.entree_nm_nb=ttk.Entry(self,textvariable=self.nom_nombre,font=('Helvetica', size)) #Barre de recherche
        self.entree_nm_nb.pack(fill="x")                
        self.entree_nm_nb.insert(0, "Nom ou numéro Pokemon") #Indications à l'user
        # Liaison d'événement pour effacer le texte initial lorsqu'un clic est effectué sur l'entry
        self.entree_nm_nb.bind("<FocusIn>", self.effacer_texte)
        # Liaison d'événement pour restaurer le texte initial s'il n'y a pas de texte entré
        self.entree_nm_nb.bind("<FocusOut>", self.remettre_texte)
        #Si on appuie sur la touche return
        self.entree_nm_nb.bind('<Return>', self.rechercher)

        #Boutton pour chercher les résultats
        self.afficher_frames=True #Booleen permettant de savoir si afficher les frames des pokemons ou pas
        self.boutton_recherche=ttk.Button(mere,text="chercher!")
        self.boutton_recherche.place(relx=0.4*self.winfo_width(),y=0)

        self.resultats=ttk.Treeview(self,columns=("Id_numero","Id_nom","Caract1","Caract2"),show="headings")  #""""Tableur tkinter"""""


        self.nom_nombre.trace("w", self.ecriture_actualisation)  #Bizare car obligé 3 arguments!

    def configuration_affichage_resultats(self,filtres_affiches):
        longeur_frame=self.winfo_width()
        longeur_par_colonne=longeur_frame//len(filtres_affiches)
        self.resultats=ttk.Treeview(self,columns=("Id_nom","Id_numero","Caract1","Caract2"),show="headings")
        
        #On itère à la fois sur la liste des filtres et sur les colonnes de notre treeview
        for filtre, col in zip(filtres_affiches, self.resultats["columns"]):
            self.resultats.heading(col, text=filtre)  #On change les titres des colonnes
            self.resultats.column(col,width=longeur_par_colonne)  #On met une largeur uniforme pour chaque colonne
                                                                                #On pourrait les personalisé....
        

    #On peut recevoir de la methode trace un nombre k d'arguments qu'on va pas utiliser.
    def ecriture_actualisation(self,*args): 
        entree=self.entree_nm_nb.get()
        self.resultats.delete(*self.resultats.get_children()) #Pour effacer les trucs d'avant

        if entree!="" and entree!="Nom ou numéro Pokemon":
            self.resultats.pack(fill="x")
            nombre_elements = len(self.resultats.get_children())
            # Configuration de la hauteur de la ListBox pour qu'elle corresponde au nombre d'éléments
            # if nombre_elements>7:
            #     self.resultats.configure(height=100) #hateur max pouvant occuper!
            # else:
            #     self.resultats.configure(height=nombre_elements)

            # self.afficher_frames=False
            # data=self.boutton_recherche.invoke() #Pourquoi tkniter convert un pandas df a un str???
            # self.afficher_frames=True

            # print(data)
            # self.resultats.insert("","end",values=(entree,))
            self.boutton_recherche.invoke()  #Pourquoi conversion en str!!!!

        else:
            self.resultats.pack_forget()


    def affichage_temps_reel(self,data_set):
        for index, (nb, nm, t1, t2) in enumerate(data_set):
            self.resultats.insert(parent="", index=index, values=(nb, nm, t1, t2))


    def rechercher(self,event):
        self.pack=False
        self.boutton_recherche.invoke()  #Une nouvelle fonction car bind nous donne des arguments qu'on veut pas
        self.pack=True

    
    def effacer_texte(self,event): #Dans les deux cas on s'en sert pas du event fourni par Bind
        # Efface le texte initial lorsque l'utilisateur clique dans l'entry
        if self.nom_nombre.get() == "Nom ou numéro Pokemon":
            self.nom_nombre.set("")

        # Change la couleur du texte à noir lorsque l'utilisateur commence à taper
        self.entree_nm_nb.config(foreground="black")


    def remettre_texte(self, event):
        print("ok")
        # Restaure le texte initial si l'entry est vide

        if not self.nom_nombre.get():
            self.nom_nombre.set("Nom ou numéro Pokemon")

        # Change la couleur du texte à gris si l'entry est vide
        self.entree_nm_nb.config(foreground="grey")

        return
        x,y=self.entree_nm_nb.winfo_x(),self.entree_nm_nb.winfo_y()
        x_2,y_2=self.entree_nm_nb.winfo_width(),self.entree_nm_nb.winfo_height()
        if x<int(event.x)<x_2 and y<int(event.y)<y_2:
            print("ok")

    
    def set_command(self,command):#On reçoit la commande du boutton du Controller
        self.boutton_recherche["command"]= lambda: command(self.entree_nm_nb.get(),
                                                           self.pack) #Initialisé à True!   


#Frame personalisée représentant les configurations à la disposition de l'user
class Frame_dynamique_configuration(ttk.Frame):
    def __init__(self, mere, pos_initial, pos_final,pos_y,side_gauche,hauteur,largeur,vitesse):
        """Pos_initial:position relx avant animation
           Pos_final: position relx après animation
           pos_y: position rely
           side_gauche:booleen determinant si le frame bouge vers la gauche (True) ou vers la droite (False)
           hauteur,largeur,vitesse:[...] """
        super().__init__(mere)

        self.start = pos_initial + 0.04
        self.end = pos_final - 0.04
        self.pos_y=pos_y
        self.largeur = largeur
        self.hauteur=hauteur

        self.position = pos_initial
        self.invisible_GUI = True #dans ce cas, si Frame pas visible sur le GUI
        self.Y = side_gauche  
        self.vitesse=vitesse
        self.place(relx=self.start, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)


    def animation(self):
        if self.invisible_GUI:
            self.animation_entree()
        else:
            self.animation_sortie()


    def animation_entree(self):
        if self.Y:  
            if self.position > self.end: #Si pas arivee
                self.position -= 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_entree)
            else:
                self.invisible_GUI=False #Frame visible sur le GUI
        else:  # Si droite
            if self.position < self.end: #Si pas arivee
                self.position += 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_entree)
            else:
                self.invisible_GUI=False
  

    def animation_sortie(self):
        if self.Y:  # Si gauche
            if self.position < self.start: #Si pas arivee
                self.position += 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_sortie)
            else:
                self.invisible_GUI=True #Frame pas visible sur le GUI
        else:  #Si droite
            if self.position > self.start: #Si pas arivee
                self.position -= 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_sortie)
            else:
                self.invisible_GUI=True


#Frame personalisee representant les filtres à la disposition d el'user
class Frame_dynamique_filtres(ttk.Frame):
    def __init__(self, mere, pos_initial, pos_final, pos_x, side_haut, largeur, hauteur, vitesse,teleport):
        super().__init__(mere)
       
        self.start = pos_initial + 0.04
        self.end = pos_final - 0.04
        self.pos_x = pos_x
        self.largeur = largeur
        self.hauteur = hauteur

        self.position = pos_initial
        self.invisible_GUI = True
        self.Y = side_haut
        self.vitesse = vitesse
        self.teleport=teleport
        self.place(rely=self.start, relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
        self.position=self.teleport[1]


    def configuration_initiale(self,information):
            self.squirtels=Image.open("View/squirtels_light.jpeg")
            self.squirtels_obscur=Image.open("View/squirtels_obscur.jpg")
            self.squirtel_actuel=self.squirtels
            self.cv=Fond_Ecran(self,self.squirtels)
            self.cv.pack(fill="both",expand=1)
            # print("Je suis GUI et j'ai reçue l'info de Controller:")
            # print(information[0],"\n\n")
            for cle,valeur in information[0].items():
                if not (valeur[1]=="Id_Type"):
                    if valeur[1]=="Categorique_Type":
                        # print("\n")
                        # print(cle,information[1][cle],len(information[1][cle]))
                        ttk.Label(self.cv,text=cle).pack()
                        i=1
                        if not information[0][cle][0]:
                            for valeur_possible in information[1][cle]:
                                if f"{valeur_possible}"!="nan":
                                    if i<7:
                                        # print(i)
                                        ttk.Button(self.cv,
                                                text=f"{valeur_possible}").place(relx=0,rely=i*0.1)
                                    elif i<13:
                                        a=i-6
                                        ttk.Button(self.cv,
                                                text=f"{valeur_possible}").place(relx=0.2,rely=a*0.1)
                                    elif i<22:
                                        a=i-12
                                        ttk.Button(self.cv,
                                                text=f"{valeur_possible}").place(relx=0.4,rely=a*0.1)

                                    i+=1
                # else:
                #     print("\n\n********",cle,information[1][cle],len(information[1][cle]),"\n\n********")


    def animation(self,boutton_filtres):
        if self.invisible_GUI:
            boutton_filtres["text"]="Cacher filtres"
            
            if self.teleport[0]:
                self.place(rely=self.teleport[1], relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
            self.animation_entree()
        else:
            boutton_filtres["text"]="Filtres avancées"
            self.animation_sortie()


    def animation_entree(self):
        if self.Y:
            if self.position > self.end:
                self.position -= 0.008
                self.place(rely=self.position, relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_entree)
            else:
                self.invisible_GUI = False
        else:
            if self.position < self.end:
                self.position += 0.008
                self.place(rely=self.position, relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_entree)
            else:
                self.invisible_GUI = False


    def animation_sortie(self):
        if self.Y:
            if self.position < self.start:
                self.position += 0.008
                self.place(rely=self.position, relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_sortie)
            else:
                self.invisible_GUI = True
        else:
            if self.position > self.start:
                self.position -= 0.008
                self.place(rely=self.position, relx=self.pos_x, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_sortie)
            else:
                self.invisible_GUI = True

#Frame qui affiche tous les pokemons (graphiquement)
class Frame_Affichage_Pokemons(ttk.Frame):
    def __init__(self, mere):
        super().__init__(mere)
        self.dico_pokemons_cartes=[]
        self.dico_image_cartes=[]
        # tk.Canvas(self,bg="#2992B0").pack(fill="both",expand=1)
        # self.fond_carte_pokemons=Fond_Ecran(self,Image.open("View/fond_ecran_pokedex.jpeg").resize((100,100)),
        #            "#2992B0",True)
        # self.fond_carte_pokemons.pack(fill="both",expand=1)
        filas=tuple(range(803//3))
        print("pokemons:","802","filas:",filas)
        # self.rowconfigure(filas, weight=1, uniform="a")
        self.columnconfigure((0,1,2),weight=1,uniform="a")
        self.boutton_afficher_plus=ttk.Button(mere,text="Afficher_plus")
        self.boutton_afficher_plus.pack(side="top")
        self.cartes_pokemons_affichees=[]
        # self.cargar_imagenes()
    
    def initialisation_cartes_pokemons(self,data_pokemons):
        print("Initialisation pokecartes[")
        for index,pokemon_info in data_pokemons.iterrows():
            if index==0 or index==150 or index==250 or index==350 or index==450 or index==550 or index==650 or index==750 or index==800 or index==850:
                print("*")
            # self.pokemon_carte=self.poke_carte(pokemon_info[1],pokemon_info[0],
                                            #    ImageTk.PhotoImage(Image.open("Model/Characters_image/25-phd.png").resize((100,200))))
            nom=pokemon_info.iloc[1]
            numero=pokemon_info.iloc[0]
            self.pokemon_carte=self.poke_carte(nom,numero)
            # self.dico_pokemons_cartes[nom,numero]=self.pokemon_carte[0]
            self.dico_pokemons_cartes.append(((nom,numero),self.pokemon_carte[0]))
            # self.dico_image_cartes[nom]=self.pokemon_carte[1]
            self.dico_image_cartes.append((nom,self.pokemon_carte[1]))
        print("]\n Fin initialisation")

    def cargar_imagenes(self):
        self.imagenes_pokemon = []
        print("Initialisation pokecartes images[")
        for i in range(1, 700):  # Suponiendo que tienes 151 Pokémon
            if i==0 or i==150 or i==250 or i==350 or i==450 or i==550 or i==650 :
                print("*")
            self.imagen = ImageTk.PhotoImage(Image.open(f"Model/Characters_image/{i}.png").resize((100, 80)))
            self.imagenes_pokemon.append(self.imagen)
        self.images=self.imagenes_pokemon
            
    def affichage_30pokemon(self,pokemon_data,commpteur_pokemons):
        

        
        for index, pokemon_info in pokemon_data.iterrows():
            columna = index % 3  # Ahora hay tres columnas (0, 1, 2)
            linea = index // 3 
            # self.dico_image_cartes[pokemon_info[1]].create_image(90, 40, image=self.images[index], anchor="center")
            # self.dico_image_cartes[index][1].create_image(90, 40, image=self.images[index], anchor="center")
            # self.carte=self.dico_pokemons_cartes[pokemon_info[1], pokemon_info[0]]
            self.carte=self.dico_pokemons_cartes[index][1]
            self.carte.grid(row=linea, column=columna, padx=10, pady=10)
            self.cartes_pokemons_affichees.append(self.carte)

        
    def set_command(self,command):
        self.boutton_afficher_plus["command"]=command

    #Fonction qui return un frame qui affiche des infos basique du pokemon
    def poke_carte(self, nom, numero,image_tk=None):
        self.carte_pokemon = ttk.Frame(self)
        self.carte_pokemon.rowconfigure((0,1,2,3,4,5,6,7,8),weight=1,uniform="a")
        self.carte_pokemon.columnconfigure((0,1,2,3,4),weight=1,uniform="a")
        self.fond_carte_pokemon = tk.Canvas(self.carte_pokemon, bg="#2992B0")
        self.fond_carte_pokemon.place(x=0,y=0,relheight=1,relwidth=1)

        

        # Canvas où il y aura limage du  Pokemon
        self.canvas_pokemon = tk.Canvas(self.carte_pokemon, bg="#2992B0")
        if image_tk is not None:
            self.canvas_pokemon.create_image(40,40,image=image_tk,anchor="center")
            self.carte_pokemon.image_tk = image_tk #On le garde en instance pour pas qu'il se fasse elim
        self.canvas_pokemon.grid(row=0,rowspan=4,column=0,columnspan=5,sticky="nsew")


        # Labels pour nom et numero
        label_pokemon_nom = ttk.Label(self.carte_pokemon, text=f"{nom}")
        label_pokemon_nom.grid(row=5,rowspan=2,column=0,columnspan=3,sticky="nsew")

        label_pokemon_numero = ttk.Label(self.carte_pokemon, text=f"#{numero}")
        label_pokemon_numero.grid(row=4,rowspan=1,column=0,columnspan=1,sticky="nsw")


        # Canvas où il yaura les types de pkemon (en icone)
        canvas_type1 = tk.Canvas(self.carte_pokemon, bg="green")
        canvas_type1.grid(row=8,rowspan=1,column=0,columnspan=2,sticky="nsew")

        canvas_type2 = tk.Canvas(self.carte_pokemon, bg="yellow")
        canvas_type2.grid(row=8,rowspan=1,column=3,columnspan=2,sticky="nsew")

        return self.carte_pokemon,self.canvas_pokemon


class Poke_Details_Window(tk.Toplevel): #On crée une autre fenêtre qui n'interfere pas notre fenêtre principale 
    def __init__(self,nom_pokemon,direction_gif,direction_image=None):
        super().__init__()
        
        self.thread_en_marche=True #Controle du Thread

        self.title(f"Info of {nom_pokemon} ")
        #Initialisation taille du pokedex_GUI
        ecran_largeur = self.winfo_screenwidth()
        ecran_longeur = self.winfo_screenheight()
        self.geometry(f"{ecran_largeur-(ecran_largeur//2)}x{ecran_longeur-(ecran_longeur//2)}")
        self.size #Juste pour actualiser les info sur la taille de la fenêtre
                    #Car en t=0 début tkinter fournies les relatives puis après en pixel
        self.largeur_fenetre = self.winfo_screenwidth()
        self.hauteur_fenetre = self.winfo_screenheight()
        
        self.minsize(500,300)
        
        self.ecran=Image.open("View/Back1.jpeg")
# View/pokemon__template_no_evolution_by_trueform_d3hs6u9.png
        self.details_ecran=Fond_Ecran(self,self.ecran,"red",False,affichage_pokemon=Image.open(direction_image))
        self.direction_gif=direction_gif
        self.details_ecran.pack(fill="both",expand=1)

    
    def configuration_gif(self,width_rel=0.5, height_rel=0.25):
        gif_pokemon = Image.open(self.direction_gif)
        self.gif_frames = []
        

        gif_largeur = int(self.largeur_fenetre * width_rel)
        gif_hauteur = int(self.hauteur_fenetre * height_rel)
        for frame in range(gif_pokemon.n_frames):
            gif_pokemon.seek(frame)
            frame_photo = ImageTk.PhotoImage(gif_pokemon.copy().resize((gif_largeur,gif_hauteur)))
            self.gif_frames.append(frame_photo)
        self.delai_frames_gif = gif_pokemon.info["duration"]
        self.afficher_gif(0)


    def afficher_gif(self, compteur_frames_gif, pos_x_rel=0.25, pos_y_rel=0.25):
        if self.thread_en_marche:
            frame = self.gif_frames[compteur_frames_gif]
            canvas_width = self.details_ecran.winfo_width()
            canvas_height = self.details_ecran.winfo_height()
            pos_x = int(canvas_width * pos_x_rel)
            pos_y = int(canvas_height * pos_y_rel)
            
            # Supprimer l'image précédente si elle existe
            if hasattr(self, 'image_on_canvas'):
                self.details_ecran.delete(self.image_on_canvas)
            
            # Afficher la nouvelle frame
            self.image_on_canvas = self.details_ecran.create_image(pos_x, pos_y, image=frame, anchor='center')
            
            # Planifier la mise à jour suivante
            compteur_frames_gif = (compteur_frames_gif + 1) % len(self.gif_frames)
            self.after(self.delai_frames_gif, self.afficher_gif, compteur_frames_gif, pos_x_rel, pos_y_rel)


    def afficher_image(self,largeur_rel=0.25,hauteur_rel=0.25,x_rel=0.50,y_rel=0.45):
        self.image_pokemon=Image.open(self.direction_image)
        image_largeur = int(self.largeur_fenetre * largeur_rel)
        image_hauteur = int(self.hauteur_fenetre * hauteur_rel)
        pos_x = int(self.largeur_fenetre * x_rel)
        pos_y = int(self.hauteur_fenetre * y_rel)

        print("\n config de ton window:",self.largeur_fenetre,self.hauteur_fenetre)
        print("\n config de taille image:",image_largeur,image_hauteur)
        print("\n config de position image:",pos_x,pos_y,"\n")
        self.image_pokemon_tk=ImageTk.PhotoImage(self.image_pokemon.resize((image_largeur,image_hauteur)))
        self.details_ecran.create_image(pos_x,pos_y,image=self.image_pokemon_tk,anchor="center")
        

    def fermer_and_stop_thread(self):
        self.thread_en_marche=False #Controle du Thread
        self.destroy()





