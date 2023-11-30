import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokedex Python App")
        self.geometry("1000x600")
        self.minsize(500,300)
        lim=(0,0,2000,6000)
        
        #Initialisation deux images de fond_ecran dépendant du mode
        self.ecran=Image.open("View/fond_ecran_pokedex.jpeg")
        self.ecran_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png")
        self.ecran_actuel=self.ecran
        
        #Initialisation du Fond d_ecran avec un canvas personnalise
        self.fond_ecran=Fond_Ecran(self,lim,self.ecran,"red")
        self.fond_ecran.pack(expand=True,fill="both")
        
        #Initialisation d_un Frame dynamique personnalisee contenant
        #       les configurations du Pokedex 
        self.Frame_Configuration=Frame_dynamique(self,-0.3,0,False,hauteur=0.2,largeur=0.4)
        self.boutton_configuration=ttk.Button(self,text="Configuration",
                                              command=self.Frame_Configuration.animation).place(relx=0,rely=0.2)
        #Boutton permettant de switch entre mode obscure ou pas
        buton_obscur=ttk.Button(self.Frame_Configuration,text="Obscure Mode",
                                command=self.actualisation_mode_obscur).place(relx=0.5,rely=0.5)

        #Initialisation Frame contenant bare de recherche
        self.Frame_filtrage=Frame_Recherche_simple(self)
        self.Frame_filtrage.place(relx=0.30,relwidth=0.4,y=0)

        #Initialisation d_un Frame dynamique personnalisee contenant
        #       les filtres possibles 
        self.filtres_avancee=Frame_dynamique(self,1.0,0.80,True,hauteur=0.45,largeur=0.25)
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

    def ok(self, text):
        self.Frame_affichage.affichage_resultat_filtrage(textsasa)

class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,a,ecran,fond="magenta",expand_ecran=False,numb_pokemons=200):
        super().__init__(mere,bg=fond,scrollregion=a)
        self.numb_pokemons=numb_pokemons
        self.expand_ecran=expand_ecran
        self.image_fond_ecran=ecran
        self.ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
        
        self.bind('<Configure>', self.config_fond_ecran)

    def config_fond_ecran(self,event=None):

        largeur=self.winfo_width()
        hauteur=self.winfo_height()

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
            num_columnas = num_filas
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
        self.image_on_canvas = None 
        
        self.fond_Affichage=Fond_Ecran(self,None,ecran,expand_ecran=True)
        self.fond_Affichage.config_fond_ecran()
        # self.ratio_image=self.ecran.size[0]/self.ecran.size[1]
        # self.config_fond_ecran(self.ecran,num_frames)

        self.fond_Affichage.pack(side="left",fill="both",expand=1)

        scroll=ttk.Scrollbar(self,orient="vertical",command=self.fond_Affichage.yview)
        self.fond_Affichage.configure(yscrollcommand=scroll.set)
        scroll.place(relx=1,rely=0,relheight=1,anchor="ne")

        self.fond_Affichage.configure(yscrollcommand=scroll)
        self.fond_Affichage.bind("<Configure>",lambda e: self.fond_Affichage.configure(scrollregion= self.fond_Affichage.bbox("all")))

        self.Frame1=ttk.Frame(self.fond_Affichage)
        self.Frame2=ttk.Frame(self.fond_Affichage)
        self.fond_Affichage.create_window((20,20), window=self.Frame1, anchor="nw")
        self.fond_Affichage.create_window((820,20), window=self.Frame2, anchor="nw")

    def config_fond_ecran(self, ecran, num_frames=5):
        print("redimenzionando[.................]")
        largeur=self.fond_Affichage.winfo_width()
        hauteur=self.fond_Affichage.winfo_height()

        ecran_ratio=largeur/hauteur

        if self.ratio_image<ecran_ratio:
            x=int(largeur)
            y=int(x/self.ratio_image)
        else:
            y=int(hauteur)
            x=int(y*self.ratio_image)

        updated_ecran=ecran.resize((x,y))
        self.updated_ecran_tk=ImageTk.PhotoImage(updated_ecran)
        if self.image_on_canvas is None:
            self.image_on_canvas = self.fond_Affichage.create_image(int(largeur/2),
                        int(hauteur/2),
                        image=self.updated_ecran_tk,
                        anchor="center")
        else:
            print("he cambiado la imagen!!!!")
            self.fond_Affichage.itemconfig(self.image_on_canvas, image=self.updated_ecran_tk)

        # Créer l'image sur el canvas
        self.ecran_tk = ImageTk.PhotoImage(ecran)
        num_filas = int(num_frames ** 0.5)  # Calcula el número de filas y columnas para una cuadrícula cuadrada
        num_columnas = num_filas
        for i in range(num_filas):
            for j in range(num_columnas):
                self.fond_Affichage.create_image(j*self.ecran.width, i*self.ecran.height, image=self.ecran_tk, anchor="nw")
        self.fond_Affichage.create_image(0, 0, image=self.ecran_tk, anchor="nw")
        
    def initialisation(self,data):
        # print("commande bien reçu! Data reçu:\n",data)
        # Crear dos Frames, uno para la columna izquierda y otro para la derecha
        
        # Alternar entre agregar marcos a la columna izquierda y derecha
        for index, row in data.iterrows():
            if index % 2 == 0:  # Si el índice es par, agregar a la columna izquierda
                self.frame_unitaire_affichage(row["Name"],row["Number"], self.Frame1)
                
            else:  # Si el índice es impar, agregar a la columna derecha
                self.frame_unitaire_affichage(row["Name"],row["Number"], self.Frame2)
                # self.Frame2.pack(side="left")

        # self.config_fond_ecran(self.ecran)

    def frame_unitaire_affichage(self,nom,numero,columna):
        fr=ttk.Frame(columna)
        cv=tk.Canvas(fr,bg="orange",width=500,height=100)
        cv.pack(fill="both",expand=1)

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
        
        fr.pack(pady=5,padx=(10,0))
        

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
       
        self.boutton_recherche=ttk.Button(mere,text="chercher!")
        self.boutton_recherche.place(relx=0.7,y=0)

        self.nom_nombre=tk.StringVar()
        self.nom_nombre.trace("w", self.temps_reel)  #Bizare car obligé 3 arguments!

        self.entry_nm_nb=ttk.Entry(self,textvariable=self.nom_nombre)
        self.entry_nm_nb.pack(fill="x")                
        self.entry_nm_nb.insert(0, "Nom ou numéro Pokemon")
        # Liaison d'événement pour effacer le texte initial lorsqu'un clic est effectué sur l'entry
        self.entry_nm_nb.bind("<FocusIn>", self.clear_placeholder_text)
        # Liaison d'événement pour restaurer le texte initial s'il n'y a pas de texte entré
        self.entry_nm_nb.bind("<FocusOut>", self.restore_placeholder_text)


    def temps_reel(self,*args):
        self.boutton_recherche.invoke()

    def set_command(self,command):
        self.boutton_recherche["command"]= lambda: command(self.entry_nm_nb.get())

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

class Frame_dynamique (ttk.Frame):
    def __init__(self, pere, pos_initial, pos_final, Y,hauteur,largeur):
        super().__init__(master=pere)
        
        self.start = pos_initial + 0.04
        self.end = pos_final - 0.04
        self.largeur = largeur
        self.hauteur=hauteur

        self.position = pos_initial
        self.home = True
        self.Y = Y  # True para izquierda, False para derecha

        self.place(relx=self.start, rely=0, relheight=self.hauteur, relwidth=self.largeur)

    def animation(self):
        if self.home:
            self.animation_palante()
        else:
            self.animation_patras()

    def animation_palante(self):
        if self.Y:  # Si es izquierda
            if self.position > self.end:
                self.position -= 0.008
                self.place(relx=self.position, rely=0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_palante)
            else:
                self.home=False
        else:  # Si es derecha
            if self.position < self.end:
                self.position += 0.008
                self.place(relx=self.position, rely=0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_palante)
            else:
                self.home=False

        

    def animation_patras(self):
        if self.Y:  # Si es izquierda
            if self.position < self.start:
                self.position += 0.008
                self.place(relx=self.position, rely=0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_patras)
            else:
                self.home=True
        else:  # Si es derecha
            if self.position > self.start:
                self.position -= 0.008
                self.place(relx=self.position, rely=0, relheight=self.hauteur, relwidth=self.largeur)
                self.after(10, self.animation_patras)
            else:
                self.home=True
        



# g=GUI([])
# g.letsgoooo()
