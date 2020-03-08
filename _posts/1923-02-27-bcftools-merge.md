---
layout: post
title: "How to merge 7000 VCF files with bcftools merge?"
author: Shicheng Guo
date: 1923-02-28
categories: bioinformatics
tags: Genetics Genomics bcftools merge  
---

Sometimes, maybe you want to merge >7000 vcf files/samples into one big VCF file with `bcftools merge`, for example PMRP have 20,000 samples/vcf files:
```
bcftools merge -l merge.txt -Oz -o merge.vcf.gz
```
if the sample counts <1021, everything is okay. However, if it is >= 1021, bcftools merge will reports:
```
[E::hts_idx_load3] Could not load local index file '229209.fstl1.vcf.gz.tbi'
Failed to open 229209.fstl1.vcf.gz: could not load index
```
Okay. Here is my final solution developed based on WouterDeCoste's post. I hope it is helpful. One of my friends told me his computer allowed merging 7000 VCF at one time. I am not sure whether it is caused by a specific file operating setting.
```
ls *.vcf.gz | split -l 500 - subset_vcfs

for i in subset_vcfs*; 
do 
bcftools merge -0 -l $i -Oz -o merge.$i.vcf.gz; 
tabix -p vcf merge.$i.vcf.gz
done

ls merge.*.vcf.gz > merge.txt
bcftools merge -l merge.txt -0 -Oz -o all_merged.vcf.gz
bcftools annotate -x INFO,^FORMAT/GT all_merged.vcf.gz -Oz -o Final.vcf.gz
```
-0 is to set missing to reference


Another example I want to share as the following: Project Exome-sequencing:


1, rename WP files to -a files
```
use strict;
my @file=glob("WP_*.gz");
foreach my $file(@file){
my(undef,$id,undef)=split/_/,$file;
print "$file\t$id\n";
system("cp $file $id-a.filtered.vcf.gz")
}
```

2, the file name is not exactly same with sample id for the vcf. What's more, vcfs are from to project
```
rm sample.txt
for i in `ls *.vcf.gz`
do
echo $i
#bcftools index -f -t $i
bcftools query -l $i >> sample.txt
done
```

3, sampleid is too long, rename the sample id
```
use strict;
use Cwd;
chdir getcwd;
my $file="sample.txt";
open F, $file || die "cannot open $file\n";
while(<F>){
chomp;
my $file=$_;
my($id,undef)=split/.filtered.vcf.gz/,$file;
if($id =~/-a/){
my ($name,undef)=split/-/,$id;
print "$id $name\n";
}else{
my (undef,$name,undef)=split/_/,$id;
print "$id $name\n";
}
}
```
4, sometimes, the computer have limited `ulimit` setting, you cannot merge too many samples at the same time. Here, I showed the solution to merge every 200 files and finally we will merge 7000 samples.
```
ls *.vcf.gz | split -l 200 - subset_vcfs

for i in subset_vcfs*; 
do 
echo $i
bcftools merge -0 -l $i -Oz -o merge.$i.vcf.gz; 
tabix -p vcf merge.$i.vcf.gz
done

ls merge.*.vcf.gz > merge.txt
bcftools merge -l merge.txt -0 -Oz -o all_merged.vcf.gz
bcftools annotate -x INFO,^FORMAT/GT all_merged.vcf.gz -Oz -o Final.vcf.gz
```



