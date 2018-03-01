
# coding: utf-8

# In[1]:

# Autors: Bertram Hutten, Luuk van Damme, Teun van Duffelen en Justin Huberts
# Date of creation: around the beginning of February
# Functionality: 
# Known Bugs: 
# TO_ADD: Radiobutton voor readingframes, blastbutton (Na het inlezen, voor één of alle reading frames)

from read import load_file
from dataprocessing import findStartPositions, findNextCodon, findNextStopCodon, findOpenReadingFrames

from tkinter import ttk
from tkinter import *  

#Alleen nodig als je Jupyter notebook gebruikt
get_ipython().magic('matplotlib')

#Hier vind de actie plaats
class ORFGUI(Frame):  
    def __init__(self, master):
        try:
            seq = StringVar() #De sequentie als string
            self = self #Laat de code zichzelf in de ogen kijken door 'm een spiegel voor te leggen...
            
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


