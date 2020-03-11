---
layout: post
title: "How to Prepare Annotation DB Folder for Bioinformatics Analysis"
author: Shicheng Guo
date: 1920-02-28
categories: bioinformatics
tags: Genetics Genomics GWAS PostGWAS ANNOVAR
---

Here, I list all the used annotation in my previous publication: 

* VIP: Very Important Pharmacogenes: N=66
* InnateDB: All [immmnue system](https://www.innatedb.com/redirect.do?go=resourcesGeneLists) related genes list N=4723
* FDR drug marker: [Pharmacogenomic Biomarkers](https://www.fda.gov/drugs/science-and-research-drugs/table-pharmacogenomic-biomarkers-drug-labeling) in Drug Labeling
* FDR:FDA_approved_drugtarget: 460 [FDA_approved_drugtarget](https://raw.githubusercontent.com/Shicheng-Guo/AnnotationDatabase/master/FDA_approved_drugtarget.txt)


Step by step to prepare your db folder (hg38): 

```
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cytoBand.txt.gz -O cytoBand.hg38.bed.gz
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cpgIslandExt.txt.gz -O cpgIsland.hg38.bed.gz
wget https://raw.githubusercontent.com/Shicheng-Guo/miRNA-RA/master/db/hsa.gff.hg19.bed -O hsa.gff3.hg38.bed 
wget http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/liftOver -O liftOver
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg18/liftOver/hg18ToHg19.over.chain.gz -O hg18ToHg19.over.chain.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz -O hg19ToHg38.over.chain.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg38/liftOver/hg38ToHg19.over.chain.gz -O hg38ToHg19.over.chain.gz
wget https://raw.githubusercontent.com/Shicheng-Guo/GscRbasement/master/manhattan.qqplot.R -O manhattan.plot.R
wget https://raw.githubusercontent.com/Shicheng-Guo/Gscutility/master/localhit.pl -O localhit.pl
wget https://raw.githubusercontent.com/Shicheng-Guo/rheumatoidarthritis/master/R/make.fancy.locus.plot.unix.R -O make.fancy.locus.plot.unix.R
```