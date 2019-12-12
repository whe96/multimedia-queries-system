import torch
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
import glob
import os
import collections
from utils import read_image_folder, timeit
from scipy import spatial
from test import simulate_similarity
from PIL import Image


class ResNet:

    def __init__(self, dir, feature_dir, width, height, batch_size=8, fps=6,mode="exact"):
        self.dir = dir
        self.feature_dir = feature_dir
        self.width = width
        self.height = height
        self.batch_size = batch_size
        self.fps = fps
        self.mode = mode

        self.resnet18 = models.resnet18(pretrained=True)
        feature_extractor = torch.nn.Sequential(*list(self.resnet18.children())[:-1])
        feature_extractor.eval()
        self.feature_extractor = feature_extractor

        self.features = {}
        self.transform = transforms.Compose([
            transforms.Resize(224),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        self.crop = transforms.CenterCrop(size=224)

    @timeit
    def semantic_search(self, imgs, fps=10):
        features1 = self.extract_feature(imgs)
        span = 1 / fps
        res = collections.defaultdict(list)
        for name in sorted(self.features.keys()):
            t = 0
            while t < 20:
                idx = self.second_to_frame(t)
                end_idx = self.second_to_frame(t + 5)
                features2 = self.features[name][idx:end_idx]
                features2 = np.array([features2[i] for i in range(features2.shape[0]) if i % self.fps == 0])
                similarity = self.compare(features1, features2)
                res[name].append(similarity)
                t += span
        return res

    def compare(self, features1, features2):
        if self.mode == "exact":
            _min = min(features1.shape[0], features2.shape[0])
            res = []
            for i in range(_min):
                res.append((2 - spatial.distance.cosine(features1[i], features2[i]))/2)
            return sum(res) / len(res)
        elif self.mode == "average":
            feature1 = np.average(features1,axis=0)
            feature2 = np.average(features2,axis=0)
            return (2 - spatial.distance.cosine(feature1, feature2))/2

    def random_compare(self, video1, start1, video2, start2):
        start_idx1 = self.second_to_frame(start1)
        end_idx1 = self.second_to_frame(start1 + 5)
        features1 = self.features[video1][start_idx1:end_idx1]
        start_idx2 = self.second_to_frame(start2)
        end_idx2 = self.second_to_frame(start2 + 5)
        features2 = self.features[video2][start_idx2:end_idx2]
        return self.compare(features1, features2)

    def second_to_frame(self, second, start_idx=0, max_duration=20):
        max_idx = max_duration * self.fps
        frame_idx = int(second * self.fps) + start_idx
        if frame_idx > max_idx:
            frame_idx -= 1
        return frame_idx

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
            imgs = read_image_folder(video,extension="rgb")
            features = self.extract_feature(imgs)
            print(name, features.shape)
            np.save(output_filename, features)

    @timeit
    def extract_feature(self, imgs):
        imgs = [imgs[i] for i in range(len(imgs)) if i % int(30/self.fps) == 0]
        with torch.no_grad():
            res = []
            frames = []
            idx = 0
            for img in imgs:
                idx += 1
                img = Image.fromarray(img)
                img = self.transform(img)
                frames.append(img)
                if idx == self.batch_size:
                    frames = torch.stack(frames)
                    features = self.feature_extractor(frames).squeeze().numpy()
                    frames = []
                    idx = 0
                    res.append(features)
            if idx:
                frames = torch.stack(frames)
                features = self.feature_extractor(frames).squeeze().numpy()
                res.append(features)
            res = np.vstack(res)
            return res

    def random_validation(self, num_iters=100):
        return simulate_similarity(self.random_compare, num_iters)


if __name__ == '__main__':
    dir = "data/dataset"
    feature_dir = "feature/resnet_resize"
    resnet = ResNet(dir, feature_dir, 352, 288,mode="average")
    # resnet.preprocess()
    resnet.load()
    resnet.random_validation(100)
    # print(resnet.compare("starcraft",0,"starcraft",8))
