#coding=utf-8

#import numpy as np
#import cv2
from PIL import Image
import os
import json
import shutil

def main(img_path, total_img_path, total_test_path, gt_path, total_train_gt_path, total_test_gt_path, json_file):

    dict = [json.loads(line) for line in open(json_file).readlines()]

    #generate train img
    for i in range(len(dict)-351):   # 2018-10-11-->505; 2018-12-18-->317; 2019-05-08-->351;
        index = i+8411                  # 2018-10-11-->1; 2018-12-18-->5172; 2019-05-08-->8411
        name = dict[i]['filename']
        name, name1 = name.replace(".", "_rcb."), name.replace(".jpg", "_rcb.png")

        oldname = img_path + name
        newname = total_img_path + str(index) + '.jpg'
        oldname1 = gt_path + name1
        newname1 = total_train_gt_path + str(index) + '.png'

        if not os.path.exists(total_img_path):
            os.makedirs(total_img_path)
        if not os.path.exists(total_train_gt_path):
            os.makedirs(total_train_gt_path)

        shutil.copy(oldname, newname)
        shutil.copy(oldname1, newname1)
        print(index)
    print('------------complete train_dataset-------------')

    #generate test img
    for j in range(len(dict)-351, len(dict)):     # 2018-10-11-->505; 2018-12-18-->317; 2019-05-08-->351;
        index = j-2767                            # 2018-10-11-->5170; 2018-12-18-->2733; 2019-05-08-->2767;
        name = dict[j]['filename']
        name, name1 = name.replace(".", "_rcb."), name.replace(".jpg", "_rcb.png")

        oldname = img_path + name
        newname = total_test_path + str(index) + '.jpg'
        oldname1 = gt_path + name1
        newname1 = total_test_gt_path + str(index) + '.png'

        if not os.path.exists(total_test_path):
            os.makedirs(total_test_path)
        if not os.path.exists(total_test_gt_path):
            os.makedirs(total_test_gt_path)

        shutil.copy(oldname, newname)
        shutil.copy(oldname1, newname1)
        print(index)
    print('------------complete test_dataset-------------')

    with open('/home/user/czr/nullmax_data/2018-10&12/json_file/total_train.json', 'a') as f:
        for i in range(3590):                   # 2018-10-11-->5171; 2018-12-18-->3239; 2019-05-08-->3590;
            content = dict[i]
            d = json.dumps(content)
            f.write(d)
            #f.write('\n')
            #guide only when write the last json
            if i != 3589:
                f.write('\n')

    with open('/home/user/czr/nullmax_data/2018-10&12/json_file/total_test.json', 'a') as f:
        for i in range(351):                    # 2018-10-11-->505; 2018-12-18-->317; 2019-05-08-->351;
            content = dict[i+3590]              # 2018-10-11-->5171; 2018-12-18-->3239; 2019-05-08-->3590;
            d = json.dumps(content)
            f.write(d)
            #f.write('\n')
            # guide only when write the last json
            if i != 350:
                f.write('\n')
    print('------------complete json_file-------------')

if __name__ == '__main__':
    img_path = '/home/user/czr/nullmax_data/2019-05-08-22-14/DATASET/data/'
    gt_path = '/home/user/czr/nullmax_data/2019-05-08-22-14/DATASET/Labels/'
    json_file = '/home/user/czr/nullmax_data/2019-05-08-22-14/json_file/lane_params.json'

    total_img_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/img/'
    total_test_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/test/'
    total_train_gt_path = '/home/user/czr/nullmax_data/2018-10&12/LaneLabels/total_train_Labels/'
    total_test_gt_path = '/home/user/czr/nullmax_data/2018-10&12/LaneLabels/totoal_test_Labels/'

    main(img_path, total_img_path, total_test_path, gt_path, total_train_gt_path, total_test_gt_path, json_file)