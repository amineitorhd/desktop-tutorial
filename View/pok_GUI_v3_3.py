import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        self.fond_ecran=Fond_Ecran(self,self.ecran,"red",True)
        self.fond_ecran.pack(expand=True,fill="both")


        self.filtres_avancee=Frame_dynamique_filtres(self,1.5,0.35,0.0502,True,0.4,0.80,2,teleport=(True,0.95))
        
        self.boutton_filtres_avancee=ttk.Button(self,text="Filtres",
                                              command=lambda:self.filtres_avancee.animation(self.boutton_filtres_avancee))
        self.boutton_filtres_avancee.place(relx=0.0502,rely=0.95,relwidth=0.4)

#Initialisation des réglages du Pokedex_GUI
        self.configuration=Frame_dynamique_configuration(self,-0.4,0.035,0.50,False,0.4,0.2,5)
        self.config_configuration()
        

#Ordre d'initialisation important!!!
        #Initialisation de la barre de recherche
        self.zone_recherche=Frame_Recherche_simple(self,size=ecran_longeur//60)
        self.zone_recherche.place(relx=0.005,relwidth=0.4,y=0)


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


    def recup_data_apres_filtrage(self,data):
        print("Je suis GUI et j'ai reçue le résultat du Controller\n")
        print(data,type(data))


    def affichage_info_complete_pok(self,pokemon):
        poke_info_window=Poke_Details_Window(pokemon[1])
        # poke_info_window.demarage()

    def demarage(self):
        self.mainloop()

#Création objet Canvas pour gerer l'affichage du fond d'ecran
#Aussi pour gerer les regions de scroll possibles
class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,ecran,fond="magenta",expand_ecran=False):
        super().__init__(mere,bg=fond)
        self.image_fond_ecran=ecran

        #Si il faut afficher plus de pokemons, il faut agrandir la fenêtre
        self.expandir_ecran=expand_ecran

        #Si le canvas change de taille (<=> si fenetre change de taille (car canvas occupant toute la fenêtre))
        self.bind('<Configure>', self.config_fond_ecran)


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
        
        if self.expandir_ecran:
            num_lignes=int(numb_pokemons//7) #Calculs arbitraires
            num_colonnes=int(largeur//1024)+1

            #On prefère cree une image en dessous l'autre pour garder la visibilité
            #Au lieu de redimensioner l'hauteur
            for i in range(num_lignes):
                self.create_image(0,i*x, image=self.ecran_actualisee_tk, anchor="nw")
            
            #On ajuste le scroll_region à chaque actualisation de l'ecran.
            self.config(scrollregion=(0,0,largeur,num_lignes*x-750)) #750: choisie arbitrairement


    def switch_mode_ecran(self,ecran):
        self.image_fond_ecran=ecran #On change d'ecran
        self.config_fond_ecran() #on actualise le fond d'ecran


#Frame personnalisée représentant la barre de recherche
class Frame_Recherche_simple(ttk.Frame):
    def __init__(self,mere,size):
        super().__init__(mere)
        self.mere=mere
        #On cree un style personalisée pour nos bouttons
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', size-3))



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
        self.boutton_recherche=ttk.Button(mere,text="chercher!",style='TButton')
        self.boutton_recherche.place(relx=0.4*self.winfo_width(),y=0)

        self.resultats_tempsreel=ttk.Treeview(self,columns=("Id_numero","Id_nom","Caract1","Caract2"),show="headings")  #""""Tableur tkinter"""""


        self.nom_nombre.trace("w", self.temps_reel)  #Bizare car obligé 3 arguments!

    def configuration_affichage_resultats(self,filtres_affiches):
        longeur_frame=self.winfo_width()
        longeur_par_colonne=longeur_frame//len(filtres_affiches)
        self.resultats_tempsreel=ttk.Treeview(self,columns=("Id_nom","Id_numero","Caract1","Caract2"),show="headings")
        
        #On itère à la fois sur la liste des filtres et sur les colonnes de notre treeview
        for filtre, col in zip(filtres_affiches, self.resultats_tempsreel["columns"]):
            self.resultats_tempsreel.heading(col, text=filtre)  #On change les titres des colonnes
            self.resultats_tempsreel.column(col,width=longeur_par_colonne)  #On met une largeur uniforme pour chaque colonne
                                                                                #On pourrait les personalisé....
        self.resultats_tempsreel.bind('<Double-1>', self.selection)  # Si double click
        self.resultats_tempsreel.bind('<Return>', self.selection)  # Ou si appuie sur enter


    #On peut recevoir de la methode trace un nombre k d'arguments qu'on va pas utiliser.
    def temps_reel(self,*args): 
        entree=self.entree_nm_nb.get()
        self.resultats_tempsreel.delete(*self.resultats_tempsreel.get_children()) #Pour effacer les trucs d'avant

        if entree!="" and entree!="Nom ou numéro Pokemon":
            self.resultats_tempsreel.pack(fill="x")
            nombre_elements = len(self.resultats_tempsreel.get_children())
            # Configuration de la hauteur de la ListBox pour qu'elle corresponde au nombre d'éléments
            # if nombre_elements>7:
            #     self.resultats_tempsreel.configure(height=100) #hateur max pouvant occuper!
            # else:
            #     self.resultats_tempsreel.configure(height=nombre_elements)

            # self.afficher_frames=False
            # data=self.boutton_recherche.invoke() #Pourquoi tkniter convert un pandas df a un str???
            # self.afficher_frames=True

            # print(data)
            # self.resultats_tempsreel.insert("","end",values=(entree,))
            self.boutton_recherche.invoke()  #Pourquoi conversion en str!!!!

        else:
            self.resultats_tempsreel.pack_forget()


    def affichage_temps_reel(self,data_set):
        print("\n\n\n\n\nJe suis GUI et j'ai reçu ça pour le treeview:\n\n\n\n\n")
        i=0
        for nb,nm,t1,t2 in data_set:

            self.resultats_tempsreel.insert(parent="",index=i,values=(nb,nm,t1,t2))
            i+=1


    def rechercher(self,event):
        self.pack=False
        self.boutton_recherche.invoke()  #Une nouvelle fonction car bind nous donne des arguments qu'on veut pas
        self.pack=True

    def selection(self,event):
        for pokemon in self.resultats_tempsreel.selection():
            a=self.resultats_tempsreel.item(pokemon)
            print(a["values"])
            self.mere.affichage_info_complete_pok(a["values"])

    
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

    #On reçoit la commande du boutton du Controller
    def set_command(self,command):
        self.boutton_recherche["command"]= lambda: command(self.entree_nm_nb.get(),
                                                           self.pack) #Initialisé à True!   


    def cambiar_tamaño_texto(self,new):
        self.size=new


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
            print("Je suis GUI et j'ai reçue l'info de Controller:")
            print(information[0])
            for cle,valeur in information[0].items():
                if not (valeur[1]=="Id_Type"):
                    if valeur[1]=="Categorique_Type":
                        print("\n")
                        print(information[1][cle],len(information[1][cle]))
                        ttk.Label(self.cv,text=cle).pack()
                        i=1
                        if not information[0][cle][0]:
                            for valeur_possible in information[1][cle]:
                                if f"{valeur_possible}"!="nan":
                                    if i<7:
                                        print(i)
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


class Poke_Details_Window(tk.Toplevel): #On crée une autre fenêtre qui n'interfere pas notre fenêtre principale 
    def __init__(self,nom_pokemon):
        super().__init__()
        self.title(f"Info of {nom_pokemon} ")
        #Initialisation taille du pokedex_GUI
        ecran_largeur = self.winfo_screenwidth()
        ecran_longeur = self.winfo_screenheight()
        self.geometry(f"{ecran_largeur-(ecran_largeur//2)}x{ecran_longeur-(ecran_longeur//2)}")
        self.minsize(500,300)

        self.ecran=Image.open("View/template.png")

        self.details_ecran=Fond_Ecran(self,self.ecran,"red",False)
        self.details_ecran.pack(fill="both",expand=1)






