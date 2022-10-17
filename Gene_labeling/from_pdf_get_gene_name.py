# 从所有的PDF中提取所有包含指定gene的句子

import os
import json
import csv
import pandas as pd
from label import get_gene_dict, get_sentence_from_textjs1, sentences_gene


def save_labeling(file, pmid, sentences, labels):
    print('labels:', labels)
    with open(file, 'a+', newline='', encoding='utf_8_sig') as f:
        # tsv_w = csv.writer(f, delimiter='\t')
        tsv_w = csv.writer(f)
        for i in range(len(sentences)):
            con = [pmid, sentences[i], labels[i]]
            tsv_w.writerow(con)


if __name__ == '__main__':
    relation_path = 'relation.csv'
    relation_json = 'relation.json'
    # get_gene_dict(relation_path, relation_json)  # Extract all genes from relation.csv (There is a description in the function)

    with open(relation_json, 'r', encoding='UTF-8') as js:
        gene_dict = json.load(js)

    sentences_file = 'occur_gene_sen1.csv'
    with open(sentences_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PMID', 'sentence', 'gene'])

    json_path = '../Text_data'
    for jf in os.listdir(json_path):
        pmid = jf.split('_text.json')[0]
        print('pmid:', pmid)
        file_content = get_sentence_from_textjs1(json_file=os.path.join(json_path, jf))
        if pmid in gene_dict:
            for s in range(len(file_content)):
                if len(file_content[s][0]) > 10:
                    can_sen, match_words = sentences_gene(file_content[s][0], gene_list=set(gene_dict[pmid][0]), gene_num=0)
                    if len(can_sen) > 0:
                        print('candidate sentence:', can_sen)
                        save_labeling(sentences_file, pmid, can_sen, match_words)
        else:
            print('NO ', pmid, ' in relation.csv')
