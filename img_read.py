#coding=utf-8

import cv2

img = cv2.imread('/home/user/czr/nullmax_data/2018-10&12/DATASET/2018-10-11/frame_vc1_7340_rcb.jpg')
cv2.imshow('s', img)
cv2.waitKey(0)
cv2.destroyAllWindows()