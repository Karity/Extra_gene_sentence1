import json
import pandas as pd
import numpy as np
import csv
from collections import defaultdict
import os


def get_gene_dict(relation_path, relation_json):
    '''
    The gene will be extracted in two forms, as described below.
    The results will be stored in a json file (usually only need to run once)
    :param relation_path:
    :param relation_json:
    :return:
    '''
    relation_file = pd.read_csv(relation_path)
    # gene_dict = defaultdict(list)
    gene_dict = {}
    pmid_list = []
    for i in range(len(relation_file)):
        pmid_list.append(relation_file.iloc[i, 0])

    for pmid in pmid_list:
        gene_list = []
        pari_gene = []
        for i in range(len(relation_file)):
            if relation_file.iloc[i, 0] == pmid:
                gene_list.append(relation_file.iloc[i, 2])
                gene_list.append(relation_file.iloc[i, 4])
                pari_gene.append(relation_file.iloc[i, 2])
                pari_gene.append(relation_file.iloc[i, 4])
                # if relation_file.iloc[i, 3] == 'activate_relation':
                #     pari_gene.append(relation_file.iloc[i, 2])
                #     pari_gene.append(relation_file.iloc[i, 4])
                # elif relation_file.iloc[i, 3] == 'inhibit_relation':
                #     pari_gene.append(relation_file.iloc[i, 2])
                #     pari_gene.append(relation_file.iloc[i, 4])
        gene_dict[str(pmid)] = [list(set(gene_list)), pari_gene]  # There are two forms of saving. One is to use set
        # to remove duplicates('list(set(gene_list))'), and the other('pari_gene') is to use the gene name whose
        # order is consistent with that in relation.csv (this is used to label sentences)

    with open(relation_json, 'w', encoding='UTF-8') as js:
        json.dump(gene_dict, js)


def process_word(word_list):
    chunk = []
    for name in word_list:
        name = name.replace(')', ' ')
        name = name.replace('(', ' ')
        name = name.replace('\'', ' ')
        name = name.strip()

        if '/' in name:
            names = name.split('/')
            chunk.extend(names)
        elif ',' in name:
            names = name.split(',')
            chunk.extend(names)
        elif '.' in name:
            name = name.replace('.', '')
            chunk.append(name)
        else:
            chunk.append(name)

    chunk = [c for c in chunk if len(c.strip()) > 0]
    return chunk


def sentences_gene(sentence: str, gene_list: set, gene_num=1):
    sentence_ = sentence.split('.')  # 将段落分为小句子
    candidate_sen = []
    match_words = []
    for i in range(len(sentence_)):
        # print('sentence:', sentence_[i])
        s = sentence_[i].strip().split()  #
        s = process_word(s)
        matches = set(s).intersection(gene_list)
        matches = [match for match in matches if len(match) > 0]
        if len(matches) > gene_num:
            can_sen = ' '.join(s)
            candidate_sen.append(can_sen)
            # candidate_sen.append(sentence_[i].strip())
            match_words.append(matches)
    return candidate_sen, match_words


def get_sentence_from_textjs(json_file):
    with open(json_file, 'r', encoding='UTF-8') as js:
        j_file = json.load(js)
        content = j_file[1]['body_text']
        file_content = []
        for i in range(len(content)):  # num of section1 {}
            for k, v in content[i].items():
                for j in range(len(content[i][k])):
                    con = list(content[i][k][j].values())
                    if len(con) < 2:
                        if type(con[0]) == list:
                            for m in range(len(con[0])):
                                for k1, v1 in con[0][m].items():
                                    file_content.append([v1])
                        else:
                            file_content.append(con)
                    else:
                        file_content.append([con[1]])
        return file_content


def get_sub_content(content):
    file_con = []
    file_sub_con = []
    for m in range(len(content)):
        for k2, v2 in content[m].items():
            if type(v2) != list:
                file_con.append(v2)
            else:
                for i in range(len(v2)):
                    file_sub_con.append(v2[i])
    return file_con, file_sub_con


def get_sentence_from_textjs1(json_file):
    with open(json_file, 'r', encoding='UTF-8') as js:
        j_file = json.load(js)
        content = j_file[1]['body_text']
        file_content = []

        for i in range(len(content)):  # num of section1 {}
            for k, v in content[i].items():
                while type(v) == list and len(v) > 0:
                    con, v = get_sub_content(v)
                    file_content.append(con)
        final_content = []
        for idx in range(len(file_content)):
            for idx1 in range(len(file_content[idx])):
                final_content.append([file_content[idx][idx1]])
        return final_content


def save_labeling(file, pmid, sentences, labels):
    print('labels:', labels)
    with open(file, 'a+', newline='', encoding='utf_8_sig') as f:
        tsv_w = csv.writer(f, delimiter='\t')
        # tsv_w.writerow(['sentence', 'label'])
        for i in range(len(sentences)):
            con = [pmid, sentences[i], labels[i]]
            tsv_w.writerow(con)


def labeling_sentences(sentences, gene_dict, match_words, if_replace=False):  # if_relpace: use '@GENE$' replace gene which in gene_dict
    label = []
    for i in range(len(sentences)):
        print('can_sentence:', sentences[i])
        print('gene_dict:', gene_dict)
        print('match_words:', match_words[i])
        label_ = None
        label__ = None
        for m in range(0, len(match_words[i])):  # ['MEK', 'BRAF', 'AKT']
            for n in range(m + 1, len(match_words[i])):
                match_word_index = [k for k, v in enumerate(gene_dict) if v == match_words[i][m]]
                for index in match_word_index:
                    if index % 2 == 0:
                        if gene_dict[index + 1] == match_words[i][n]:
                            label_ = 1
                        else:
                            label__ = 0
                    elif index % 2 == 1:
                        if gene_dict[index - 1] == match_words[i][n]:
                            label_ = 1
                        else:
                            label__ = 0
        if if_replace:
            sen_split = sentences[i].split()
            for word in sen_split:
                if word in match_words[i]:
                    sen_split[sen_split.index(word)] = '@GENE$'
            sentences[i] = ' '.join(sen_split)
        if label_:
            label.append(label_)
        else:
            label.append(label__)
    return sentences, label


def get_relation_gene(sentences, gene_dict, match_words):
    relation_gene = []
    for i in range(len(sentences)):
        print('can_sentence:', sentences[i])
        print('gene_dict:', gene_dict)
        print('match_words:', match_words[i])
        relation_ = None
        relation__ = None
        for m in range(0, len(match_words[i])):
            for n in range(m + 1, len(match_words[i])):

                match_word_index = [k for k, v in enumerate(gene_dict) if v == match_words[i][m]]
                for index in match_word_index:
                    if index % 2 == 0:
                        if gene_dict[index + 1] == match_words[i][n]:
                            relation_ = match_words[i][m], match_words[i][n]
                        else:
                            relation__ = None
                    elif index % 2 == 1:
                        if gene_dict[index - 1] == match_words[i][n]:
                            relation_ = match_words[i][n], match_words[i][m]
                        else:
                            relation__ = None
        if relation_:
            relation_gene.append(relation_)
        else:
            relation_gene.append(relation__)
    return sentences, relation_gene


if __name__ == '__main__':
    relation_path = 'relation.csv'
    relation_json = 'relation.json'
    # get_gene_dict(relation_path, relation_json)  # Extract all genes from relation.csv (There is a description in the function)

    # json_path = '../Text_data'
    json_path = '../test_fetched_pdfs'  # Store the article content extracted from the pdf. See the file Text_data for an example

    with open(relation_json, 'r', encoding='UTF-8') as js:
        gene_dict = json.load(js)

    tsv_file = 'file2.tsv'  # Store the found sentences that can be labeled
    # file.tsv Matched gene -> '@GENE$'
    # file1.tsv No change
    with open(tsv_file, 'w', newline='', encoding='utf_8_sig') as f:
        tsv_w = csv.writer(f, delimiter='\t')
        tsv_w.writerow(['PMID', 'sentence', 'label'])

    for jf in os.listdir(json_path):
        pmid = jf.split('_text.json')[0]
        print('pmid:', pmid)
        file_content = get_sentence_from_textjs1(json_file=os.path.join(json_path, jf))
        if pmid in gene_dict:
            with open(tsv_file, 'a+', newline='', encoding='utf_8_sig') as f:
                tsv_w = csv.writer(f, delimiter='\t')
                # tsv_w.writerow([pmid])
            for s in range(len(file_content)):
                if len(file_content[s][0]) > 10:
                    can_sen, match_words = sentences_gene(file_content[s][0], gene_list=set(gene_dict[pmid][0]), gene_num=1)
                    if len(can_sen) > 0:
                        print('candidate sentence:', can_sen)
                        # can_sen, label = labeling_sentences(can_sen, gene_dict[pmid][1], match_words)
                        # save_labeling(tsv_file, can_sen, label)
                        can_sen, relation_gene = get_relation_gene(can_sen, gene_dict[pmid][1], match_words)
                        save_labeling(tsv_file, pmid, can_sen, relation_gene)
        else:
            print('NO ', pmid, ' in relation.csv')




