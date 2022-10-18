# 获取slices_path文件夹下的gene relation slices对应的文本
import os
import csv
import pandas as pd

from sort_num_img import sort_gt

# relation_file = 'file_base.tsv'
relation_file = 'file2.tsv'
# slices_path = '../slices_images'
slices_path = '../slices_images1'

file = pd.read_csv(relation_file, sep='\t', index_col=['PMID', 'sentence', 'label'])


def get_gene_pari():
    gene_pari = []
    for i in range(len(file)):
        if type(file.iloc[i].name[2]) is str:
            label = file.iloc[i].name[2].replace('(', '').replace(')', '').replace('\'', '').split(',')
            for j in range(len(label)):
                label[j] = label[j].strip()
            gene_pari.append(str(sorted(label)))
            print(label, type(label))
            print(label[0])
    return gene_pari


image_sentence_file = 'corr_inf.csv'
with open(image_sentence_file, "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image", "sentence"])


def write_corr_information(image_name: str, corr_sentences: list, dst_file: str = image_sentence_file):
    with open(dst_file, 'a+', encoding='utf_8_sig') as file:
        for i in range(len(corr_sentences)):
            writer = csv.writer(file)
            con = [image_name, corr_sentences[i]]
            writer.writerow(con)


def get_sentences():
    for dir in os.listdir(slices_path):
        gene_pari = dir.split('+')
        print(sorted(gene_pari))
        for img in os.listdir(os.path.join(slices_path, dir)):
            pmid = img.split('_page')[0]
            print('pmid:', pmid)
            corr_sentence = []
            for i in range(len(file)):
                if str(file.iloc[i].name[0]) == pmid and type(file.iloc[i].name[2]) is str:
                    label = file.iloc[i].name[2].replace('(', '').replace(')', '').replace('\'', '').split(',')
                    for j in range(len(label)):
                        label[j] = label[j].strip()
                    if sorted(label) == sorted(gene_pari):
                        corr_sentence.append(file.iloc[i].name[1])
            print(corr_sentence)
            write_corr_information(img, corr_sentence)


# l = ['PI3K', 'AKT']
# l2 = ['AKT', 'PI3K']
# list1 = sorted(l)
# list2 = sorted(l2)  # 不改变list本身
# print(list1, list2)
# print(list1 == list2)
# from collections import Counter
# a = Counter(l)
# b = Counter(l2)
# print(a, b)
# print(dict(a) == dict(b))

if __name__ == '__main__':
    # gene_pari = get_gene_pari() print(gene_pari) sort_dict = sort_gt(gene_pari) for key, val in sort_dict.items():
    # print(key)
    # sort_dict = {'PI3K+AKT': 46, 'AKT+MTOR': 36, 'RAS+Raf': 35, 'Raf+MEK': 33, 'MEK+ERK': 23,
    #              'PI3K+RAS': 11, 'JAK+STAT': 9, 'MTOR+AKT': 9}
    sort_dict = {'AKT+PI3K': 71, 'ERK+MEK': 71, 'ALK+FISH': 71, 'ALK+EGFR': 71, 'PI3K+PTEN': 71, 'JAK2+STAT3': 71,
                 'EGFR+PI3K': 71, 'RB1+TP53': 71, }
    get_sentences()
