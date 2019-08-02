#coding=utf-8

import os
import json
from PIL import Image

img_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/data12/rcb12/2018-12-18/'
ground_lane_path = '/home/user/czr/nullmax_data/2018-10&12/ground_lane/2018-12-18/'
#gt_path = '/home/user/czr/nullmax_data/LaneLabels/2017-07-01/'
#egolane_json_path = '/home/user/czr/nullmax_data/ego_lane_json/lane-2017-07-01.json'
#dirs = os.listdir(img_path)
dirs1, dirs2 = os.listdir(img_path), os.listdir(ground_lane_path)
#f = open(egolane_json_path, 'r')
#dict = json.loads(f.read())
#f.close()
#tmp = []
#for i in range(len(dict)):
#    name = dict[i]['filename']
#    name = name.replace(".", "_rcb.")
#    tmp.append(name)

count = 0
for x in dirs1:
   if x not in dirs2:
       count += 1
       os.remove(os.path.join(img_path, x))
       print(count, x)

'''
img_path = '/home/user/czr/nullmax_data/2018-10&12/ground_lane/2018-12-18/'
egolane_json_path = '/home/user/czr/nullmax_data/2018-10&12/json_file/lane-2018-10-11.json'
dirs = os.listdir(img_path)
dict = [json.loads(line) for line in open(egolane_json_path).readlines()]

tmp = []
for i in range(len(dict)):
    name = dict[i]['filename']
    name = name.replace(".", "_rcb.")
    tmp.append(name)

count = 0
for x in dirs:
   if x in tmp:
       count += 1
       img_name = img_path + x
       img = Image.open(img_name).convert('RGB')
       img.save('/home/user/czr/nullmax_data/2018-10&12/DATASET/2018-10-11/' + x)
       #os.remove(os.path.join(img_path, x))
       print(count)
       '''