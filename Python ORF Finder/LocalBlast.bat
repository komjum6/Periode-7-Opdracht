cd C:\BLAST\blast-2.7.1+\bin
makeblastdb -in ORF.fasta -dbtype prot -out Local
blastp -db Local -query Genes.txt -evalue 0.00001 -out Result.txt
Result.txt