#coding=utf-8
#读取label中像素点的B, G, R值
import os
import cv2
import numpy as np


def read_RGB(data_path):
    dirs = os.listdir(data_path)
    num = 0
    for d in dirs:
        num += 1
        img_path = os.path.join(data_path, d)
        img = np.array(cv2.imread(img_path))
        sp = img.shape
        height, width = sp[0], sp[1]
        for i in range(height):
            tmp = []
            for j in range(width):
                if img[i, j ,0] != 0 or img[i, j, 1] != 0 or img[i, j, 2] != 0:         #判断像素值是否为0
                    tmp.append([i, j])
            if tmp != []:
                with open("%s pixel_coordinate.txt"%d, 'a') as f:
                    f.write(str(tmp))                                                   #按行记录坐标
                    f.write("\n")
        print("Finished read No.%s pixel coordinate"%num)
    return num

if __name__ == '__main__':
    data_path = "/xxx/xxx/xxx/"                                  #添加自己的路径
    read_RGB(data_path)