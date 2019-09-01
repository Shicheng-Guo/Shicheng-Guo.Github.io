---
layout: post
title: "Next generation protocol to bcftools in medical genetics research"
author: Shicheng Guo
date: 2018-10-01
categories: bioinformatics
tags: bcftools vcftools samtools GATK
image: images/bcftools_2019_samtools_GATK_Shicheng_Guo.png

---
Today, I will give a talk about "Next generation protocol to [bcftools](https://samtools.github.io/bcftools/bcftools.html#annotate) in medical genetics research" in MCRI research hub meeting. As we know, bcftools, [vcftools](http://vcftools.sourceforge.net/man_latest.html), [plink2](https://www.cog-genomics.org/plink/2.0/), [GATK4](https://software.broadinstitute.org/gatk/gatk4) have been widely used in medical genetics and population genetics research. The usage of these tools require lots of experiences. However, the original protocols are quite limited espeically lacking of real-data example. Here, I will provide the real-data examples and solution to most frequently problem we meet in the usage of these tools. 

#### bcftools view 
bcftools view is the most frequent command to use for SNPs filtering, sample filtering, format changing. 
```
bcftools view -i '(IMP=1 & R2>0.6)|IMPUTED=0' chr$i.dose.dbSNP.hg19.vcf.gz |  bcftools annotate -x ^FORMAT/GT -Oz -o chr$i.dose.dbSNP.clean.hg19.vcf.gz

bcftools view -i \'R2\>0.6\|TYPED=1\|TYPED_ONLY=1\' -Oz chr$i.dose.vcf.gz -Oz -o chr$i.dose.filter.vcf.gz

```
#### bcftools annotation
```
bcftools annotate -a ~/hpc/db/hg19/dbSNP152/dbSNP152.chr$i.hg19.vcf.gz -c ID  chr$i.dose.contig.vcf.gz -Oz -o chr$i.dose.dbSNP.hg19.vcf.gz >>$i.job
```
### vcftools
```
vcf-sort -t ~/hpc/temp/ dbSNP152.chr1.hg19.vcf.gz | bgzip -c > dbSNP152.chr1.hg19.sort.vcf.gz
```

#### GATK
```
gatk CreateSequenceDictionary -R hg19.fa -O hg19.dict 
```
#### SnpSift 

#### Example 1. How to build vcf annotation database for bcftools annotate
```
# hg19 dbSNP
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz.md5
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz.tbi
# hg38 dbSNP
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/All_20180418.vcf.gz
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/All_20180418.vcf.gz.md5
wget ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/All_20180418.vcf.gz.tbi

# copy files from UW-Madison to MCRI

```
