import torch
import torchaudio
import glob
import numpy as np
import os
import collections
from scipy import spatial
from test import simulate_similarity
from utils import timeit


class Audio:

    def __init__(self, dir, feature_dir, fps=100, mode="average",offset=10):
        self.dir = dir
        self.feature_dir = feature_dir
        self.fps = fps
        self.mode = mode
        self.offset = offset

        self.features = {}

    @timeit
    def audio_search(self, filename, compare_fps=10):
        span = 1 / compare_fps
        feature = self.extract_mfcc(filename)
        res = collections.defaultdict(list)
        for name in sorted(self.features.keys()):
            t = 0
            while t + 5 < 20:
                idx = self.second_to_idx(t)
                end_idx = self.second_to_idx(t + 5)
                simi = self.compare(feature, self.features[name][idx:end_idx])
                res[name].append(simi)
                t += span
        return res

    def compare(self, feature1, feature2):
        mode = self.mode
        if self.mode == "exact":
            _min = min(feature1.shape[0], feature2.shape[0])
            feature1 = feature1[:_min]
            feature2 = feature2[:_min]
            res = []
            t = 0
            while t < _min:
                simi = 1 - spatial.distance.cosine(feature1[t], feature2[t])
                res.append(simi)
                t += self.offset
            return sum(res) / len(res)
        elif self.mode == "average":
            feature1 = np.average(feature1, axis=0)
            feature2 = np.average(feature2, axis=0)
            return 1 - spatial.distance.cosine(feature1, feature2)
        elif self.mode == "max":
            feature1 = np.amax(feature1, axis=0)
            feature2 = np.amax(feature2, axis=0)
            return 1 - spatial.distance.cosine(feature1, feature2)
        else:
            raise ValueError("Unknown mode {}".format(self.mode))

    def second_to_idx(self, second, start_idx=0, max_idx=2000):
        frame_idx = int(second * self.fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

    def random_compare(self, name1, start1, name2, start2):
        start_idx1 = self.second_to_idx(start1)
        end_idx1 = self.second_to_idx(start1 + 5)
        feature1 = self.features[name1][start_idx1:end_idx1]

        start_idx2 = self.second_to_idx(start2)
        end_idx2 = self.second_to_idx(start2 + 5)
        feature2 = self.features[name2][start_idx2:end_idx2]
        similarity = self.compare(feature1, feature2)
        return similarity

    def extract_mfcc(self, filename):
        with torch.no_grad():
            waveform, sample_rate = torchaudio.load(filename)
            mfcc = torchaudio.transforms.MFCC(melkwargs={"n_fft": 882})(waveform).numpy()[0].transpose(1,0)  # use only single channel
            return mfcc

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
            output = os.path.join(self.feature_dir, name)
            filename = os.path.join(self.dir, name, "{}.wav".format(name))
            mfcc = self.extract_mfcc(filename)
            print(output, mfcc.shape)
            np.save(output, mfcc)

    def random_validation(self, num_iters=100):
        simulate_similarity(self.random_compare, num_iters)


if __name__ == '__main__':
    dir = "data/dataset"
    feature_dir = "feature/mfcc"
    audio = Audio(dir, feature_dir, mode="max")
    # audio.preprocess()
    audio.load()
    audio.random_validation(100)
