cd D:\School\HAN\2017?2018 (Bi2c)\Course 7\Tutor\Periode-7-Opdracht\Python ORF Finder
move ORF.txt C:\Program Files\NCBI\blast-2.7.1+\bin
cd C:\Program Files\NCBI\blast-2.7.1+\bin
makeblastdb -in ORF.txt -dbtype nucl -out Local
tblastn -db Local -query Genes.txt -evalue 0.00001 -outfmt 5 -out Result.txt
Result.txt
move Result.txt D:\School\HAN\2017?2018 (Bi2c)\Course 7\Tutor\Periode-7-Opdracht\Python ORF Finder