# import pandas as pd
#
#
# def sort_gt(gt_list):
#     counts = {}
#     for word in gt_list:
#         counts[word] = counts.get(word, 0) + 1
#     items = list(counts.items())
#     items.sort(key=lambda x: x[1], reverse=True)  # 排序
#     for i in range(100):
#         word, count = items[i]
#         print("{0:<10}{1:>5}".format(word, count))
#
#
# if __name__ == '__main__':
#     file = pd.read_csv('base/relation1.csv')
#     print(len(file))
#     file_name = []
#     for i in range(len(file)):
#         file_name.append(file.iloc[i, 1])
#     print(len(file_name))
#     sort_gt(file_name)
import pandas as pd


def sort_gt(gt_list, top_num=10):  # 排序 返回前top_num个
    counts = {}
    for word in gt_list:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)  # 排序
    sort_dict = {}
    for idx in range(top_num):
        word, count = items[idx]
        sort_dict[word] = count
        print("{0:<10}{1:>5}".format(word, count))
    return sort_dict


if __name__ == '__main__':
    file = pd.read_csv(r'D:\PyCharmProject\Full_pipeline\base/relation1.csv')
    print(len(file))
    file_name = []
    for i in range(len(file)):
        file_name.append(file.iloc[i, 1])

    print(file_name)
    print(len(file_name))
    sort_gt(file_name)