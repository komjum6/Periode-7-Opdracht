from dna_features_viewer import GraphicFeature, GraphicRecord
from tkinter import END
import random
import matplotlib.pyplot as plt

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
                'GGG' : 'G',
    
'ANC' : 'X', #Ik heb hier wat toegevoegd om N's af te vangen. Het lukt maar niet.
'CNA' : 'X',
'NCA' : 'X',
'NCN' : 'X',
'TCN' : 'X',
'TNC' : 'X',
'NGT' : 'X',
'ANG' : 'X',
'GNA' : 'X',
'ANN' : 'X',
'NGA' : 'X',
'NNA' : 'X',
'GNT' : 'X',
'CTN' : 'X',
'CNG' : 'X',
'CGN' : 'X',
'NAC' : 'X',
'GNN' : 'X',
'GAN' : 'X',
'TAN' : 'X',
'NNG' : 'X',
'NNT' : 'X',
'ACN' : 'X',
'CNT' : 'X',
'AGN' : 'X',
'NGN' : 'X',
'GCN' : 'X',
'NAG' : 'X',
'CNN' : 'X',
'NGC' : 'X',
'GTN' : 'X',
'TNN' : 'X',
'NCT' : 'X',
'NTA' : 'X',
'TGN' : 'X',
'NNC' : 'X',
'ANT' : 'X',
'GNC' : 'X',
'NAT' : 'X',
'NTG' : 'X',
'NAN' : 'X',
'CAN' : 'X',
'NTC' : 'X',
'TNG' : 'X',
'NTN' : 'X',
'TNA' : 'X',
'ATN' : 'X',
'NCG' : 'X',
'NNN' : 'X'
} #Belangrijke toevoeging

StartCodon = 'ATG'

StopCodons = ['TAG', 'TGA', 'TAA']

#-----------------------------------------Begin van de Functies, hieronder zijn functies die in andere functies worden gebruikt---------------------------------------------

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
    
#-----------------------------------------Hieronder zijn functies voor het maken van de data van de plots-------------------------------------------------------------
    
def findOpenReadingFrames(self, seq, seqje, Frameskew = -3):
    
    seqje = str(seqje)
    seqje = seqje.upper() #Hoofdletters
    
    #Hier wordt de lijst gereversed
    if Frameskew < 0:
        ejqes = seqje[::-1]
    
    # Een lijst voor de resultaten
    result = []
    # loop over de lijst met findStartPositions:
    if Frameskew >= 0:
        for startPosition in findStartPositions(seqje):
            # pak de stop positie voor iedere start positie:
            stopPosition = findNextStopCodon(seqje, startPosition)
            # check dat we de stop posities hebben:
            if stopPosition != None:
                # Maak een tuple met start en stopposities en tel daar Frameskew bij op:
                result.append( (startPosition + Frameskew, stopPosition + Frameskew) )
    else:
        for startPosition in findStartPositions(ejqes):
            # pak de stop positie voor iedere start positie:
            stopPosition = findNextStopCodon(ejqes, startPosition)
            # check dat we de stop posities hebben:
            if stopPosition != None:
                # Maak een tuple met start en stopposities en tel daar Frameskew bij op:
                result.append( (startPosition + Frameskew, stopPosition + Frameskew) )
                
    #Roep de volgende functies aan, de variabele Frameskew mag niet groter zijn dan 2
    if Frameskew != 3:
        findOpenReadingFrames(self, seq, seqje, Frameskew +1) #Recursie
        printOpenReadingFrames(self, seq, seqje, result, Frameskew) #Gaat verder met de data in een volgende functie
    
def printOpenReadingFrames(self, seq, seqje, result, Frameskew, recordlijst = [], Frameskewlijst = []):
    #Er is geen Reading Frame 0
    if Frameskew >=0:
        Frameskew += 1
    
    features = []
    displayString = ""
    count = 0
    for x in range(0,len(result)):
        found_orf = seqje[slice(*result[count])] #Door de index te veranderen is door de ORF's te bladeren
        #print("This is ",count," index: ",found_orf)
        displayString = displayString + "\n" + " Index " + str(count) + " Reading Frame " + str(Frameskew) + "\n" + found_orf #Een string maken met alle ORF's
        color = "#%06x" % random.randint(0, 0xFFFFFF) #Een willekeurige kleur wordt gekozen
        features.append(GraphicFeature(start=result[count][0], end=result[count][1], strand=+1, color=color, label= str(count) + " Index ORF", labelcolor=color)) #Het toevoegen van de entries aan het figuur
        #print("result count ",*result[count]) #Print de start en stoppositie van de ORF's
        count += 1

    self.text.insert(END, displayString) #De orf's als strings laten zien in de GUI
    record = GraphicRecord(sequence_length=len(seqje), features=features) #Het maken van een figuur met de ORF's
    
    recordlijst.append(record) #Vul de lijst met recordobjecten
    Frameskewlijst.append(str(Frameskew)) #Maak een string lijst met de Reading Frames voor de namen van de figuren
    
    if len(recordlijst) == 6: #Er zijn altijd maar 6 Reading Frames mogelijk
        plotOpenReadingFrames(self, recordlijst, Frameskewlijst) #Aanroepen van de volgende functie
        
#-----------------------------------------De functie voor het maken van de plots zelf-------------------------------------------------------------
    
def plotOpenReadingFrames(self, recordlijst, Frameskewlijst):
    
    fig, ((ax1, ax2, ax3), (ax4, ax5 , ax6)) = plt.subplots(nrows = 2, ncols = 3, figsize=(80, 80), sharex='col', sharey='row') #Het toewijzen van de plaatsen van de subplots en een gedeelde x en y-as
    st = fig.suptitle("Reading Frames", fontsize="x-large") #De naam van de verzameling van de figuren

    #plt.subplot(611)
    rec1 = recordlijst[0] #Maak een variabele van de eerste index van de lijst met record objecten
    re1 = rec1.plot(ax = ax1) #Plot dit object en wijs het plaats toe binnen het grote Figuur
    ax1.set_title(Frameskewlijst[0]) #De titel wordt gezet

    #plt.subplot(612)
    rec2 = recordlijst[1]
    re2 = rec2.plot(ax = ax2)
    ax2.set_title(Frameskewlijst[1])

    #plt.subplot(613)
    rec3 = recordlijst[2]
    re3 = rec3.plot(ax = ax3)
    ax3.set_title(Frameskewlijst[2])

    #plt.subplot(614)
    rec4 = recordlijst[3]
    re4 = rec4.plot(ax = ax4)
    ax4.set_title(Frameskewlijst[3])

    #plt.plot(615)
    rec5 = recordlijst[4]
    re5 = rec5.plot(ax = ax5)
    ax5.set_title(Frameskewlijst[4])

    #plt.subplot(616)
    rec6 = recordlijst[5]
    re6 = rec6.plot(ax = ax6)
    ax6.set_title(Frameskewlijst[5])

    fig.tight_layout() #Maak de layout tight
    st.set_y(0.95) # shift subplots omlaag om ruimte te maken voor de Titel der Figuren
    fig.subplots_adjust(top=0.90,bottom=0.05,hspace = 0.2) #De spacing van de Figuren

    plt.show() #De aanpassingsfase is over (zoals het zetten van de titel etc), nu worden de figuren getoont
    
    
#-----------------------------------------Garbage code, DO NOT DELETE (may be useful later)-------------------------------------------------------------        
    
    #record.plot(figure_width=15) #Het figuur wordt gemaakt, de grootte van het figuur valt aan te passen
    #plt.title(str(Frameskew)) #De titel wordt gezet
    
    #plt.show() #De aanpassingsfase is over (zoals het zetten van de titel etc), nu worden de figuren getoont
    
    
    
    #seq.set(str(result))
    #print(seq.get())
    
    