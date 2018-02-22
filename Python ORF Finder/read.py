from tkinter import filedialog

def load_file(self, seq):
    #Hier worden de headers en het DNA in een class opgeslagen
    class ORF:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA
    orflijst = [] #Dit is een lijst waar alle ORF objecten (eigenlijk nog gewoon DNA en headers...) in komen
    Filename = self.fileName = filedialog.askopenfilename(filetypes = (("My Files","*.fasta"),("All Files","*.*")),title = "Choose a Fasta File") #Dit maakt een Filechooser. Moet later ook .fna en .faa kunnen lezen (optioneel).
    file = open(Filename, "r") #Openen van de file
    print("Your Filename is: ", Filename, "\n") #Printen van de naam van de file

    yconcat = "" 
    headerlist = []
    DNAlist    = []

    for line in file:
        if line.startswith(">"):
            x = line
            headerlist.append(x)
            DNAlist.append(yconcat)
            yconcat = ""
        if line.startswith(">") == False:
            y = line
            yconcat += y

    DNAlist.append(yconcat)
    DNAlist.pop(0) #Er is een keer een lege string toegevoegd.

    indexcount = 0
    for header in headerlist:
        orf = ORF(headerlist[indexcount],DNAlist[indexcount])
        indexcount += 1
        orflijst.append(orf)

    for orf in orflijst:
        print(orf.header)
        print(orf.DNA)

    #Hier kan gekozen worden welk DNA in de lijst gebruikt wordt
    seq.set(orflijst[0].DNA)