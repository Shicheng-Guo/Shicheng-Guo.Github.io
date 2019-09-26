How to apply RIblast to predict ncRNA interaction target
```
cd ~/hpc/tools/RIblast/extdata
wget http://ftp.ensembl.org/pub/release-97/fasta/homo_sapiens/ncrna/Homo_sapiens.GRCh38.ncrna.fa.gz
wget http://ftp.ensembl.org/pub/release-97/fasta/homo_sapiens/cdna/Homo_sapiens.GRCh38.cdna.all.fa.gz 
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/mrna.fa.gz -O Homo_sapiens.GRCh38.mrna.fa.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_31/gencode.v31.transcripts.fa.gz

gunzip Homo_sapiens.GRCh38.ncrna.fa.gz
gunzip Homo_sapiens.GRCh38.cdna.all.fa.gz 
gunzip Homo_sapiens.GRCh38.mrna.fa.gz 
gunzip gencode.v31.transcripts.fa.gz

../RIblast db -i Homo_sapiens.GRCh38.mrna.fa  -o Homo_sapiens.GRCh38.mrna.fa.db
../RIblast db -i Homo_sapiens.GRCh38.cdna.all.fa  -o Homo_sapiens.GRCh38.cdna.all.fa.db
../RIblast db -i Homo_sapiens.GRCh38.ncrna.fa  -o Homo_sapiens.GRCh38.ncrna.fa.db
../RIblast db -i gencode.v31.transcripts.fa  -o gencode.v31.transcripts.fa.db

grep AC004585.1 Homo_sapiens.GRCh38.ncrna.fa.txt > AC004585.fa
../RIblast ris -i AC004585.fa -o AC004585.txt -d Homo_sapiens.GRCh38.cdna.all.fa.db
```
