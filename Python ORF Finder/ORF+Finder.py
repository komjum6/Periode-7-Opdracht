
# coding: utf-8

# In[1]:

# Autors: Bertram Hutten, Luuk van Damme, Teun van Duffelen en Justin Huberts
# Date of creation: around the beginning of February
# Functionality: 
# Known Bugs: 
# TO_ADD: Radiobutton voor readingframes, blastbutton (Na het inlezen, voor één of alle reading frames)

from read import *
from dataprocessing import findStartPositions, findNextCodon, findNextStopCodon, findOpenReadingFrames

#from tkinter import filedialog
from tkinter import ttk
from tkinter import *  
# from dna_features_viewer import GraphicFeature, GraphicRecord
# import random

#Alleen nodig als je Jupyter notebook gebruikt
get_ipython().magic('matplotlib')

#Hier vind de actie plaats
class ORFGUI(Frame):  
    def __init__(self, master):
        try:
            seq = StringVar() #De sequentie als string
            self = self
            
#             def findOpenReadingFrames(seqje):
#                 seqje = str(seqje)
#                 seqje = seqje.upper()
#                 # Een lijst voor de resultaten
#                 result = []
#                 # loop over de lijst met findStartPositions:
#                 for startPosition in findStartPositions(seqje):
#                     # pak de stop positie voor iedere start positie:
#                     stopPosition = findNextStopCodon(seqje, startPosition)
#                     # check dat we de stop posities hebben:
#                     if stopPosition != None:
#                         # Maak een tuple met start en stopposities:
#                         result.append( (startPosition, stopPosition) )
                
#                 #ranges = [(n, min(n+1, 3)) for n in range(1, 3)]
#                 #print("This is first index: ",ranges)
                
#                 features = []
#                 displayString = ""
#                 count = 0
#                 for x in range(0,len(result)):
#                     found_orf = seqje[slice(*result[count])] #Door de index te veranderen is door de ORF's te bladeren
#                     print("This is ",count," index: ",found_orf)
#                     displayString = displayString + str(count) + " index " + found_orf + "\n" #Een string maken met alle ORF's
#                     color = "#%06x" % random.randint(0, 0xFFFFFF) #Een willekeurige kleur wordt gekozen
#                     features.append(GraphicFeature(start=result[count][0], end=result[count][1], strand=+1, color=color, label= str(count) + " Index ORF", labelcolor=color)) #Het toevoegen van de entries aan het figuur
#                     print("result count ",*result[count]) #Print de start en stoppositie van de ORF's
#                     count += 1
                    
#                 self.text.insert(END, displayString) #De orf's als strings laten zien in de GUI
#                 record = GraphicRecord(sequence_length=len(seqje), features=features) #Het maken van een figuur met de ORF's
#                 record.plot(figure_width=15) #Het figuur wordt gemaakt, de grootte van het figuur valt aan te passen
#                 seq.set(str(result))
#                 print(seq.get())

            #Het maken van de master, het hoofdscherm
            self.master = master #De master is het hoofdscherm
            master.title("ORF Predictor") #De titel van het hoofdscherm
            self.button = Button(master, text="Load File and find ORF's", command = lambda:[load_file(self, seq),findOpenReadingFrames(self, seq, seqje=seq.get())]) #Een button met text en twee functies
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


