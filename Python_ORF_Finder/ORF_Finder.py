
# coding: utf-8

# In[ ]:

# Autors: Bertram Hutten, Luuk van Damme, Teun van Duffelen en Justin Huberts
# Date of creation: around the beginning of February (the second, the third or anything like it)
# Functionality: It's possible to find ORF's in a given Fasta file with this application. It visualises them and it sends them to a database.
# It's also possible to retrieve the information form that database using this application. 
# The user can choose between a single Fasta file or a Multiple Fasta file using the input index which defaults to index 0, the first entry.
# Known Bugs: It's currently not possible to load multiple fasta files after each other, you have to restart the application. 
# Also, some Fasta files containing N's don't work, for example SD.fa. (example we used)
# TO_ADD: 

from read import load_file, CreateHelpWindow
from dataprocessing import findStartPositions, findNextCodon, findNextStopCodon, findOpenReadingFrames

from tkinter import *  
import tkinter as tk #Dit is python versie 3.6 dus Tkinter is niet de import

import os #Voor de icon

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
            self.CheckBlastInt = IntVar() #Een integer om het Blasten aan of uit te zetten
            #self = self #Laat de code zichzelf in de ogen kijken door 'm een spiegel voor te leggen...
            
            #Het maken van de master, het hoofdscherm
            self.master = master #De master is het hoofdscherm
            master.title("ORF Predictor") #De titel van het hoofdscherm
            master.iconbitmap(os.path.abspath("Logotje.ico"))
            self.button = Button(master, text="Load File and find ORF's",bg="green", command = lambda:[load_file(self, self.seq),findOpenReadingFrames(self, seqje=self.seq.get())]) #Een button met text en twee functies
            self.button.bind("<Button-1>") #De button vertellen wat voor actie het activeerd            
            self.button.grid(row=0) #De button toevoegen aan het 'grid', rij 0
            
            self.radiobuttonsingle = Radiobutton(master, text="All Reading Frames\nin one Figure", value=1, variable=self.radioInt, command=self.radioInt.set(0)) #Een button om deze manier van grafiekdisplay te kiezen
            self.radiobuttonsingle.config(indicatoron=0, bd=4, width=15, value=0) #Dit maakt de button een vierhoek ipv een cirkel
            self.radiobuttonsingle.grid(row=1, column=0, padx=10, pady=5, sticky=W) #De button toevoegen aan het 'grid', rij 1. De sticky zorgt ervoor dat het links wordt toegevoegd.
            self.radiobuttonmultiple = Radiobutton(master, text="All Reading Frames\nin seperate Figures", value=2, variable=self.radioInt, command=self.radioInt.set(1)) #Een button om deze manier van grafiekdisplay te kiezen
            self.radiobuttonmultiple.config(indicatoron=0, bd=4, width=15, value=1) #Dit maakt de button een vierhoek ipv een cirkel
            self.radiobuttonmultiple.grid(row=1, column=0, padx=10, pady=5, sticky=E) #De button toevoegen aan het 'grid', rij 1. De sticky zorgt ervoor dat het rechts wordt toegevoegd.
            
            self.radiobuttonmultipleBig = Radiobutton(master, text="All Reading Frames\nin seperate Big Figures", value=3, variable=self.radioInt, command=self.radioInt.set(2)) #Een button om deze manier van grafiekdisplay te kiezen
            self.radiobuttonmultipleBig.config(indicatoron=0, bd=4, width=20, value=2) #Dit maakt de button een vierhoek ipv een cirkel
            self.radiobuttonmultipleBig.grid(row=2, column=0, padx=10, pady=5) #De button toevoegen aan het 'grid', rij 2.
            
            self.Entry = Entry(master, bd=5) #Een balkje om indeces in te voegen wordt aangemaakt
            self.Entry.grid(row=3, sticky=E) #De button toevoegen aan het 'grid', rij 3. De sticky zorgt ervoor dat het rechts wordt toegevoegd.
            self.LabelEntry = Label(master, text="Input Index Fasta",foreground="blue",font=("Helvetica", 12)) #Voor de Entry wordt een label gemaakt
            self.LabelEntry.grid(row=3, sticky=W) #De button toevoegen aan het 'grid', rij 3. De sticky zorgt ervoor dat het links wordt toegevoegd.
            
            self.CheckBlastButton = Checkbutton(master, text = "Perform Blast", variable = self.CheckBlastInt, onvalue = 1, offvalue = 0, height=5, width = 10) #Een button om te Blasten of niet
            self.CheckBlastButton.grid(row=4) #De button toevoegen aan het 'grid', rij 4.
            
            self.label = Label(master, text ="ORF IN DNA",foreground="red",font=("Helvetica", 16)) #Het maken van een label
            self.label.grid(row=5) #De label toevoegen aan het 'grid', rij 5
            
            self.textframe = Frame(master, width=400, height=400) #Dit wordt toch veranderd, dus 400 x 400 is eigenlijk onnodig
            self.textframe.grid(row=6) #Het frame toevoegen aan het 'grid', rij 6
            self.text = Text(self.textframe, height=6, width=30) #Het maken van een textblok in het frame
            self.text.grid(row=6, column=0, sticky="nsew", padx=5, pady=5) #Het textblok toevoegen aan het 'grid', rij 6, in het frame
            self.scrollbar = Scrollbar(self.textframe, orient="vertical", command = self.text.yview) #Het maken van een scrollbar
            self.scrollbar.grid(row=6, column=1, sticky="nsew") #De scrollbar toevoegen aan het 'grid', rij 6, in het frame
            self.text['yscrollcommand'] = self.scrollbar.set #De scrollbar een commando meegeven
            
            self.HelpWindowbutton = Button(master, text="Help", width=30, bg="purple", font=("Papyrus", 10), command = lambda:[CreateHelpWindow(self, master)]) #Een button die een hulpscherm geeft, moet in een lambda vanwege een bug als alternatief
            self.HelpWindowbutton.bind("<Button-1>") #De button vertellen wat voor actie het activeerd
            self.HelpWindowbutton.grid(row=7) #De button toevoegen aan het 'grid', rij 7
        
            root.mainloop() #Het uitvoeren van de mainloop
            
        except TclError:
            messagebox.showerror("Warningmessage", "TclError, tkinter has issues") #Deze error komt als je .pack() en .grid() door elkaar gebruikt
        
    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name, "destroyed") #Dit is het bericht dat komt als de GUI is afgesloten
          
    
if __name__ == "__main__":
    try:
        root = Tk()
        my_gui = ORFGUI(root)
    except Exception as x:
            messagebox.showerror("Warningmessage", "A Rare Random Error appeared" + "\n" + str(x)) #Alle mogelijke andere errors die de applicatie kan hebben worden afgevangen


