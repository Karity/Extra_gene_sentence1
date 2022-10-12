import os
import csv
import pandas as pd


relation_file = 'file_base.tsv'
# with open(relation_file, 'r', encoding='UTF-8') as file:
#     print(file)


file = pd.read_csv(relation_file, sep='\t', index_col=['PMID', 'sentence', 'label'])
print(len(file))
print(type(file))
print(type(file.iloc[1].name))
print(file)
print(file.iloc[0].name[0])
for i in range(len(file)):
    print(file.iloc[i].name)

