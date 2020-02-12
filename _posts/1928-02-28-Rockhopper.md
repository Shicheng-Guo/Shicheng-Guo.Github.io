---
layout: post
title: "RNA-seq data to reveal novel response mechanism to bacterial"
author: Shicheng Guo
date: 1928-02-28
categories: bioinformatics
tags: dual-RNAseq nr.faa diamond samsa2

---

bacterial RNA-seq analysis with Rockhopper: RNA-seq data to reveal novel response mechanism to bacterial within host wound tissues


```
Here is a small pipeline to do microbial RNA-seq analysis with [Rockhopper][1], Here I suppose you have pair-end RNA-seq data and single-end reads will be much easier for which I will not show it in this post:  

Step 1: Download Rockhopper including both Windows and Java versions. Please remember download Rockhopper.exe is important since it can be used to create reference much easier. You can download the reference from windows system and copy them to your Linux server. 
    wget https://cs.wellesley.edu/~btjaden/Rockhopper/download/current/Rockhopper.exe
    wget http://cs.wellesley.edu/~btjaden/Rockhopper/download/current/Rockhopper.jar
Step 2: create reference: 
Step 3: prepare the running script with Perl and bash
ls *.fastq.gz | paste - - > input.txt
perl -p -i -e 's/\s/\&/'  input.txt
paste 
```

```
#########################################################################################################
##### RNA-seq data to reveal novel response mechanism to bacterial within host wound tissues ###########
#########################################################################################################
## 02/04/2020
wget http://cs.wellesley.edu/~btjaden/Rockhopper/download/current/Rockhopper.jar
cd ~/hpc/project/RnaseqBacterial/extdata/rnaseq
genome_DIR1=~/hpc/project/RnaseqBacterial/extdata/rnaseq/Rockhopper_Results/genomes/Staphylococcus_aureus_subsp__aureus_USA300_FPR3757
genome_DIR2=

mkdir temp
for i in $(ls *.fastq.gz | rev | cut -c 17- | rev | uniq)
do
echo $i
echo \#PBS -N $i  > $i.job
echo \#PBS -l nodes=1:ppn=12 >> $i.job
echo \#PBS -M Guo.shicheng\@marshfieldresearch.org >> $i.job
echo \#PBS -m abe  >> $i.job
echo \#PBS -o $(pwd)/temp/ >>$i.job
echo \#PBS -e $(pwd)/temp/ >>$i.job
echo cd $(pwd) >> $i.job
echo java -Xmx1200m -cp Rockhopper.jar Rockhopper -g $genome_DIR1 $i\_R1_001.fastq.gz%$i\_R2_001.fastq.gz -o ./Rockhopper_Results/$i >> $i.job
qsub  $i.job
done
```

How do download nr.faa for diamond and samsa2
```
wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
diamond makedb --in nr.gz -d nr
```

Here is R script to summarize microbial dual-transcriptome data
```r

setwd("//mcrfnas2/bigdata/Genetic/Projects/shg047/project/RnaseqBacterial/extdata/rnaseq/Rockhopper_Results")

perl -p -i -e "s/\'/-/g" gene.tab.matrix.v4.txt
perl -p -i -e "s/\(/-/g" gene.tab.matrix.v4.txt
perl -p -i -e "s/\)/-/g" gene.tab.matrix.v4.txt
perl -p -i -e "s/\,/-/g" gene.tab.matrix.v4.txt
perl -p -i -e "s/\:/-/g" gene.tab.matrix.v4.txt
perl -p -i -e "s/\;/-/g" gene.tab.matrix.v4.txt

data<-read.table("gene.tab.matrix.v4.txt",head=T,row.names=1,sep="\t",as.is=T,check.names = F)
head(data)
dim(data)

data<-data[order(apply(data[,1:24],1,function(x) sum(x>0)),decreasing = T),]
data<-data[,c(order(as.numeric(colnames(data[1:24]))),25,26)]

data$pc<-percent(apply(data[,1:24],1,function(x) sum(x>0))/24)
data$mean<-round(apply(data[,1:24],1,function(x) mean(x)),0)
data$sd<-round(apply(data[,1:24],1,function(x) sd(x)),0)
data$cv<-round(apply(data[,1:24],1,function(x) cv(x)),2)

head(data)
write.csv(data,file="gene.tab.matrix.v6.csv",quote=F,row.names = T)

GOI1<-read.table("https://raw.githubusercontent.com/Shicheng-Guo/RnaseqBacterial/master/extdata/interestlist1.txt")
GOI2<-read.table("https://raw.githubusercontent.com/Shicheng-Guo/RnaseqBacterial/master/extdata/interestlist2.txt")

x1<-tolower(GOI1[,1])
x2<-tolower(GOI1[,1])
x3<-tolower(data$N1)

x1[which( ! x1 %in% x3)]
x2[which( ! x2 %in% x3)]

out1<-na.omit(data[match(tolower(GOI1[,1]),tolower(data$N1)),])
out2<-na.omit(data[match(tolower(GOI2[,1]),tolower(data$N1)),])
out1
out2
write.csv(out1,file="gene.tab.matrix.table3.csv",quote=F)
write.csv(out2,file="gene.tab.matrix.table4.csv",quote=F)
```
