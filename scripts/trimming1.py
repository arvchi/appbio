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
    for record in SeqIO.parse(fq, "fastq"):  # Parse through each accession
        for i in range(0, len(record.seq)):  # Create iterator over each base call
            if numpy.mean(record.letter_annotations["phred_quality"][i:]) < 14 or i == len(record.seq):
                import pdb; pdb.set_trace()
                trimmed_sequences.append(record[0:i])
                break  # stop the loop

SeqIO.write(trimmed_sequences, "trimmed_seqs.fasta", "fasta")  ## write to file

        seq_lengths.append(len(record.seq))
        seq_qualities.extend(record.letter_annotations["phred_quality"])
        # I use extend instead of append because ojbect is already list


SeqIO.write(trimmed_sequences, "trimmed_seqs.fasta", "fasta")  ## write to file

# Statistics
print(numpy.mean(seq_lengths))
print(numpy.mean(seq_qualities))
print("max quality:", (max(seq_qualities)))
print("min quality:", (min(seq_qualities)))
numpy.std(seq_qualities)

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
