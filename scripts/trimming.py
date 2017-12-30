#! /usr/bin/env python

import argparse
from Bio import SeqIO
import matplotlib.pyplot as plt
import numpy
import os
import sys

parser = argparse.ArgumentParser(description='takes fastq files as input, \
                                 trims reads, gives statistics and plots')
parser.add_argument('algorithm',
                    help='which algorithm to use, e.g. tr1 or tr2')
parser.add_argument('fastq_file',
                    help='path to fastq file, e.g. "miseq1.fq"')
parser.add_argument('output_dir',
                    help='Save plots to this directory, e.g. "./Results"')
args = parser.parse_args()

# Trim and Store
trimmed_sequences = []
with open(args.fastq_file, "rU") as fq:
    records = list(SeqIO.parse(fq, "fastq"))

# Control input file
if not records:
    sys.exit("Error: Empty file or wrong filetype. Script halted.")


# Get length and quality (for downstream statistics)
untrimmed_seq_lengths = []
untrimmed_seq_qualities = []
untrimmed_seq_tail_q = []
for record in records:
    untrimmed_seq_lengths.append(len(record.seq))
    untrimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])
    tail = len(record.seq) - 20
    untrimmed_seq_tail_q.extend(record.letter_annotations["phred_quality"][tail:])


# Do trimming with algorithm 1 or 2 depending on user input
if args.algorithm == "tr1":  # Algorithm 1
    trimmed = 0  # for keeping counts
    not_trimmed = 0  # for keeping counts
    short_sequences = 0  # for control
    for record in records:  # Parse through each accession
        if len(record.seq) < 30:
            short_sequences += 1  # Warning comes further down
            trimmed_sequences.append(record)  # store w/o trimming
        else:
            # Calculate threshold
            mean_quality = numpy.mean(
                record.letter_annotations["phred_quality"][0:30])
            std_quality = numpy.std(
                record.letter_annotations["phred_quality"][0:30])
            threshold = mean_quality - (1 * std_quality)
            for i in range(0, len(record.seq)):  # Iterate over each base
                # Check quality threshold and trim
                if numpy.mean(
                     record.letter_annotations["phred_quality"][i:]
                     ) < threshold:
                    trimmed_sequences.append(record[0:i])  # up to i:th base
                    trimmed += 1
                    break  # stop the loop
                elif i == (len(record.seq)-1):  # If end of sequence
                    trimmed_sequences.append(record)  # keep whole record
                    not_trimmed += 1
elif args.algorithm == "tr2":  # Algorithm 2
    trimmed = 0  # for keeping counts
    not_trimmed = 0  # for keeping counts
    short_sequences = 0  # for control
    for record in records:  # Parse through each accession
        if len(record.seq) < 30:
            short_sequences += 1  # Warning comes further down
            trimmed_sequences.append(record)  # store w/o trimming
        else:
            # Calculate metrics
            mean_quality = numpy.mean(
                record.letter_annotations["phred_quality"][0:50])
            std_quality = numpy.std(
                record.letter_annotations["phred_quality"][0:50])
            threshold = mean_quality - (1 * std_quality)
            for i in range(len(record.seq)-20, len(record.seq)):  # start from the last 20 bases
                # Check quality threshold and trim
                if numpy.mean(
                     record.letter_annotations["phred_quality"][i:]
                     ) < threshold:
                    trimmed_sequences.append(record[0:i])  # up to i:th base
                    trimmed += 1
                    break  # stop the loop
                elif i == (len(record.seq)-1):  # If end of sequence
                    trimmed_sequences.append(record)  # keep whole record
                    not_trimmed += 1

# Warnings
if short_sequences > 0:
    print("Warning, ", short_sequences,
          "sequences were less than 30 bp and not trimmed")

# Write to file
file_name = "trimmed_seqs.fastq"
SeqIO.write(trimmed_sequences, os.path.join(args.output_dir, file_name),
            "fastq")

# Get statistics after trimming
trimmed_seq_lengths = []
trimmed_seq_qualities = []
trimmed_seq_tail_q = []
for record in trimmed_sequences:
    trimmed_seq_lengths.append(len(record.seq))
    trimmed_seq_qualities.extend(record.letter_annotations["phred_quality"])
    tail = len(record.seq) - 20
    trimmed_seq_tail_q.extend(record.letter_annotations["phred_quality"][tail:])
    # I use extend instead of append because ojbect is already list

# Statistical output
print("Nr of seqs trimmed:", trimmed)
print("Nr of seqs not_trimmed:", not_trimmed+short_sequences)
print("Mean seq length before trimming:", numpy.mean(untrimmed_seq_lengths))
print("Mean quality before trimming:", numpy.mean(untrimmed_seq_qualities))
print("Mean quality of tail before trimming:", numpy.mean(untrimmed_seq_tail_q))
if trimmed:  # if there are any trimmed reads
    print("Mean seq length after trimming:", numpy.mean(trimmed_seq_lengths))
    print("Mean quality after trimming:", numpy.mean(trimmed_seq_qualities))
    print("Mean quality of tail after trimming:", numpy.mean(trimmed_seq_tail_q))
else:
    print("Mean seq length after trimming: N/A. No reads trimmed")



# Plots
if trimmed:
    plt.figure(1)
    plt.hist(untrimmed_seq_lengths,
             alpha=0.5,
             label="untrimmed",
             color="blue")
    plt.hist(trimmed_seq_lengths,
             alpha=0.5,
             label="trimmed",
             color="green")
    plt.legend(loc='upper right')
    plt.title("Seq length histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    file_name = "seqlength.pdf"
    plt.savefig(os.path.join(args.output_dir, file_name))  # save to output_dir

    plt.figure(2)
    plt.hist(untrimmed_seq_qualities,
             alpha=0.5,
             label="untrimmed",
             color="blue")
    plt.hist(trimmed_seq_qualities,
             alpha=0.5,
             label="trimmed",
             color="green")
    plt.legend(loc='upper right')
    plt.title("Seq quality histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    file_name = "seqquality.pdf"
    plt.savefig(os.path.join(args.output_dir, file_name))  # save to output_dir
    print("Plots saved in specified directory")
else:
    print("No plots were produced, as no reads were trimmed")
