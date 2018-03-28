from tkinter import filedialog, messagebox

#--------------------------------------------Het laden van het bestand------------------------------------------------

def load_file(self, seq):
    #Hier worden de headers en het DNA in een class opgeslagen
    class DNA:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA
            
    dnalijst = [] #Dit is een lijst waar alle ORF objecten (eigenlijk nog gewoon DNA en headers...) in komen
    Filename = self.fileName = filedialog.askopenfilename(filetypes = (("My Files","*.fasta"),("All Files","*.*")),title = "Choose a Fasta File") #Dit maakt een Filechooser.
    file = open(Filename, "r") #Openen van de file
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