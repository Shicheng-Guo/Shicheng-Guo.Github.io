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
# collect gene regions. don't forget to extend regions with -5K to +5K to region regions to cover promoter and enhancer SNPs
awk '{print $1,$2-5000,$3+5000,$4}' OFS="\t"  MUC.hg19.bed | bedtools sort -i > MUC.hg19.sort.bed

bcftools annotate -a ~/hpc/db/hg19/dbSNP152/dbSNP152.chr$i.hg19.vcf.gz -c ID  chr$i.dose.contig.vcf.gz -Oz -o chr$i.dose.dbSNP.hg19.vcf.gz >>$i.job

# merge MUC genotypes from chr1 to chr22
cd /gpfs/home/guosa/hpc/rheumatology/RA/he2020/impute/R3
ls chr*.dose.MUC.clean.hg19.vcf.gz > MUC.vcf.txt
bcftools concat -f MUC.vcf.txt -Oz -o MUC.hg19.vcf.gz
bcftools annotate -a ~/hpc/db/hg19/dbSNP152/dbSNP152.chr$i.hg19.vcf.gz -c ID  chr$i.dose.contig.vcf.gz -Oz -o MUC.hg19.vcf.gz

# https://github.com/Shicheng-Guo/AnnotationDatabase/blob/master/hg19/refGene.hg19.VCF.sort.bed.gz
# https://github.com/Shicheng-Guo/AnnotationDatabase/blob/master/hg19/refGene.hg19.VCF.sort.bed.gz.tbi

bcftools annotate -a ~/hpc/db/hg19/refGene.hg19.VCF.sort.bed.gz -c CHROM,FROM,TO,GENE -h <(echo '##INFO=<ID=GENE,Number=1,Type=String,Description="Gene name">') MUC.hg19.vcf.gz -Oz -o MUC.anno.hg19.vcf.gz

# review dbSNPs from vcf.gz file
bcftools view -i '%iD=="rs35705950"' MUC.anno.hg19.vcf.gz | less -S 
bcftools view -i '%iD=="rs79920422"' MUC.anno.hg19.vcf.gz | less -S 


```
### vcftools
```
zcat dbSNP152.chr1.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr1.hg19.sort.vcf.gz &
zcat dbSNP152.chr7.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr7.hg19.sort.vcf.gz &
zcat dbSNP152.chr8.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr8.hg19.sort.vcf.gz &
zcat dbSNP152.chr9.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr9.hg19.sort.vcf.gz &
```

#### GATK
Some of my colleagues meet lots of GATK bugs. Please be sure GATK requires `Java 1.8` other Java will have some unexpected errors. On the other side, please download the database from [GATK Resource Bundle ftp server](https://software.broadinstitute.org/gatk/download/bundle) rather than other database. 
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
scp nu_guos@submit-1.chtc.wisc.edu:/home/nu_guos/All_20180423* ~/hpc/db/hg19/dbSNP

# split with chrosome name

# SNP orders are not correct, sort chr1,chr7,chr8,chr9
mkdir ./temp/chr1/
mkdir ./temp/chr7/
mkdir ./temp/chr8/
mkdir ./temp/chr9/
zcat dbSNP152.chr1.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr1.hg19.sort.vcf.gz &
zcat dbSNP152.chr7.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/ | bgzip -c > dbSNP152.chr7.hg19.sort.vcf.gz &
zcat dbSNP152.chr8.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/chr8 | bgzip -c > dbSNP152.chr8.hg19.sort.vcf.gz &
zcat dbSNP152.chr9.hg19.vcf.gz | vcf-sort -p 16 -t ./temp/chr9 | bgzip -c > dbSNP152.chr9.hg19.sort.vcf.gz &
mv dbSNP152.chr8.hg19.sort.vcf.gz dbSNP152.chr8.hg19.sort.vcf.gz
mv dbSNP152.chr9.hg19.sort.vcf.gz dbSNP152.chr9.hg19.sort.vcf.gz
tabix -p vcf dbSNP152.chr8.hg19.sort.vcf.gz &
tabix -p vcf dbSNP152.chr9.hg19.sort.vcf.gz &
```

#### Footnote:

* human refGene hg19 TSS: https://raw.githubusercontent.com/Shicheng-Guo/AnnotationDatabase/master/hg19/refGene_hg19_TSS.bed
* human refGene hg38 TSS: https://raw.githubusercontent.com/Shicheng-Guo/AnnotationDatabase/master/hg38/refGene.hg38.TSS.bed
