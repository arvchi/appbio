# 2017-12-15 Set dirs and download data
* Set up dirs and README.
* git init.
* download data, store in /data/fastq/
* unzip compressed fastq files:

```sh
gunzip *
```

# 2017-12-15 Create program file and draft outline
* see trimming1.py.

# 2017-12-24 Add statistics and plots
* See trimming1.py.
* Script now returns some general statistics and histograms, can be used to test effects of algorithm.

# 2017-12-25 Ideas for algorithm
* Break after the quality has been under 1 SD in two consecutive calls?
* Break when the remaining bases have low quality (i.e. under x SD of mean)?

# 2017-12-27 Re-shape the program - iterate twice
* Originally, I intended to parse through the fastq file once and do the trimming instantly. However, I now want to iterate once first to get some statistics, i.e. mean and sd, which I will use for the subsequent trimming (trimming will require additional iteration). Therefore, I decided to store all records in a list first, and then iterate over the list as many times as necessary.

# 2017-12-27 Evaluation of first algorithm on test and real data
* My impression is that the current algorithm trims many reads but improves quality only marginally.

## Miseq1
Nr of seqs trimmed: 22
Nr of seqs not_trimmed: 3
Mean seq length before trimming: 245.8
Mean seq length after trimming: 176.48
Mean quality before trimming: 17.1938161107
Mean quality after trimming: 18.2554397099

## Miseq2
Nr of seqs trimmed: 121838
Nr of seqs not_trimmed: 128162
Mean seq length before trimming: 168.813372
Mean seq length after trimming: 101.328744
Mean quality before trimming: 29.3656623126
Mean quality after trimming: 34.9965331061

# 2017-12-27 Improve speed TO-DO
* Remove one iteration (baked it in previous iteration) to make program faster.

# 2017-12-27 Use argparse to simplify usage
