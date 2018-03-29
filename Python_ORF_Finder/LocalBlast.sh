#!/bin/bash
makeblastdb -in ORF.txt -dbtype nucl -out Local
tblastn -db Local -query Genes.txt -outfmt 5 -out Result.txt
chmod 777 Result.txt 
./Result.txt
