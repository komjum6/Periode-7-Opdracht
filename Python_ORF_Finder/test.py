# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 12:45:58 2018

@author: Luukv
"""

def main():
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

main()