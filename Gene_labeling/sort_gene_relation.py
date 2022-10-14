# 获取在relation_file文件中提及到的数量较多的gene对 所对应的slices
import json
import os
import shutil

import pandas as pd

from sort_num_img import sort_gt

relation_file = 'file2.tsv'
file = pd.read_csv(relation_file, sep='\t', index_col=['PMID', 'sentence', 'label'])


def get_gene_pari():
    """将relation_file文件中的gene对 以 a+b 的形式（b+a也会被替换为a+b，即做了一样的排序）存放"""
    gene_pari = []
    for i in range(len(file)):
        if type(file.iloc[i].name[2]) is str:
            label = file.iloc[i].name[2].replace('(', '').replace(')', '').replace('\'', '').split(',')
            for j in range(len(label)):
                label[j] = label[j].strip()
            label1 = sorted(label)
            gene_pari_ = label1[0] + '+' + label1[1]
            gene_pari.append(str(gene_pari_))
    return gene_pari


def get_relation_name(reation_json_dir):
    """
    返回符合条件的所有关系对 以及 对应的json文件名
    :param reation_json_dir: 结果的一级目录
    :return:
    """
    relation_name = []
    json_name = []
    for pdf_dir in os.listdir(reation_json_dir):
        relation_json_dir = os.path.join(reation_json_dir, pdf_dir, 'img', 'relation')
        for json_file in os.listdir(relation_json_dir):
            relation_json = os.path.join(relation_json_dir, json_file)
            img_file = relation_json.split('\\')[-1].split('_relation.json')[0]
            # print(relation_json)
            with open(relation_json) as js:
                js_file = json.load(js)
                for k, v in js_file.items():
                    if v['startor'] != '-' and v['startor'] is not None and v['receptor'] != '-' \
                            and v['receptor'] is not None and (v['startor'] != v['receptor']):
                        if v['relation_category'] == 'activate_relation':
                            relation_name.append(v['startor'] + '+' + v['receptor'])
                            json_name.append(relation_json)
                        elif v['relation_category'] == 'inhibit_relation':
                            relation_name.append(v['startor'] + '-' + v['receptor'])
                            json_name.append(relation_json)
    return relation_name, json_name


def get_relation_json(json_file_name, relation_name, relation):
    """
    获得符合要求的关系对 (关系对的内容等于relation) 对应的json文件的list
    :param json_file_name:
    :param relation_name:
    :param relation:
    :return:
    """
    json_name = []
    [json_name.append(json_file_name[i]) for i, x in enumerate(relation_name) if x == relation]
    return json_name


def get_relation_slices(relation_json_list, relation, slices_dir):
    """
    在上述符合要求的json的list中(relation_json_list) 将slices_dir中符合要求的图片(图片内容是关系对relation) 复制到新的文件夹中
    :param relation_json_list:
    :param relation:
    :param slices_dir:
    :return:
    """
    img_save_folder = r'C:\Users\lk\Desktop\\' + relation
    print(img_save_folder)
    if not os.path.exists(img_save_folder):
        os.makedirs(img_save_folder)
    for json_file in relation_json_list:
        img_name_prefix = json_file.split('\\')[-1].split('_relation.json')[0]
        with open(json_file) as js:
            js_file = json.load(js)
            current_relation_index = []
            for k, v in js_file.items():
                if v['startor'] != '-' and v['startor'] is not None and v['receptor'] != '-' \
                        and v['receptor'] is not None and (v['startor'] != v['receptor']):
                    current_relation_index.append(k)
            if len(current_relation_index) > 0:
                for idx in current_relation_index:
                    if js_file[idx]['relation_category'] == 'activate_relation':
                        relation_name = js_file[idx]['startor'] + '+' + js_file[idx]['receptor']
                        if relation_name == relation:
                            shutil.copy(slices_dir + '/' + img_name_prefix + '_' + idx + '.jpg', img_save_folder)
                    elif js_file[idx]['relation_category'] == 'inhibit_relation':
                        relation_name = js_file[idx]['startor'] + '-' + js_file[idx]['receptor']
                        if relation_name == relation:
                            shutil.copy(slices_dir + '/' + img_name_prefix + '_' + idx + '.jpg', img_save_folder)


if __name__ == '__main__':
    slices_path = r'E:\LAPTOP\gene_and_relation_slices'  # 目标目录
    # # path = 'test/result'
    path = r'E:\LAPTOP\new_result1'  # 存放数据的目录
    relation_name_list, img_file = get_relation_name(path)

    # sort_dict = sort_gt(relation_name_list, 8)
    # print(sort_dict)
    # for key, val in sort_dict.items():
    #     print(key)
        # get_relation_slices(get_relation_json(img_file, relation_name_list, key), key, slices_path)

    gene_pari = get_gene_pari()
    sort_dict = sort_gt(gene_pari)
    print(sort_dict)
    for key, val in sort_dict.items():
        print(key)
        get_relation_slices(get_relation_json(img_file, relation_name_list, key), key, slices_path)







