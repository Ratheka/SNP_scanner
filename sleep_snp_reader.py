# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 09:17:07 2019

sleep_snp_reader.py - compares a list of genes that have research supporting
an effect on sleep with a CSV of a human's DNA, listing out the relevant pairs
in a third file, with empty lines for absent genes.

@author: ratheka
"""
import csv
import re

with open("./sleep_relevant_snps.txt", "r") as sleep_genes:
    relevant_snp_list = sleep_genes.readlines()
 
relevant_snp_list = [str(snp[:-1]).lower() for snp in relevant_snp_list]

relevant_snp_set = set(relevant_snp_list)
gene_file = input("What is the gene file to read?")

with open(gene_file, 'r') as f:
  reader = csv.reader(f)
  your_gene_list = list(reader)


your_gene_dict = {}
rsid_regex = re.compile(r'(r)(s)\d+')
base_pair_regex = re.compile(r'[A|T|C|G|D|I|-]+')


for line in your_gene_list:

    line_str = str(line)
    if '#' in line_str:
        continue
    if 'RSID' in line_str:
        continue
    rsid_result = rsid_regex.search(line_str)
    if rsid_result:
        rsid_base_pair = base_pair_regex.search(line_str)
        if not rsid_base_pair:
            print(rsid_result.group())
        your_gene_dict[rsid_result.group()] = rsid_base_pair.group()

gene_keyset = set(your_gene_dict.keys())
your_sleep_geneset = gene_keyset.intersection(relevant_snp_set)
gene_announce_base = "Found a relevant gene!  It's {}, which you have in the form: {}"
with open('sleep_genes.txt', 'w') as genefile:
    for gene in your_sleep_geneset:
        gene_announce_line = (gene_announce_base.format(gene, your_gene_dict[gene]))
        print(gene_announce_line)                      
        genefile.write(gene + '\t' + your_gene_dict[gene] + '\n')

    