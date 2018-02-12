
# coding: utf-8

# In[28]:

from tkinter import filedialog
from tkinter import ttk
from tkinter import *  
from dna_features_viewer import GraphicFeature, GraphicRecord
import random

#Alleen nodig als je Jupyter notebook gebruikt
get_ipython().magic('matplotlib')

#Hier worden de headers en het DNA in een class opgeslagen
class ORF:
    def __init__(self, header, DNA):
        self.header = header
        self.DNA = DNA
 
#Hier vind de actie plaats
class ORFGUI(Frame):  
    def __init__(self, master):
        try:
            seq = StringVar() #De sequentie als string
            aminoAcidMap = {  #Een aminozuurdictionary
                'TTT' : 'F',
                'TTC' : 'F',
                'TTA' : 'L',
                'TTG' : 'L',
                
                'TCT' : 'S',
                'TCC' : 'S',
                'TCA' : 'S',
                'TCG' : 'S',

                'TAT' : 'Y',
                'TAC' : 'Y',
                'TAA' : '*',
                'TAG' : '*',

                'TGT' : 'C',
                'TGC' : 'C',
                'TGA' : '*',
                'TGG' : 'W',


                'CTT' : 'L',
                'CTC' : 'L',
                'CTA' : 'L',
                'CTG' : 'L',

                'CCT' : 'P',
                'CCC' : 'P',
                'CCA' : 'P',
                'CCG' : 'P',

                'CAT' : 'H',
                'CAC' : 'H',
                'CAA' : 'Q',
                'CAG' : 'Q',

                'CGT' : 'R',
                'CGC' : 'R',
                'CGA' : 'R',
                'CGG' : 'R',


                'ATT' : 'I',
                'ATC' : 'I',
                'ATA' : 'I',
                'ATG' : 'M',

                'ACT' : 'T',
                'ACC' : 'T',
                'ACA' : 'T',
                'ACG' : 'T',

                'AAT' : 'N',
                'AAC' : 'N',
                'AAA' : 'K',
                'AAG' : 'K',

                'AGT' : 'S',
                'AGC' : 'S',
                'AGA' : 'R',
                'AGG' : 'R',


                'GTT' : 'V',
                'GTC' : 'V',
                'GTA' : 'V',
                'GTG' : 'V',

                'GCT' : 'A',
                'GCC' : 'A',
                'GCA' : 'A',
                'GCG' : 'A',

                'GAT' : 'D',
                'GAC' : 'D',
                'GAA' : 'E',
                'GAG' : 'E',

                'GGT' : 'G',
                'GGC' : 'G',
                'GGA' : 'G',
                'GGG' : 'G'}

            StartCodon = 'ATG'

            StopCodons = ['TAG', 'TGA', 'TAA']

            def load_file():
                orflijst = [] #Dit is een lijst waar alle ORF objecten (eigenlijk nog gewoon DNA en headers...) in komen
                Filename = self.fileName = filedialog.askopenfilename(filetypes = (("My Files","*.fasta"),("All Files","*.*")),title = "Choose a Fasta File") #Dit maakt een Filechooser
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
            
            def findStartPositions(SEQ):
                # uppercase seq
                SEQ = SEQ.upper()
                # maak een lijst voor de resultaten
                resultstart = []
                # loop over alle indeces behalve de laatste twee want daar kunnen geen codons starten
                for i in range(len(SEQ)-2):
                    # kijk of het codon een startcodon is
                    if SEQ[i:i+3] == StartCodon:
                        # append de startcodon positie bij de lijst
                        resultstart.append(i)
                # Retourneer de lijst
                return resultstart
            
            def findNextCodon(seq, start, codon):
                # loop over een lijst met indeces
                # Er worden hier stappen van 3 genomen    
                seq = seq.upper()
                for i in range(start, len(seq), 3):
                    # kijk of de huidige startpositie diegene is die we zoeken
                    if seq[i:i+3] == codon:
                        # Retourneer de startpositie van het codon
                        return i
                return None
            
            def findNextStopCodon(seq, start):
                # uppercase de sequentie:
                seq = seq.upper()
                # Maak een lijst voor codons
                results = []
                # loop over de stopcodons
                for stopCodon in StopCodons:
                    # Vindt de startpositie van het volgende codon
                    pos = findNextCodon(seq, start, stopCodon)
                    # Check of pos niet gelijk is aan None, want dan zou de codon niet zijn gevonden
                    if pos != None:
                    # append de start positie bij de lijst 
                        results.append(pos)
                if len(results) > 0:
                    # Als de positie van een of meer stop codons wordt gevonden retourneren we de kleinste (dichtsbijzijnde)
                    return min(results)
                else:
                    # return None als er geen stop condons zijn
                    return None
            
            def findOpenReadingFrames(seqje):
                seqje = str(seqje)
                seqje = seqje.upper()
                # Een lijst voor de resultaten
                result = []
                # loop over de lijst met findStartPositions:
                for startPosition in findStartPositions(seqje):
                    # pak de stop positie voor iedere start positie:
                    stopPosition = findNextStopCodon(seqje, startPosition)
                    # check dat we de stop posities hebben:
                    if stopPosition != None:
                        # Maaek een tuple met start en stopposities:
                        result.append( (startPosition, stopPosition) )
                
                #ranges = [(n, min(n+1, 3)) for n in range(1, 3)]
                #print("This is first index: ",ranges)
                
                features = []
                displayString = ""
                count = 0
                for x in range(0,len(result)):
                    found_orf = seqje[slice(*result[count])] #Door de index te veranderen is door de ORF's te bladeren
                    print("This is ",count," index: ",found_orf)
                    displayString = displayString + str(count) + " index " + found_orf + "\n" #Een string maken met alle ORF's
                    color = "#%06x" % random.randint(0, 0xFFFFFF) #Een willekeurige kleur wordt gekozen
                    features.append(GraphicFeature(start=result[count][0], end=result[count][1], strand=+1, color=color, label= str(count) + " Index ORF", labelcolor=color)) #Het toevoegen van de entries aan het figuur
                    print("result count ",*result[count]) #Print de start en stoppositie van de ORF's
                    count += 1
                    
                self.text.insert(END, displayString) #De orf's als strings laten zien in de GUI
                record = GraphicRecord(sequence_length=len(seqje), features=features) #Het maken van een figuur met de ORF's
                record.plot(figure_width=15) #Het figuur wordt gemaakt, de grootte van het figuur valt aan te passen
                seq.set(str(result))
                print(seq.get())

            #Het maken van de master, het hoofdscherm
            self.master = master #De master is het hoofdscherm
            master.title("ORF Predictor") #De titel van het hoofdscherm
            self.button = Button(master, text="Load File and find ORF's", command = lambda:[load_file(),findOpenReadingFrames(seq.get())]) #Een button met text en twee functies
            self.button.bind("<Button-1>") #De button vertellen wat voor actie het activeerd            
            self.button.grid(row=0) #De button toevoegen aan het 'grid', rij 0
            self.label = Label(master, text ="ORF IN DNA",foreground="red",font=("Helvetica", 16)) #Het maken van een label
            self.label.grid(row=1) #De label toevoegen aan het 'grid', rij 1
            
            #progressbar = ttk.Progressbar(master, orient='horizontal', mode='determinate')
            #progressbar.grid(row=3,padx=5, pady=5) #Dit heeft een waarde tussen 0 en 100
            
            self.frame = Frame(master, width=400, height=400) #Dit wordt toch veranderd, dus 400 x 400 is onnodig
            self.frame.grid(row=2) #Het frame toevoegen aan het 'grid', rij 2
            self.text = Text(self.frame, height=6, width=30) #Het maken van een textblok in het frame
            self.text.grid(row=2, column=0, sticky="nsew", padx=5, pady=5) #Het textblok toevoegen aan het 'grid', rij 2, in het frame
            self.scrollbar = Scrollbar(self.frame, orient="vertical", command = self.text.yview) #Het maken van een scrollbar
            self.scrollbar.grid(row=2, column=1, sticky="nsew") #De scrollbar toevoegen aan het 'grid', rij 2, in het frame
            self.text['yscrollcommand'] = self.scrollbar.set #De scrollbar een commando meegeven
            
            root.mainloop() #Het uitvoeren van de mainloop
            
            
            
        
        except TclError:
            print("TclError") #Deze error komt als je .pack() en .grid() door elkaar gebruikt
        
    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, "destroyed") #Dit is het bericht dat komt als de GUI is afgesloten
          
    
if __name__ == "__main__":
    root = Tk()
    my_gui = ORFGUI(root)


