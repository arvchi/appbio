#! /usr/bin/env python

import sys
from Bio import SeqIO

trimmed_sequences = []
with open('/Users/arvin/Box Sync/Kurser/Applied.bioinformatics/Project/data/fastq/miseq1.fq', "rU") as fq:
    for record in SeqIO.parse(fq, "fastq"):
         # if record.letter_annotations["phred_quality"] ...
         # do something
         # trimmed_sequences.append(record)

SeqIO.write(trimmed_sequences, "trimmed_seqs.fasta", "fasta")  ## write to file
