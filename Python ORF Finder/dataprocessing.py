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
                'GGG' : 'G'}

StartCodon = 'ATG'

StopCodons = ['TAG', 'TGA', 'TAA']


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
    
def findOpenReadingFrames(self, seq, seqje, Frameskew = -3):
    
    seqje = str(seqje)
    seqje = seqje.upper()
    
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
                # Maak een tuple met start en stopposities:
                result.append( (startPosition + Frameskew, stopPosition + Frameskew) )
    else:
        for startPosition in findStartPositions(ejqes):
            # pak de stop positie voor iedere start positie:
            stopPosition = findNextStopCodon(ejqes, startPosition)
            # check dat we de stop posities hebben:
            if stopPosition != None:
                # Maak een tuple met start en stopposities:
                result.append( (startPosition + Frameskew, stopPosition + Frameskew) )
                
    #Roep de volgende functie aan
    if Frameskew != 4:
        findOpenReadingFrames(self, seq, seqje, Frameskew +1)
        printOpenReadingFrames(self, seq, seqje, result, Frameskew)
    
def printOpenReadingFrames(self, seq, seqje, result, Frameskew):
    features = []
    displayString = ""
    count = 0
    for x in range(0,len(result)):
        found_orf = seqje[slice(*result[count])] #Door de index te veranderen is door de ORF's te bladeren
        #print("This is ",count," index: ",found_orf)
        displayString = displayString + str(count) + " index " + found_orf + "\n" #Een string maken met alle ORF's
        color = "#%06x" % random.randint(0, 0xFFFFFF) #Een willekeurige kleur wordt gekozen
        features.append(GraphicFeature(start=result[count][0], end=result[count][1], strand=+1, color=color, label= str(count) + " Index ORF", labelcolor=color)) #Het toevoegen van de entries aan het figuur
        #print("result count ",*result[count]) #Print de start en stoppositie van de ORF's
        count += 1

    self.text.insert(END, displayString) #De orf's als strings laten zien in de GUI
    record = GraphicRecord(sequence_length=len(seqje), features=features) #Het maken van een figuur met de ORF's
    #plt.title(str(Frameskew))
    record.plot(figure_width=15) #Het figuur wordt gemaakt, de grootte van het figuur valt aan te passen
    plt.title(str(Frameskew))
    plt.show()
    
    seq.set(str(result))
    #print(seq.get())
    