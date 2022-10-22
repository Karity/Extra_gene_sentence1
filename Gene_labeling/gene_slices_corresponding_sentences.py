# 获得gene slices对应的句子
# from_pdf_get_gene_name.py
# gene_name2slices.py

import os
import pandas as pd
import csv

sentences_path = 'occur_gene_name_sentences.csv'
gene_slices_path = '../abc'
# gene_slices_path = '../test'


def change_str2list(string: str, replace_list: list) -> list:  # str: ['ERK', 'EGFR', 'MEK'] -> list: ['ERK', 'EGFR', 'MEK']  (replace_list: ['[', ']', '\''])
    replace_list.append(' ')  # 添加一个空格 因为在str中两个用逗号分割的词之间有一个空格
    for chr in replace_list:
        string = string.replace(chr, '')
    return string.split(',')


def from_csv_get_sentences(sentences, gene=None, pmid=None, img_name=None, save_file='gene_slices_sentences.csv'):
    # file = pd.read_csv(sentences, sep=',', index_col=['PMID', 'sentence', 'gene'])
    file = pd.read_csv(sentences)
    for i in range(len(file)):
        if str(file.iloc[i, 0]) == pmid:
            gene_list = change_str2list(file.iloc[i, 2], ['[', ']', '\''])
            if gene in gene_list:
                print(i+2, 'gene_list:', gene_list)
                with open(save_file, 'a+', newline='', encoding='utf_8_sig') as f:
                    tsv_w = csv.writer(f)
                    con = [img_name, file.iloc[i, 1]]
                    tsv_w.writerow(con)


    pass


def get_sentences(gene_slices, sentences, file):
    for dir in os.listdir(gene_slices):
        gene = dir
        print(dir)
        for slices in os.listdir(os.path.join(gene_slices, dir)):
            img_name = os.path.join(gene_slices, dir, slices)
            pmid = slices.split('_')[0]
            print(pmid)
            from_csv_get_sentences(sentences, gene, pmid, img_name, file)

    pass


if __name__ == '__main__':
    sentences_file = 'gene_slices_sentences.csv'
    with open(sentences_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image', 'caption'])
    get_sentences(gene_slices_path, sentences_path, sentences_file)

