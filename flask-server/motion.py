import cv2
import math
import numpy as np
import os
import glob
import collections
from scipy import spatial
from utils import read_image, read_image_folder, timeit
from test import simulate_similarity

class Motion:

    def __init__(self, mode="average"):
        self.features = {}
        self.mode = mode
        self.weights = [1, 1, 1]


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
        return

    def compare(self, features1, features2):
        mode = self.mode
        if mode == "exact":
            l = min(features1.shape[0], features2.shape[0])
            res = []
            for t in range(l):
                tmp = 1 - spatial.distance.cdist(features1[t], features2[t], metric='cosine')
                similarity = sum([x * y / sum(self.weights) for x, y in zip([tmp[0][0], tmp[1][1], tmp[2][2]], self.weights)])
                res.append(similarity)
            return sum(res) / len(res)
        elif mode == "average":
            feature1 = np.average(features1, axis=0)
            feature2 = np.average(features2, axis=0)
            res = []
            for c in range(feature1.shape[0]):
                res.append(1 - spatial.distance.cosine(feature1[c], feature2[c]))
            return sum([x * y for x, y in zip(res, self.weights)]) / sum(self.weights)
        else:
            raise ValueError("Unknown mode {}".format(mode))



    def extract_features(self, imgs):
        mode = "imgFlow"

        res = []
        if (mode == "imgFlow"):
            tmpImg = cv2.resize(imgs[0], dsize=(64, 80))
            prvs  = cv2.cvtColor(tmpImg, cv2.COLOR_BGR2GRAY)
        else:
            prvs = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)

        counter = 0

        for img in imgs:
            if (counter < 1):
                counter+=1
                continue
            if (mode == "imgFlow"):
                imgResize = cv2.resize(img, dsize=(64, 80))
                next = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)
                flowNext = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 16, 15, 3, 5, 1.2, 0)

                xNext = flowNext[..., 0]
                yNext = flowNext[..., 1]

                XYDimen = np.vstack([xNext.flatten(), yNext.flatten()])
                res.append(XYDimen)
                prvs = next
                counter += 1

        res = np.array(res)
        print(res)
        return res


    def preprocess(self):
        videos = glob.glob(os.path.join('video database', '*'))
        # videos = 'video database'
        for video in videos:
            name = os.path.basename(video)
            output_filename = os.path.join('feature_dir', name)
            imgs = read_image_folder(video, extension="rgb")
            features = self.extract_features(imgs)
            print(name, features.shape)
            np.save(output_filename, features)

    def load(self):
        features = glob.glob(os.path.join('feature_dir', '*'))
        for feature in features:
            name = os.path.basename(feature).split('.')[0]
            npy = np.load(feature)
            self.features[name] = npy
        print("Finish loading motion features from {}".format(features))

    def second_to_frame(self, second, start_idx=1, max_idx=600, fps=30):
        frame_idx = int(second * fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

    def random_compare(self, video1, start1, video2, start2):
        start_idx1 = self.second_to_frame(start1)
        end_idx1 = self.second_to_frame(start1 + 5)
        features1 = self.features[video1][start_idx1:end_idx1]

        start_idx2 = self.second_to_frame(start2)
        end_idx2 = self.second_to_frame(start2 + 5)
        features2 = self.features[video2][start_idx2:end_idx2]

        similarity = self.compare(features1, features2)
        return similarity

    def random_validation(self, num_iters):
        return simulate_similarity(self.random_compare, num_iters=num_iters)

if __name__ == '__main__':
    optical = Motion()
    video = 'video database/interview'

    optical.load()

    # optical.preprocess()
    # color.load()
    optical.random_validation(1000)
