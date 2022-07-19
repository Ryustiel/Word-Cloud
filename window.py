'''
Created on 30 mars 2020

@author: Moi

PS : Vous pouvez vous amuser avec les fichiers textes "long", "treslong", "trestreslong" et "insanelylong" pour voir les differents etats du bouton0 en fonctions des conditions.
Ces fichiers ont beaucoup de caracteres mais il ne s'agit que du meme mot : le temps de traitement est extremement court meme pour le plus gros.

Je rappelle egalement qu'il faut maintenir shift en cliquant sur le bouton lorsqu'il est rouge ou violet.
C'est une "securite enfant" on va dire (en vrai c'etait sense eviter les clics accidentels mais j'ai pas eu le temps de coder l'indicateur)

Aussi, il faut cliquer hors de la zone de texte ~plein de fois~ pour que l'appui sur la touche shift soit transmise au bouton.
Si j'avais eu le temps encore, j'aurais fait en sorte que la zone de saisie perde le focus (avoir le focus = recevoir la saisie clavier; le focus se change en appuyant sur tab) apres la generation du texte (+ un petit delai), ou lorsque le bouton est survole.
Mais je n'ai pas eu le temps de le faire. Donc il faut faire des petits clics au hasard pour se detacher de la zone de texte pour l'instant...
'''
#imports...
import tkinter as tk
#import fwords #module de tri du texte #@UnresolvedImport
#import cloudgen #module de generation d'image #@UnresolvedImport
global text_cache #(string) sauvegarde le dernier texte charge dans le module fwords (permet de verifier si le texte a change lors de l'appel de la fonction titleAnalyzer)
text_cache = "" #cela evite que la fonction recherche a nouveau les mots alors que c'est deja enregistre dans la variable public_dict

WordsParameters = [10, 4, 10] #WordsParameters est un tableau qui contient tous les parametres disponibles dans le menu median (orange) sauf les cases a cocher dont l'etat est directement represente par la variable de verouillage LockedItems.
#il comprend dans cet ordre [le nombre de mots a afficher](int), [la longueur minimale des mots](int) et [la longueur maximale des mots](int)
#les valeurs longueur minimale et longueur maximale sont issue du meme menu (menuB).

#attributs de la fenetre TKinter
window = tk.Tk()
#window.iconbitmap("icons/icon.ico")
window.title("Thing")
window.geometry("700x350") #Taille de la fenetre en pixels
window.resizable(0, 0) #NoResizing desactive le changement de taille

#Static -----------------------------------------------------------

bgimage = tk.PhotoImage(file="base_frame.gif") #image

bg = tk.Canvas(window, width=700, height=350, bd=-2) #Background Display Widget
bgvisual = bg.create_image(0, 0, anchor=tk.NW, image=bgimage)

bg.place(x=0, y=0) #position

#Indicateur > Text Manager ----------------------------------------

titleIndicator = tk.Label(window, font=('Impact', 10), bg="white", text="BLAH", justify="center") #definis le widget indicateur de titre

#comportement
def setTitleIndicator(mode):
    """
    En fonction du parametre "mode", met a jour le label indicateur situe sous la boite d'entree de fichier texte et le bouton d'execution a sa droite.
    """
    #mode est un integer qui reflette l'etat du TitleIndicator
    if (mode==0): #Les sorties des valeurs mode sont ordonnees par occurence. (mode==0) a plus de chances d'etre True que (mode==1)...
        titleIndicator.place(x=87, y=43) #position de l'indicateur (de maniere a ce qu'il soit centre)
        titleIndicator["text"] = "o o o" #s'affiche lorsque le programme attends toujours une entree texte
        titleIndicator["fg"] = "black" #change la couleur du texte pour convenir ce qu'il indique
        setButton0(0) #rend indisponible le bouton (l'etat 0 correspond a sa disparition)
    elif (mode==1):
        titleIndicator.place(x=48, y=43) #position de l'indicateur
        titleIndicator["text"] = "Fichier Introuvable" #s'affiche quand le contenu de title ne correspond au nom d'aucun fichier
        titleIndicator["fg"] = "black"
    elif (mode==2):
        titleIndicator.place(x=38, y=43) #position de l'indicateur
        titleIndicator["text"] = "Comporte des Espaces" #s'affiche lorsque le contenu de title contient des espaces : les noms de fichiers ne doivent pas contenir d'espaces
        titleIndicator["fg"] = "black"
    elif (mode==3):
        titleIndicator.pack()
        titleIndicator.pack_forget() #decharge le label lorsque le texte est suffisament court pour etre traite instantanement (< x caracteres) ou qu'aucun text n'est present sur la ligne  
    elif (mode==4):
        titleIndicator.place(x=87, y=41) #position de l'indicateur
        titleIndicator["text"] = "Long" #La longueur du texte est comprise entre 20_000 et 80_000 caracteres : son traitement peut etre relativement long
        titleIndicator["fg"] = "#DDEE00"
    elif (mode==5):
        titleIndicator.place(x=74, y=42)
        titleIndicator["text"] = "Tres Long" #La longueur du texte est comprise entre 80_000 et 360_000 caracteres
        titleIndicator["fg"] = "orange"
    elif (mode==6):
        titleIndicator.place(x=46, y=42)
        titleIndicator["text"] = "Beaucoup Trop Long" #La longueur du texte est comprise entre 360_000 et 1_000_000 caracteres
        titleIndicator["fg"] = "red"
    elif (mode==7):
        titleIndicator.place(x=84, y=41)
        titleIndicator["text"] = "Insane" #La longueur du texte est superieure a 1_000_000 carateres
        titleIndicator["fg"] = "purple"
        
#position
titleIndicator.place(x=87, y=44)

#Text Manager-------------------------------------------------------
#title
titlebox = tk.Entry(window, relief='flat', font=('Impact', 20), width=13, justify="center", bg="white", insertwidth=8, insertbackground="orange", selectbackground="gold", selectforeground="black")
textbox = tk.Text(window, state="disabled", relief='flat', wrap="word", width=24, height=18, bg="white", insertwidth=2, selectbackground="orange", selectforeground="black")

#position
titlebox.place(x=11, y=11)
textbox.place(x=7, y=60)

#les id des callback lances (pour les arreter via after_cancel (pour reinitialiser le delai d'analyse a chaque saisie de mot))
ID_identifier = [None, None] #un nouvel id de callback (string) sera stocke ici a chaque actualisation du delai (la seconde entree du tableau sert pour la fonction button0() lors du clic de reactualisation)
#ID identifier est un tableau
#comportements 
def delayAnalyzer(*args):
    """
    declenche titleAnalyzer lorsque l'utilisateur arrete de saisir du texte.
    Cette fonction est declenchee par la pression d'une touche lorsque la zone de saisie de texte est selectionnee.
    """
    setTitleIndicator(0) #actualise l'indicateur de titre pour signaler a l'utilisateur que sa saisie a ete prise en compte
    if not(ID_identifier[0] is None): #n'execute l'instruction after_cancel que si un identifiant est deja contenu dans ID_identifier
        window.after_cancel(ID_identifier[0]) #annule le callback de titleAnalyzer initie auparavant
    ID_identifier[0] = window.after(600, titleAnalyzer) #debute (a nouveau...) un callback de titleAnalyzer avec un delai de 500 ms 
    
def titleAnalyzer():
    """
    Charge le texte specifie dans la zone de saisie a l'aide de la fonction fwords.loaded(),
    Puis ajuste l'etat de l'indicateur de titre et du bouton0 via les fonctions setButton0 et setTitleIndicator selon le texte precharge.
    Cette fonction peut egalement declencher automatiquement l'analyse d'un texte si il est suffisament court (avec la fonction fullGeneration())
    """
    global text_cache #text_cache est une string contenant le dernier texte ouvert et analyse par sorted(). Cette variable est mise a jour par fullGeneration()
    submenuUnload() #ferme les menus secondaires
    
    textbox.config(state="normal") #rend editable le widget textbox
    textbox.delete(0.0, "end") #efface l'espace de texte pour le faire correspondre au nouveau titre
    
    if (titlebox.get() == ""): #lorsque la saisie du titre est vide
        setTitleIndicator(3) #defini l'indicateur
        textbox.config(state="disabled") #rend a nouveau le widget ineditable
    else:
        goOn = True #ignore le reste des instructions si False (est un booleen)
        for char in titlebox.get(): #pour chaque caractere du titre
            if (char == " "): #regarde si c'est un espace. Si ca l'est :
                setTitleIndicator(2) 
                textbox.config(state="disabled")
                goOn = False #pour eviter des executions inutiles
                break
        
        if (goOn):
            if (fwords.loaded(titlebox.get()) == None): #charge le fichier en utilisant le nom indique dans titlebox. Si la fonction retourne un NoneType, le message de l'indicateur est mis a jour et la fonction s'arrete, sinon, l'execution continue, la fonction loaded() met automatiquement a jour la public_string qui sera lue dans les executions suivantes.
                setTitleIndicator(1)
                
            elif (text_cache == fwords.public_string): #si le texte est deja charge, saute la verification de la longueur et propose directement le bouton reload (actualisation)
                textbox.insert("end", fwords.public_string)
                textbox.config(state="disabled")
                setTitleIndicator(3)
                setButton0(1)
                
            else: #les actions suivantes dependent du nombre de caracteres du fichier texte
                
                textbox.insert("end", fwords.public_string) #affiche du texte dans l'espace de texte textbox
                textbox.config(state="disabled") #desactive a nouveau la boite de texte
                char_count = len(fwords.public_string) #(int) nombre de caracteres du fichier charge
                print(char_count)
                
                if (char_count <= 20_000):
                    setTitleIndicator(3) #change l'indicateur
                    setButton0(1) #definit le bouton pour permettre a l'utilisateur de generer a nouveau une image a partir du meme texte
                    fullGeneration()#genere directement l'image sans afficher le bouton de confirmation (car le texte est assez court pour que le delai ne se ressente meme pas)
                    #fait apparaitre le bouton reload pour tenter un nouvel affichage
                    
                elif (char_count > 20_000) and (char_count <= 80_000):
                    setTitleIndicator(4)
                    setButton0(2) #change le bouton 0 (mode confirmation : l'utilisateur doit clicker sur le bouton pour trier effectivement le texte)
                    
                elif (char_count > 80_000) and (char_count <= 360_000):
                    setTitleIndicator(5)
                    setButton0(3) #mode confirmation, autre couleur...
                    
                elif (char_count > 360_000) and (char_count <= 1_000_000):
                    setTitleIndicator(6)
                    setButton0(4) #same
                    
                else:
                    setTitleIndicator(7)
                    setButton0(5) #mode confirmation avec combinaison click shift de securite
#association des evenements
titlebox.bind("<KeyPress>", delayAnalyzer)
titlebox.bindtags(tagList=('Entry', '.!entry', '.', 'all')) #donne la priorite a la class du widget qui gere le traitement de texte (la priorite est donnee aux events specifiques au widgets par defaut)

#Image frame-------------------------------------------------------

cloudgen.setDrawArea((300, 300)) #render size according to the widget
renderimage = tk.PhotoImage(file="render.gif") #load

display = tk.Canvas(window, width=300, height=300, bd=-2, background='orange') #Displaying App
displayed_image = display.create_image(0, 0, anchor=tk.NW, image=renderimage)
#Texte resume des mots affiches (revele par bouton 4)
display_text = tk.Text(window, state="disabled", relief='flat', wrap="word", width=27, height=12, font=('Impact', 13), bg="black", foreground="orange", insertwidth=2, selectbackground="black", selectforeground="white", cursor="arrow") 

display.place(x=375, y=25) #position

#fonctions liees a l'image
def updateDisplay():
    """
    update app main image display canvas with the latest version of file "render.gif"
    """
    window.quit()  #stopping event loop to reload the registered images
    #image registration and update
    if ((WordsParameters[0] == 0) or (WordsParameters[2] == 0)):
        renderimage = tk.PhotoImage(file="blank.gif") #utilise blank.gif pour simuler l'absence de mots a la place de render.gif car aucune nouvelle image n'a ete generee (wordCount est defini a 0)
    else:
        renderimage = tk.PhotoImage(file="render.gif")
    display.itemconfig(displayed_image, image=renderimage) #met a jour l'image
    window.mainloop() #reactive la gestion des evenements
    
def reGenerate():
    """
    recupere les parametres et genere un nuage a partir du dictionnaire publique et l'affiche
    """
    if (WordsParameters[0] > 0) and (WordsParameters[2] > 0):
        fwords.getRelevant(fwords.sorted_dict, WordsParameters[0], forlength=WordsParameters[1], upto=WordsParameters[2], exclude=LockedItems[2])
        cloudgen.render(cloudgen.getDrawingInstructions()) #genere l'image a partir de sets d'instructions eux memes obtenus du resultat de la fonction fullLoad
    updateDisplay() #met a jour le canvas image display
    
def fullGeneration():
    """
    execute fowrds.grouped() et fwords.sorting() puis reGenerate()
    Enregistre le nouveau texte charge dans text_cache afin que titleAnalyzer ne le recharge pas pour rien. (detection de changement)
    """
    global text_cache
    print("Parameters :", WordsParameters)
    if (WordsParameters[0] > 0) and (WordsParameters[2] > 0): #desactive la generation lorsque le nombre de mots affiche est defini sur 0
        fwords.sorting(direct=True) #cree un dictionaire classant les mots par occurence avec les parametres selectionnes
        text_cache = fwords.public_string #enregistre le texte pour permettre a titleAnalyzer() de reconnaitre qu'il a deja ete charge et d'eviter par consequent des executions inutiles (lors du rechargement de l'image notamment, car seule le module cloudgen est necessaire)
        reGenerate()

#Menu Parametres ------------------------------------------------------------------------------------------------------------------------

#1/3 - boutons standalone (objets canvas rendus interactifs)
button0 = tk.Canvas(window, width=70, height=55, bd=-2, cursor="hand2") #bouton dynamique de confirmation pour la generation de l'image
button1 = tk.Canvas(window, width=70, height=60, bd=-2, cursor="hand2") #bouton menu nombre de mots a afficher
button2 = tk.Canvas(window, width=70, height=45, bd=-2, cursor="hand2") #bouton menu longueur des mots a classer
button3 = tk.Canvas(window, width=70, height=70, bd=-2, cursor="hand2") #case a cocher utiliser le tableau d'exception

#2/3 - indicateurs type tooltip --------
#ces labels s'affichent et disparaissent lors du survol des boutons pour donner des indications sur leur usage
tooltip0 = tk.Label(window, font=('Impact', 11), bg="white", text="")
tooltip1 = tk.Label(window, font=('Impact', 11), bg="white", text="Quantites")
tooltip2 = tk.Label(window, font=('Impact', 11), bg="white", text="Longueurs")
tooltip3 = tk.Label(window, font=('Impact', 11), bg="white", text="inutiles laisses")

#3/3 - menus secondaires et leurs elements (sliders et boutons) ---------------
menuA_wordcount = tk.Frame(window) #cadre menu hebergeant les curseurs de selection
cursorA1 = tk.Scale(menuA_wordcount, font=('Impact', 10), orient='vertical', from_=0, to=80, resolution=10, length=200, sliderlength=25) #curseur de selection
cursorA2 = tk.Scale(menuA_wordcount, font=('Impact', 10), orient='vertical', from_=0, to=9, length=200, sliderlength=25)
menuB_wordlength = tk.Frame(window) #chaque menu a son propre cadre et ses propres curseurs
cursorB1 = tk.Scale(menuB_wordlength, font=('Impact', 10), orient='vertical', from_=0, to=28, length=180, sliderlength=25)
cursorB2 = tk.Scale(menuB_wordlength, font=('Impact', 10), orient='vertical', from_=0, to=28, length=180, sliderlength=25)
labelB3 = tk.Label(menuB_wordlength, font=('Impact', 10), text="     min      max")

hovermenu = tk.Frame(window) #menu option de l'image finale [render] (s'affiche lorsqu'elle est survolee)
button4 = tk.Canvas(hovermenu, width=20, height=20, bd=-2, cursor="hand2") #type case a cocher
button5 = tk.Canvas(hovermenu, width=20, height=20, bd=-2, cursor="hand2")

#gestion des images : les fichiers sont nommes "button." [.. vide pour l'etat standard des boutons, H pour l'etat Hover, et T pour l'etat Tick (lorsque clicke ou coche)]
#(les boutons sont nommes "button." . designe leur identifiant), 
#les variables designant les images sont nomees "image..", les variables designant les elements canvas des boutons sont nommes "visualB." . est l'identifiant du bouton qui les contient
#imports d'images -------------------
image0 = [None] #les differentes formes dependent de l'etat du bouton, et sont classe selon leur declencheur dans ces trois tableaux (normal, survol, clic)
image0H = [None] #chaque entree du tableau contiendra donc une variable d'image sauf la premiere ([0]) qui reste vierge pour que la variable d'etat des boutons correspondent aux id d'entrees de tableau (car il existe un etat pour lequel aucune image n'est affichee : l'etat 0)
image0T = [None] #il y a 5 etats de boutons representes par une image, le 6e l'est par son absence (None)
image0.append(tk.PhotoImage(file="icons/button0A.gif")) #visuel bouton 0 etat A (reload) [etat de base : non clicke, non survole]
image0H.append(tk.PhotoImage(file="icons/button0AH.gif")) #H : meme bouton lorsque survole
image0T.append(tk.PhotoImage(file="icons/button0AT.gif")) #T : meme bouton lorsque clicke
image0.append(tk.PhotoImage(file="icons/button0B.gif"))
image0H.append(tk.PhotoImage(file="icons/button0BH.gif"))
image0T.append(tk.PhotoImage(file="icons/button0BT.gif"))
image0.append(tk.PhotoImage(file="icons/button0C.gif"))
image0H.append(tk.PhotoImage(file="icons/button0CH.gif"))
image0T.append(tk.PhotoImage(file="icons/button0CT.gif"))
image0.append(tk.PhotoImage(file="icons/button0D.gif"))
image0H.append(tk.PhotoImage(file="icons/button0DH.gif"))
image0T.append(tk.PhotoImage(file="icons/button0DT.gif"))
image0.append(tk.PhotoImage(file="icons/button0E.gif"))
image0H.append(tk.PhotoImage(file="icons/button0EH.gif"))
image0T.append(tk.PhotoImage(file="icons/button0ET.gif"))

image1 = tk.PhotoImage(file="icons/button1.gif") #visuel bouton menu nombre de mots
image1H = tk.PhotoImage(file="icons/button1H.gif") 
image1T = tk.PhotoImage(file="icons/button1T.gif") 
image2 = tk.PhotoImage(file="icons/button2.gif") #visuel bouton menu longueur des mots
image2H = tk.PhotoImage(file="icons/button2H.gif")
image2T = tk.PhotoImage(file="icons/button2T.gif")
image3 = tk.PhotoImage(file="icons/button3.gif") #visuel bouton utiliser les exceptions
image3H = tk.PhotoImage(file="icons/button3H.gif")
image3T = tk.PhotoImage(file="icons/button3T.gif")
image4 = tk.PhotoImage(file="icons/button4.gif") #visuel bouton menu liste de mots
image4H = tk.PhotoImage(file="icons/button4H.gif")
image4T = tk.PhotoImage(file="icons/button4T.gif")
image5 = tk.PhotoImage(file="icons/button5.gif") #visuel bouton de sauvegarde
image5H = tk.PhotoImage(file="icons/button5H.gif")

#inscription des images sur les boutons
visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0[0])
visual1 = button1.create_image(0, 0, anchor=tk.NW, image=image1)
visual2 = button2.create_image(0, 0, anchor=tk.NW, image=image2)
visual3 = button3.create_image(0, 0, anchor=tk.NW, image=image3)
visual4 = button4.create_image(0, 0, anchor=tk.NW, image=image4)
visual5 = button5.create_image(0, 0, anchor=tk.NW, image=image5)

#etats du Bouton 0 ---------------------------------------------------------------------------------
def setButton0(state): #fonction interne : affecte le comportement du button 0
    """
    definit l'etat du bouton zero selon l'argument "state"
    """
    global visual0ID #une variable de type integer qui contient une valeur entre 0 et 5 (6 valeurs differentes) correspondant a l'indice de l'image a afficher par le bouton dans les trois tableaux d'image button0..
    if (state == 0):
        if (visual0ID != 0):
            visual0ID = 0
            button0.pack()
            button0.pack_forget() #decharge le bouton si il ne l'est pas deja
    else:
        if (visual0ID == 0):
            button0.place(x=210, y=10) #replace le bouton si son etat precedent etait 0 (cache)
        
        visual0ID = state #met a jour l'indice d'image du bouton 0 (utilise par les evenements hover et click pour mettre a jour le visuel)
        onLeave0()
        
#EVENEMENTS ------------------------------------------------------------------------------------------------------------------------------------
LockedItems = [False, False, False, False] #ce tableau represente l'etat des boutons et de leurs label respectif. Chaque entree peut adopter les valeurs True ou False.
#L'etat d'un label est verifie lorsqu'une commande onLeave est executee. Un bouton LockedItems[numero] = True n'est plus affecte par l'utilisateur tant que le menu secondaire ouvert n'est pas ferme (mettant a jour cette variable)
#Pour les cases a cocher, cette variable represente leur etat coche ou non (etant cochees, elles ne changent pas d'apparence lors de hover), Le clic sur la case a cocher est le seul evenement qui peut changer son etat de verrouillage
#Le bouton 5 prend effet instantanement et n'a pas besoin de fonction de verouillage.

#evenements generiques
def submenuUnload(*args): #decharge les menus secondaires. (cette fonction est apelee lors des clicks sur le fond, de l'actualisation de l'affichage du texte, et de l'ouverture d'un nouveau menu secondaire)
    """
    fait disparaitre certains menus
    """
    if (LockedItems[0] == True) or (LockedItems[1] == True): #verifie que l'un des deux menus secondaires est bien ouvert pour eviter les executions inutiles
            
        LockedItems[0] = False #met a jour la variable d'etat des boutons
        LockedItems[1] = False
        onLeave1() #met a jour les boutons
        onLeave2()
        menuA_wordcount.pack() #inscrit l'objet
        menuA_wordcount.pack_forget() #le fait disparaitre
        menuB_wordlength.pack()
        menuB_wordlength.pack_forget()
    
    if (LockedItems[3] == True): #fait disparaitre l'affichage du texte lorsqu'une autre action est entreprise
        action4()
        
def scaleAUpdate(*args):
    WordsParameters[0] = cursorA1.get() + cursorA2.get() #la somme du curseur des dizaines et des unites donne le parametre [nombre de mots]
    tooltip1["text"] = str(WordsParameters[0])+" mots" #actualise le tooltip indicateur du bouton pour qu'il reflette la valeur du parametre defini
    
def scaleBUpdate(*args):
    WordsParameters[1] = cursorB1.get() #met a jour les parametres a partir des informations des cursors
    WordsParameters[2] = cursorB2.get()
    cursorB1["to"] = WordsParameters[2] #la valeur maximale du curseur "min" vaut la valeur actuelle du curseur "max" de sorte a ce qu'il ne soit pas possible de selectionner une valeur minimale superieure a la valeur maximale
    #les methodes de classe recalculent automatiquement les ecarts du curseur concerne
    if (WordsParameters[1] == WordsParameters[2]):
        tooltip2["text"] = str(WordsParameters[1])+" lettres"
    elif (WordsParameters[1] == 0):
        tooltip2["text"] = "jusqu'a "+str(WordsParameters[2])+" lettres"
    else:
        tooltip2["text"] = "de "+str(WordsParameters[1])+" a "+str(WordsParameters[2])+" lettres"
        
#evenements lies aux clics bouton ----------------------------------------------------------------
# Bouton Principal
def action0(*args):
    """
    gere les actions clic du bouton 0
    """
    submenuUnload() #ferme les menus
    global visual0ID #recupere l'identifiant visuel
    
    if (visual0ID == 1):
        if not(ID_identifier[1] is None): #meme structure que dans delayAnalyzer()
            window.after_cancel(ID_identifier[1])
        ID_identifier[1] = window.after(200, onLeave0) #la latence de l'effet "clic" est ajoutee artificiellement, car la simple generation de l'image est tres rapide contrairement au traitement du texte lui meme
        window.after(1, reGenerate) #genere une nouvelle image en utilisant le tri de mots deja effectue
        visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0T[visual0ID]) #ajuste l'apparence du bouton pour signaler le clic #@UnusedVariable
    #declenche l'action correspondante au bouton (information alternative transportee par visual0ID)
        
    elif (visual0ID < 4): #pour les valeurs 2 et 3 de visual0ID...
        window.after(2, titleAnalyzer) #actualisation du bouton (par la fonction titleAnalyzer) apres la generation (le delai d'affichage de l'ancien bouton depend donc directement du temps de latence de la commande "after", qui depend lui meme du lag occasionne par le traitement du texte)
        window.after(1, fullGeneration) #tri les mots et genere une nouvelle image
        visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0T[visual0ID])
        
def action0shift(*args):
    """
    gere les actions clic du bouton 0 lorsque la touche shift est pressee
    """
    #copie de la version action0 mais pour le cas specifique de visualID > 3, car cette action necessite la pression sur la touche shift pendant le clic
    #il est possible de lire directement le rapport d'evenement <ButtonPress event state=Mod3 num=1 x=24 y=30> qui precise les touches additionnelles pressees, mais je n'ai pas trouve comment lire les chevrons, et la methode que j'aurais employe sinon (lecture des char un par un) aurait ete trop longue et consommatrice de ressources
    global visual0ID
    if (visual0ID > 3): #pour les valeurs 4 et 5 de visual0ID...
        print("TEXT TOO BIG ! shift required")
        window.after(2, titleAnalyzer)
        window.after(1, fullGeneration)
        visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0T[visual0ID])
    
# Boutons de menu parametres
def action1(*args):
    """
    gere les actions clic du bouton 1
    """
    if (LockedItems[0]): 
        submenuUnload() #retire le menu dans le cas ou il etait deja ouvert et deverouille les effets graphiques
        onEnter1() #fait reapparaitre le label (simule l'arrivee de la souris)
        visual1 = button1.create_image(0, 0, anchor=tk.NW, image=image1H) #retablit la texture de Hover du bouton
    else: #ne fait apparaitre le menu que si il a deja ete ferme
        submenuUnload() 
        onLeave1() #fait disparaitre le label
        visual1 = button1.create_image(0, 0, anchor=tk.NW, image=image1T) #modifie la texture du bouton pour indiquer l'ouverture du menu #@UnusedVariable
        menuA_wordcount.place(x=280, y=84) #ouvre le menu du nombre de mots
        LockedItems[0] = True #verouille les effets graphiques du bouton (tant que le menu secondaire est ouvert)
    
def action2(*args): #meme structure
    """
    gere les actions clic du bouton 2
    """
    if (LockedItems[1]): 
        submenuUnload()
        onEnter2()
        visual2 = button2.create_image(0, 0, anchor=tk.NW, image=image2H)
    else:
        submenuUnload()
        onLeave2()
        visual2 = button2.create_image(0, 0, anchor=tk.NW, image=image2T) #@UnusedVariable
        menuB_wordlength.place(x=280, y=124) #ouvre le menu des longueurs de mots
        LockedItems[1] = True
    
# Case a cocher
def action3(*args):
    """
    gere les actions clic du bouton 3
    """
    submenuUnload()
    #inverse l'etat de LockedItems qui represente ici l'etat de la case a cocher en plus de l'etat de verrouillage de l'animation du bouton
    if (LockedItems[2]):
        visual3 = button3.create_image(0, 0, anchor=tk.NW, image=image3H) #met a jour le visuel (decochage) car contrairement aux autres widgets, ce changement d'etat depend directement d'une nouvelle interaction avec ce meme bouton
        tooltip3["text"] = "inutiles laisses" #met a jour le tooltip du bouton pour qu'il reflette son etat
        LockedItems[2] = False
    else:
        visual3 = button3.create_image(0, 0, anchor=tk.NW, image=image3T) #met a jour le visuel du bouton (case cochee) #@UnusedVariable
        tooltip3["text"] = "inutiles exclus"
        LockedItems[2] = True

# Menu Mots Trouves
def action4(*args):
    """
    gere les actions clic du bouton 4
    """
    if (LockedItems[3]):
        visual4 = button4.create_image(0, 0, anchor=tk.NW, image=image4) #met a jour le visuel pour la meme raison que pour le bouton 3
        display_text.pack()
        display_text.pack_forget()
        LockedItems[3] = False
    else:
        submenuUnload()
        visual4 = button4.create_image(0, 0, anchor=tk.NW, image=image4T)
        display_text["state"] = "normal" #rend le widget editable
        display_text.delete(0.0, "end") #efface son contenu
        display_text.insert("end", fwords.textOutput(fwords.public_dict)) #recupere le texte a afficher depuis le module fwords (le texte correspond a l'etat du dernier dictionnaire qui a servi a la generation d'une image (public_dict))
        display_text["state"] = "disabled" #desactive a nouveau la fenetre de texte
        display_text.place(x=402, y=50)
        LockedItems[3] = True
    
# Bouton Sauvegarde
def action5(*args):
    """
    gere les actions clic du bouton 5
    """
    submenuUnload()
    #fonction sauvegarde (des effets visuels etaient prevus et devaient etre geres par cette fonction, autrement j'aurais directement affecte save() au clic et ommis la fermeture des fenetres secondaires)
    cloudgen.save()
    
#evenements de survol ------------------------------------------------------------------------------
def onEnter1(*args):
    """
    gere le survol du bouton 1
    """
    if (LockedItems[0] == False): #ne s'execute que si le bouton n'est pas verouille
        tooltip1.place(x=280, y=150) #place le tooltip a cote du bouton
        visual1 = button1.create_image(0, 0, anchor=tk.NW, image=image1H) #modifie la texture du bouton pour indiquer le survol  #@UnusedVariable
def onLeave1(*args):
    """
    gere le survol du bouton 1
    """
    if (LockedItems[0] == False):
        visual1 = button1.create_image(0, 0, anchor=tk.NW, image=image1) #retablit la texture d'origine  #@UnusedVariable
        tooltip1.pack() #execute pack() pour que l'element soit dans le registre de tkinter
        tooltip1.pack_forget() #execute pack forget pour le faire decharger
        
def onEnter2(*args): #meme structure que la fonction precedente
    """
    gere le survol du bouton 2
    """
    if (LockedItems[1] == False):
        tooltip2.place(x=280, y=222)
        visual2 = button2.create_image(0, 0, anchor=tk.NW, image=image2H) #@UnusedVariable
def onLeave2(*args):
    """
    gere le survol du bouton 2
    """
    if (LockedItems[1] == False):
        visual2 = button2.create_image(0, 0, anchor=tk.NW, image=image2) #@UnusedVariable
        tooltip2.pack() 
        tooltip2.pack_forget()
        
def onEnter3(*args): #meme structure...
    """
    gere le survol du bouton 3
    """
    tooltip3.place(x=280, y=285) #mais l'affichage du label ne depend pas de l'etat de verouillage
    if (LockedItems[2] == False):
        visual3 = button3.create_image(0, 0, anchor=tk.NW, image=image3H) #@UnusedVariable
def onLeave3(*args):
    """
    gere le survol du bouton 3
    """
    tooltip3.pack() 
    tooltip3.pack_forget()
    if (LockedItems[2] == False):
        visual3 = button3.create_image(0, 0, anchor=tk.NW, image=image3) #@UnusedVariable
        
def onEnter4(*args):
    """
    gere le survol du bouton 4
    """
    if (LockedItems[3] == False):
        visual4 = button4.create_image(0, 0, anchor=tk.NW, image=image4H) #@UnusedVariable
def onLeave4(*args):
    """
    gere le survol du bouton 4
    """
    if (LockedItems[3] == False):
        visual4 = button4.create_image(0, 0, anchor=tk.NW, image=image4) #@UnusedVariable
        
def onEnter5(*args): #ce bouton n'a pas besoin d'etre verrouille
    """
    gere le survol du bouton 5
    """
    visual5 = button5.create_image(0, 0, anchor=tk.NW, image=image5H) #@UnusedVariable
def onLeave5(*args):
    """
    gere le survol du bouton 5
    """
    visual5 = button5.create_image(0, 0, anchor=tk.NW, image=image5) #@UnusedVariable
        
def onEnter0(*args): #meme structure sans contrainte de verrouillage (parce que le bouton disparait lorsqu'il est indisponible)
    """
    gere le survol du bouton 0
    """
    global visual0ID #la texture du bouton change aussi selon l'identifiant visuel
    visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0H[visual0ID]) #@UnusedVariable
    if (visual0ID != 1): #verifie qu'il y ait bien des contraintes a afficher dans le tooltip (le bouton n'est pas un bouton reload (visual0ID = 1))
        tooltip0["text"] = str(visual0ID) #met a jour les informations du tooltip (qui contiennent des informations sur la longueur des textes)
    else:
        tooltip0["text"] = "rafraichir" #texte specifique au bouton reload
    tooltip0.place(x=280, y=25)
    
def onLeave0(*args):
    """
    gere le survol du bouton 0
    """
    visual0 = button0.create_image(0, 0, anchor=tk.NW, image=image0[visual0ID]) #@UnusedVariable
    tooltip0.pack() 
    tooltip0.pack_forget()
    
def onEnterImg(*args): #lorsque l'image est survolee,
    """
    gere le survol de l'image
    """
    hovermenu.place(x=655, y=285) #fait apparaitre le menu hover dans le coin inferieur droit. Il permet d'afficher la liste des mots qui apparaissent sur l'image, ou de la sauvegarder 
def onLeaveImg(*args):
    """
    gere le survol de l'image
    """
    hovermenu.pack() 
    hovermenu.pack_forget() #fait disparaitre le menu hover
    
#inscription des evenements -----------------------------------------------------------------------
cursorA1["command"]=scaleAUpdate #evenement : mise a jour de la valeur du curseur (actualise le label et la valeur dans la variable parameters)
cursorA2["command"]=scaleAUpdate
cursorB1["command"]=scaleBUpdate
cursorB2["command"]=scaleBUpdate

bg.bind("<1>", submenuUnload) #retire les menus secondaires lorsque le fond est clique
display_text.bind("<1>", action4) #permet de fermer la fenetre display_text juste en clickant dessus
display.bind("<Enter>", onEnterImg) #affiche le menu hover lorsque survole
display.bind("<Leave>", onLeaveImg)
hovermenu.bind("<Enter>", onEnterImg) #l'evenement est egalement applique au menu hover lui meme pour eviter qu'il disparaisse lors du passage de display (l'image) a hovermenu, car ce sont des elements distincts (il disparait quand meme mais reapparait instantanement)
hovermenu.bind("<Leave>", onLeaveImg)
display_text.bind("<Enter>", onEnterImg) #same, pour la coherence du menu
display_text.bind("<Leave>", onLeaveImg)

button0.bind("<Enter>", onEnter0) #se declenche lors de l'arrivee de la souris (ici du widget button1)
button0.bind("<Leave>", onLeave0) #se declenche lors de la sortie de la sourie (du widget button1)
button0.bind("<1>", action0) #se declenche lors du clic sur ce meme widget
button0.bind("<Shift-1>", action0shift) #shift maintenu pendant le clic
button1.bind("<Enter>", onEnter1) #sm...
button1.bind("<Leave>", onLeave1)
button1.bind("<1>", action1)
button2.bind("<Enter>", onEnter2)
button2.bind("<Leave>", onLeave2)
button2.bind("<1>", action2)
button3.bind("<Enter>", onEnter3)
button3.bind("<Leave>", onLeave3)
button3.bind("<1>", action3)
button4.bind("<Enter>", onEnter4)
button4.bind("<Leave>", onLeave4)
button4.bind("<1>", action4)
button5.bind("<Enter>", onEnter5)
button5.bind("<Leave>", onLeave5)
button5.bind("<1>", action5)

#enregistrement des elements du menu parametres -----------------------------------------------------------------------
button1.place(x=210, y=125) #boutons
button2.place(x=210, y=210)
button3.place(x=210, y=265)
button0.place(x=210, y=10)

cursorA1.pack(side='left') #elements des menus secondaires
cursorA2.pack(side='right')
cursorB1.grid(row=1, column=0)
cursorB2.grid(row=1, column=1)
labelB3.grid(row=0, column=0, columnspan=2)
button4.pack(side='top')
button5.pack(side='bottom')

#-------------------------
#valeurs par defaut
global visual0ID #Le bouton 0 est d'abord inactif
visual0ID = 1
action3() #simule un clic sur la case "exclure inutiles" pour demarrer le programme avec ce parametre actif
cursorA1.set(10) #valeurs par defaut des pointeurs des curseurs (pour retranscrire l'etat des parametres par defaut)
cursorB1.set(4)
cursorB2.set(10)

#texte par defaut
titlebox.insert(0,"Title")
titleAnalyzer() #declenche l'analyse de ce texte

print("DONE") #print original qui existe depuis la toute premiere fonction tkinter. Elle n'a jamais ete desactivee; C'est mon petit vestige a moi
window.mainloop() #boucle principale de la fenetre; gestion des evenements