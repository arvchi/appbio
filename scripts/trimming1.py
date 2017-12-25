#! /usr/bin/env python

import sys
from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy

# Trim and Store
trimmed_sequences = []
seq_lengths = []
seq_qualities = []
with open('/Users/arvin/Box Sync/Kurser/2017_Applied.bioinformatics/Project/data/fastq/miseq1.fq', "rU") as fq:
    for record in SeqIO.parse(fq, "fastq"):
         # if record.letter_annotations["phred_quality"] ...
         # do something
         trimmed_sequences.append(record)
         seq_lengths.append(len(record.seq))
         seq_qualities.extend(record.letter_annotations["phred_quality"])
         # I use extend instead of append because ojbect is already list

# import pdb; pdb.set_trace()

SeqIO.write(trimmed_sequences, "trimmed_seqs.fasta", "fasta")  ## write to file

# Statistics
numpy.mean(seq_lengths)
numpy.mean(seq_qualities)
max(seq_qualities)

# Plot Length
plt.figure(1)
plt.hist(seq_lengths)
plt.title("Seq length histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/seqlength.pdf")

# Plot Quality
plt.figure(2)
plt.hist(seq_qualities)
plt.title("Seq quality histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/seqquality.pdf")
