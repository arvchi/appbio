# 2017-12-15 Set directories and download data
* Set up dirs and README.
* git init.
* download data, store in /data/fastq/
* unzip compressed fastq files:

```sh
gunzip *
```

# 2017-12-15 Create program file and draft outline
* see trimming.py.

# 2017-12-24 Add statistics and plots
* See trimming.py.
* Script now returns some general statistics and histograms, can be used to test effects of algorithm on test data (miseq1).

# 2017-12-27 Re-shape the program - iterate twice
* Originally, I intended to parse through the fastq file once and do the trimming instantly. However, I now want to iterate once first to get some statistics, i.e. mean and sd, which I will use for the subsequent trimming (trimming will require additional iteration). Therefore, I decided to store all records in a list first, and then iterate over the list as many times as necessary.

# 2017-12-27 Algorithm 1
* Takes the 30 first calls and calculates the mean and sd.
* Why 30? Should be enough calls to give an accurate representation of the quality, before the technical quality decline have started.
* Algorithm 1 iterates over each base and checks the mean of the remaining bases from i and onwards. If the mean is lower than 1 standard devation from the mean of the first 50 bases, the sequence will be cut at that point.
* Why 1 standard deviation? Played around with this on the test data, and settled on 1 sd as a cutoff between improving quality and losing sequences. Obviously test data doesn't necessarily reflect all other data out there, so that's a deficiency in the calibration method I am using.

# 2017-12-27 Evaluation of algorithm 1 on test and real data

## Miseq1
Nr of seqs trimmed: 19
Nr of seqs not_trimmed: 6
Mean seq length before trimming: 245.8
Mean seq length after trimming: 206.12
Mean quality before trimming: 17.1938161107
Mean quality after trimming: 17.8461090627

## Miseq2
Nr of seqs trimmed: 104960
Nr of seqs not_trimmed: 145040
Mean seq length before trimming: 168.813372
Mean seq length after trimming: 148.828088
Mean quality before trimming: 29.3656623126
Mean quality after trimming: 29.9118627124

# 2017-12-27 Improve speed?
* The program takes some time when run on the large file.
* One way to make faster is to put the second and third (statistics) iterations together.
* This would improve speed, but make the script more difficult to understand.
* For now, I choose to not improve speed.

# 2017-12-27 Added argparse to simplify program usage
* See script.

# 2017-12-27 Algorithm 2
* One disadvantage with the previous method is that all bases will be cut once the mean of the remaining bases is below the threshold, however, many of those bases that were cut could be even before the base call quality actually drops.
* Maybe it's better to look at 5-10 consecutive bases (i.e. i, i+1, i+n ... instead of i:), and cut the sequence when all consecutive bases fall below a certain threshold.

# 2017-12-28 Evaluation of Algorithm 2

## Miseq1
Nr of seqs trimmed: 12
Nr of seqs not_trimmed: 13
Mean seq length before trimming: 245.8
Mean quality before trimming: 17.1938161107
Mean seq length after trimming: 222.36
Mean quality after trimming: 17.6422018349

## Miseq2
Nr of seqs trimmed: 34877
Nr of seqs not_trimmed: 215123
Mean seq length before trimming: 168.813372
Mean quality before trimming: 29.3656623126
Mean seq length after trimming: 157.109984
Mean quality after trimming: 29.9810005709


# 2017-12-30 Adding some statistics
* My algorithms don't have a big impact on overall quality, but in fact, only the tails of the reads should be improved, this may or may not be reflected by the mean base call quality over the whole read.
* Therefore, my program now also reports the quality of the 20 last bases, before and after trimming.

## tr1 on miseq2
Mean quality of tail before trimming: 28.5856804
Mean quality of tail after trimming: 30.3682810509
## tr2 on miseq2
Mean quality of tail before trimming: 28.5856804
Mean quality of tail after trimming: 29.1001448445

# 2018-01-01 Adding controls
* Empty file will produce warning. Tested and works.
* Fasta file as input (instead of fastq) will give same error message. Tested and works.
* File with short sequences: Short seqs will not be trimmed (but stored as is). Warning will be written to stdout. Tested and works.
* Unambigious nucletoides are not considered. Going through each base and check it would make program less efficient, and not really the purpose either. Include in discussion.
