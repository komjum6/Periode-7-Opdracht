def main():
    DNAlijst = leesBestand()
    bepaalGCpercentage(DNAlijst)

def leesBestand():
    Filename = 'Generic Path'
    file = open(Filename, "r")
    class DNA:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA
    
    DNAobjectlist = []
    headerlist = []
    
    for line in file:
        if line.startswith(">"):
            x = line
            headerlist.append(x)
            DNAobjectlist.append(yconcat)
            yconcat = ""
        if line.startswith(">") == False:
            y = line 
            yconcat += y

    DNAobjectlist.append(yconcat)
    DNAobjectlist.pop(0) #Er is een keer een lege string toegevoegd.
    
    for header in headerlist: 
        dna = DNA(headerlist[indexcount],DNAlist[indexcount])
        indexcount += 1
        dnalijst.append(dna)
    
    return dnalijst

def bepaalGCpercentage(sequentie):
    print("hey")

def schrijfHTMLrapport(gcPercentage, sequentie, bestandsnaam):
    print("hey")

main()