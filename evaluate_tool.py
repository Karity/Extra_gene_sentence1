from difflib import SequenceMatcher
import os
import csv
import re
import string
import pandas as pd
import glob
import json
from collections import defaultdict
import string_lib as str_lib
from tqdm import tqdm


class evaluate:
    def __init__(self) -> None:
        # self.gene_results = [gene_file.split("_")[1].split(".")[0] for gene_file in os.listdir(self.ALVA_BIOBERT_PATH)]
        self.indpendent_gene_relations = "data/updated_relations.csv"
        self.independent_path = "RE/INDEPENDENT_DATA/"

    def retrieve_gene_relations(self):
        genes_dict = defaultdict(list)
        for result_file in os.listdir(self.independent_path):
            pmcid = result_file.split(".")[0]

            with open(self.independent_path + result_file, 'r', encoding="UTF8") as f:
                gene_names = list(set(f.read().lower().strip().split('\n')))
                genes_dict[pmcid].extend(gene_names)
        return genes_dict

    def retrieve_updated_relations(self):
        rel_dict = defaultdict(list)
        df = pd.read_csv(self.indpendent_gene_relations)
        for col in df.iterrows():
            gene_pair = [col[1]['StartID'], col[1]['ReceptorID']]
            rel_dict[col[1]['PMID']].append(gene_pair)

        for key, value in rel_dict.items():
            content = ""
            for pair in value:
                pair = [p.lower() for p in pair]
                content += '\n'.join(pair) + '\n'

            with open('RE/INDEPENDENT_DATA/PMC' + str(key) + '.txt', 'w') as f:
                f.write(content)
        return rel_dict

    def fuzzy_rule(self, name_list):
        chunk = []
        for name in name_list:
            name = name.replace(')', ' ')
            name = name.replace('(', ' ')
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

        # chunk = []
        # for name in name_list:
        #     name = name.strip()
        #     if '/' in name:
        #         names = name.split('/')
        #         chunk.extend(names)
        #     elif name.startswith('('):
        #         name = ''.join(name[name.find("(")+1:name.find(")")])
        #         if ',' in name:
        #             name = name.split(',')
        #             chunk.extend(name)
        #         else:
        #             chunk.append(name)
        #     elif '.' in name:
        #         name = name.replace('.', '')
        #         chunk.append(name)

        # elif name.find("-") >= 0:
        #     if not name[name.find("-") + 1:len(name)].isalpha() or len(name[name.find("-") + 1:len(name)]) < len(
        #             name[0:name.find("-")]):
        #         name = name[0:name.find("-")]
        #         chunk.append(name)
        #     if name.find("-") < 2:
        #         name = name[name.find("-") + 1:len(name)]
        #         chunk.append(name)
        # else:
        #     chunk.append(name)

    # compares similarity between two strings

    def write_pred_results_to_json(self, gene_dict):
        json_dict = defaultdict(list)
        stopwords = str_lib.str_list_ops.return_stop_words()
        for key, value in gene_dict.items():
            formatted_values = [val for val in value if val not in stopwords]
            formatted_values = [val for val in formatted_values if not val.isdigit()]
            formatted_values = [val for val in formatted_values if len(val) > 2]
            json_dict[key].extend(formatted_values)
        with open("data/hugo_output.json", "w") as f:
            json.dump(json_dict, f, indent=3)

    def write_dict_to_txt_file(self, def_dict, dir):
        for key, value in def_dict.items():
            with open(dir + key + '.tsv', 'w', encoding='UTF8') as f:
                val = ''.join(value)
                f.write(val)
