
---
title: "Genome-wide multiple bedgraph data analysis with Intervene"
author: Shicheng Guo
date: 2017-09-30
categories: bioinformatics
tags: intervene bedgraph bedtools macs2
image: images/Shicheng-Guo-Intervene_plots.png

---

Today, I will give a talk about how to do multiple bedgraph data analysis with Intervene for ChIP-seq or MBD-seq data with [Intervene](https://intervene.readthedocs.io/en/latest/introduction.html). Intervene is a tool for intersection and visualization of multiple genomic region and gene sets (or lists of items). Intervene provides an easy and automated interface for effective intersection and visualization of genomic region sets or lists of items, thus facilitating their analysis and interpretations.

```
conda install -c bioconda intervene

for i in 2019032901 2019032903 2019040901 2019051703 2019052301 2019053101 2019053102
do
intervene venn -i /gpfs/home/guosa/hpc/methylation/pancrease/medip/venn/$i*.bed --project $i
done
```
Here, you can find the venn diagrams which are quite fancy. We can prepare venn for each sample. 
