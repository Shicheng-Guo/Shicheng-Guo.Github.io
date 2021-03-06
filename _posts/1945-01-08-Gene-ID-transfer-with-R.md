---
layout: post
title: "Gene ID Transfer with R between Symbol, Gene ID and KEGG ID"
author: Shicheng Guo
date: 1945-01-08
categories: research
tags: GeneID Symbol KEGG ID

---

* Transfer between Gene ID and Gene Symbol:

```
library("org.Hs.eg.db")
symbol <- as.list(org.Hs.egALIAS2EG)
symbol2geneid<-data.frame(names(symbol),as.character(symbol))
```
* Transfer between ENSG and ENST with Gene Symbol
```
library("org.Hs.eg.db")
symbol <- as.list(org.Hs.egALIAS2EG)
symbol2geneid<-data.frame(names(symbol),as.character(symbol))
```

* Transfer between ENSG and ENST with Gene ID
```
library("org.Hs.eg.db")
symbol <- as.list(org.Hs.egALIAS2EG)
symbol2geneid<-data.frame(names(symbol),as.character(symbol))
```

* Transfer between ENSG and ENST with KEGG ID
```
library("org.Hs.eg.db")
symbol <- as.list(org.Hs.egALIAS2EG)
symbol2geneid<-data.frame(names(symbol),as.character(symbol))
```

* Transfer between ENSG and ENST with KEGG ID
```
library("org.Hs.eg.db")
symbol <- as.list(org.Hs.egALIAS2EG)
symbol2geneid<-data.frame(names(symbol),as.character(symbol))
```

Disclosure.
* All the opinions are my own and not the views of my employer
* All the blogs are my own and not the views of my employer
* All the opinions are my own and not the views of my employer
* All the contents are my own and should never be taken seriously
* All the contents are only used for help. reminding me if misleading happens
* All the figures are only used for non-profit education. reminding me if infrigement happens
