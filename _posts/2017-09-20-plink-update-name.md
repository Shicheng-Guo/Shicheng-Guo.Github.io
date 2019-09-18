---
layout: post
title: "How to update SNP id in plink dataset with bcftools or plink"
author: Shicheng Guo
date: 2017-09-20
categories: bioinformatics
tags: computational packages plink bcftools
image: images/Shicheng-Guo-GWAS-plink-bcftools-700px-New_lz_cond_only.png	

---

Recently, colleagues always ask me what's the best solution to replace SNP ids in plink map files. Actually, there are tens of different solutions and you only need to mask one of these and then apply it for all the times. Now let me show you several different solutions. 

1. bcftools annotate

```
plink --bfile ROI --recode vcf --out ROI
bcftools view ROI.vcf -Oz -o ROI.vcf.gz
tabix -p vcf ROI.vcf.gz
bcftools annotate -a ~/hpc/db/hg19/dbSNP/All_20180423.hg19.vcf.gz -c ID ROI.vcf.gz -Oz -o ROI.hg19.vcf.gz
```

2. plink --update-name

You need prepare the old id and new id relationship or mapping file before you use this function. However, the best solution is to replace the old id with chr:pos and then download chr:pos, new id from ucsc.

```
plink --bfile ROI --recode vcf --out ROI
bcftools view ROI.vcf -Oz -o ROI.vcf.gz
tabix -p vcf ROI.vcf.gz
bcftools annotate -a ~/hpc/db/hg19/dbSNP/All_20180423.hg19.vcf.gz -c ID ROI.vcf.gz -Oz -o ROI.hg19.vcf.gz
```

These two method will be best choice. hope you enjoy it. 
