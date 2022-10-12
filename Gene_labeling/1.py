# 获取相同元素在list中的下标


# a = [0 ,1 ,2 ,3 ,4]
# b = [0 ,2 ,6]
# list(set(a).intersection(set(b)))  # 使用 intersection 求a与b的交集，输出：[0, 2]
# list(set(a).union(b))              # 使用 union 求a与b的并集，输出：[0, 1, 2, 3, 4, 6]
# list(set(b).difference(set(a)))    # 使用 difference 求a与b的差(补)集：求b中有而a中没有的元素，输出： [6]
# list(set(a).difference(set(b)))    # 使用 difference 求a与b的差(补)集：求a中有而b中没有的元素，输出：[1, 3, 4]
# list(set(a).symmetric_difference(b))   # 使用 symmetric_difference 求a与b的对称差集，输出：[1, 3, 4, 6]


a = [0, 1, 2, 3, 4]
b = [0, 2, 6]
print(list(set(a).intersection(set(b))))

c = ['abc', 'da']
d = ['abc', 'das ', 'ad ']
print(list(set(c).intersection(set(d))))

gene_dict = ['PDK1', 'CDK', 'EGFR', 'PI3K', 'CDK', 'MTOR', 'MEK', 'ERK', 'MTOR', 'CDK', 'PI3K', 'PDK1', 'BRAF', 'MEK', 'AKT', 'PI3K', 'PDK1', 'CDK', 'MTOR', 'CDK']
match_words = ['MEK', 'BRAF', 'AKT']
print(gene_dict.count(match_words[0]))
print(gene_dict.index(match_words[0], gene_dict.count(match_words[0])))
index_ = [k for k, v in enumerate(gene_dict) if v == match_words[0]]  # 获取相同元素在list中的下标
print(index_)

nums = [2, 5, 5, 11]
# 找出元素值为5的索引
index = [i for i, val in enumerate(nums) if val == 5]
print(index)

for m in range(0, len(match_words)):  # ['MEK', 'BRAF', 'AKT']
    for n in range(m + 1, len(match_words)):
        match_word_index = [k for k, v in enumerate(gene_dict) if v == match_words[m]]



