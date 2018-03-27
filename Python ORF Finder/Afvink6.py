
def main():
    Filename = 'H5N1seq1.fasta' #Generic Fasta Path

    DNAlijst = leesBestand(Filename)
    bepaalGCpercentage(DNAlijst)
    schrijfHTMLrapport(DNAlijst, Filename)

#Openen en lezen van bestand.
def leesBestand(Filename):

    file = open(Filename, "r")
    class DNA:
        def __init__(self, header, DNA):
            self.header = header
            self.DNA = DNA

        def setGC(self, gc):
            self.gcperc = gc

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

#berekening van het GC percentage van de sequentie.
def bepaalGCpercentage(sequentielijst):
    for sequentie in sequentielijst:
        rawSeq = sequentie.DNA
        sequentie.setGC(float(rawSeq.count('G')+rawSeq.count('C'))/len(rawSeq)*100)

def schrijfHTMLrapport(sequenties, bestandsnaam):
    htmlString = ""

    htmlString += """
        <html>
        <body>
            <h1>%i sequences analysed</h1>
        """%(len(sequenties))

    for seq in sequenties:
        htmlString += "<p>sequence %s has a GC percentage of %i</p>"%(seq.DNA, seq.gcperc)

    htmlString += """
        </body>
        </html>
        """

    f = open(bestandsnaam+"_rapport.html", "w")
    f.write(htmlString)
    f.close()

main()
