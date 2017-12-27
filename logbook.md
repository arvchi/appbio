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
* Break after the quality has been under x SD in two consecutive calls?
* Break when the remaining bases have low wuality (i.e. under x SD of mean)?
* I have created a framework for this in the script, but don't understand how to trim the bases from the records.

# 2017-12-27 Re-shape the program - iterate twice
* Originally, I intended to parse through the fastq file once and do the trimming instantly. However, I now want to iterate once first to get some statistics, i.e. mean and sd, which I will use for the subsequent trimming (trimming will require additional iteration). Therefore, I decided to store all records in a list first, and then iterate over the list as many times as necessary.
