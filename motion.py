import cv2

from utils import read_image_folder



if __name__ == '__main__':
    imgs = read_image_folder("data/dataset/sports",extension='rgb')
    pre = cv2.cvtColor(imgs[0],cv2.COLOR_RGB2GRAY)
    next = cv2.cvtColor(imgs[1],cv2.COLOR_RGB2GRAY)
    cv2.imshow('test',imgs[0])
    cv2.waitKey(0)
    cv2.imshow('test',imgs[1])
    cv2.waitKey(0)
    flow = cv2.calcOpticalFlowFarneback(pre, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    x,y = flow[...,0],flow[...,1]

    cv2.imshow('test',x)
    cv2.waitKey(0)
    print(x.shape)