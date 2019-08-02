#coding=utf-8
#读取json文件中所需的坐标信息

import os
import json

def read_json_coordinate(img_path, json_path, save_path):
      count = 0
      f = open(json_path, 'r')
      dict = json.loads(f.read())
      f.close()
      dirs = os.listdir(img_path)
      with open(save_path, 'w') as f:
          for ix in range(len(dirs)):
              dirs[ix] = dirs[ix].replace('_rcb.', '.')
          for i in range (len(dict)):
              if dict[i]['filename'] in dirs:
                  count += 1
                  tmp = []
                  for j in range(len(dict[i]['annotations'])):
                      if dict[i]['annotations'][j]['class'] != ["dot-lane"]:
                          x_list = dict[i]['annotations'][j]['xn'].split(';')
                          y_list = dict[i]['annotations'][j]['yn'].split(';')
                          l = [[float(x), float(y)] for x, y in zip(x_list, y_list)]
                          l.sort(key=lambda k: k[1], reverse=True)              #every lane in the same img:Arranged in descending order of y_coordinate
                          tmp.append(l)
                  tmp.sort()                                           #all lanes in the same img:Arranged in descending order of first_x_coordinate
                  tmp1 = []
                  for m in range(len(tmp)):
                      if tmp[m][0][1] > 900.0:
                          tmp1.append(tmp[m])
                  for p in range(len(tmp1)-1):
                      if tmp1[p][0][0] < 960.0 and tmp1[p+1][0][0] > 960.0:
                          coordinate =[[tmp1[p][i][0] for i in range(len(tmp1[p]))],
                                       [tmp1[p][i][1] for i in range(len(tmp1[p]))],
                                       [tmp1[p+1][i][0] for i in range(len(tmp1[p+1]))],
                                       [tmp1[p+1][i][1] for i in range(len(tmp1[p+1]))]]
                          d = {}
                          d['filename'] = dict[i]['filename']
                          d['c'] = coordinate
                          d = json.dumps(d)
                          f.write(d)
                          if count != len(dirs):
                              f.write('\n')
                          print("complete No.%d" % count)


if __name__ == "__main__":
    img_path = '/home/user/czr/nullmax_data/2018-10&12/DATASET/data12/rcb12/2018-12-18/'
    json_path = "/home/user/czr/nullmax_data/2018-10&12/json_file/2018-12/2018-12-18-13-49.json"
    save_path = '/home/user/czr/nullmax_data/2018-10&12/json_file/2018-12/lane-2018-12-18.json'
    read_json_coordinate(img_path, json_path, save_path)