cd C:\Users\Luukv\Desktop\ORF finder\Periode-7-Opdracht\Python ORF Finder
move ORF.txt C:\BLAST\blast-2.7.1+\bin
cd C:\BLAST\blast-2.7.1+\bin
makeblastdb -in ORF.txt -dbtype nucl -out Local
tblastn -db Local -query Genes.txt -evalue 0.00001 -outfmt 5 -out Result.txt
Result.txt
move Result.txt C:\Users\Luukv\Desktop\ORF finder\Periode-7-Opdracht\Python ORF Finder