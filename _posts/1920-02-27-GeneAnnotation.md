---
layout: post
title: "Usuaful Gene Annotation List in Bioinformatics Analysis"
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
```