#! /usr/bin/env python

import sys
from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy

# Trim and Store
trimmed_sequences = []

with open('/Users/arvin/Box Sync/Kurser/2017_Applied.bioinformatics/Project/data/fastq/miseq1.fq', "rU") as fq:
    records = list(SeqIO.parse(fq, "fastq"))

# Get statistics
untrimmed_seq_lengths = []
untrimmed_seq_qualities = []
for record in records:
    untrimmed_seq_lengths.append(len(record.seq))
    untrimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])

# Create quality threshold
threshold = numpy.mean(untrimmed_seq_qualities) - numpy.std(untrimmed_seq_qualities)

# Do trimming
for record in records:  # Parse through each accession
    for i in range(0, len(record.seq)):  # Create iterator over each base call
        if numpy.mean(record.letter_annotations["phred_quality"][i:]) < threshold or i == (len(record.seq)-1):
            # If condition is met OR end of sequence
            # import pdb; pdb.set_trace()
            trimmed_sequences.append(record[0:i])
            break  # stop the loop
import pdb; pdb.set_trace()

SeqIO.write(trimmed_sequences, "trimmed_seqs.fasta", "fasta")  ## write to file

# Get statistics after trimming
trimmed_seq_lengths = []
trimmed_seq_qualities = []
for record in trimmed_sequences:
    trimmed_seq_lengths.append(len(record.seq))
    trimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])
    # I use extend instead of append because ojbect is already list

# Statistics
print("untrimmed mean seq length;", numpy.mean(untrimmed_seq_lengths))
print("trimmed mean seq length:", numpy.mean(trimmed_seq_lengths))
print("untrimmed mean quality:", numpy.mean(untrimmed_seq_qualities))
print("trimmed mean quality:", numpy.mean(trimmed_seq_qualities))
#print("max quality:", (max(seq_qualities)))
#print("min quality:", (min(seq_qualities)))

# Plots
plt.figure(1)
plt.hist(untrimmed_seq_lengths)
plt.title("Untrimmed Seq length histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/untrimmed_seqlength.pdf")

plt.figure(2)
plt.hist(untrimmed_seq_qualities)
plt.title("Untrimmed Seq quality histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/untrimmed_seqquality.pdf")

plt.figure(3)
plt.hist(trimmed_seq_lengths)
plt.title("Trimmed Seq length histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/trimmed_seqlength.pdf")

plt.figure(4)
plt.hist(trimmed_seq_qualities)
plt.title("Trimmed Seq quality histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.savefig("../results/trimmed_seqquality.pdf")
