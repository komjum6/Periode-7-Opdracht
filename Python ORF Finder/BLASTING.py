import xlrd
import time
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez
import mysql.connector

Entrez.email = 'cripplezzz@gmail.com'

#testSeq = 'GTCTCGCACCCGGCCAAGCAGGGCTTCGTGCAGGCCTTCGCCATCTACTTCGACACCATGCTGGTGTGCACCTCCACCGCCTTCCTGCTGCTGTCCACCGGCATGTACAACACCTTCCGCGTAGTGGTGGAGGACGGCGCCGAGAAGCTGGAGGCGGTGGTGACCGGCGTGCCGGGCCTGCTGCCCTCCGAGGGCGCGCAGTTCGCCCAGGCCGCGGTCGAGTCGGTGCTGCCGGGCTGGGGCGCGGGCTTCGTGGCGCTGGCGCTGTTCTTCTTCGCCTTCACCACGATCATGGCCTACC'
#testRes = open('testResult.xml', 'r')

#Gets DNA sequences from source data, BLASTs these, analyses the results, and filters and saves good results to a database
def main():
    forw, backw, header = getSeq()
    if len(forw) == len(backw):
        for entry in range(len(forw)):
            timeStart = time.time()
            print('Blasting sequences %s at %s' %(entry+1, time.ctime(timeStart)))
            print('1..')
            forwRes = blast(forw[entry])
            time.sleep(5)
            print('2..')
            backRes = blast(backw[entry])
            print('Finished at %s!' %(time.ctime(time.time())))
            print('Process took %s minutes.\n' %(format(((time.time()-timeStart)/60), '.2f')))
            resHandler(forwRes, backRes, header[entry], entry)
            save(mode=1, header=header[entry], forward=forw[entry], reverse=backw[entry])
            time.sleep(5)

#Gets the forward and reverse sequences from the source dataset
def getSeq():

    file = xlrd.open_workbook('Sequences/Course4_dataset_v03.xlsx')
    dataset = file.sheet_by_name('groep10')
    forward = dataset.col_values(1)
    backward = dataset.col_values(4)
    headers = dataset.col_values(0)

    realHeader = []
    for header in headers:
        header = header.rstrip('_1')
        realHeader.append(header)

#    print(forward)
#    print(len(forward), len(backward))

    return forward, backward, realHeader

#BLASTs a sequence using BLASTx, the Non Redundant database, and BLOSUM62
def blast(sequence):
    results = NCBIWWW.qblast('blastx', 'nr', sequence, matrix_name='BLOSUM62')
#    print(results.read())
#    save(NCBIXML.read(result))
    return NCBIXML.read(results)

#Takes in the BLAST results of both sequences (forward and reverse), and filters these results by comparing the forward to
#the backward, and an e-value- and identity threshold, as well as assigning an ID number to every result
def resHandler(forwRes, backRes, header, entry):
    maxEValue = 4e-8
    minIdentity = 25

    ID = 1

    forwName = set()
    backName = set()

    for name in forwRes.alignments:
        forwName.add(name.title)

    for name in backRes.alignments:
        backName.add(name.title)

#    print(forwName, backName)
#    print(len(backName))

    titles = forwName & backName
#    print(titles)

    print('Analizing results.')
    for alignment in forwRes.alignments:
        BlastID = str(entry+1) + '-' + str(ID)
        ID += 1
#        print(BlastID)
        
        if alignment.title in titles or len(backName) == 0:
#            print('found one!')
            for hsp in alignment.hsps:
                try:
                    if hsp.expect < maxEValue and (float(hsp.identities)/float(hsp.align_length)*100) > minIdentity:
                        getData(alignment, BlastID, header)
                except:
                    pass

    if ID == 1:
        print('No good results found.')

#Gets the required data from the input alignment, the data fetched is alignment title, protein name, protein accession,
#e-value, identity score, organism name, and organism family, genus, and species names
def getData(alignment, ID, header):
    print('Fetching data from results.')
    for hsp in alignment.hsps:
        title = alignment.title
        protName = title[title.index(' ')+1:title.index('[')-1]
        access = alignment.accession
        evalue = hsp.expect
        identity = (float(hsp.positives)/float(hsp.align_length))*100
        orgName = title[title.index('[')+1:title.index(']')]

        #print(orgName)
        family, genus, species = getTax(access)
        if ' ' in orgName:
            if genus == orgName[:orgName.index(' '):]:
                species = orgName[orgName.index(' ')+1:]
                species = species[0].upper() + species[1:]

        if ' ' in orgName:
            if family == orgName[:orgName.index(' '):]:
                genus = orgName[orgName.index(' ') + 1:]
                genus = genus[0].upper() + genus[1:]

        print('')
        print(protName)
        print(orgName)
        print(family)
        print(genus)
        print(species)
        print(access)
        print(evalue)
        print(identity)
        print('')

        save(header=header,
             blastID=ID, accesscode=access, evalue=evalue, identity=identity,
             protname=protName, orgname=orgName,
             family=family, genus=genus, species=species)

#Gets the taxonomic lineage of an organism using it's access code, consulting the NCBI Protein database, and returns the
#family, genus, and species names
def getTax(number):
    protData = Entrez.efetch(db='protein', id=number, rettype="gb", retmode="text")
    results = protData.read()
#    print(results)

    lineage = results[results.index('ORGANISM'):]
    lineage = lineage[lineage.index('\n') + 1:]
    lineage = lineage[:lineage.index('.')].replace('\n', '').replace(' ', '').split(';')
#    print(lineage)

    while len(lineage) < 7:
        lineage.append('NULL')
    while len(lineage) > 7:
        lineage = lineage[:9]
    species = lineage[len(lineage)-1]
    genus = lineage[len(lineage)-2]
    family = lineage[len(lineage)-3]
#    print(family, genus, species)
    return family, genus, species

#Saves the results of the getData function, as well as both DNA sequences, the header of these sequences, and an ID number for the results
def save(mode=0, header='NULL', forward='NULL', reverse='NULL',
         blastID='NULL', accesscode='NULL', evalue='NULL', identity='NULL',
         protname='NULL', orgname='NULL',
         family='NULL', genus='NULL', species='NULL'):

    if mode == 0:
        print('Saving results to database')

    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='owe4_bi1a_1',
        db='owe4_bi1_9',
        passwd='blaat1234')

    cursor = conn.cursor()

    if blastID != 'NULL' and header != 'NULL' and accesscode != 'NULL' and evalue != 'NULL' and identity != 'NULL' and mode == 0:
        cursor.execute("""INSERT INTO `Blast_Results` (`Blast_ID`, `Header`, `Access_code`, `E-value`, `Percent_identity`)
                       VALUES ("%s", "%s", "%s", "%s", "%s")""" % (blastID, header, accesscode, str(evalue), str(identity)))
        print('25%')
    time.sleep(2)
    cursor.execute("SELECT `Organism_ID` FROM `Micro-organisms`")
    rows = cursor.fetchall()
    if orgname != 'NULL' and family != 'NULL' and genus != 'NULL' and species != 'NULL' and mode == 0 and orgname not in str(rows):
        cursor.execute("""INSERT INTO `Micro-organisms` (`Organism_ID`, `Family`, `Genus`, `Species`)
                       VALUES ("%s", "%s", "%s", "%s")""" % (orgname, family, genus, species))
        print('50%')
    time.sleep(2)
    if blastID != 'NULL' and accesscode != 'NULL' and protname != 'NULL' and orgname != 'NULL' and mode == 0:
        cursor.execute("""INSERT INTO `Proteins` (`Blast_ID`, `Access_code`, `FUNCTION`, `Micro-organism`, `Organism_ID`)
                       VALUES ("%s", "%s", "%s", "%s", "%s")""" % (blastID, accesscode, protname, orgname, orgname))
        print('75%')
    if header != 'NULL' and forward != 'NULL' and reverse != 'NULL' and mode == 1:
        cursor.execute("""INSERT INTO `Sequences` (`Header`, `Forward`, `Reverse`)
                       VALUES ("%s", "%s", "%s")""" % (header, forward, reverse))
        print('100%')

    conn.commit()
    cursor.close()
    conn.close()
    if mode == 1:
        print('Saved results to database')
        print('')

'''
    print(header, forward, reverse,\
          accesscode, evalue, identity,\
          protname, orgname,\
          family, genus, species)
'''
main()
#getTax('Burkholderia gladioli BSR3 chromosome 1')
#resHandler(NCBIXML.read(testRes))
#getProt('SDW86145')
#print(getSeq())
'''
requirements:
    e-value
    identity
    coverage
'''