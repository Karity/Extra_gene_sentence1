import re
import string
from difflib import SequenceMatcher

from tqdm import tqdm


class str_list_ops:

    def __init__(self) -> None:
        pass

    def common_elements(list_a, list_b):
        # print(list_a)
        a_set = set(list_a)
        b_set = set(list_b)

        # check length
        if len(a_set.intersection(b_set)) > 0:
            return list(a_set.intersection(b_set))
        else:
            return []

    def intersection_over_union(list1, list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection

        return float(intersection) / union

    def match_ratio(list1, list2):
        return float(len(list2) / len(list1))

    def format_gene_array(string):
        result = string.replace('[', '').replace(']', '').replace("'", '').strip()
        result = result.split(', ')
        return (result)

    def filter_stop_words(self, text_list, stopwords):
        filtered = [word for word in text_list if word.lower() not in stopwords and not re.search('^(?:(?:[0-9]{2}[:\/,]){2}[0-9]{2,4}|am|pm)$', word)]
        return filtered

    def return_stop_words(self):
        stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own',
                     'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                     'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this',
                     'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same',
                     'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under',
                     'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my',
                     'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'using']
        return stopwords

    def common_gene_in_text(self, text_list, text):
        text_list = list(set(text_list))
        result = []
        found = []
        for word in text_list:
            if word in text:
                found.append(word)
                start = text.index(word)
                end = start + len(word)
                for i in range(start, 0, -1):
                    if text[i].isspace() or text[i] in [' ', ',', '/', ';', ':', '?']:
                        start = i
                        break
                for j in range(end, len(text)):
                    if text[j].isspace() or text[j] in [' ', ',', '/', ';', ':', '?']:
                        end = j
                        break

                result.append(text[start:end].strip())

        return result
