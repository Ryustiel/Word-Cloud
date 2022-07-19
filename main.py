'''
Created on 30 mars 2020

@author: Moi
'''
#imports...
import tkinter as tk
global text_cache #(string) sauvegarde le dernier texte charge dans le module 
text_cache = "" #cela evite que la fonction recherche a nouveau les mots alors que c'est deja enregistre dans la variable public_dict


'''
MODULE fwords
'''
#skipped_words tab 
#new english words at the beginning of the tab
#new french words at the end.

#skipped_chars et skipped_words sont des tableaux (ou listes) qui contiennent des caracteres et de mots susceptible d'apparaitre dans le texte qui seront testes dans les fonctions grouped et getRelevant.
skipped_chars = ["/", '\"', "\'", ".", ",", ")", "(", "]", "[", "{", "}", "!", "?", ";", ":", "_", "-"]
skipped_words = ["will", "can", "would", "and", "with", "from", "this", "about", "dans", "etait", "etaient", "plus", "pour", "mais", "qu'il", "sans", "jamais", "comme", "c'etait", "n'etait", "meme", "avait", "avaient", "etre", "vous", "nous"]

#global text variables
global public_string #public_string est une string qui contient les caracteres du dernier texte charge. Elle est rendue publique pour permettre de lire le texte plusieurs fois sans devoir le recharger.
global sorted_dict #sorted_dict est un dictionnaire pour permettre la repetition de getRelevant() sans devoir trier le texte a nouveau (bouton actualiser)
global public_dict #permet de redessiner l'image (au tout debut quand j'ai fait ce module, je pensais devoir redessiner l'image, c'est pour ca que j'ai tout rendu publique, mais deja les dictionnaires sont publiques par defaut comme les tableaux, et en plus j'en ai pas eu besoin. Mais je laisse comme ca parce que je trouve ca plus logique de declarer ce qui est global, et l'instruction global fait pas planter le programme)
public_string = "None" #definit le type des variables
sorted_dict = {}
public_dict = {}

def loaded(text):
    """
    charge le fichier correspondant au nom passe en parametre (text) et interprete les caracteres utf-8
    Gere les erreurs dus aux noms de fichiers incorrects en retournant None.
    Le resultat est conserve dans la variable globale public_string du module
    \n
    """
    try: #verifie si la variable text correspond bien au nom d'un fichier en essayant une premiere fois de l'ouvrir
        open("texts/"+str(text)+".txt", "r")
    except (FileNotFoundError): #en cas d'echec, affiche un message d'erreur et interromp la fonction
        print("Nom de Fichier Invalide")
        return None
    
    global public_string
    public_string = "" #reinitialise la string pour qu'elle ne contienne que le dernier texte genere
    public_string = open("texts/"+str(text)+".txt", "rb").read().decode("utf-8") #convertis le texte en utf-8 via l'attribut decode, qui necessite un bytecode sur lequel operer (d'ou l'option de lecture "rb")
    
    return public_string
    

def grouped(string): 
    """
    Transforme la string entree en parametre (argument string) en un dictionnaire comprenant les informations d’occurrence et de longueur pour chaque mot du texte.
    Il est oraganise sous cette forme; "{word:(count, length)}"
    Note : Des caracteres de ponctuation sont retires, et toutes les lettres sont reduites en minuscules afin d'obtenir un resultat pertinant.
    """
    #replace specific characters by spacings (in string generated form text file)
    for exception in skipped_chars:
        string = string.replace(exception, " ")
        #split and lowercase every entry
        tab = string.split() #isole chaque ensemble de caracteres separe par des espaces
        for i in range(len(tab)):
            tab[i] = tab[i].lower() #convertit les majuscules en minuscules

    word_data = {}
    
    while (len(tab) > 0):
        reference = tab[0] #reference (string) correspond a un mot arbitraire du tableau des mots du texte qui servira de reference pour compter les mots de ce texte
        count = 0 #count est un integer qui est incremente a chaque fois qu'un mot reference est trouve
        del_tab = [] #ce tableau contient les numeros de rangee de chaque mot trouve (qui correspond a reference). Cela permettra de les retirer du tableau par la suite et de limiter les verifications inutiles.
        
        for word in range(len(tab)):
            if (tab[word] == reference): #lorsque le mot selectionne correspond a la reference,
                count = count + 1 #compte ce mot (pour finalement obtenir son nombre d'occurrence dans le tableau)
                del_tab.append(word) #enregistre son identifiant de rangee afin de le supprimer par la suite (supprimer le mot directement a cette etape perturbe l'execution de la boucle for car les identifiants de rangee du tableau sont mis a jour instantanement)
                
        decaleur = 0 #integer qui reflette le nombre de decalages de tous les identifiants de rangee du tableau, car a chaque suppression, le tableau est mis a jour de sorte que tous les identifiants de rangee des mots apres celui qui a ete supprime est decale de -1
        for i in del_tab:
            del tab[i-decaleur] #supprime les mots deja trouves pour eviter des operations de comparaison inutiles dans le tableau
            decaleur = decaleur + 1
            
        word_data.update({reference:(count, len(reference))}) #met a jour les informations du dictionnaire avec reference qui correspond au mot sur lequel se sont basees les instructions precedentes, le nombre d'occurrences enregistre dans la variable count, et la longueur de ce mot pour faciliter le travail des fonctions suivantes.
            
    return (word_data)


def sorting(direct=True, word_data=None):
    """
    Retourne un dictionnaire de format "{word:(count, length)}" trie a partir de celui donne par l'argument "word_data"
    sorted_dict etant un dictionnaire, il aussi est accessible directement
    Si le parametre direct est defini sur True, le dictionnaire word_data est automatiquement genere a partir de public_string en recourant a la fonction grouped().
    """
    global sorted_dict
    #if direct=True execute the loaded and grouped functions.
    if (direct==True):
        global public_string
        word_data = grouped(public_string)

    values_tab = [0] #Tableau de valeurs vierge. Il servira a organiser les valeurs des entrees dictionnaire.

    #gathers every unique "count" value in word_data dict. (for these to be sorted)
    for key, (count, length) in word_data.items(): #j'aurais pu uniquement rechercher parmis les values, mais j'ai trop peur de modifier mon programme maintenant. (est-ce sous optimal...?)
        no_skip=True #No skip est un booleen qui sert a sauter l'instruction append d'une valeur a values_tab lorsqu'elle y existe deja. Une seule valeur par tableau devrait accelerer l'execution de sort().
        for value in values_tab: #verifie si la valeur de count de ce mot est deja dans values_tab
            if (count == value):
                no_skip=False #definit no_skip sur False, evitant l'ajout de la valeur dans values_tab
    
        #no_skip (False if value already found); adds entry to tab when True.
        if(no_skip):
            values_tab.append(count)

    #trie le tableau
    values_tab.sort() 

    #rebuilding the dict, using sorted values from values_tab.
    sorted_dict = {} #sorted_dict est un dictionnaire qui reprendra les entrees du dictionnaire entre, mais triees par occurrence. (valeur "count")
         
    while (len(word_data) > 0): #le fonctionnement est similaire a la fonction grouped()
        reference = values_tab[-1] #les valeurs de reference sont prises a l'envers, car l'instruction sort() trie les valeurs par ordre croissant, alors qu'il me faut un ordre decroissant de mots dans le dictionnaire.
        del_tab = [] #meme fonctionnement que del_tab de la fonction grouped.
        
        for key, (count, length) in word_data.items(): #cherche dans le dictionnaire d'origine les mots qui correspondent a la valeur reference, qui correspond d'abord a l'occurrence la plus elevee de tous les mots, puis la deuxieme plus elevee, plus la troisieme, etc...
            if (count == reference):
                sorted_dict.update({key:(count, length)}) #integre le mot et ses informations d'occurrence et de longueur dans le tableau lorsque son occurrence correspond a la reference.
                del_tab.append(key) #le del tab repertorie tous les mots qui ont ete ajoutes au dictionnaire lors de cette instance for
             
        for key in del_tab:
            word_data.pop(key) #effet similaire a del word_data[key] mais comme c'est un attribut du dictionnaire et qu'un autre attribut (update) est deja utilise, je trouvais ca plus symmetrique. Et aussi le mot pop est joli.
        del values_tab[-1] #comme il n'y a qu'une seule valeur du tableau qui est utilisee pour reference, cette valeur est ici supprimee.
                
    return sorted_dict


#pick most common words.
#max_output => how much entries will be given at most
#exclude => when set to False, allow words of 3 letters or less and even those in the exclusion tab to be counted and output.
def getRelevant(sorted_dict, max_output=5, exclude=True, forlength=None, upto=0, public=True):
    """
    Recherche les mots pertinants dans le dictionnaire sorted_dict en se basant sur les parametres de nombre de mots "max_output", d'exclusion "exclude", et de longueur "forlength" et "upto".
    Le dictionnaire renvoye est organise "{word:(count, length)}"
    Si public=True, le dictionnaire public_dict est mis a jour avec les informations de return de cette fonction.
    """
    global public_dict #ce dictionnaire est destine a etre publique; Je sais qu'il n'est pas utile de le declarer (les emplacements de sauvegarde a IDs sont globaux de base) mais finalement je trouve ca plus lisible.
    relevant_dict = {} #relevant_dict est le dictionnaire de sortie
    word_count=0 #cet integer reflette le nombre de mots deja ajoutes au dictionnaire de sortie. Il marche de concert avec max_output pour arreter la fonction lorsque la limite de mots a trouver est atteinte.

    if (upto==0):
        upto = forlength #lorsqu'aucune limite superieure n'est specifiee, cherche les mots dont la longueur correspond exactement a forlength (cette syntaxe etait destinee a l'execution directe de la fonction, avant qu'il nous soit demande de concevoir une interface)

    for key, (count, length) in sorted_dict.items():
        no_skip=True #booleen qui determine si le mot est ajoute ou non a la fin de la chaine de tests de correspondance du mot aux criteres (tout ce qui se trouve dans cette boucle for)
        #skip if length under 4 or length does not correspond to forlength value
        if ((forlength is None) and exclude and (length < 3)) or not(forlength is None) and ((length < forlength) or (length > upto)):
            no_skip = False 
        #skip if key string in skipped_words
        elif exclude: #interromp l'execution lorsque le mot correspond a l'une des entrees du tableau skipped_words, si les exceptions sont bannies (exception = True)
            for exception in range(len(skipped_words)):
                if (key == skipped_words[exception]):
                    no_skip = False
                    break
        #stops the function when max output count reached
        if (word_count >= max_output): #arrete la fonction si le nombre maximal d'occurrences est rencontre. (j'aurais peut etre du le placer au tout debut de la chaine, mais la encore, j'ai peur de toucher a mon programme)
            break
        else:
            if (no_skip):
                #appends key-count to relevant_dict (length is now useless)
                relevant_dict.update({key:(count, length)}) #met a jour le compte de mots corrects trouves, et ajoute les informations du mot au relevant_dict final.
                word_count = word_count + 1
    #updates fwords
    if (public):
        public_dict = relevant_dict #si public=True, indiquant que l'execution de cette fonction est destinee a remplacer le dictionnaire publique, public_dict est mis a jour avec les informations du relevant_dict final.
        
    return relevant_dict


def textOutput(iterable_dict):
    """
    Renvoie une string generee a partir des informations d'iterable_dict, qui doit adopter le format "{word:(count, length)}".
    Cette string est destinee a etre affichee dans le widget liste, ou dans la console.
    """
    string = "" #cette string contient des informations sur derniers mots resultant du dictionnaire entre (respectant le format indique)
    rank = 0 #integer incremente a chaque mot retranscrit, si bien qu'il peut etre utilise pour representer le classement du mot (plus le mot apparait souvent, plus son classement est proche de 1)
    for word, (count, length) in iterable_dict.items(): #@UnusedVariable
        rank = rank + 1 #incremente rank pour que l'indice corresponde au rang du mot
        string = string + (str(rank)+": le mot "+ word +" apparait "+ str(count) +" fois.\n") #ajoute a la string une ligne pour le mot word contenant ses informations

    return string #cette fonction servait a l'origine a tester ma fonction de tri lorsqu'il ne fallait pas encore faire d'interface. 
    #Je l'ai garde par nostalgie et c'est pour lui donner une utilite que j'ai cree le widget liste.





'''
MODULE CLOUDGEN
'''
from PIL import Image, ImageDraw, ImageFont
import random
from math import sqrt, ceil
import datetime

#taille de l'image
def setDrawArea(value):
    """
    set draw_area to value.
    """
    global draw_area
    draw_area = value
    return None

#item generation
    #public_instructions DICT : {word:(x1, y1, x2, y2)}
global public_instructions
public_instructions = {} #met a 0 public instructions au debut de la fonction en cas d'execution inattendue de render()

def checkPos(checking, reference):
    """
    Compare les aires definies par checking et reference, qui sont des tuples contenant des coordonnees (x1, y1, x2, y2)
    Renvoie False si deux aires se touchent, sinon False.
    """
    #checking coords
    if (checking[0] >= reference[0]) and (checking[0] <= reference[2]): #test x1 compris entre x1' et x2'
        if (checking[1] >= reference[1]) and (checking[1] <= reference[3]): #test y1 compris entre y1' et y2'
            return False
        elif (checking[3] >= reference[1]) and (checking[3] <= reference[3]): #test y2 compris entre y1' et y2' (les test y sont repetes dans les instructions suivantes)
            return False
    elif (checking[2] >= reference[0]) and (checking[2] <= reference[2]): #test x1 compris entre x1' et x2'
        if (checking[1] >= reference[1]) and (checking[1] <= reference[3]):
            return False
        elif (checking[3] >= reference[1]) and (checking[3] <= reference[3]):
            return False
    elif (checking[0] <= reference[0]) and (checking[2] >= reference[2]): #test x1 inferieur a x1' et x2 superieur a x2' (le mot est plus large que les precedents : cela peut se produire pour la largeur (coordonnees x) mais pas pour la hauteur, car les mots sont places par ordre decroissant de taille (la hauteur de base (avant taille relative) est la meme pour tous les mots, la largeur en revanche depend aussi du nombre de lettres)
        if (checking[1] >= reference[1]) and (checking[1] <= reference[3]):
            return False
        elif (checking[3] >= reference[1]) and (checking[3] <= reference[3]):
            return False
    return True


def getPos(length, height):
    """
    Genere des tuples "(x1, y1, x2, y2)" definissant des zones de dimensions "length" et "height" basees sur des coordonnees aleatoires
    Elles doivent representer la surface occupee par un mot.
    Lorsque la surface ne rencontre aucun mot deja place, renvoie le tuple la definissant.
    """
    global public_instructions
    cap = 0 - length*100 #augmente le nombre de repetitions de la boucle lorsque les mots sont plus longs car ils sont difficiles a palcer
    ok = False #cette variable bool correspond a l'etat de la recherche de coordonnees. Elle sert a declencher le return du tuple lorsqu'un emplacement correct a ete trouve.
    while (cap < 2859): #le cap limite une repetition infinie du placement de mots
        cap = cap + 1  #incrementation du cap
        #genere une position aleatoire
        # les limites superieures correspondent a la largeur et hauteur de l'image moins la taille du mot, car les coordonnees generees sont celles du coin superieur gauche.
        randx = random.randrange(1, draw_area[0]-length-1)
        randy = random.randrange(1, draw_area[1]-height-1)
        randx2 = randx + length #genere les coordonnees du deuxieme point, afin d'obtenir la surface occupee par le mot
        randy2 = randy + height
        #recherche la position...
        if (public_instructions == {}): #skip checking if there is no word to check at
            ok = True
        else:
            for x1, y1, x2, y2 in public_instructions.values(): #compare la position aleatoire a celle de tous les mots deja places, dont la surface est conservee dans public_instructions.
                if (checkPos((randx, randy, randx2, randy2), (x1, y1, x2, y2)) == True):
                    ok = True
                else:
                    ok = False #des qu'une position incorrecte est trouvee, arrete la boucle et recherche un nouvel emplacement aleatoire.
                    break
        if (ok == True):
            return (randx, randy, randx2, randy2) #retourne les coordonnees quand elles sont correctes : le booleen ok a l'etat True en sortant de la boucle for.
        
    #si aucun mot n'est trouve, notifie d'une erreur.
    print("THERES A FREAKING ERROR : word (size "+str(length)+"; "+str(height)+") couldn't be mapped")
    return False
  
  
def getDrawingInstructions(words=None):
    """
    A partir des informations de public_dict (in fwords), genere et retourne un dictionnaire drawing_istructions utilisable par render() pour generer une image.
    Custom word data can be input through the "words" parameter => (format : {"word":(size, length)})
    """
    global draw_area
    global public_instructions
    public_instructions = {} #reset instructions (to rewrite)
    
    if (words==None):
        word_counts = list(public_dict.values()) #tableau de tuples : [(occurences, longueurs)]
        close_max_factor = 0.0 #float qui correspond a la ressemblance entre l'ensemble et le maximum des valeurs
        row_factor = 0.0 #float qui augmente la taille des caracteres en fonction des mots disponibles (car ils peuvent s'organiser sur plusieurs rangees (qui dependent elles memes de leur taille))
        max_word = 0
        
        if (len(word_counts) == 0): #genere une image vierge si aucun mot n'est contenu dans la variable
            return public_instructions
        else:
            ecart = word_counts[0][0] - word_counts[-1][0]
        
        if (ecart == 0): #previens une eventuelle division par zero (lorsque tous les chiffres ont la meme valeur)
            for data in word_counts: #explique juste en dessous
                close_max_factor = close_max_factor + data[1] #0/0 doit valoir 1 avec le calcul de rapport que j'ai fait, j'ai donc ajoute cette exception
                row_factor = row_factor + 1
            maxpx = ceil(220 / close_max_factor)
            
        else:
        
            #proportion de lettres a la taille maximale (somme des ecarts au max)
            for data in word_counts:
                close_max_factor = close_max_factor + ((data[0] - word_counts[-1][0]) / ecart)*data[1] #word_counts[-1][0] : occurence minimale d'un mot
                #le taux de ressemblance a la valeur maximale vaut (valeur - valeur minimale)/ecart entre valeur max et valeur minimale
                #en multipliant chaque valeur par le nombre de lettres associees, la somme obtenue est la ressemblance a la valeur maximale.
                #lorsque toutes les lettres ont la valeur maximale, la somme vaut (valeur maximale * nbr de lettres)
                #diviser la ressemblance a la valeur maximale par le nombre total de lettres donne la proportion (entre 0 et 1) de ressemblance de chaque lettre a la valeur maximale.
                row_factor = row_factor + 1 #sqrt( (data[0] - word_counts[-1][0]) / ecart ) #l'augmentation de cette valeur depend des mots et non des lettres
                max_word = max_word + 1
                #print(close_max_factor, row_factor, max_word)
                
            #row_factor = row_factor * 10 / max_word
            maxpx = ceil(220 * sqrt(row_factor) / close_max_factor) #220 est la taille maximale d'une lettre seule
                
        print(close_max_factor, row_factor, max_word)
        print("ROW FACTOR =>", row_factor)
        
        minpx = ceil(maxpx / 4) #le mot le plus petit a pour taille 1/6 du mot le plus grand
        
        maxct = word_counts[0][0] #intervalle des valeurs de l'occurence des mots
        minct = word_counts[-1][0]
        
        print([maxpx, minpx, maxct, minct])
    
        #permet de passer de l'intervalle [minct; maxct] a l'intervalle [minpx; maxpx] (pour que la taille des mots correspondent a la taille de l'image tout en conservant les rapports d'occurence)
        if ((maxct - minct) == 0):
            conversion_factor = (maxpx-minpx) #evite une division par 0 lorsque tous les mots font la meme taille 
        else:
            conversion_factor = (maxpx-minpx) / (maxct - minct)
    
        #for each word, calculates size, request Position, and update Drawing Instructions
        for word, (count, word_length) in public_dict.items():
            #maxct - count donne la difference entre le maximum de l'intervalle des occurences (maxct) et l'occurence du mot selectionne
            #multiplie par conversion_factor pour passer a l'intervalle suivant, on obtient donc la distance relative au maximum de l'intervalle des tailles de lettres (maxpx)
            #soustraire cette distance au max au max lui meme permet de recuperer la valeur actuelle du mot.
            height = round( maxpx - (conversion_factor * (maxct - count)) ) #la hauteur est fixe car toutes les lettres sont alignees
            length = round( word_length * height /1.5 ) #height correspond a la hauteur et la longueur d'une seule lettre, c'est pourquoi elle est multipliee au nombre de lettres pour obtenir la longueur totale de l'element multilettres

            coords = getPos(length, height)
            if not(coords == False):
                public_instructions.update({word:coords})

    return public_instructions


#PIL Generation ------------------------------
def render(instructions=None):
    """
    genere une image en utilisant le dictionnaire entre, qui possede le format drawing_instructions "{word:(x1, y1, x2, y2)}".
    """
    if (instructions==None): #if no instructions specified, get them from there (public_instructions).
        global public_instructions
        instructions = public_instructions

    output = Image.new("RGB", (draw_area[0], draw_area[1]), "white") #output correspond a la nouvelle image generee (donnees du fichier qui sera ecrit a la fin de la fonction)
    for word, coords in instructions.items():
        #definit la police pour l'ecriture des mots
        font = ImageFont.truetype('Fonts/DejaVuSans.ttf', (coords[3]-coords[1]))
        
        #drawing
        editing = ImageDraw.Draw(output) #utilise une variable alternative pour clarifier les executions suivantes.
        editing.ellipse([coords[0], coords[1], coords[2], coords[3]], fill=( random.randrange(150, 250), random.randrange(50, 250), random.randrange(50, 250) )) #trace les bulles qui entourent les mots.
        editing.text((coords[0], coords[1]), word, (0,0,0), font=font) #inscrit les mots sur les bulles

    output.save("render.gif") #met a jour le fichier render.gif (avec l'image qui vient d'etre generee)
    return None #cette fonction n'a pas de sortie. (j'aurais pu ne rien mettre, ca aurait donne le meme resultat, mais ca lui donne un caractere authentique)
    
def save(*args):
    """
    duplique l'image render.gif resultant de la derniere execution de render(),
    et la nomme d'apres l'heure et la date actuelle.
    """
    saving = Image.open("render.gif", "r") #ouvre l'image render a sauvegarder
    name = str(datetime.datetime.now()) #enregistre la date et heure actuelle dans la variable string "name" 
    name = name.replace(":", " ") #retire tous les caracteres ":" qui ne peuvent pas etre presents dans les noms de fichiers windows
    saving.save( "saved/"+ name + '.gif' ) #genere le fichier
    print("saved") #et un message console
    
#definis la taille de l'image des le depart (modifiable plus tard en parametre si j'ai le temps de le faire)
#setDrawArea((300, 300))





'''
MODULE TKinter
'''
WordsParameters = [10, 4, 10] #WordsParameters est un tableau qui contient tous les parametres disponibles dans le menu median (orange) sauf les cases a cocher dont l'etat est directement represente par la variable de verouillage LockedItems.
#il comprend dans cet ordre [le nombre de mots a afficher](int), [la longueur minimale des mots](int) et [la longueur maximale des mots](int)
#les valeurs longueur minimale et longueur maximale sont issues du meme menu (menuB).

#attributs de la fenetre TKinter
window = tk.Tk()
#window.iconbitmap("icons/icon.ico")
window.title("Thing")
window.geometry("700x350")
window.resizable(0, 0) #NoResizing

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
    Charge le texte specifie dans la zone de saisie a l'aide de la fonction loaded(),
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
            if (loaded(titlebox.get()) == None): #charge le fichier en utilisant le nom indique dans titlebox. Si la fonction retourne un NoneType, le message de l'indicateur est mis a jour et la fonction s'arrete, sinon, l'execution continue, la fonction loaded() met automatiquement a jour la public_string qui sera lue dans les executions suivantes.
                setTitleIndicator(1)
                
            elif (text_cache == public_string): #si le texte est deja charge, saute la verification de la longueur et propose directement le bouton reload (actualisation)
                textbox.insert("end", public_string)
                textbox.config(state="disabled")
                setTitleIndicator(3)
                setButton0(1)
                
            else: #les actions suivantes dependent du nombre de caracteres du fichier texte
                
                textbox.insert("end", public_string) #affiche du texte dans l'espace de texte textbox
                textbox.config(state="disabled") #desactive a nouveau la boite de texte
                char_count = len(public_string) #(int) nombre de caracteres du fichier charge
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
titlebox.bindtags(tagList=('Entry', '.!entry', '.', 'all')) #donne la priorite a la class du widget qui gere le traitement de texte (la priorite est donnee aux events specifiques aux widgets par defaut)

#Image frame-------------------------------------------------------

setDrawArea((300, 300)) #render size according to the widget
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
        getRelevant(sorted_dict, WordsParameters[0], forlength=WordsParameters[1], upto=WordsParameters[2], exclude=LockedItems[2])
        render(getDrawingInstructions()) #genere l'image a partir de sets d'instructions eux memes obtenus du resultat de la fonction fullLoad
    updateDisplay() #met a jour le canvas image display
    
def fullGeneration():
    """
    execute fowrds.grouped() et sorting() puis reGenerate()
    Enregistre le nouveau texte charge dans text_cache afin que titleAnalyzer ne le recharge pas pour rien. (detection de changement)
    """
    global text_cache
    print("Parameters :", WordsParameters)
    if (WordsParameters[0] > 0) and (WordsParameters[2] > 0): #desactive la generation lorsque le nombre de mots affiche est defini sur 0
        sorting(direct=True) #cree un dictionaire classant les mots par occurence avec les parametres selectionnes
        text_cache = public_string #enregistre le texte pour permettre a titleAnalyzer() de reconnaitre qu'il a deja ete charge et d'eviter par consequent des executions inutiles (lors du rechargement de l'image notamment, car seule le module cloudgen est necessaire)
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
        display_text.insert("end", textOutput(public_dict)) #recupere le texte a afficher depuis le module fwords (le texte correspond a l'etat du dernier dictionnaire qui a servi a la generation d'une image (public_dict))
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
    save()
    
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