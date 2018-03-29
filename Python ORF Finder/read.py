from tkinter import filedialog, messagebox, END, TclError
import tkinter as tk
import os #Voor de icon en de image

#--------------------------------------------Het laden van het bestand------------------------------------------------

def load_file(self, seq):
    #Hier worden de headers en het DNA in een class opgeslagen
    class DNA:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA
            
    dnalijst = [] #Dit is een lijst waar alle ORF objecten (eigenlijk nog gewoon DNA en headers...) in komen
    try:
        Filename = self.fileName = filedialog.askopenfilename(filetypes = (("My Files","*.fasta"),("All Files","*.*")),title = "Choose a Fasta File") #Dit maakt een Filechooser.
        file = open(Filename, "r") #Openen van de file
    except IOError:
        messagebox.showerror("Warningmessage", "File not Found\n      or\nFile is corrupted\n      or\nFile isn't given")
    print("Your Filename is: ", Filename, "\n") #Printen van de naam van de file
    read_file(self, seq, dnalijst, file, DNA) #Aanroepen volgende functie

#-----------------------------------------Het echte lezen van het bestand----------------------------------------------
    
def read_file(self, seq, dnalijst, file, DNA):

    yconcat = "" 
    headerlist = []
    DNAlist    = [] 

    for line in file: #Hier wordt het bestand gelezen
        if line.startswith(">"): #Hier worden de headers gelezen
            x = line
            headerlist.append(x)
            DNAlist.append(yconcat)
            yconcat = ""
        if line.startswith(">") == False: #Hier worden de nucleotidesequenties gelezen
            y = line 
            yconcat += y

    DNAlist.append(yconcat)
    DNAlist.pop(0) #Er is een keer een lege string toegevoegd.
    get_data(self, seq, dnalijst, DNA, headerlist, DNAlist) #Aanroepen volgende functie

#-----------------------------------------Het vullen van de lijsten met data---------------------------------------------

def get_data(self, seq, dnalijst, DNA, headerlist, DNAlist):
    
    indexcount = 0
    for header in headerlist: #Hier wordt de lijst met DNA objecten gevuld
        dna = DNA(headerlist[indexcount],DNAlist[indexcount])
        indexcount += 1
        dnalijst.append(dna)

    #Hier kan gekozen worden welk DNA in de lijst gebruikt wordt, dit is voor Multiple Fasta Files
    index = self.Entry.get()
    if index == "": #Het instellen van een defaultindex als er geen input wordt gegeven, de eerste header wordt dan genomen
        index = 0
    try:
        seq.set(dnalijst[int(index)].DNA) #Het DNA object waarmee verder wordt gegaan in de applicatie
    except IndexError:
        messagebox.showerror("Warningmessage", "That index doesn't exist\nTip: the first one is 0")
        
#-----------------------------------------Het maken van een hulpscherm-----------------------------------------------------

def CreateHelpWindow(self, master):
    
    self.HelpWindow = tk.Toplevel(master) #Maakt een nieuwe window om de gebruiker te helpen
    self.HelpWindow.iconbitmap(os.path.abspath("Logotje.ico"))
    self.HelpWindowbutton.config(text="New Window Already Active",state="disabled") #Maakt de button inactief
    
    self.Hulptextframe = tk.Frame(self.HelpWindow) #Het maken van een Frame
    self.Hulptextframe.grid(row=0) #Het frame toevoegen aan het 'grid', rij 0
    self.Hulptext = tk.Text(self.Hulptextframe, height=6, width=70) #Het maken van een textblok in het frame
    self.Hulptext.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) #Het textblok toevoegen aan het 'grid', rij 0, in het frame
    self.Hulpscrollbar = tk.Scrollbar(self.Hulptextframe, orient="vertical", command = self.Hulptext.yview) #Het maken van een scrollbar
    self.Hulpscrollbar.grid(row=0, column=1, sticky="nsew") #De scrollbar toevoegen aan het 'grid', rij 0, in het frame
    self.Hulptext['yscrollcommand'] = self.Hulpscrollbar.set #De scrollbar een commando meegeven
    
    try: #Dit is puur omdat Justin wat tijd over had
        from PIL import Image, ImageTk
        
        im = Image.open(os.path.abspath("Logotje.gif"))
        im = im.resize((200,200), Image.ANTIALIAS)
        self.tkimage = ImageTk.PhotoImage(im)
        self.goodcanvas = tk.Canvas(self.Hulptextframe)
        self.goodcanvas.create_image(100, 0, image=self.tkimage, anchor="nw")
        self.goodcanvas.grid(row=1)
        
    except TclError:
        messagebox.showerror("Warningmessage", "TclError, can't find Image\nBut you can continue without,\nClose the Window then") #Deze error komt als het de Image niet kan vinden
    except ImportError:
        print("PIL is required to view our magnificent Logo") #Het is niet per se nodig dat ik het logo laat zien en het is dan irritant als je een pop-up krijgt dus dit is een print()
    
    self.Hulptext.insert(END, "De stappen die U moet ondernemen om te werken met onze software zijn:\n1. Kies uw manier van display van de ORF's\n2. Kies een index om een bepaalde nucleotidesequentie binnen een Fasta bestand te gebruiken (optioneel)\n3. Maak de keuze of U kiest voor het Blasten van de resultaten of niet\n4. Druk op de knop voor het laden en vinden van ORF's\n5. Kies een bestand (Het liefst een .Fasta)\n6. Aanschouw en Enjoy\n\nPS: Zijn er bugs? Herstart gewoon") #Laat deze text zien in het textveld
    
    master.wait_window(self.HelpWindow) #Checkt of de window niet gesloten is
    if not self.HelpWindow.winfo_exists(): #Als de window gesloten is kijkt het of het nog bestaat
        self.HelpWindowbutton.config(text="Help",state="normal") #Als het niet bestaat maakt het de button weer actief
        