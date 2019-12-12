import cv2
import numpy as np
import os
import glob
import collections
from scipy import spatial
from utils import read_image_folder, timeit
from test import simulate_similarity


class Motion:

    def __init__(self, dir, feature_dir, mode="average"):
        self.dir = dir
        self.featrue_dir = feature_dir
        self.features = {}
        self.mode = mode

    @timeit
    def motion_search(self, imgs, fps=10):
        span = int(30 / fps)
        features = self.extract_features(imgs)
        l = features.shape[0]
        res = collections.defaultdict(list)
        for name in sorted(self.features):
            features2 = self.features[name]
            idx = 0
            while idx < features2.shape[0]:
                similarity = self.compare(features, features2[idx:idx + l])
                res[name].append(similarity)
                idx += span
        return res

    def compare(self, features1, features2):
        mode = self.mode
        if mode == "exact":
            l = min(features1.shape[0], features2.shape[0])
            res = []
            for t in range(l):
                if not features1[t].any() or not features2[t].any():
                    res.append(0)
                else:
                    # print(sum(features1[t]),sum(features2[t]))
                    similarity = (2 - spatial.distance.cosine(features1[t], features2[t]))/2
                    res.append(similarity)
            return sum(res) / len(res)
        elif mode == "average":
            feature1 = np.average(features1, axis=0)
            feature2 = np.average(features2, axis=0)
            return (2 - spatial.distance.cosine(feature1, feature2))/2
        elif mode == "max":
            feature1 = np.amax(features1, axis=0)
            feature2 = np.amax(features2, axis=0)
            return (2 - spatial.distance.cosine(feature1, feature2))/2
        else:
            raise ValueError("Unknown mode {}".format(mode))

    def extract_features(self, imgs):
        imgs = [cv2.resize(img, dsize=(64, 80)) for img in imgs]

        res = []
        prvs = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)

        for img in imgs[1:]:
            next = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 16, 15, 3, 5, 1.2, 0)

            x, y = flow[..., 0], flow[..., 1]

            feature = np.hstack([x.flatten(), y.flatten()])
            res.append(feature)
            prvs = next

        res = np.array(res)
        return res

    def preprocess(self):
        videos = glob.glob(os.path.join(self.dir, '*'))
        for video in videos:
            name = os.path.basename(video)
            output_filename = os.path.join(self.featrue_dir, name + '.npy')
            imgs = read_image_folder(video, extension="rgb")
            features = self.extract_features(imgs)
            print(name, features.shape)
            np.save(output_filename, features)

    def load(self):
        features = glob.glob(os.path.join(self.featrue_dir, '*'))
        for feature in features:
            name = os.path.basename(feature).split('.')[0]
            npy = np.load(feature)
            self.features[name] = npy
        print("Finish loading motion features from {}".format(features))

    def second_to_frame(self, second, start_idx=0, max_idx=599, fps=30):
        frame_idx = int(second * fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

    @timeit
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
    dir = "data/dataset"
    feature_dir = "feature/optical_flow"
    motion = Motion(dir, feature_dir,mode="exact")
    # motion.preprocess()
    motion.load()
    motion.random_validation(100)
