from collections import defaultdict
import os
import evaluate_tool as tool
from itertools import islice

# dict1 = defaultdict(list)
# dict1[1] = ['abc']
# print(dict1[2])  # 输出默认值：[]
# print(dict1)

# a = [1, 2, 3]
# b = [2, 3, 4]
# print(set(a).intersection(set(b)))  # [2, 3]

FULL_TEXT = 'test_txt/'  # modify this to the directory path that contains the raw text files

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


def annotate_lbl_sentences(sentence_list, hugo_ner):
    processed_sentence = ""
    for sentence in sentence_list:
        sentence_tokens = sentence.split()
        matches = set(sentence_tokens).intersection(hugo_ner)
        matches = [match for match in matches if len(match) > 0]  # 与hogo_ner匹配的字符串
        indices_sentence_tokens = [sentence_tokens.index(x) for x in matches]
        new_sentence = ""
        if len(matches) < 1:
            processed_sentence += sentence
        else:
            for item in indices_sentence_tokens:
                sentence_tokens[item] = '@GENE$'  # 把匹配上的替换为 '@GENE$'
                new_sentence = ' '.join(sentence_tokens)
            processed_sentence += new_sentence + '\n'
    processed_sentence = processed_sentence.strip().split('\n')
    return processed_sentence


labeled_dict = defaultdict(list)
occur = {}


def from_file_get_sentences(source_file):
    pmcid = source_file.split('.')[0]
    with open(source_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
        file_sentences = file_content.split('$$')
        file_sentences = [sentence.lower().replace('\n', '').strip() for sentence in file_sentences if len(sentence.strip()) > 0]  # 去掉换行和空格
        file_sentences = chunkify(file_sentences, GRP_SENTENCES)
        print('file_sentences:', file_sentences)
        for sentence in file_sentences:
            sentence_tokens = sentence.split()  # 以空格为分割取出每个句子中的每个词
            sentence_tokens = [token.lower() for token in sentence_tokens]
            eval = tool.evaluate()
            sentence_tokens = eval.fuzzy_rule(sentence_tokens)
            labeled_dict[pmcid].append(sentence.replace('\n', '') + '\n')
        return file_sentences


if __name__ == '__main__':
    eval = tool.evaluate()
    for file in os.listdir('test_txt'):
        file_name = os.path.join('test_txt', file)
        sentences = from_file_get_sentences(file_name)
        annotated_dict = defaultdict(list)
        for key, value in labeled_dict.items():
            print(key, ':', value)
            gene_relations = eval.retrieve_gene_relations()
            sentence = annotate_lbl_sentences(value, gene_relations[key])
            annotated_dict[key] = (sentence)
        eval.write_dict_to_txt_file(annotated_dict, OUTPUT)









