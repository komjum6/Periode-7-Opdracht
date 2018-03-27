# Created Tuesday May 16th 2017
# By Teun van Duffelen, for HAN
# Version 1.0


#import time
from Bio.Blast import NCBIWWW, NCBIXML
#from Bio import Entrez
import mysql.connector

#BLASTs a sequence using BLASTx, the Non Redundant database, and BLOSUM62
def blast(sequence):
    results = NCBIWWW.qblast('blastx', 'nr', sequence, matrix_name='BLOSUM62')
    #    print(results.read())
    #    save(NCBIXML.read(result))
    return NCBIXML.read(results)

# Gets the required data from the input alignment, the data fetched is alignment title, protein name, protein accession, e-value, identity score, organism name, and organism family, genus, and species names
def getData(alignment, ID, header):
    print('Fetching data from results.')
    for hsp in alignment.hsps:
        title = alignment.title
        protName = title[title.index(' ') + 1:title.index('[') - 1]
        access = alignment.accession
        evalue = hsp.expect
        identity = (float(hsp.positives) / float(hsp.align_length)) * 100
        orgName = title[title.index('[') + 1:title.index(']')]

        # print(orgName)
        family, genus, species = getTax(access)
        if ' ' in orgName:
            if genus == orgName[:orgName.index(' '):]:
                species = orgName[orgName.index(' ') + 1:]
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

# Saves the results of the getData function, as well as both DNA sequences, the header of these sequences, and an ID number for the results
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
                       VALUES ("%s", "%s", "%s", "%s", "%s")""" % (
        blastID, header, accesscode, str(evalue), str(identity)))
        print('25%')
    time.sleep(2)
    cursor.execute("SELECT `Organism_ID` FROM `Micro-organisms`")
    rows = cursor.fetchall()
    if orgname != 'NULL' and family != 'NULL' and genus != 'NULL' and species != 'NULL' and mode == 0 and orgname not in str(
            rows):
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


res = blast()
