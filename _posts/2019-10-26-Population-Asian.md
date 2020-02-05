---
layout: post
title: "Population Genetics in East Asian and Allele Frequency"
author: Shicheng Guo
date: 2019-10-26
categories: research
tags: East Asian Population MAF
image: images/2019-Shicheng-Guo-China-Asian-India.png	
---

Here, I want to summarize Population Genetics in East Asian and Allele Frequency. 


###  Aim and Background
* Z Du,2019, Genomics, Proteomics & Bioinformatics, [Whole Genome Analyses of Chinese Population and De Novo Assembly of A Northern Han Genome](https://www.ncbi.nlm.nih.gov/pubmed/31494266)
* S Liu,2018, Cell, [Genomic analyses from non-invasive prenatal testing reveal genetic associations, patterns of viral infections, and history in Chinese populations](https://www.ncbi.nlm.nih.gov/pubmed/30290141)
* H Bai,2018, Nature Genetics, [Whole-genome sequencing of 175 Mongolians uncovers population-specific genetic architecture and gene flow throughout North/East Asia](https://www.nature.com/articles/s41588-018-0250-5)


###  How to pre-process the plink data and association study (basic, not advanced)
```
cd ~/hpc/rheumatology/RA/RA500
#plink --file result_extract_forward --make-bed --out RA500
plink --bfile RA500 --mind 0.05 --make-bed --out RA2020-B1
plink --bfile RA2020-B1 --geno 0.1 --make-bed --out RA2020-B2
plink --bfile RA2020-B2 --maf 0.01 --make-bed --out RA2020-B3
plink --bfile RA2020-B3 --hwe 0.00001 --make-bed --out RA2020-B4
plink2 --bfile RA2020-B4 --king-cutoff 0.125
plink2 --bfile RA2020-B4 --remove plink2.king.cutoff.out.id --make-bed -out RA2020-B5
plink --bfile RA2020-B5 --check-sex
plink --bfile RA2020-B5 --impute-sex --make-bed --out RA2020-B6
plink --bfile RA2020-B6 --check-sex
grep PROBLEM plink.sexcheck | awk '{print $1,$2}' > sexcheck.remove
plink --bfile RA2020-B6 --remove sexcheck.remove --make-bed --out RA2020-B7
plink --bfile RA2020-B7 --test-missing midp 
awk '$5<0.000001{print}' plink.missing | awk '{print $2}' > missing.imblance.remove
plink --bfile RA2020-B7 --exclude missing.imblance.remove --make-bed --out RA2020-B8
plink --bfile RA2020-B8 --pca --threads 31
# perl phen.pl RA2020-B8.fam > RA2020-B8.fam.new
# mv RA2020-B8.fam.new RA2020-B8.fam
plink --bfile RA2020-B8 --logistic --covar plink.eigenvec --covar-number 1-5 --adjust
plink --bfile RA2020-B8 --assoc --adjust gc --threads 31  --ci 0.95 --out RA500
plink --bfile RA2020-B8 --assoc mperm=1000000 --adjust gc --threads 31
```

###  Prepare Population Specific Genoytping data based on 1000 Genome Phase 3 data
```
#############################################
cd ~/hpc/db/hg19/beagle
for i in {1..22} X Y
do
wget http://bochet.gcc.biostat.washington.edu/beagle/1000_Genomes_phase3_v5a/b37.vcf/chr$i.1kg.phase3.v5a.vcf.gz
done
wget http://bochet.gcc.biostat.washington.edu/beagle/genetic_maps/plink.GRCh37.map.zip
wget http://bochet.gcc.biostat.washington.edu/beagle/1000_Genomes_phase3_v5a/sample_info/20140625_related_individuals.txt
wget http://bochet.gcc.biostat.washington.edu/beagle/1000_Genomes_phase3_v5a/sample_info/integrated_call_male_samples_v3.20130502.ALL.panel
wget http://bochet.gcc.biostat.washington.edu/beagle/1000_Genomes_phase3_v5a/sample_info/integrated_call_samples.20130502.ALL.ped
wget http://bochet.gcc.biostat.washington.edu/beagle/1000_Genomes_phase3_v5a/sample_info/integrated_call_samples_v3.20130502.ALL.panel
mkdir EUR
mkdir EAS

grep EUR integrated_call_samples_v3.20130502.ALL.panel | awk '{print $1}'> EUR.List.txt
grep EAS integrated_call_samples_v3.20130502.ALL.panel | awk '{print $1}' > EAS.List.txt

mkdir temp
for i in {1..22} X Y
do
echo \#PBS -N $i  > $i.job
echo \#PBS -l nodes=1:ppn=1 >> $i.job
echo \#PBS -M Guo.shicheng\@marshfieldresearch.org >> $i.job
echo \#PBS -m abe  >> $i.job
echo \#PBS -o $(pwd)/temp/ >>$i.job
echo \#PBS -e $(pwd)/temp/ >>$i.job
echo cd $(pwd) >> $i.job
# echo tabix -p vcf chr$i.1kg.phase3.v5a.vcf.gz >> $i.job
# echo bcftools view chr$i.1kg.phase3.v5a.vcf.gz -S EUR.List.txt -Oz -o ./EUR/chr$i.1kg.phase3.v5a.EUR.vcf.gz >>$i.job
echo bcftools view chr$i.1kg.phase3.v5a.vcf.gz -S EAS.List.txt -Oz -o ./EAS/chr$i.1kg.phase3.v5a.EAS.vcf.gz >>$i.job
qsub $i.job
done
```


### How to prepare vcf files which can be submitted to michigan imputaiton server 
```
cd ~/hpc/rheumatology/RA/RA500
mkdir michigan
plink --bfile RA2020-B8 --list-duplicate-vars ids-only suppress-first
plink --bfile RA2020-B8 --alleleACGT --snps-only just-acgt --exclude plink.dupvar --make-bed --out RA2020-B9
cd michigan
mkdir temp
wget https://faculty.washington.edu/browning/conform-gt/conform-gt.24May16.cee.jar -O conform-gt.24May16.cee.jar
for i in {1..23} 
do
echo \#PBS -N $i  > $i.job
echo \#PBS -l nodes=1:ppn=12 >> $i.job
echo \#PBS -M Guo.shicheng\@marshfieldresearch.org >> $i.job
echo \#PBS -m abe  >> $i.job
echo \#PBS -o $(pwd)/temp/ >>$i.job
echo \#PBS -e $(pwd)/temp/ >>$i.job
echo cd $(pwd) >> $i.job
echo plink --bfile ../RA2020-B9 --chr $i --recode vcf-iid --out RA2020-B9.chr$i >> $i.job
echo bcftools view RA2020-B9.chr$i.vcf -Oz -o RA2020-B9.chr$i.vcf.gz >>$i.job
echo tabix -p vcf RA2020-B9.chr$i.vcf.gz >>$i.job
echo java -jar ./conform-gt.24May16.cee.jar gt=RA2020-B9.chr$i.vcf.gz match=POS chrom=$i ref=~/hpc/db/hg19/beagle/EAS/chr$i.1kg.phase3.v5a.EAS.vcf.gz  out=RA2020-B9.chr$i.beagle.vcf.gz  >>$i.job
echo tabix -p vcf RA2020-B9.chr$i.beagle.vcf.gz >>$i.job
qsub $i.job
done
```

###  Reference


Disclosure.
* All the opinions are my own and not the views of my employer
* All the blogs are my own and not the views of my employer
* All the opinions are my own and not the views of my employer
* All the contents are my own and should never be taken seriously
* All the contents are only used for help. reminding me if misleading happens
* All the figures are only used for non-profit education. reminding me if infrigement happens
