# 将数据集修改为训练集和测试集

import csv
import pandas as pd
import numpy as np
from gene_name2slices import get_gene_name_num

path = r'E:\LAPTOP\new_result1'

data = pd.read_csv('gene_slices_sentences.csv')
print(len(data))
img_list = []
for i in range(len(data)):
    img_list.append(data.iloc[i, 0])

dict1 = {}
for key in img_list:
    dict1[key] = dict1.get(key, 0) + 1
print(dict1)

idx = 0
train_list = []
vaild_list = []
for k, v in dict1.items():
    str = idx
    idx += v
    train_list.append(list(np.arange(str, round(v * 0.8) + str)))
    vaild_list.append(list(np.arange(round(v * 0.8) + str, idx)))
train_list_ = []
vaild_list_ = []
for i in range(len(train_list)):
    for j in range(len(train_list[i])):
        train_list_.append(train_list[i][j])
    for j1 in range(len(vaild_list[i])):
        vaild_list_.append(vaild_list[i][j1])
print(train_list_)
print(vaild_list_)
print(len(train_list_), len(vaild_list_))


train_csv = 'train_sentences.csv'
vaild_csv = 'vaild_sentences.csv'

# with open(train_csv, "w") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['image', 'caption'])
#
# with open(vaild_csv, "w") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['image', 'caption'])
#
# for train_idx in train_list_:
#     with open(train_csv, 'a+', newline='', encoding='utf_8_sig') as f:
#         tsv_w = csv.writer(f)
#         con = [data.iloc[train_idx, 0], data.iloc[train_idx, 1]]
#         tsv_w.writerow(con)


def write_train_or_vaild_csv(csv_file, idx_list, full_data=data):
    with open(csv_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image', 'caption'])

    for idx_ in idx_list:
        with open(csv_file, 'a+', newline='', encoding='utf_8_sig') as f:
            tsv_w = csv.writer(f)
            con = [full_data.iloc[idx_, 0], full_data.iloc[idx_, 1]]
            tsv_w.writerow(con)


if __name__ == '__main__':
    write_train_or_vaild_csv(train_csv, train_list_)
    write_train_or_vaild_csv(vaild_csv, vaild_list_)
