import json
import os
from pathlib import Path

text_path = Path('test_fetched_pdfs')
save_path = Path('collectd_text')
# text_path = Path('test_pdfs_text')
images_and_captions = []
related_paragraphs = []
results = []


def flatten(listin):
    for i in listin:
        if isinstance(i, dict):
            for key, value in i.items():
                # print(f"\nKey:{key}")
                if isinstance(value, list):
                    flatten(value)
                else:
                    if key == "Figure":
                        a = {key: value}
                        # print("这是figure",key,value)
                    if key == "Figure_title" and value:
                        b = {key: value}
                        if value[:5].upper().find("FIG") != -1:
                            images_and_captions.append([a, b])
                        # print("这是caption",key,value)
                    # print(f"\nValue:{value}")


def flatten_2(listin, prefix):
    for i in listin:
        if isinstance(i, dict):
            for key, value in i.items():
                # print(f"\nKey:{key}")
                if isinstance(value, list):
                    flatten_2(value, prefix)
                else:
                    if key.find("paragraph") != -1:
                        if value.find(prefix) != -1:
                            # print("找到了",value)
                            related_paragraphs.append(value)


if __name__ == '__main__':

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    for json_file in text_path.glob("*.json"):
        json_name = os.path.split(json_file)[1].split('.')[0]
        print(json_name)
        with open(json_file, 'r', encoding='UTF-8') as f:
            d = json.load(f)
        data = d[1]['body_text']  # 是个list
        # print(data)
        ##  进行嵌套的遍历
        flatten(data)  # 提取到所有的 Figure和 Figure_title

        #  根据上述图片开头（figure1）找到文章中含有figure1 的段落（每个段落只找一次就行
        #  因为可能有的段落多次出现figure1
        for i in images_and_captions:
            # print(i)
            # 提取前面部分
            prefix = ''
            for j in range(len(i[1]["Figure_title"])):
                if i[1]["Figure_title"][j].isdigit() and not i[1]["Figure_title"][j + 1].isdigit():  # 终止拷贝的条件
                    prefix += i[1]["Figure_title"][j]
                    break
                else:
                    prefix += i[1]["Figure_title"][j]
            # print(prefix)
            flatten_2(data, prefix)
            temp = [i[0], i[1]]
            temp.append({"Figure_level": prefix})
            dic = {"Figure_profile:": temp, "related_paragraphs": related_paragraphs}
            results.append(dic)
            related_paragraphs = []

            # for i in results:
            #     print(i)
            name = i[0]["Figure"].split(".jpg")[0]
            # print(name)

            json_file_name = str(save_path) + '/' + name + '.json'
            file = open(json_file_name, 'w', encoding='utf-8')  # text to json file
            file_content = json.dumps(results, indent=2, ensure_ascii=False)
            file.write(file_content)

            images_and_captions = []
            results = []
