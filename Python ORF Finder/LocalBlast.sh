#!/bin/bash
makeblastdb -in ORF.txt -dbtype nucl -out Local
tblastn -db Local -query Genes.txt -evalue 0.00001 -out Result.txt
chmod 777 Result.txt 
./Result.txt
