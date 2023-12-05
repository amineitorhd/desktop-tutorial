import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex Python App")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width-(screen_width//2)}x{screen_height-(screen_height//2)}")
        self.minsize(500,300)
        lim=(0,0,2000,6000)
        

        #Initialisation deux images de fond_ecran dépendant du mode
        self.ecran=Image.open("View/fond_ecran_pokedex.jpeg")
        self.ecran_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png")
        self.ecran_actuel=self.ecran
        
        #Initialisation du Fond d_ecran avec un canvas personnalise
        self.fond_ecran=Fond_Ecran(self,lim,self.ecran,"red")
        self.fond_ecran.pack(expand=True,fill="both")

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

        #Inisialisation d_un Frame contenant les pokemons affiche
        self.Frame_affichage=Affichage_pokemons(self,
                                                self.ecran)
        self.Frame_affichage.place(x=0,rely=0.55,relwidth=1,relheight=0.45)


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
        self.Frame_affichage.fond_Affichage.change_mode_obscur(self.ecran_actuel)
        # self.Frame_affichage.config_fond_ecran(self.ecran_actuel)


    def letsgoooo(self):
        self.mainloop()



class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,a,ecran,fond="magenta",expand_ecran=False,numb_pokemons=200,):
        super().__init__(mere,bg=fond,scrollregion=a)
        self.numb_pokemons=numb_pokemons
        self.expand_ecran=expand_ecran
        self.image_fond_ecran=ecran
        self.ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
        
        self.bind('<Configure>', self.config_fond_ecran)

    def config_fond_ecran(self,event=None):

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
                # Créer l'image sur el canvas
            self.ecran_tk = ImageTk.PhotoImage(self.image_fond_ecran)
            num_filas = int(self.numb_pokemons ** 0.5)  # Calcula el número de filas y columnas para una cuadrícula cuadrada
            num_columnas = int(largeur/1024)+1
            print("Imagenes en columnas creadas son:",num_columnas)
            print("Imagenes en filas creadas son:",num_filas)
            for i in range(num_filas):
                for j in range(num_columnas):
                    self.create_image(j*self.image_fond_ecran.width, i*self.image_fond_ecran.height, image=self.ecran_tk, anchor="nw")
            self.create_image(0, 0, image=self.ecran_tk, anchor="nw")

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
        
        self.fond_Affichage=Fond_Ecran(self,(0,0,self.winfo_width(),100),ecran,
                                       expand_ecran=True)
        self.fond_Affichage.config_fond_ecran()
        # self.ratio_image=self.ecran.size[0]/self.ecran.size[1]
        # self.config_fond_ecran(self.ecran,num_frames)

        self.fond_Affichage.pack(side="left",fill="both",expand=1)

        

#Tutoriel mec marrant

        self.Frame1=ttk.Frame(self.fond_Affichage)
        self.Frame2=ttk.Frame(self.fond_Affichage)
        
        self.scroll=ttk.Scrollbar(self,orient="vertical",command=self.fond_Affichage.yview)
        self.fond_Affichage.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(relx=1,rely=0,relheight=1,anchor="ne")
        
        self.fond_Affichage.bind("<MouseWheel>",self.Mouse_Wheel_configuration)
        
        self.bind("<Configure>",self.actualisation_fenetres)

        
    def Mouse_Wheel_configuration(self,event):
        x, y = self.winfo_pointerxy()  # Obtener las coordenadas del ratón
        widget_under_cursor = self.winfo_containing(x, y)
        if not widget_under_cursor==self.mere.Frame_filtrage.resultats_tempsreel:
            self.fond_Affichage.yview_scroll(-int(event.delta / 60), "units")
        

    def actualisation_fenetres(self,event):
        print("........actualisation des fenetres d'affichage............")
        self.fond_Affichage.config(scrollregion=self.fond_Affichage.bbox("all"))
        
        self.fond_Affichage.create_window((20,20), window=self.Frame1,
                                           anchor="nw")
        self.fond_Affichage.create_window((500,20), window=self.Frame2,
                                           anchor="nw")
        

    def initialisation(self,data):
        # print("commande bien reçu! Data reçu:\n",data)
        # Crear dos Frames, uno para la columna izquierda y otro para la derecha
        self.frames_pokemons=[]
        # Alternar entre agregar marcos a la columna izquierda y derecha
        for index, row in data.iterrows():
            if index % 2 == 0:  # Si el índice es par, agregar a la columna izquierda
                self.frame_unitaire_affichage(row["Name"],row["Number"], self.Frame1)

            else:  # Si el índice es impar, agregar a la columna derecha
                self.frame_unitaire_affichage(row["Name"],row["Number"], self.Frame2)

            self.frames_pokemons.append(self.frame_unitaire_affichage)




    def frame_unitaire_affichage(self,nom,numero,columna):
        fr=ttk.Frame(columna)
        cv=tk.Canvas(fr,bg="orange")
        cv.pack()

        label_pokemon_nom=ttk.Label(cv,text=f"{nom}")
        label_pokemon_nom.place(relx=0.35,rely=0,relheight=0.3,relwidth=0.4)
        
        label_pokemon_numero=ttk.Label(cv,text=f"#{numero}")
        label_pokemon_numero.place(relx=0.9,rely=0.75)
        
        image_pokemon=tk.Canvas(cv,bg="black")
        image_pokemon.place(relx=0,rely=0,relheight=1,relwidth=0.21)
        
        image_type1=tk.Canvas(cv,bg="green")
        image_type1.place(relx=0.35,relwidth=0.1,rely=0.35,relheight=0.1)

        image_type2=tk.Canvas(cv,bg="yellow")
        image_type2.place(relx=0.46,relwidth=0.1,rely=0.35,relheight=0.1)
        return fr
        

    def affichage_resultat_filtrage(self,data):
        # Supprimer tous les widgets de Frame1 et Frame2
        for widget in self.Frame1.winfo_children():
            widget.destroy()
        for widget in self.Frame2.winfo_children():
            widget.destroy()

        self.initialisation(data)

        

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


    def temps_reel(self,*args):
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
        self.home = True
        self.Y = side_gauche  # True para izquierda, False para derecha

        self.vitesse=vitesse
        self.place(relx=self.start, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)

    def animation(self):
        if self.home:
            self.animation_palante()
        else:
            self.animation_patras()

    def animation_palante(self):
        if self.Y:  # Si es izquierda
            if self.position > self.end:
                self.position -= 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_palante)
            else:
                self.home=False
        else:  # Si es derecha
            if self.position < self.end:
                self.position += 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_palante)
            else:
                self.home=False

        

    def animation_patras(self):
        if self.Y:  # Si es izquierda
            if self.position < self.start:
                self.position += 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_patras)
            else:
                self.home=True
        else:  # Si es derecha
            if self.position > self.start:
                self.position -= 0.008
                self.place(relx=self.position, rely=self.pos_y, relheight=self.hauteur, relwidth=self.largeur)
                self.after(self.vitesse, self.animation_patras)
            else:
                self.home=True



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
