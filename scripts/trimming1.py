#! /usr/bin/env python

import argparse
from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy
import os

dir="yeah/brah"
file_name = "test.pdf"
os.path.join(dir, file_name)

parser = argparse.ArgumentParser(description='takes fastq files as input, \
                                 trims reads, gives statistics and plots')
parser.add_argument('fastq_file',
                    help='path to fastq file, e.g. "miseq1.fq"')
parser.add_argument('output_dir',
                    help='Save plots to this directory, e.g. "./Results"')
args = parser.parse_args()

# Trim and Store
trimmed_sequences = []
with open(args.fastq_file, "rU") as fq:
    records = list(SeqIO.parse(fq, "fastq"))

# Get length and quality
untrimmed_seq_lengths = []
untrimmed_seq_qualities = []
for record in records:
    untrimmed_seq_lengths.append(len(record.seq))
    untrimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])

# Create quality threshold
threshold = numpy.mean(untrimmed_seq_qualities) - (numpy.std(untrimmed_seq_qualities)*0.5)

# Do trimming
trimmed = 0  # for keeping counts
not_trimmed = 0  # for keeping counts
for record in records:  # Parse through each accession
    for i in range(0, len(record.seq)):  # Create iterator over each base call
        if numpy.mean(record.letter_annotations["phred_quality"][i:]) < threshold:
            # If condition is met
            # import pdb; pdb.set_trace()
            trimmed_sequences.append(record[0:i])
            trimmed += 1
            break  # stop the loop
        elif i == (len(record.seq)-1):  # If end of sequence
            trimmed_sequences.append(record[0:i])
            not_trimmed += 1


# Get statistics after trimming
trimmed_seq_lengths = []
trimmed_seq_qualities = []
for record in trimmed_sequences:
    trimmed_seq_lengths.append(len(record.seq))
    trimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])
    # I use extend instead of append because ojbect is already list

# Statistical output
print("Nr of seqs trimmed:", trimmed)
print("Nr of seqs not_trimmed:", not_trimmed)
print("Mean seq length before trimming:", numpy.mean(untrimmed_seq_lengths))
print("Mean seq length after trimming:", numpy.mean(trimmed_seq_lengths))
print("Mean quality before trimming:", numpy.mean(untrimmed_seq_qualities))
print("Mean quality after trimming:", numpy.mean(trimmed_seq_qualities))
#print("max quality:", (max(seq_qualities)))
#print("min quality:", (min(seq_qualities)))

# Plots
plt.figure(1)
plt.hist(untrimmed_seq_lengths, alpha=0.5, label="untrimmed", color="blue")
plt.hist(trimmed_seq_lengths, alpha=0.5, label="trimmed", color="green")
plt.legend(loc='upper right')
plt.title("Seq length histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")

file_name = "seqlength.pdf"
plt.savefig(os.path.join(args.output_dir, file_name))  # save to specified dir
print ("Plot seqlength.pdf saved")

plt.figure(2)
plt.hist(untrimmed_seq_qualities, alpha=0.5, label="untrimmed", color="blue")
plt.hist(trimmed_seq_qualities, alpha=0.5, label="trimmed", color="green" )
plt.title("Seq quality histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
file_name = "seqquality.pdf"
plt.savefig(os.path.join(args.output_dir, file_name))  # save to specified dir
print ("Plot seqquality.pdf saved")

file_name = "trimmed_seqs.fastq"
SeqIO.write(trimmed_sequences, os.path.join(args.output_dir, file_name), "fastq")  ## write to file
