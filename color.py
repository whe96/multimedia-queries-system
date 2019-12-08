import cv2
import numpy as np
from scipy import spatial
from utils import read_image


def cal_color_histogram(img):
    channelR = cv2.calcHist([img],[0],None,[256],[0,256])
    channelG = cv2.calcHist([img], [0], None, [256], [0, 256])
    channelB = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist = np.hstack([channelR,channelG,channelB]).flatten()
    return hist

if __name__ == '__main__':
    paths = [
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/flowers/flowers001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/interview/interview001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/movie/movie001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/musicvideo/musicvideo001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/sports/sports001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/starcraft/starcraft001.rgb",
        "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/traffic/traffic001.rgb"
    ]
    features = []
    for path in paths:
        img = read_image(path,352,288)
        feature = cal_color_histogram(img)
        features.append(feature)
    for i in range(len(features)):
        for j in range(i,len(features)):
            similarity = 1 - spatial.distance.cosine(features[j], features[i])
            print(i,j,similarity)