#coding=utf-8

import os
import json
import numpy as np
import cv2
from PIL import  Image

def Perspective_Transform_matrix(sy1, sy2, sy3, sy4, sx1, sx2, sx3, sx4):
    src = np.float32([[sx1/1920.0, sy1/1208.0], [sx2/1920.0, sy2/1208.0],
                      [sx3/1920.0, sy3/1208.0], [sx4/1920.0, sy4/1208.0]])
    dst = np.float32([[870/1920.0, 0/1208.0], [1185/1920.0, 0/1208.0],
                      [870/1920.0, 1208/1208.0], [1185/1920.0, 1208/1208.0]])
    M = cv2.getPerspectiveTransform(src, dst)
    M_inv = cv2.getPerspectiveTransform(dst, src)
    src1 = np.float32([[sx1, sy1], [sx2, sy2], [sx3, sy3], [sx4, sy4]])
    dst1 = np.float32([[870, 0], [1185, 0], [870, 1207], [1185, 1207]])
    M1 = cv2.getPerspectiveTransform(src1, dst1)
    M1_inv = cv2.getPerspectiveTransform(dst1, src1)
    return M, M_inv, M1, M1_inv

def draw_ego_lane(img_path, save_path, egolane_json_path):
    dict = [json.loads(line) for line in open(egolane_json_path).readlines()]
    for i in range(len(dict)):
        x_list1, x_list2 = [], []
        y_list1, y_list2 = [], []
        coord = dict[i]['c']
        name = dict[i]['filename']
        name = name.replace(".", "_rcb.")
        for j in range(len(coord[0])):
            x_list1.append(coord[0][j])
            y_list1.append(coord[1][j])
        gr_coord1 = [[x_coord, y_coord] for (x_coord, y_coord) in zip(x_list1, y_list1)]
        img = cv2.imread(img_path + name)
        im1 = cv2.polylines(img, [np.int32(gr_coord1)], isClosed=False, color=(0, 255, 0), thickness=1)
        for j in range(len(coord[2])):
            x_list2.append(coord[2][j])
            y_list2.append(coord[3][j])
        gr_coord2 = [[x_coord, y_coord] for (x_coord, y_coord) in zip(x_list2, y_list2)]
        im2 = cv2.polylines(im1, [np.int32(gr_coord2)], isClosed=False, color=(0, 255, 0), thickness=1)
        im = Image.fromarray(np.uint8(im2))
        im.save(save_path + name)
        print(i)

def Get_Perspective_img(img_path, M1, dx, dy, save_path):
    dirs = os.listdir(img_path)
    count = 0
    for d in dirs:
        srcimg = cv2.imread(img_path+d)                          # --->original shape [960, 1280, 3]
        res = cv2.warpPerspective(srcimg, M1, (dx, dy))
        img = Image.fromarray(np.uint8(res))

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        img.save(save_path + d)
        count += 1
        print("complete No.%d"%count)
    return count

def get_gt_params(pimg_path, egolane_json_path, M):
    #pinmg_path: img after perspective transform
    #egolane_json_path: json file about ego lane
    dict = [json.loads(line) for line in open(egolane_json_path).readlines()]
    params = []
    for i in range(len(dict)):
        coord = dict[i]['c']
        name = dict[i]['filename']
        name = name.replace(".", "_rcb.")
        img = cv2.imread(pimg_path + name)

        #coord[0], coord[1] = sample_more_points(coord[0], coord[1])
        #coord[2], coord[3] = sample_more_points(coord[2], coord[3])

        iml, pal = draw_gt_lane(img, M, coord[0], coord[1])
        imr, par = draw_gt_lane(iml, M, coord[2], coord[3])

        params.append([pal, par, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        im = Image.fromarray(np.uint8(imr))
        im.save('/home/user/czr/nullmax_data/2018-10&12/ground_lane/2018-12-18' + '/' + name)
    return params

def sample_more_points(x_list, y_list):
    x_res, y_res = [], []
    for i in range(len(x_list) - 1):
        x_tmp = [x_list[i], x_list[i + 1]]
        y_tmp = [y_list[i], y_list[i + 1]]
        params = np.polyfit(y_tmp, x_tmp, 1)
        params = params.tolist()
        a, b = [*params]
        y_start, y_stop = y_list[i + 1], y_list[i]
        y_prime = np.linspace(y_start, y_stop, 5)
        x_pred = a * y_prime + b
        for x, y in zip(x_pred.tolist(), y_prime.tolist()):
            x_res.append(x)
            y_res.append(y)
        coord = [(xcord, ycord) for (xcord, ycord) in zip(x_pred, y_prime)]
    x_list += x_res
    y_list += y_res
    return x_list, y_list

def draw_gt_lane(img, M, x_c, y_c):
    #img: IPM
    #M: perspective transform matrix
    #x_c & y_c:  coordinate in original image
    x_list, y_list = [], []
    img_coord = [[x, y] for (x, y) in zip(x_c, y_c) if y>540]
    for j in range(len(img_coord)):
        tmp = [[img_coord[j][0]/1920.0], [img_coord[j][1]/1207.0], [1.0]]
        tmp1 =np.array(tmp)
        res = np.dot(M, tmp1)
        res = res.tolist()
        x_list.append(res[0][0]/res[2][0])
        y_list.append(1-res[1][0]/res[2][0])
    pa = np.polyfit(y_list, x_list, 2)
    pa = pa.tolist()
    y_prime = np.linspace(0, 0.7, 20)
    p = [0] * (4 - len(pa)) + pa
    d, a, b, c = [*p]
    x_pred = d * (y_prime ** 3) + a * (y_prime) ** 2 + b * (y_prime) + c
    x_pred = x_pred * 1919
    y_prime = (1-y_prime) * 1207
    lane = [(xcord, ycord) for (xcord, ycord) in zip(x_pred, y_prime)]
    im = cv2.polylines(img, [np.int32(lane)], isClosed=False, color=(0, 255, 0), thickness=1)
    return im, pa

#add params to json file
def add_to_json(old_json_path, new_json_path, params):
    count = 0

    lane_list = [json.loads(line) for line in open(old_json_path).readlines()]

    with open(new_json_path, 'w') as fn:
        for i in range(len(lane_list)):
            count += 1
            lane_list[i]['params'] = params[i]
            d = json.dumps(lane_list[i])
            fn.write(d)
            if i != len(lane_list)-1:
                fn.write('\n')
            print("complete No.%d" % count)


if __name__ == '__main__':
    sy1, sy2, sy3, sy4 = 620, 620, 1207, 1207
    sx1, sx2, sx3, sx4 = 890, 1185, 40, 1850
    dx, dy = 1920, 1208
    img_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/data12/rcb12/2018-12-18/'
    pimg_path = '/home/user/czr/nullmax_data/2018-10&12/Perspective_img/2018-12-18/'
    egolanesave_path = '/home/user/czr/nullmax_data/2018-10&12/ego_lane/2018-12-18/'

    egolane_json_path = '/home/user/czr/nullmax_data/2018-10&12/json_file/2018-12/lane-2018-12-18.json'
    total_json_path = '/home/user/czr/nullmax_data/2018-10&12/json_file/2018-12/lane_params.json'

    M, M_inv, M1, M1_inv = Perspective_Transform_matrix(sy1, sy2, sy3, sy4, sx1, sx2, sx3, sx4)
    #draw_ego_lane(img_path, egolanesave_path, egolane_json_path)
    count = Get_Perspective_img(img_path, M1, dx, dy, pimg_path)
    params = get_gt_params(pimg_path, egolane_json_path, M)
    add_to_json(egolane_json_path, total_json_path, params)