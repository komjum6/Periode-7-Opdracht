# Created Wednesday March 28th 2018
# By Teun van Duffelen, for HAN
# Version 1.0

import cx_Oracle
UN = "owe7_pg1"
PW = "blaat1234"
ADDR = "cytosine.nl"

def query(query):
    conn = cx_Oracle.connect(UN, PW, ADDR)
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor

result = query("""SELECT * FROM FRAME""")
for frame in result:
    print(frame)
    
    

def Read():
    sequentie=""
    header=""
    ID=0
    
        
    ReadFile=open("Genes.txt", "r")
    Write=open("SQL_Interest_Genes.txt", "w")
    for line in ReadFile:
        if line.startswith(">"):
            if(ID!=0):
                Insert_Query="INSERT INTO INTEREST_GENES(ID,HEADER,SEQUENCE)"
                Values_Query="VALUES( '{0}','{1}','{2}' );".format(ID,header,sequentie)
                Query(Write,Insert_Query,Values_Query)
                sequentie=""
                ID=ID+1
                header=str(line)
                
            else:
                ID=ID+1
                header=str(line)
        else:
            sequentie+=str(line)
            
    Insert_Query="INSERT INTO INTEREST_GENES(ID,HEADER,SEQUENCE)"
    Values_Query="VALUES( '{0}','{1}','{2}' );".format(ID,header,sequentie)
    Query(Write,Insert_Query,Values_Query)
    
    ReadFile.close()
    Write.close()
    
    
    ReadFile=open("Debaryomyces_occidentalis.fas", "r")
    Write=open("SQL_Organism.txt", "w")
    for line in ReadFile:
        if line.startswith(">"):
            if(ID!=0):
                Insert_Query="INSERT INTO INTEREST_GENES(ID,HEADER,SEQUENCE)"
                Values_Query="VALUES( '{0}','{1}','{2}' );".format(ID,header,sequentie)
                Query(Write,Insert_Query,Values_Query)
                sequentie=""
                ID=ID+1
                header=str(line)
                
            else:
                ID=ID+1
                header=str(line)
        else:
            sequentie+=str(line)
            
    Insert_Query="INSERT INTO INTEREST_GENES(ID,HEADER,SEQUENCE)"
    Values_Query="VALUES( '{0}','{1}','{2}' );".format(ID,header,sequentie)
    Query(Write,Insert_Query,Values_Query)
    
    ReadFile.close()
    Write.close()
    


def Query(WriteFile,Insert,Values):
    WriteFile.write(str(Insert)+"\n")
    WriteFile.write(+str(Values)+"\n")
