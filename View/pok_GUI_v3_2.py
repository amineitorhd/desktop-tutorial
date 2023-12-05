import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex Python App")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print("----------------------------------------------------------------------")
        print("HP tamaños:",screen_height,screen_width)
        print("----------------------------------------------------------------------")
        self.geometry(f"{screen_width-(screen_width//2)}x{screen_height-(screen_height//2)}")
        self.minsize(500,300)
        lim=(0,0,2000,6000)
        

        #Initialisation deux images de fond_ecran dépendant du mode
        self.ecran=Image.open("View/fond_ecran_pokedex.jpeg").resize((screen_width+20,screen_height+25))
        self.ecran_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png").resize((screen_width+20,screen_height+15))
        self.ecran_actuel=self.ecran
        
        #Initialisation du Fond d_ecran avec un canvas personnalise
        self.fond_ecran=Fond_Ecran(self,lim,self.ecran,"red",True)
        self.fond_ecran.pack(expand=True,fill="both")

        #Inisialisation d_un Frame contenant les pokemons affiche
        self.Frame_affichage=Affichage_pokemons(self.fond_ecran,
                                                self.ecran)
        self.Frame_affichage.place(x=0,rely=0.55)


        self.Frame_filtrage=Frame_Recherche_simple(self)
        self.Frame_filtrage.place(relx=0.005,relwidth=0.4,y=0)

        #Initialisation d_un Frame dynamique personnalisee contenant
        #       les configurations du Pokedex 
        self.Frame_Configuration=Frame_dynamique_colonne(self,-0.4,0,0.25,False,0.2,0.2,10)
        self.boutton_configuration=ttk.Button(self,text="Configuration",
                                              command=self.Frame_Configuration.animation).place(relx=0,rely=0.22)
        #Boutton permettant de switch entre mode obscure ou pas
        buton_obscur=ttk.Button(self.Frame_Configuration,text="Obscure Mode",
                                command=self.actualisation_mode_obscur).place(relx=0.5,rely=0.5)


        #Initialisation d_un Frame dynamique personnalisee contenant
        #       les filtres possibles 
        self.filtres_avancee=Frame_dynamique_colonne(self,1.0,0.08,0.20,True,0.35,0.9,5)
        self.boutton_filtres_avancee=ttk.Button(self,text="Filtres",
                                              command=self.filtres_avancee.animation)
        self.boutton_filtres_avancee.place(relx=0.3,rely=0.2)


        self.scroll=ttk.Scrollbar(self.fond_ecran,orient="vertical",command=self.fond_ecran.yview)
        self.fond_ecran.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(relx=1,rely=0,relheight=1,anchor="ne")
        
        self.fond_ecran.bind("<MouseWheel>",self.Mouse_Wheel_configuration)

    def Mouse_Wheel_configuration(self,event):
        x, y = self.winfo_pointerxy()  # Obtener las coordenadas del ratón
        widget_under_cursor = self.winfo_containing(x, y)
        if not widget_under_cursor==self.Frame_filtrage.resultats_tempsreel:
            self.fond_ecran.yview_scroll(-int(event.delta / 60), "units")

    def configuration_filtres(self,filtres):
        print("ordre reçue de Presentor:")
        print("configuration des filtres")
        print(filtres)
        for filtre, filtre_type in filtres.items():
            if filtre_type[1] != 'Id_Type':
                if filtre_type[0]:  
                    label = tk.Label(self.filtres_avancee, text=filtre)
                    # entry_min = tk.Entry(self.filtres_avancee)
                    # entry_max = tk.Entry(self.filtres_avancee)
                    label.pack()
                    # entry_min.pack()
                    # entry_max.pack()
                else:  
                    label = tk.Label(self.filtres_avancee, text=filtre)
                    # entry = tk.Entry(self.filtres_avancee)
                    label.pack()
                    # entry.pack()
    

    def actualisation_mode_obscur(self):
        if self.ecran_actuel==self.ecran:
            self.ecran_actuel=self.ecran_obscur
        else:
            self.ecran_actuel=self.ecran
        self.fond_ecran.change_mode_obscur(self.ecran_actuel)



    def letsgoooo(self):
        
        self.mainloop()



class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,a,ecran,fond="magenta",expand_ecran=False):
        # super().__init__(mere,bg=fond,scrollregion=a)
        super().__init__(mere,bg=fond)
        self.expand_ecran=expand_ecran
        self.image_fond_ecran=ecran
        self.ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
        
        self.bind('<Configure>', self.config_fond_ecran)

    def config_fond_ecran(self,event=None,numb_pokemons=40):

        largeur=self.winfo_width()
        hauteur=self.winfo_height()
        # print("##############################################")
        # print(largeur,hauteur)
        # print("##############################################")

        ecran_ratio=largeur/hauteur

        if self.ratio_image<ecran_ratio:
            x=int(largeur)
            y=int(x/self.ratio_image)
        else:
            y=int(hauteur)
            x=int(y*self.ratio_image)


        updated_ecran=self.image_fond_ecran.resize((x,y))
        self.updated_ecran_tk=ImageTk.PhotoImage(updated_ecran)
        self.create_image(int(largeur/2),
                          int(hauteur/2),
                          image=self.updated_ecran_tk,
                          anchor="center")
        
        if self.expand_ecran:
            print("\n ****configurando el scroll region*****\n")
            print(numb_pokemons)    
            num_filas = int(numb_pokemons//7)  # Calcula el número de filas y columnas para una cuadrícula cuadrada
            num_columnas = int(largeur/1024)+1
            print("Imagenes en columnas creadas son:",num_columnas)
            print("Imagenes en filas creadas son:",num_filas)
            for i in range(num_filas):
                self.create_image(0, i*updated_ecran.height, image=self.updated_ecran_tk, anchor="nw")
            # self.create_image(0, 0, image=self.updated_ecran_tk, anchor="nw")


            print("\n ****configurando el scroll region*****\n")
            self.config(scrollregion=(0, 0, largeur, num_filas * updated_ecran.height-750))

    def change_mode_obscur(self,ecran):
        self.image_fond_ecran=ecran
        self.config_fond_ecran()

    def get(self):
        return self.image_fond_ecran



class Affichage_pokemons(ttk.Frame):
    def __init__(self,mere,ecran):
        super().__init__(mere)
        
        self.ecran=ecran
        self.mere=mere
        self.image_on_canvas = None 
        self.dico_frames_pokemons={}
        self.dico_frames_pokemons_grid={}
        self.data_reçue=None
        
        self.bind("<Configure>",self.actualisation_fenetres)
        self.frame_affichage_pok=ttk.Frame(mere)

        self.boutton_affichage_plus=ttk.Button(self.frame_affichage_pok,
                                               text="afficher plus",
                                               command=self.afficher_plus)
        self.index_courant = 0
        self.increment = 30


    def actualisation_fenetres(self,event):
        print("........actualisation des fenetres d'affichage............")
        self.mere.config(scrollregion=self.mere.bbox("all"))
        
        x = self.mere.winfo_width()*0.55
        y = self.mere.winfo_height()*0.2

        self.mere.create_window((x,y), window=self.frame_affichage_pok,
                                           anchor="nw")
   
    def afficher_plus(self,initialisation=False,data=None,images=None):
        if initialisation:
            self.data_reçue=data
        data = self.data_reçue.iloc[self.index_courant:self.index_courant+self.increment]
        self.index_courant += self.increment

        self.mere.config_fond_ecran(numb_pokemons=self.index_courant+self.increment)

        for index, row in data.iterrows():
            # Crear el frame
            pokemon_frame=self.dico_frames_pokemons[row[1]]
            
            

            # Posicionar el frame en la cuadrícula
            pokemon_frame.grid(row=(index+self.increment)//2, column=(index+self.increment)%2)

            self.dico_frames_pokemons_grid[row[1]]=pokemon_frame

        # Mover el botón a la siguiente posición
        self.boutton_affichage_plus.grid(row=self.index_courant, column=1)
    
    def initialisation(self,data):
        for index,row in data.iterrows():

            self.frame_pokemon=self.frame_unitaire_pok(row[1],row[0])
            self.dico_frames_pokemons[row[1]]=self.frame_pokemon

    def affichage_resultat_filtrage(self,data):
            # Supprimer tous les widgets de Frame1 et Frame2
            for id_pok,frame_pok in self.dico_frames_pokemons_grid.items():
                frame_pok.grid_remove()


            print("J'ai reçu ton data:")
            print(type(data))
            print(data)
            for index,row in data.iterrows():
                self.dico_frames_pokemons[row[1]].grid(row=index//2, column=index%2)
                self.dico_frames_pokemons_grid[row[1]]=self.dico_frames_pokemons[row[1]]



    def frame_unitaire_pok(self, nom, numero):
        self.fr = ttk.Frame(self.frame_affichage_pok)
        self.cv = tk.Canvas(self.fr, bg="black")
        self.cv.pack(fill="both",expand=1)

        

        # Canvas para la imagen del Pokemon
        self.canvas_pokemon = tk.Canvas(self.cv, bg="grey")

        self.canvas_pokemon.place(relx=0.22, rely=0, relheight=0.65, relwidth=0.58)


        # Labels para el nombre y el número del Pokemon
        label_pokemon_nom = ttk.Label(self.cv, text=f"{nom}")
        label_pokemon_nom.place(relx=0.22, rely=0.35, relheight=0.3, relwidth=0.58)

        label_pokemon_numero = ttk.Label(self.cv, text=f"#{numero}")
        label_pokemon_numero.place(relx=0.9, rely=0.75)

        # Canvas para los tipos de Pokemon
        canvas_type1 = tk.Canvas(self.cv, bg="green")
        canvas_type1.place(relx=0.22, relwidth=0.1, rely=0.3, relheight=0.05)

        canvas_type2 = tk.Canvas(self.cv, bg="yellow")
        canvas_type2.place(relx=0.33, relwidth=0.1, rely=0.3, relheight=0.05)

        return self.fr

        

    
        

class Frame_Recherche_simple(ttk.Frame):
    def __init__(self,mere):
        super().__init__(mere)
        self.pack=True
        self.boutton_recherche=ttk.Button(mere,text="chercher!")
        self.boutton_recherche.place(relx=0.4,y=0)

        self.nom_nombre=tk.StringVar()

        self.entry_nm_nb=ttk.Entry(self,textvariable=self.nom_nombre)
        self.entry_nm_nb.pack(fill="x")                
        self.entry_nm_nb.insert(0, "Nom ou numéro Pokemon")
        # Liaison d'événement pour effacer le texte initial lorsqu'un clic est effectué sur l'entry
        self.entry_nm_nb.bind("<FocusIn>", self.clear_placeholder_text)
        # Liaison d'événement pour restaurer le texte initial s'il n'y a pas de texte entré
        self.entry_nm_nb.bind("<FocusOut>", self.restore_placeholder_text)

        self.resultats_tempsreel=tk.Listbox(self)
        # self.resultats_tempsreel.pack(fill="x")

        self.nom_nombre.trace("w", self.temps_reel)  #Bizare car obligé 3 arguments!


    def temps_reel(self,*args): #On peut recevoir de la methode trace un nombre k d'arguments qu'on va pas utiliser.
        entree=self.entry_nm_nb.get()
        print(entree,entree!="")
        if entree!="":
            self.resultats_tempsreel.pack(fill="x")
            
            self.pack=False
            data=self.boutton_recherche.invoke() #Pourquoi tkniter convert un pandas df a un str???
            self.pack=True
            # print("Je suis GUI et j'ai récupérée:")
            # print(type(data[0]))
            print(data)
            
            for line in data.strip().split("\n"):
                self.resultats_tempsreel.insert(tk.END, line)

            # for _, row in data.iterrows():
            #     self.resultats_tempsreel.insert(tk.END, ', '.join(row.astype(str)))

            # self.resultats_tempsreel.insert(tk.END,entree)
        else:
            self.resultats_tempsreel.pack_forget()


    def set_command(self,command):
        self.boutton_recherche["command"]= lambda: command(self.entry_nm_nb.get(),self.pack)


    def clear_placeholder_text(self, event):
        # Efface le texte initial lorsque l'utilisateur clique dans l'entry
        if self.nom_nombre.get() == "Nom ou numéro Pokemon":
            self.nom_nombre.set("")

        # Change la couleur du texte à noir lorsque l'utilisateur commence à taper
        self.entry_nm_nb.config(foreground="black")


    def restore_placeholder_text(self, event):
        # Restaure le texte initial si l'entry est vide
        if not self.nom_nombre.get():
            self.nom_nombre.set("Nom ou numéro Pokemon")

            # Change la couleur du texte à gris si l'entry est vide
            self.entry_nm_nb.config(foreground="grey")



class Frame_dynamiquev2 (ttk.Frame):
    def __init__(self, pere, pos_initial, pos_final, Y, X, hauteur, largeur):
        super().__init__(master=pere)
        
        self.start = pos_initial + 0.04
        self.end = pos_final - 0.04
        self.largeur = largeur
        self.hauteur=hauteur

        self.position = pos_initial
        self.home = True
        self.Y = Y  # True pour gauche, False pour droite
        self.X = X  # True pour haut, False pour bas

        self.place(relx=self.start if self.Y else 0, rely=self.start if self.X else 0, relheight=self.hauteur, relwidth=self.largeur)

    def animation(self):
        if self.home:
            self.animation_palante()
        else:
            self.animation_patras()

    def animation_palante(self):
        if self.Y:  # Si c'est à gauche
            if self.position > self.end:
                self.position -= 0.008
                self.place(relx=self.position if self.Y else 0, rely=self.position if self.X else 0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_palante)
            else:
                self.home=False
        else:  # Si c'est à droite
            if self.position < self.end:
                self.position += 0.008
                self.place(relx=self.position if self.Y else 0, rely=self.position if self.X else 0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_palante)
            else:
                self.home=False

    def animation_patras(self):
        if self.Y:  # Si c'est à gauche
            if self.position < self.start:
                self.position += 0.008
                self.place(relx=self.position if self.Y else 0, rely=self.position if self.X else 0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_patras)
            else:
                self.home=True
        else:  # Si c'est à droite
            if self.position > self.start:
                self.position -= 0.008
                self.place(relx=self.position if self.Y else 0, rely=self.position if self.X else 0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_patras)
            else:
                self.home=True



class Frame_dynamique_colonne (ttk.Frame):
    def __init__(self, pere, pos_initial, pos_final,pos_y,side_gauche,hauteur,largeur,vitesse):
        super().__init__(master=pere)
        
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



class Frame_dynamique_ligne (ttk.Frame):
        def __init__(self, pere, pos_initial, pos_final,pos_x,side_top,hauteur,largeur,vitesse):
            super().__init__(master=pere)

            self.start = pos_initial + 0.04
            self.end = pos_final - 0.04
            self.pos_x=pos_x
            self.largeur = largeur
            self.hauteur=hauteur

            self.position = pos_initial
            self.home = True
            self.Y = side_top  # True para arriba, False para abajo

            self.vitesse=vitesse
            self.place(relx=self.pos_x, rely=self.start, relheight=self.hauteur, relwidth=self.largeur)

        def animation(self):
            if self.home:
                self.animation_palante()
            else:
                self.animation_patras()

        def animation_palante(self):
            if self.Y:  # Si es arriba
                if self.position > self.end:
                    self.position -= 0.008
                    self.place(relx=self.pos_x, rely=self.position, relheight=self.hauteur, relwidth=self.largeur)
                    self.after(self.vitesse, self.animation_palante)
                else:
                    self.home=False
            else:  # Si es abajo
                if self.position < self.end:
                    self.position += 0.008
                    self.place(relx=self.pos_x, rely=self.position, relheight=self.hauteur, relwidth=self.largeur)
                    self.after(self.vitesse, self.animation_palante)
                else:
                    self.home=False

        def animation_patras(self):
            if self.Y:  # Si es arriba
                if self.position < self.start:
                    self.position += 0.008
                    self.place(relx=self.pos_x, rely=self.position, relheight=self.hauteur, relwidth=self.largeur)
                    self.after(self.vitesse, self.animation_patras)
                else:
                    self.home=True
            else:  # Si es abajo
                if self.position > self.start:
                    self.position -= 0.008
                    self.place(relx=self.pos_x, rely=self.position, relheight=self.hauteur, relwidth=self.largeur)
                    self.after(self.vitesse, self.animation_patras)
                else:
                    self.home=True


# g=GUI([])
# g.letsgoooo()
