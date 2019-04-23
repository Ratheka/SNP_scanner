# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:55:37 2019

snp_scanner.py - reads a user-defined raw genome file from [myheritage, 23andme]
and compares the user's snps with a set of lists kept with the script and originally obtained from SNPedia / the polyphasic community

@author: ratheka
"""

import csv
import os
import re

class SNP_Scanner:


    def __init__(self):

        self.dict_of_known_snps = {}
        self.user_gene_data_list = []
        self.user_gene_data = {}
        self.snp_file_regex = re.compile(r'((\w+)_related_snps.txt)')
        self.file_name = ""
        self.user_results = {}

        for file in os.listdir('./'):
            file_check = self.snp_file_regex.search(file)
            if file_check:
                with open(file_check.group(0), 'r') as opened_file:
                    self.dict_of_known_snps[file_check.group(2)] = opened_file.readlines()

        for key in self.dict_of_known_snps.keys():
            for snp_list_entry in self.dict_of_known_snps[key]:
                if snp_list_entry == None:
                    self.dict_of_known_snps[key].remove(snp_list_entry)
                    continue #Can't guarantee the input files are clean


    def read_user(self):
        while True:
            filename = input('What is the filename of the genetic data to read?')
            if not os.path.isfile(filename):
                print('I\'m sorry, but I can\'t seem to locate {}.'.format(filename))
                continue
            else:
                self.file_name = filename
                break

        with open(filename, 'r') as opened_user_data_file:
            reader = csv.reader(opened_user_data_file)
            self.user_gene_data_list = list(reader)
        return

    def prepare_data(self):

        rsid_regex = re.compile(r'(?i)((r|g)(s)|i)\d+')
        base_pair_regex = re.compile(r'(?i)[^\\][A|T|C|G|D|I|-]+')

        for line in self.user_gene_data_list:
            line_str = str(line).lower()
            line_str = line_str.replace(r"\t", " ")
            if '#' in line_str:
                continue
            if 'RSID' in line_str:
                continue
            rsid_result = rsid_regex.search(line_str)
            if rsid_result:
                rsid_base_pair = base_pair_regex.search(line_str)
                self.user_gene_data[rsid_result.group()] = rsid_base_pair.group()

        for key in self.dict_of_known_snps:
            for i in range(len(self.dict_of_known_snps[key])):
                self.dict_of_known_snps[key][i] = self.dict_of_known_snps[key][i].lower().rstrip()
        return

    def scan_genes(self):
        user_rsids_set = set(self.user_gene_data.keys())

        for key in self.dict_of_known_snps.keys():
            snp_set = set(self.dict_of_known_snps[key])
            self.user_results[key] = list(snp_set.intersection(user_rsids_set))
        return

    def issue_reports(self):
        for key in self.user_results.keys():
            with open(self.file_name + '_' + str(key) + '_results.txt', 'w') as f:
                for snp_list in self.user_results.values():
                    for snp in snp_list:
                        f.write(snp + '\t' + self.user_gene_data[snp] + '\n')

def main():
    scanner = SNP_Scanner()
    scanner.read_user()
    scanner.prepare_data()
    scanner.scan_genes()
    scanner.issue_reports()


main()
