# Created Tuesday May 16th 2017
# By Teun van Duffelen, for HAN
# Version 1.0

#import cx_Oracle
from Bio.Blast import NCBIXML

#run a local BLAST
def local():
    import os, platform
    CurrentPlatform = platform.system()
    from subprocess import Popen

    if CurrentPlatform == 'Linux':
        shell = Popen("LocalBlast.sh", cwd=os.path.abspath("LocalBlast.sh"))
        stdout, stderr = shell.communicate()

    if CurrentPlatform == 'Windows':
        batch = Popen("LocalBlast.bat", cwd=os.path.abspath("LocalBlast.bat"))
        stdout, stderr = batch.communicate()

    getData(NCBIXML.parse(open("testResult.xml", "r")))

    #os.system('LocalBlast.bat')

#Gets the required data from the input alignment, the data fetched is the
#e-value, identity score, score, positives, gap, and query
def getData(alignment):
    print('Fetching data from results.')
    ID = 1
    output = open("SQL_Result.txt", "w")
    for a in alignment:
        for alignment in a.alignments:
            for hsp in alignment.hsps:
                #title = alignment.title
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

                output.write("""INSERT INTO Result (ID, Score, Expect, Identities, Positives, Gaps, Query_Subject)
                        VALUES (%i, %i, %f, %f, %i, %i, %s);"""%(ID, hsp.score, hsp.expect, identity, hsp.positives, hsp.gaps, hsp.query))
                ID += 1

    output.close()
