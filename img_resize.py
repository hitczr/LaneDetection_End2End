#coding=utf-8

import os
from PIL import Image
from torchvision import transforms


data_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/2018-10-11/'
path_list = os.listdir(data_path)
for index, name in enumerate(path_list):
    img_path = data_path + name
    img = Image.open(img_path).convert('RGB')
    img = img.crop([0, 128, 1920, 1208])
    img = img.resize((1280, 720), Image.ANTIALIAS)
    img.save(data_path + name)
    print(index+1)