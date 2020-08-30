import cv2
import torch
import os, shutil
import numpy as np
from random import choice

def search(path, s):
    result = []
    for t in os.walk(path):  # 返回的是root,dirs,files
        for filename in t[2]:  # t[2]指的就是files
            if s in os.path.splitext(filename)[0]:  # test.txt [0]为test [1]为.txt 文件名和扩展名
                result.append(filename)
    return result


def generate_single_shot_gallery(root, total):
    gallery = []
    for id in range(total):
        if id < 10:
            id_images = search(root, 'gallery_00' + str(id))
        elif id>=10 and id < 100:
            id_images = search(root, 'gallery_0' + str(id))
        else:
            id_images = search(root, 'gallery_' + str(id))

        gallery.append(choice(id_images))
    return gallery

def get_query(root):
    query = search(root, 'query')
    return query

def L2_distance(feature_1, feature_2):
    return np.sum((feature_2 - feature_1)**2)

def mycopyfile(srcfile,dstfile):
 if not os.path.isfile(srcfile):
     print("%s not exit!" % (srcfile))
 else:
     fpath,fname=os.path.split(dstfile)
 if not os.path.exists(fpath):
  os.makedirs(fpath)
 shutil.copyfile(srcfile,dstfile)

gallery = generate_single_shot_gallery('RegDB_01/', 206)
query = get_query('RegDB_01/')

for i in range(len(query)):
    query_single_name = query[i]
    query_single_image = cv2.imread('RegDB_01/' + query_single_name)
    query_single_feature = query_single_image[:,:,1]
    query_distance_dict = dict()
    for j in range(len(gallery)):
        gallery_single_name = gallery[j]
        gallery_single_image = cv2.imread('RegDB_01/' + gallery_single_name)
        gallery_single_feature = gallery_single_image[:, :, 1]
        query_distance_dict[gallery_single_name] = L2_distance(query_single_feature, gallery_single_feature)

    sorted_distance_dict = sorted(query_distance_dict.items(), key=lambda x: x[1])
    count = 0
    top_list = [query_single_name]
    for key, value in sorted_distance_dict:
        count += 1
        top_list.append(key)
        if count >= 10:
            break
    dstpath = "RegDB_results/" + query_single_name + "/"
    for k in range(len(top_list)):
        if k == 0:
            mycopyfile('RegDB_01/' + top_list[k], dstpath + top_list[k])
        else:
            mycopyfile('RegDB_01/' + top_list[k], dstpath + 'Top' + str(k) + '_' + top_list[k])







'''img_cv1 = cv2.imread('gallery_000_T_female_back_t_01102_88.png')
img_cv2 = cv2.imread('gallery_007_T_female_back_t_01625_118.png')
feature_1 = img_cv1[:,:,1]
feature_2 = img_cv2[:,:,1]

print(np.sum((feature_2 - feature_1)**2))'''

