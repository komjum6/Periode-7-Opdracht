
# coding: utf-8

# In[ ]:

# Autors: Bertram Hutten, Luuk van Damme, Teun van Duffelen en Justin Huberts
# Date of creation: around the beginning of February (the second, the third or anything like it)
# Functionality: It's possible to find ORF's in a given Fasta file with this application. It visualises them and it sends them to a database.
# It's also possible to retrieve the information form that database using this application. 
# Known Bugs: It's currently not possible to load multiple fasta files after each other, you have to restart the application. 
# Also, some Fasta files containing N's don't work, for example SD.fa. (example we used)
# TO_ADD: blastbutton (Na het inlezen, voor één of alle reading frames)

from read import load_file
from dataprocessing import findStartPositions, findNextCodon, findNextStopCodon, findOpenReadingFrames

from tkinter import *  
import tkinter as tk

#Alleen als Jupyter je IDE is
get_ipython().magic('matplotlib')

#Hier vind de actie plaats
class ORFGUI(Frame):  
    def __init__(self, master):
        try:
            self.seq = StringVar() #De sequentie als string
            self.radioInt = IntVar() #Een integer voor de radiobutton die dient voor het kiezen van grafiekweergave
            self.radioInt.set(0) #Default waarde, als geen radiobutton wordt gekozen
            self.headerInt = IntVar() #Een integer voor het kiezen van de Header in de Fasta
            self.headerInt.set(0) #Default waarde, als geen entry wordt ingevoerd
            #self = self #Laat de code zichzelf in de ogen kijken door 'm een spiegel voor te leggen...
            
            #Het maken van de master, het hoofdscherm
            self.master = master #De master is het hoofdscherm
            master.title("ORF Predictor") #De titel van het hoofdscherm
            self.button = Button(master, text="Load File and find ORF's", command = lambda:[load_file(self, self.seq),findOpenReadingFrames(self, seqje=self.seq.get())]) #Een button met text en twee functies
            self.button.bind("<Button-1>") #De button vertellen wat voor actie het activeerd            
            self.button.grid(row=0) #De button toevoegen aan het 'grid', rij 0
            
            self.radiobuttonsingle = Radiobutton(master, text="All Reading Frames\nin one Figure", value=1, variable=self.radioInt, command=self.radioInt.set(0))
            self.radiobuttonsingle.config(indicatoron=0, bd=4, width=15, value=0)
            self.radiobuttonsingle.grid(row=1, column=0, padx=10, pady=5, sticky=W)
            self.radiobuttonmultiple = Radiobutton(master, text="All Reading Frames\nin seperate Figures", value=2, variable=self.radioInt, command=self.radioInt.set(1))
            self.radiobuttonmultiple.config(indicatoron=0, bd=4, width=15, value=1)
            self.radiobuttonmultiple.grid(row=1, column=0, padx=10, pady=5, sticky=E)
            
            self.radiobuttonmultipleBig = Radiobutton(master, text="All Reading Frames\nin seperate Big Figures", value=3, variable=self.radioInt, command=self.radioInt.set(2))
            self.radiobuttonmultipleBig.config(indicatoron=0, bd=4, width=20, value=2)
            self.radiobuttonmultipleBig.grid(row=2, column=0, padx=10, pady=5)
            
            self.Entry = Entry(master, bd=5)
            self.Entry.grid(row=3, sticky=E)
            self.LabelEntry = Label(master, text="Input Index Fasta",foreground="blue",font=("Helvetica", 12))
            self.LabelEntry.grid(row=3, sticky=W)
            
            self.label = Label(master, text ="ORF IN DNA",foreground="red",font=("Helvetica", 16)) #Het maken van een label
            self.label.grid(row=4) #De label toevoegen aan het 'grid', rij 1
            
            #progressbar = ttk.Progressbar(master, orient='horizontal', mode='determinate')
            #progressbar.grid(row=3,padx=5, pady=5) #Dit heeft een waarde tussen 0 en 100
            
            self.textframe = Frame(master, width=400, height=400) #Dit wordt toch veranderd, dus 400 x 400 is onnodig
            self.textframe.grid(row=5) #Het frame toevoegen aan het 'grid', rij 2
            self.text = Text(self.textframe, height=6, width=30) #Het maken van een textblok in het frame
            self.text.grid(row=5, column=0, sticky="nsew", padx=5, pady=5) #Het textblok toevoegen aan het 'grid', rij 2, in het frame
            self.scrollbar = Scrollbar(self.textframe, orient="vertical", command = self.text.yview) #Het maken van een scrollbar
            self.scrollbar.grid(row=5, column=1, sticky="nsew") #De scrollbar toevoegen aan het 'grid', rij 2, in het frame
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



# In[ ]:

from itertools import permutations

x = 'CGATNNN'


perms = []

for i in range(1, len(x)+1):
    for c in permutations(x, i):
        if len(c) == 3:
            if "N" in c:
                perms.append("".join(c))
                    
perms = list(set(perms))
            
for p in perms:
    print("'" + p + "'" + " : " + "'X'" + ",") 

