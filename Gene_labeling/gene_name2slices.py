# 将指定的gene从图片中得到相应的slices，并存放在以gene命名的文件夹下
import os
import cv2
import json
import numpy as np
from typing import Union, List


def cropimg(src_img, box):
    top = box[0]
    bottom = box[1]
    left = box[2]
    right = box[3]
    dst_img = src_img[top:bottom, left:right]
    return dst_img


def get_gene_box(bbox):
    x11, x12, x21, x22 = bbox[0], bbox[1], bbox[2], bbox[3]
    return np.array([x12, x12 + x22, x11, x11 + x21])


def get_gene_name_num(image_path, num=-1):
    '''
    获取文件夹下面的所有图片中的gene个数
    :param image_path:
    :return:
    '''
    gene_bbox = {}
    gene_num = {}
    for dir in os.listdir(image_path):
        for image in os.listdir(os.path.join(image_path, dir, 'img')):
            if image.endswith('.jpg'):
                image_name = image.split('.jpg')[0]
                gene_json = os.path.join(image_path, dir, 'img', 'gene_name', image_name + '_elements.json')
                with open(gene_json) as js:
                    js_file = json.load(js)
                    for i in range(1, len(js_file)):
                        if js_file[i]['post_gene_name'] != '-' and js_file[i]['post_gene_name'] is not None:
                            gene_bbox.setdefault(js_file[i]['post_gene_name'], []).append(js_file[i]['coordinates'])
    for k, v in gene_bbox.items():
        gene_num[k] = len(v)
    list1 = sorted(gene_num.items(), key=lambda x: x[1], reverse=True)
    return list1[: num]


def make_dir(dir: Union[List, str], last_slant: bool = True):
    """
    使用dir中的参数构成一个文件夹
    :param dir:
    :param last_slant: 若为True：则 a/b/c/ ; 若为False：则 a/b/c
    :return:
    """
    if isinstance(dir, str):
        dir = [dir]
    dst_dir = dir[0]
    for dir1 in dir[1:]:
        dst_dir = os.path.join(dst_dir, dir1)
    if last_slant:
        dst_dir = dst_dir + '\\'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    return dst_dir


def get_gene_slices(image_path, gene_name: Union[str, List] = None, img_save_folder_root='../abc/'):
    """
    获取指定gene_name的slices并存放在相应的文件夹下
    :param image_path:
    :param gene_name:
    :param img_save_folder_root:
    :return:
    """
    if isinstance(gene_name, str):
        gene_name = [gene_name]
    print('gene_name:', gene_name)
    for gene in gene_name:
        img_save_folder = make_dir(dir=[img_save_folder_root, gene])
        for dir in os.listdir(image_path):
            for image in os.listdir(os.path.join(image_path, dir, 'img')):
                if image.endswith('.jpg'):
                    image_name = image.split('.jpg')[0]
                    img = cv2.imread(os.path.join(image_path, dir, 'img', image))
                    gene_json = os.path.join(image_path, dir, 'img', 'gene_name', image_name + '_elements.json')
                    # print('gene_json:', gene_json)
                    gene_bbox = {}
                    with open(gene_json) as js:
                        js_file = json.load(js)
                        for i in range(1, len(js_file)):
                            if js_file[i]['post_gene_name'] == gene:
                                gene_bbox.setdefault(js_file[i]['post_gene_name'], []).append(js_file[i]['coordinates'])
                    for k, v in gene_bbox.items():
                        for idx in range(len(v)):
                            bbox = v[idx]
                            crop_bbox = get_gene_box(bbox)
                            crop_img = cropimg(img, crop_bbox)
                            img_slice_name = image_name + '_' + str(idx) + '.jpg'
                            print(img_slice_name)
                            cv2.imwrite(filename=img_save_folder + img_slice_name, img=crop_img)
                    # print('gene_bbox:', gene_bbox)


if __name__ == '__main__':
    # path = '../relation'
    path = r'E:\LAPTOP\new_result1'
    # gene_num = get_gene_name_num(path, num=5)
    # print(gene_num)
    #
    get_gene_slices(path, gene_name=['MTOR', 'AKT'])
