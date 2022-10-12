import sys
import os
import json
import pandas as pd
import csv
import string_lib
# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

import evaluate_tool as tool
from collections import defaultdict
from itertools import islice

eval = tool.evaluate()
str_lib = string_lib.str_list_ops()
FULL_TEXT = r"F:\PyCharm Project\Extra_gene_sentence\Text_data/"  # modify this to the directory path that contains the raw text files

GRP_SENTENCES = 1
OUTPUT = 'output/'


def chunkify(lst, chunk_size):
    lst = [l.strip().replace('.', '') for l in lst]
    lst = iter(lst)
    output = []
    res = iter(lambda: tuple(islice(lst, chunk_size)), ())
    for new_list in res:
        output.append(' '.join(list(new_list)).strip())
    return output


def list_diff(a, b):
    c = set(a) - set(b)
    return list(c)


def extract(raw_string, start_marker, end_marker):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]


def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"


def list_diff(a, b):
    c = set(a) - set(b)
    return list(c)


def add_period(string_list):
    result = []
    for string in string_list:
        string = string.split()
        string[-2] = string[-2] + '.'
        string[-1] = '  ' + string[-1]
        result.append(' '.join(string))
    return result


def annotate_lbl_sentences(sentence_list, hugo_ner):
    processed_sentence = ""
    for sentence in sentence_list:
        sentence_tokens = sentence.split()
        matches = set(sentence_tokens).intersection(hugo_ner)
        matches = [match for match in matches if len(match) > 0]
        indices_sentence_tokens = [sentence_tokens.index(x) for x in matches]
        new_sentence = ""
        if len(matches) < 1:
            processed_sentence += sentence
        else:
            for item in indices_sentence_tokens:
                sentence_tokens[item] = '@GENE$'
                new_sentence = ' '.join(sentence_tokens)
            processed_sentence += new_sentence + '\n'
    processed_sentence = processed_sentence.strip().split('\n')
    return processed_sentence


def extract(raw_string, start_marker, end_marker):
    start = raw_string.index(start_marker) + len(start_marker)
    end = raw_string.index(end_marker, start)
    return raw_string[start:end]


gene_relations = eval.retrieve_gene_relations()
dir = os.listdir(FULL_TEXT)

labeled_dict = defaultdict(list)
occur = {}
for file in dir:
    pmcid = file.split('.')[0]
    with open(FULL_TEXT + file, 'r', encoding='UTF-8') as f:
        content = f.read()
        sentences = content.split('$$')
        sentences = [sentence.lower().replace('\n', '').strip() for sentence in sentences if len(sentence.strip()) > 0]
        sentences = chunkify(sentences, GRP_SENTENCES)
        for sentence in sentences:
            sentence_tokens = sentence.split()
            sentence_tokens = [token.lower() for token in sentence_tokens]
            sentence_tokens = eval.fuzzy_rule(sentence_tokens)
            labeled_dict[pmcid].append(sentence.replace('\n', '') + '\n')

annotated_dict = defaultdict(list)
for key, value in labeled_dict.items():
    sentence = annotate_lbl_sentences(value, gene_relations[key])
    annotated_dict[key] = (sentence)

eval.write_dict_to_txt_file(annotated_dict, OUTPUT)
