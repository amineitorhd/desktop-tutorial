import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class GUI(tk.Tk):
    def __init__(self,filtres):
        super().__init__()
        self.title("Pokedex Python App")
        self.geometry("1000x600")
        self.minsize(500,300)
        lim=(0,0,2000,6000)
        self.fond_ecran=Fond_Ecran(self,lim,"red")
        self.ecran=self.fond_ecran.get()
        self.ecran_obscur=Image.open("View/fond_ecran_pokedex_obscur_mode.png")
        self.ecran_actuel=self.ecran

        self.Frame_filtrage=Frame_Recherche_simple(self)
        self.Frame_filtrage.place(relx=0.30,relwidth=0.4,y=0)

        self.Frame_affichage=Affichage_pokemons(self,self.ecran,50)
        self.Frame_affichage.place(x=0,rely=0.35,relwidth=1,relheight=0.65)

        buton_obscur=ttk.Button(self,text="fuckoff",command=self.actualisation_mode_obscur)
        buton_obscur.place(relx=0.5,rely=0.5)

        self.filtres_avanc=Filtres_avancee(self,1.0,0.7)
        self.boutton_filtres_avanc=ttk.Button(self,text="plus de filtres",command=self.filtres_avanc.animation)
        self.boutton_filtres_avanc.place(relx=0.25,rely=0.5)
        tk.Canvas(self.filtres_avanc,bg="red").pack(fill="both",expand=1)

    def actualisation_mode_obscur(self):
        if self.ecran_actuel==self.ecran:
            self.ecran_actuel=self.ecran_obscur
        else:
            self.ecran_actuel=self.ecran
            
        
        self.fond_ecran.change_mode_obscur(self.ecran_actuel)
        self.Frame_affichage.config_fond_ecran(self.ecran_actuel)

    def letsgoooo(self):
        self.mainloop()

class Fond_Ecran(tk.Canvas):
    def __init__(self,mere,a,fond="red"):
        super().__init__(mere,bg=fond,scrollregion=a)
        self.pack(expand=True,fill="both")
        self.set_fond_ecran()
        self.bind('<Configure>', self.config_fond_ecran)

    def set_fond_ecran(self):
        self.image_fond_ecran=Image.open("View/fond_ecran_pokedex.jpeg")
        self.ratio_image=self.image_fond_ecran.size[0]/self.image_fond_ecran.size[1]
 

    def config_fond_ecran(self,event):

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

    def change_mode_obscur(self,ecran):
        self.image_fond_ecran=ecran
        self.config_fond_ecran(None)

    def get(self):
        return self.image_fond_ecran

class Affichage_pokemons(ttk.Frame):
    def __init__(self,mere,ecran,num_frames):
        super().__init__(mere)
        self.ecran=ecran
        self.image_on_canvas = None 
        self.Affichage=tk.Canvas(self,bg="yellow")
        self.ratio_image=self.ecran.size[0]/self.ecran.size[1]
        self.config_fond_ecran(self.ecran,num_frames)

        self.Affichage.pack(side="left",fill="both",expand=1)

        scroll=ttk.Scrollbar(self,orient="vertical",command=self.Affichage.yview)
        scroll.pack(side="right",fill="y")

        self.Affichage.configure(yscrollcommand=scroll)
        self.Affichage.bind("<Configure>",lambda e: self.Affichage.configure(scrollregion= self.Affichage.bbox("all")))

        self.Frame1=ttk.Frame(self.Affichage)
        self.Frame2=ttk.Frame(self.Affichage)
        self.Affichage.create_window((20,20), window=self.Frame1, anchor="nw")
        self.Affichage.create_window((820,20), window=self.Frame2, anchor="nw")

    def config_fond_ecran(self, ecran, num_frames=5):
        print("redimenzionando[.................]")
        largeur=self.Affichage.winfo_width()
        hauteur=self.Affichage.winfo_height()

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
            self.image_on_canvas = self.Affichage.create_image(int(largeur/2),
                        int(hauteur/2),
                        image=self.updated_ecran_tk,
                        anchor="center")
        else:
            print("he cambiado la imagen!!!!")
            self.Affichage.itemconfig(self.image_on_canvas, image=self.updated_ecran_tk)

        # Créer l'image sur el canvas
        self.ecran_tk = ImageTk.PhotoImage(ecran)
        num_filas = int(num_frames ** 0.5)  # Calcula el número de filas y columnas para una cuadrícula cuadrada
        num_columnas = num_filas
        for i in range(num_filas):
            for j in range(num_columnas):
                self.Affichage.create_image(j*self.ecran.width, i*self.ecran.height, image=self.ecran_tk, anchor="nw")
        self.Affichage.create_image(0, 0, image=self.ecran_tk, anchor="nw")
        
        

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

        self.config_fond_ecran(self.ecran)

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
        self.nom_nombre=tk.StringVar()
        self.nom_nombre.trace("w", self.affichage)


        self.entry_nm_nb=ttk.Entry(self,textvariable=self.nom_nombre)
        self.entry_nm_nb.pack(side="top",fill="x")        
        self.entry_nm_nb.insert(0, "Nom ou numéro Pokemon")
        # Liaison d'événement pour effacer le texte initial lorsqu'un clic est effectué sur l'entry
        self.entry_nm_nb.bind("<FocusIn>", self.clear_placeholder_text)
        # Liaison d'événement pour restaurer le texte initial s'il n'y a pas de texte entré
        self.entry_nm_nb.bind("<FocusOut>", self.restore_placeholder_text)

        self.boutton_recherche=ttk.Button(mere,text="chercher!")
        self.boutton_recherche.place(relx=0.7,y=0)

    def affichage(self,*args):
        print("waoooow:   ", self.nom_nombre.get())
    
    def set_command(self,command):
        print("ok")
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

class Filtres_avancee (ttk.Frame):
    def __init__(self,pere,pos_initial,pos_final):
        super().__init__(master=pere)
        self.start=pos_initial+0.04
        self.end=pos_final-0.04
        self.largeur=abs(pos_initial-pos_final)
        
        self.position=pos_initial
        self.home=True

        self.place(relx=self.start,rely=0,relheight=1,relwidth=self.largeur)

    def animation(self):
        if self.home:
            self.animation_palante()
        else:
            self.animation_patras()

    def animation_palante(self):
        if self.position>self.end:
            self.position-=0.008
            self.place(relx=self.position,rely=0,relheight=1,relwidth=self.largeur)
            self.after(10,self.animation_palante)
        else:
            self.home=False

    def animation_patras(self):
        if self.position<self.start:
            self.position+=0.008
            self.place(relx=self.position,rely=0,relheight=1,relwidth=self.largeur)
            self.after(10,self.animation_patras)
        else:
            self.home=True



# g=GUI([])
# g.letsgoooo()
