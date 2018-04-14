# ImmunoRepertoire
Antibody repertoire analysis pipeline
fastq -> fasta -> igblast align -> extract CDR3/variable seq/V segment sequences

## Requirements

### 1.PEAR: a fast and accurate Illumina Paired-End reAd mergeR

Zhang et al (2014) Bioinformatics 30(5): 614-620 | doi:10.1093/bioinformatics/btt593

You can get it from [PEAR](https://sco.h-its.org/exelixis/web/software/pear/)


### 2.Stand-alone IgBLAST: A tool for immunoglobulin (IG) and T cell receptor (TR) V domain sequences

IgBLAST was developed at NCBI to facilitate analysis of immunoglobulin variable domain sequences (IgBLAST has recently been extended to perform analysis for T cell receptor (TR) sequences). It uses BLAST search algorithm.

You can get it from [Standalone IgBLAST](ftp://ftp.ncbi.nih.gov/blast/executables/igblast/release/)

Additionally, you should down the file ***edit_imgt_file.pl***, director ***internal_data, optional_file***.

### 3.CD-HIT: 

it is a very widely used program for clustering and comparing protein or nucleotide sequences.

You can get it from [CD-HIT](https://github.com/weizhongli/cdhit/releases)


### 3.IMGT Germline sequence

This project, we get Immuno Germline sequence F+ORF+in-frame P sections from [IMGT](http://www.imgt.org/vquest/refseqh.html), and makes it standardized by **edit_imgt_file.pl**.

Refer to python3 module *changeo*

## Pipeline

### Merge paired-end fastq and change ID

python MergeSplit.py /path/to/fastq

### IgBLAST run wrap

sh IgBLAST4HumanBCR.sh in.fasta

### Parse IgBLAST result

python ParseIgBLAST.py -f in.fasta -i igblast_result -o outname
