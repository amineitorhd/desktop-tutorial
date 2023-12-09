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
        self.ecran_obscur=Image.open("View/fond_ecran_dark.jpeg").resize((ecran_largeur+20,
                                                                                        ecran_longeur+15))
        self.ecran_actuel=self.ecran  #Variable qui va permettre de switch les ecrans

        
        #Initialisation du fond d'ecran 
        self.fond_ecran=Fond_Ecran(self,self.ecran,"red",ecran_principal=True)
        self.fond_ecran.pack(expand=True,fill="both")

        self.test=ttk.Button(self,text="sort")
        # self.test.place(relx=0.1,rely=0,relheight=1,relwidth=0.2)


        self.filtres_avancee=Frame_dynamique_filtres(self,1.5,0.15,0.0502,True,0.4,0.85,2,teleport=(True,0.95))
        
        self.boutton_filtres_avancee=ttk.Button(self,text="Filtres",
                                              command=lambda:self.filtres_avancee.animation(self.boutton_filtres_avancee))
        self.boutton_filtres_avancee.place(relx=0.0502,rely=0.95,relwidth=0.4,relheight=0.05)

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

        self.boutton_configuration=ttk.Button(self,text="Configuration",
                                                    command=self.configuration.animation).place(relx=0,
                                                    rely=0.9,relheight=0.1,relwidth=0.05)

            
    def sort_command(self,command):
        self.test["command"]=command

    def gestion_fenetre(self,event):
        self.fond_ecran.create_window(((self.winfo_width()//2)*0.95,0),window=self.affichage_pokemons,
                                      anchor="nw",width=(self.winfo_width()//2*1.0499))


    def actualisation_mode_obscur(self):
        if self.ecran_actuel==self.ecran:
            self.ecran_actuel=self.ecran_obscur #On swich d'ecran
            couleur="black"
        else:
            self.ecran_actuel=self.ecran
            couleur="#2992B0"

        if self.configuration.ecran_actuel_configuration==self.configuration.image_configuration:
            self.configuration.ecran_actuel_configuration=self.configuration.image_configuration_obscure
        else:
            self.configuration.ecran_actuel_configuration=self.configuration.image_configuration

        if self.filtres_avancee.squirtel_actuel==self.filtres_avancee.squirtels:
            self.filtres_avancee.squirtel_actuel=self.filtres_avancee.squirtels_obscur
        else:
            self.filtres_avancee.squirtel_actuel=self.filtres_avancee.squirtels
            
        self.fond_ecran.switch_mode_ecran(self.ecran_actuel) #On met a jour le nouveau ecran
        self.configuration.fond_ecran_configuration.switch_mode_ecran(self.configuration.ecran_actuel_configuration)
        self.filtres_avancee.cv.switch_mode_ecran(self.filtres_avancee.squirtel_actuel)

        for pokemon,carte in self.affichage_cartes_pokemons.dico_image_carte.items():
            carte[0].configure(bg=couleur)


    def affichage_info_pokemon(self,pokemon):
        print(f"tu veux plus d'info de: {pokemon}")


    def affichage_info_complete_pok(self,pokemon,gif,image):
        nom=pokemon
        poke_info_window=Poke_Details_Window(nom,gif,image)
        for info in pokemon:
            ttk.Label(poke_info_window,text=f"{info}").pack(side="right")
        # Si on ferme le window, on indique d'arrêter lethred
        poke_info_window.protocol("WM_DELETE_WINDOW", poke_info_window.fermer_and_stop_thread)
        
        threading.Thread(target=poke_info_window.configuration_gif).start()  #On le traite à part pour pas perturber le fonctionnement de notre GUI.


    def demarage(self):
        self.mainloop()


#Création objet Canvas pour gerer l'affichage du fond d'ecran
#Aussi pour gerer les regions de scroll possibles
class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,ecran,fond="magenta",affichage_pokemon=None,ecran_principal=False):
        super().__init__(mere,bg=fond)
        self.image_fond_ecran=ecran
        self.mere=mere
        self.ecran_principal=ecran_principal
        #Si le canvas change de taille (<=> si fenetre change de taille (car canvas occupant toute la fenêtre))
        self.bind('<Configure>', self.config_fond_ecran)
        self.affichage_pokemon=affichage_pokemon
        #attribut affichage_pokemon: On l'utilise que pour notre fenêtre top_level


    def config_fond_ecran(self,event=None,numb_pokemons=40): #valeur arbitraire (numb de pokemons par ecran)
        #On utilise pas l'argument event fournie par "bind"    
        
        #On va ajuster le fond d'ecran selon la taille de la fenêtre
        largeur=self.winfo_width()
        hauteur=self.winfo_height()
        print("info ecran:",largeur,hauteur)
        
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
        if self.affichage_pokemon is not None:
            self.image_tk = ImageTk.PhotoImage(self.affichage_pokemon.resize((100,200)))

            # Obtenir les dimensions du Canvas
            largeur_canvas = self.winfo_width()
            hauteur_canvas = self.winfo_height()

            # Afficher l'image au centre du Canvas
            self.create_image(largeur_canvas // 2, hauteur_canvas // 2, image=self.image_tk, anchor="center")
        if self.ecran_principal:
            for filtre,scale in self.mere.filtres_avancee.stock_scale_tkinter.items():
                scale.dessin_slider(largeur*0.4*0.352,hauteur*0.1*0.95)
    

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
            self.pack=False
            self.boutton_recherche.invoke()
            self.pack=True  #Pourquoi conversion en str!!!!
        else:
            self.resultats.pack_forget()


    def affichage_temps_reel(self,data_set):
        for index, (nb, nm, t1, t2) in enumerate(data_set):
            self.resultats.insert(parent="", index=index, values=(nb, nm, t1, t2))


    def rechercher(self,event):
        self.boutton_recherche.invoke()  #Une nouvelle fonction car bind nous donne des arguments qu'on veut pas

    
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

        self.mere=mere #On garde une référence de notre GUI 

        self.image_configuration=Image.open("View/configuration_light.jpeg")
        self.image_configuration_obscure=Image.open("View/configuration_obscure2.jpeg")
        self.ecran_actuel_configuration=self.image_configuration
        self.fond_ecran_configuration=Fond_Ecran(self,self.image_configuration,"yellow")
        self.fond_ecran_configuration.pack(fill="both",expand=1)
        self.fond_ecran_configuration.bind("<Button-1>",self.verificar_clic)


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

    def verificar_clic(self, event):
            # Convertir posiciones relativas a absolutas
            x1_dark = self.winfo_width() * 0.54
            y1_dark = self.winfo_height() * 0.61
            x2_dark = x1_dark + (self.winfo_width() * 0.185)
            y2_dark = y1_dark + (self.winfo_height() * 0.17)

            x1_reset = self.winfo_width() * 0.315
            y1_reset = self.winfo_height() * 0.61
            x2_reset = x1_reset + (self.winfo_width() * 0.185)
            y2_reset = y1_reset + (self.winfo_height() * 0.17)


            # Verificar si el clic está dentro del área definida
            if x1_dark <= event.x <= x2_dark and y1_dark <= event.y <= y2_dark:
                # #Boutton permettant de switch entre mode obscure ou pas
                print("light/dark version!!!")
                self.mere.actualisation_mode_obscur()
            elif x1_reset <= event.x <= x2_reset and y1_reset <= event.y <= y2_reset:
                print("reset click!")
            else:
                print("Clic fuera del área definida.")


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
        self.dico_scales={}
        self.stock_scale_tkinter={}

        self.squirtels=Image.open("View/filtres_ecran.jpeg")
        self.squirtels_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png")
        self.squirtel_actuel=self.squirtels
        self.cv=Fond_Ecran(self,self.squirtels)
        self.cv.pack(fill="both",expand=1)

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
        b=0
            # Variables para controlar la posición de los elementos
        label_rely = 0.005
        incremento = 0.13
        print(information[0])
        for cle,valeur in information[0].items():
            if not (valeur[1]=="Id_Type"):
                if valeur[1]=="Categorique_Type":
                    ttk.Label(self.cv,text=cle,background="red",font=("Helvetica",15)).place(relx=0.09,rely=0.05,relwidth=0.37,relheight=0.045)
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
                elif valeur[1] == "BatailleStat_Type":
                    # Crear y colocar el label
                    label = ttk.Label(self.cv, text=cle)
                    label.place(relx=0.643, rely=label_rely, relwidth=0.352, relheight=0.03)

                    # Crear y colocar el DoubleSlider
                    slider_rely=label_rely+0.03
                    self.scale = DoubleSlider(self,filtre=cle)
                    self.scale.place(relx=0.643, rely=slider_rely, relwidth=0.352, relheight=0.07)
                    self.stock_scale_tkinter[cle]=self.scale
                    self.dico_scales[cle]=(None,None)

                    # Incrementar la posición para el siguiente filtro
                    label_rely += incremento
                    slider_rely += incremento
            self.boutton_reset=ttk.Button(self.cv,text="Reset")
            self.boutton_reset.place(relx=0.01,rely=0.92,relwidth=0.4,relheight=0.07)
            self.boutton_application=ttk.Button(self.cv,text="Appliquer")
            self.boutton_application.place(relx=0.45,relwidth=0.51,rely=0.92,relheight=0.07)
        # for cle,valeur in self.dico_scales.items():
        #     print(cle)
        #     print(valeur[1],valeur[2])
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


    def set_command(self,command):
        self.boutton_application["command"]=command

    def bout_reset_set_command(self,command):
        self.boutton_reset["command"]=command



#Frame qui affiche tous les pokemons (graphiquement)
class Frame_poke_affichage_v2(ttk.Frame):
    def __init__(self,mere,fond_ecran):
        super().__init__(mere)
        self.pokemons_affiches=30
        self.dico_pokemon_carte={} #Contient toutes les cartes
        self.dico_image_carte={}  #Tous les canvas qui doivent contenir une image
        self.poke_cartes_affichees=[] #Tous les pokemons affiches
        self.images_stock=[] #Toutes les images pour que le recolecteur ne les effacent pas

        self.affichage_par30=True  #Pour differencié du cas lorsqu'on on cherche par filtres.
        self.nb_poke_resultats=0

        self.place(relx=0.5,rely=0.05,relwidth=0.4999,relheight=0.9)
        self.canvas=tk.Canvas(self,bg="pink",scrollregion=(0,0,self.winfo_width(),self.pokemons_affiches*330))
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
            carte,numero=self.dico_pokemon_carte[poke_nom]
            image_carte=self.dico_image_carte[poke_nom][0]
            carte.pack(fill="both",padx=(0,15))
            self.amine=ImageTk.PhotoImage(Image.open(self.dico_image_carte[poke_nom][1]).resize((150,200)))
            self.images_stock.append(self.amine)
            image_carte.create_image(40,40,image=self.amine,anchor="nw")
            self.poke_cartes_affichees.append(carte)
        self.boutton_afficher_plus.pack(fill="both",expand=1)

    def affichage_poke_specifique(self,poke_nom_data):
        
        for carte in self.poke_cartes_affichees:
            carte.pack_forget()
            self.boutton_afficher_plus.pack_forget()
        self.poke_cartes_affichees.clear()
        for num,poke_nom in enumerate(poke_nom_data):
            if num<30:
                carte,numero=self.dico_pokemon_carte[poke_nom]
                image_carte=self.dico_image_carte[poke_nom][0]
                direction=self.dico_image_carte[poke_nom][1]
                carte.pack(fill="both",padx=(0,15))
                self.amine=ImageTk.PhotoImage(Image.open(direction).resize((150,200)))
                self.images_stock.append(self.amine)
                image_carte.create_image(80,40,image=self.amine,anchor="nw")
                self.poke_cartes_affichees.append(carte)
                print(num)
            else:
                print(num)
                self.boutton_afficher_plus.pack(fill="both",expand=1)
                
                break
        

    def configuration_affichage(self,_):
        if self.affichage_par30:
            if self.pokemons_affiches*330>=self.winfo_height():
                hauteur_fenetre_scroll=self.pokemons_affiches*330
                self.canvas.bind_all("<MouseWheel>",lambda event: self.canvas.yview_scroll(-int(event.delta/60),"units"))
                self.scroll_bar.place(relx=1,rely=0,relheight=1,anchor="ne")

            else:
                hauteur_fenetre_scroll=self.winfo_height()
                self.canvas.unbind_all("<MouseWheel>")
                self.scroll_bar.place_forget()
        else:
            print("option recherche!!!")
            if self.nb_poke_resultats*330>=self.winfo_height():
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
        print("hauteur actualisée:",hauteur_fenetre_scroll)

    def creation_poke_carte(self, nom, numero,type1,type2):
        self.carte_pokemon = ttk.Frame(self.frame)

        # Canvas para el fondo de la carta de Pokemon
        self.fond_carte_pokemon = tk.Canvas(self.carte_pokemon, bg="#2992B0")
        self.fond_carte_pokemon.pack(fill="both", expand=True)


        self.canvas_information=tk.Canvas(self.fond_carte_pokemon,bg="pink")     
        self.canvas_information.pack(side="right",fill="both",expand=True)
      

        # Canvas para la imagen del Pokemon
        self.canvas_pokemon = tk.Canvas(self.fond_carte_pokemon, bg="#2992B0")
        self.canvas_pokemon.pack(side="right", fill="both")


        # Label para el nombre y número del Pokemon
        label_pokemon_nom = tk.Label(self.canvas_information, text=f"{nom}", font=("Helvetica", 20), bg="grey")
        # label_pokemon_nom=tk.Canvas(self.canvas_information,bg="grey")
        label_pokemon_nom.pack(side="top", fill="x")


        label_pokemon_numero = tk.Label(self.canvas_information, text=f"#{numero}", bg="#2992B0")
        # label_pokemon_numero=tk.Canvas(self.canvas_information,bg="black")
        label_pokemon_numero.pack(side="top", fill="x")

        # Canvas para los tipos de Pokemon
        # canvas_type1 = tk.Canvas(self.canvas_information, bg="green")
        # canvas_type1.create_text(20, 60, text=type1, font=("Helvetica", 20))
        canvas_type1=tk.Label(self.canvas_information,text=f"{type1}",bg="red",font=("Helvetica", 15))
        canvas_type1.pack(side="top",fill="both",expand=True)

        if type2 != "nan":
            # canvas_type2 = tk.Canvas(self.canvas_information, bg="yellow")
            # canvas_type2.create_text(20, 60, text=type2, font=("Helvetica", 20))
            canvas_type2=tk.Label(self.canvas_information,text=f"{type2}",bg="blue",font=("Helvetica", 15))
            canvas_type2.pack(side="top",fill="both",expand=True)

        return self.carte_pokemon, self.canvas_pokemon


    def initialisation_cartes_pokemons(self,data_pokemons,data_media):
        print("initialisation cartes:")
        for index,pokemon_info in data_pokemons.iterrows():
            poke_nom=pokemon_info.iloc[1]
            poke_numero=pokemon_info.iloc[0]
            poke_1=pokemon_info.iloc[2]
            poke_2=pokemon_info.iloc[3]
            pokemon_carte=self.creation_poke_carte(poke_nom,poke_numero,f"{poke_1}",f"{poke_2}")
            self.dico_pokemon_carte[poke_nom]=pokemon_carte[0],poke_numero
            self.dico_image_carte[poke_nom]=pokemon_carte[1],data_media[poke_nom]

        print("fin initialisation")


    def bout_set_command(self,command):
        self.boutton_afficher_plus["command"]=lambda: command(self.affichage_par30)



class Poke_Details_Window(tk.Toplevel): #On crée une autre fenêtre qui n'interfere pas notre fenêtre principale 
    def __init__(self,nom_pokemon,direction_gif,direction_image):
        super().__init__()
        self.direction_image=direction_image
        self.thread_en_marche=True #Controle du Thread

        self.title(f"Info of {nom_pokemon} ")
        #Initialisation taille du pokedex_GUI
        ecran_largeur = self.winfo_screenwidth()
        ecran_longeur = self.winfo_screenheight()
        self.geometry("890x750")
        self.size #Juste pour actualiser les info sur la taille de la fenêtre
                    #Car en t=0 début tkinter fournies les relatives puis après en pixel
        self.largeur_fenetre = self.winfo_screenwidth()
        self.hauteur_fenetre = self.winfo_screenheight()
        
        self.minsize(550,720)
        self.maxsize(900,1200)
        
        self.ecran=Image.open("View/poke_info.jpeg")
# View/pokemon__template_no_evolution_by_trueform_d3hs6u9.png
        self.details_ecran=Fond_Ecran(self,self.ecran,"red",affichage_pokemon=Image.open(direction_image))
        self.direction_gif=direction_gif
        self.details_ecran.pack(fill="both",expand=1)

    
    def configuration_gif(self,width_rel=0.5, height_rel=0.25):
        gif_pokemon = Image.open(self.direction_gif)
        self.gif_frames = []
        

        gif_largeur = int(self.largeur_fenetre * width_rel)
        gif_hauteur = int(self.hauteur_fenetre * height_rel)
        for frame in range(gif_pokemon.n_frames):
            gif_pokemon.seek(frame)
            frame_photo = ImageTk.PhotoImage(gif_pokemon.copy())
            self.gif_frames.append(frame_photo)
        self.delai_frames_gif = gif_pokemon.info["duration"]
        self.afficher_gif(0)


    def afficher_gif(self, compteur_frames_gif, pos_x_rel=0.25, pos_y_rel=0.49):
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



class DoubleSlider(tk.Canvas):
    def __init__(self, master=None, min_val=0, max_val=309,filtre="", **kwargs):
        super().__init__(master, bg="#2992B0", **kwargs)
        self.master=master
        self.min_val = min_val
        self.max_val = max_val
        self.first_thumb_val = min_val  # Valor del pulgar azul
        self.second_thumb_val = max_val  # Valor del pulgar rojo
        self.filtre=filtre


        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)

        self.canvas_max=tk.Canvas(self,bg="red")
        self.canvas_max.place(relx=0.55,rely=0.15,relwidth=0.4,relheight=0.4)
        self.canvas_min=tk.Canvas(self,bg="blue")
        self.canvas_min.place(relx=0.05,rely=0.15,relwidth=0.4,relheight=0.4)

        # Crear elementos de texto para los valores mínimo y máximo
        self.text_min = self.canvas_min.create_text(40, 10, text=str(self.min_val),font=("Helvetica",15), anchor="w", fill="white")
        self.text_max = self.canvas_max.create_text(40, 10, text=str(self.max_val),font=("Helvetica",15), anchor="e", fill="white")


    def dessin_slider(self, largeur_relative, hauteur_relative):
        self.width = largeur_relative  # Ancho solicitado del Canvas
        self.height = hauteur_relative  # Altura solicitada del Canvas

        self.margin = 20  # Margen para los pulgares
        self.line_y = self.height // 2  # Posición y para la línea

        self.delete("all")
        self.create_line(self.margin, self.line_y, self.width - self.margin, self.line_y, fill="lightgray", width=10)
        self.first_thumb = self.create_oval(self.margin - 10, self.line_y - 5, self.margin + 10, self.line_y + 5, fill="blue", outline="blue", tags="thumb")
        self.second_thumb = self.create_oval(self.width - self.margin - 10, self.line_y - 5, self.width - self.margin + 10, self.line_y + 5, fill="red", outline="red", tags="thumb")
 

    def click(self, event):
        closest = self.find_closest(event.x, event.y)[0]
        if closest == self.first_thumb:
            self.active_thumb = self.first_thumb
        elif closest == self.second_thumb:
            self.active_thumb = self.second_thumb


    def drag(self, event):
        if hasattr(self, 'active_thumb'):
            x = min(max(event.x, self.margin), self.width - self.margin)
            val = int(((x - self.margin) / (self.width - 2 * self.margin)) * (self.max_val - self.min_val) + self.min_val)
            if self.active_thumb == self.first_thumb:
                if val <= self.second_thumb_val:  # Condición para el pulgar azul
                    self.first_thumb_val = val
                    self.coords(self.active_thumb, x - 10, self.line_y - 5, x + 10, self.line_y + 5)
                    self.canvas_min.itemconfig(self.text_min, text=str(val))  # Actualizar texto del valor mínimo


            else:
                if val >= self.first_thumb_val:  # Condición para el pulgar rojo
                    self.second_thumb_val = val
                    self.coords(self.active_thumb, x - 10, self.line_y - 5, x + 10, self.line_y + 5)
                    self.canvas_max.itemconfig(self.text_max, text=str(val))  # Actualizar texto del valor máximo
        self.update_values()


    def update_values(self):
        # Actualiza los valores en dico_scales
        self.master.dico_scales[self.filtre] = (self.first_thumb_val, self.second_thumb_val)
        


