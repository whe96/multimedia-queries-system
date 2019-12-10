import cv2
import numpy as np
import os
import glob
import collections
from scipy import spatial
from utils import read_image, timeit
from test import simulate_similarity


class Color:

    def __init__(self, dir, feature_dir, width, height, color_space='RGB', bins=32):
        self.dir = dir
        self.feature_dir = feature_dir
        self.color_space = color_space
        self.bins = bins
        self.width = width
        self.height = height
        self.features = {}

        if color_space == 'RGB':
            self.weights = [1, 1, 1]
        elif color_space == 'YCrCb':
            self.weights = [2, 1, 1]

    @timeit
    def search(self, imgs, fps=10):
        span = int(30 / fps)
        feature = self.extract_features(imgs)
        l = feature.shape[0]
        res = collections.defaultdict(list)
        for name in sorted(self.features):
            feature2 = self.features[name]
            idx = 0
            while idx+l < feature2.shape[0]:
                similarity = self.compare(feature, feature2[idx:idx + l])
                res[name].append(similarity)
                idx += span
        return res

    def compare(self, features1, features2):
        if not features1.shape == features2.shape:
            raise ValueError("Feature shape not match {} vs {}".format(features1.shape, features2.shape))
        res = []
        for t in range(features1.shape[0]):
            tmp = 1-spatial.distance.cdist(features1[t],features2[t],metric='cosine')
            similarity = sum([x * y / sum(self.weights) for x, y in zip([tmp[0][0],tmp[1][1],tmp[2][2]], self.weights)])
            res.append(similarity)
        return sum(res)/len(res)


    def extract_features(self, imgs):
        res = []
        for img in imgs:
            channel1 = cv2.calcHist([img], [0], None, [self.bins], [0, 256]).flatten()
            channel2 = cv2.calcHist([img], [1], None, [self.bins], [0, 256]).flatten()
            channel3 = cv2.calcHist([img], [2], None, [self.bins], [0, 256]).flatten()
            hist = np.vstack([channel1, channel2, channel3])
            res.append(hist)
        res = np.array(res)
        return res

    """
        Output is 3 x bins
    """

    # @timeit
    def cal_color_histogram(self, img_path):
        img = read_image(img_path, self.width, self.height)
        channel1 = cv2.calcHist([img], [0], None, [self.bins], [0, 256]).flatten()
        channel2 = cv2.calcHist([img], [1], None, [self.bins], [0, 256]).flatten()
        channel3 = cv2.calcHist([img], [2], None, [self.bins], [0, 256]).flatten()
        hist = np.vstack([channel1, channel2, channel3])
        return hist

    def load(self):
        features = glob.glob(os.path.join(self.feature_dir, '*'))
        for feature in features:
            name = os.path.basename(feature).split('.')[0]
            npy = np.load(feature)
            self.features[name] = npy
        print("Finish loading color features from {}".format(features))

    def preprocess(self):
        videos = glob.glob(os.path.join(self.dir, '*'))
        for video in videos:
            name = os.path.basename(video)
            output_filename = os.path.join(self.feature_dir, name)
            res = []
            for i in range(1, 600 + 1):
                img_path = self.get_img_path(name, i)
                hist = self.cal_color_histogram(img_path)
                res.append(hist)
            res = np.array(res)
            print(name, res.shape)
            np.save(output_filename, res)

    def validate(self, num_ites=10):
        simulate_similarity(self.compare, num_ites)

    def get_img_path(self, name, idx):
        return os.path.join(self.dir, name, "{}{:03d}.rgb".format(name, idx))

    def second_to_frame(self, second, start_idx=1, max_idx=600, fps=30):
        frame_idx = int(second * fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

    @timeit
    def get_avg_histogram(self, video, start, query_duration=5):
        start_idx = self.second_to_frame(start)
        end_idx = self.second_to_frame(start + query_duration)
        hists = self.features[video][start_idx:end_idx]
        hists = np.average(hists, axis=0)
        return hists

    # def compare(self,video1,start1,video2,start2):
    #     feature1 = self.get_avg_histogram(video1,start1)
    #     feature2 = self.get_avg_histogram(video2,start2)
    #     res = []
    #     for i in range(feature1.shape[0]):
    #         res.append(1 - spatial.distance.cosine(feature1[i], feature2[i]))
    #     similarity = sum([x*y/sum(self.weights) for x,y in zip(res,self.weights)])
    #     return similarity


if __name__ == '__main__':
    dir = "data/dataset"
    outdir = "feature/color"
    color = Color(dir, outdir, 352, 288)
    # color.preprocess()
    color.load()
    # for i in [10,50,100,500,1000,2000,5000,10000]:
    #     color.validate(i)
    color.validate(1000)
