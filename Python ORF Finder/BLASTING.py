# Created Tuesday May 16th 2017
# By Teun van Duffelen, for HAN
# Version 1.0

#import cx_Oracle
from Bio.Blast import NCBIXML


#run a local BLAST
def local():
    import os
    #os.system('LocalBlast.bat')

    getData(NCBIXML.read(open("testResult.xml", "r")))

#Gets the required data from the input alignment, the data fetched is alignment title, protein name, protein accession,
#e-value, identity score, organism name, and organism family, genus, and species names
def getData(alignment):
    print('Fetching data from results.')
    ID = 1
    for alignment in alignment.alignments:
        for hsp in alignment.hsps:
            title = alignment.title
            #protName = title[title.index(' ')+1:title.index('[')-1]
            #access = alignment.accession
            identity = (float(hsp.positives)/float(hsp.align_length))*100
            #orgName = title[title.index('[')+1:title.index(']')]

            '''print('')
            print(hsp.score)
            print(hsp.expect)
            print(identity)
            #print(protName)
            print(hsp.positives)
            print(hsp.gaps)
            print(hsp.query)
            print('')'''

            print("""INSERT INTO Result (ID, Score, Expect, Identities, Positives, Gaps, Query_Subject)
                    VALUES (%i, %i, %f, %f, %i, %i, %s)"""%(ID, hsp.score, hsp.expect, identity, hsp.positives, hsp.gaps, hsp.query))
            ID += 1

        #save(header=header,
        #     blastID=ID, accesscode=access, evalue=evalue, identity=identity,
        #     protname=protName, orgname=orgName,
        #     family=family, genus=genus, species=species)

#Saves the results of the getData function, as well as both DNA sequences, the header of these sequences, and an ID number for the results
def save(mode=0, header='NULL', forward='NULL', reverse='NULL',
         blastID='NULL', accesscode='NULL', evalue='NULL', identity='NULL',
         protname='NULL', orgname='NULL',
         family='NULL', genus='NULL', species='NULL'):
    if mode == 0:
        print('Saving results to database')

    conn = cx_Oracle.connect("owe7_pg1", "blaat1234", "cytosine.nl")

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

local()
