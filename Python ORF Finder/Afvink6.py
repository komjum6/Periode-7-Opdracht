
def main():
    DNAlijst = leesBestand()
    bepaalGCpercentage(DNAlijst)

def leesBestand():
    Filename = 'D:\Bio-Infmap\Data\Periode_7\H5N1seq1.fasta' #Generic Fasta Path
    file = open(Filename, "r")
    class DNA:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA

    yconcat = ""
    DNAobjectlist = []
    headerlist = []
    dnalijst = []

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

    indexcount = 0
    for header in headerlist:
        dna = DNA(headerlist[indexcount],DNAobjectlist[indexcount])
        indexcount += 1
        dnalijst.append(dna)

    return dnalijst

def bepaalGCpercentage(sequentielijst):
    for sequentie in sequentielijst:
        sequentie = sequentie.DNA
        gc = (sequentie.count('G')+sequentie.count('C'))/len(sequentie)
        schrijfHTMLrapport(sequentie, gc)

def schrijfHTMLrapport(gcPercentage, sequentie, bestandsnaam):
    f = open(bestandsnaam+"_rapport.html", "w")
    f.write("""
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <h1>Your sequence: %s</h1>
            <p>this sequence has been calculated to have a GC of %i</p>
        </body>
        </html>
    """ %(sequentie, gcPercentage))
    f.close()
    
main()
