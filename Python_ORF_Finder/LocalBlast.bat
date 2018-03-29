cd C:\Users\Luukv\Desktop\ORF_Finder\Periode-7-Opdracht\Python_ORF_Finder
move Genes.txt C:\Program Files\NCBI\blast-2.7.1+\bin

move ORF.txt C:\Program Files\NCBI\blast-2.7.1+\bin

cd C:\Program Files\NCBI\blast-2.7.1+\bin

makeblastdb -in ORF.txt -dbtype nucl -out Local

tblastn -db Local -query Genes.txt -outfmt 5 -out Result.txt

Result.txt

move ORF.txt C:\Users\Luukv\Desktop\ORF_Finder\Periode-7-Opdracht\Python_ORF_Finder
move Result.txt C:\Users\Luukv\Desktop\ORF_Finder\Periode-7-Opdracht\Python_ORF_Finder
move Genes.txt C:\Users\Luukv\Desktop\ORF_Finder\Periode-7-Opdracht\Python_ORF_Finder
