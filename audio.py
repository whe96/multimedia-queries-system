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

    def __init__(self,dir,feature_dir,fps=100):
        self.dir = dir
        self.feature_dir = feature_dir
        self.fps = fps

        self.features = {}

    @timeit
    def search(self,filename,fps=10):
        span = 1/fps
        feature = self.extract_mfcc(filename)
        res = collections.defaultdict(list)

        for name in sorted(self.features.keys()):
            t = 0
            while t+5<20:
                idx = self.second_to_idx(t)
                end_idx = self.second_to_idx(t+5)
                simi = self.compare(feature,self.features[name][idx:end_idx])
                res[name].append(simi)
                t += span
        return res

    def compare(self,feature1,feature2,span=10):
        _min = min(feature1.shape[0],feature2.shape[0])
        feature1 = feature1[:_min]
        feature2 = feature2[:_min]
        res = []
        t = 0
        while t<_min:
            simi = 1-spatial.distance.cosine(feature1[t],feature2[t])
            res.append(simi)
            t += span
        return sum(res)/len(res)


    def second_to_idx(self,second, start_idx=1, max_idx=2000):
        frame_idx = int(second * self.fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

    def get_feature(self,name,start,end):
        start_idx = self.second_to_idx(start)
        end_idx = self.second_to_idx(end)
        features = self.features[name][start_idx:end_idx]
        feature = np.average(features,axis=0)
        return feature
    #
    # def compare(self, name1, start1, name2, start2):
    #     feature1 = self.get_feature(name1,start1,start1+5)
    #     feature2 = self.get_feature(name2,start2,start2+5)
    #     return 1 - spatial.distance.cosine(feature1, feature2)

    def load(self):
        features = glob.glob(os.path.join(self.feature_dir, '*'))
        for feature in features:
            name = os.path.basename(feature).split('.')[0]
            npy = np.load(feature)
            self.features[name] = npy
        print("Finish loading color features from {}".format(features))


    def extract_mfcc(self,filename):
        with torch.no_grad():
            waveform, sample_rate = torchaudio.load(filename)
            mfcc = torchaudio.transforms.MFCC(melkwargs={"n_fft":882})(waveform).numpy()[0].transpose(1,0) # use only single channel
            return mfcc

    # def preprocess(self):
    #     videos = glob.glob(os.path.join(self.dir, '*'))
    #     for video in videos:
    #         name = os.path.basename(video)
    #         output = os.path.join(self.feature_dir,name)
    #         filename = os.path.join(self.dir,name,"{}.wav".format(name))
    #         mfcc = self.extract_mfcc(filename)
    #         print(output,mfcc.shape)
    #         np.save(output,mfcc)
    #
    # def validate(self,num_iters=1000):
    #     simulate_similarity(self.compare,num_iters)
    #
    # def compare2(self,filename,start1,name,start2):
    #     features = self.extract_mfcc(filename)
    #     start_idx = self.second_to_idx(start1)
    #     end_idx = self.second_to_idx(start1+5)
    #     features = features[start_idx:end_idx]
    #     feature = np.average(features, axis=0)
    #     # feature = np.amax(features, axis=0)
    #     feature2 = self.get_feature(name, start2, start2 + 5)
    #     return 1 - spatial.distance.cosine(feature, feature2)

if __name__ == '__main__':
    dir = "data/dataset"
    feature_dir = "feature/mfcc"
    audio = Audio(dir,feature_dir)
    # audio.preprocess()
    audio.load()
    # print(audio.compare("interview",1,"interview",8))
    print(audio.compare2("data/test/sports2.wav",10,"sports",5))
    # audio.validate()
