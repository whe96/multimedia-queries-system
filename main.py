import os
from semantic import ResNet
from color import Color
from audio import Audio
from test import simulate_similarity
from utils import read_image_folder, timeit
import collections
from multiprocessing.pool import ThreadPool


class VideoSearchEngine:
    width = 352
    height = 288

    @timeit
    def __init__(self, dir, color_dir, semantic_dir, audio_dir):
        color = Color(dir, color_dir, 352, 288, color_space="RGB", mode="average", bins=32)
        color.load()

        resnet = ResNet(dir, semantic_dir, 352, 288)
        resnet.load()

        audio = Audio(dir, audio_dir, mode="max")
        audio.load()

        self.audio = audio
        self.resnet = resnet
        self.color = color

    """
        input: folder path,weights(optional)
        return: [{dir:,data:,score:}}
    """

    @timeit
    def search_folder(self, folder, weights=None, extension="rgb"):
        if not os.path.exists(folder):
            raise ValueError("Folder {} not exists".format(folder))
        name = os.path.basename(folder)
        audio_filename = os.path.join(folder, name + ".wav")
        imgs = read_image_folder(folder, extension, width=self.width, height=self.height)[:150]
        print(len(imgs))

        # threading pool
        print(os.cpu_count())
        pool = ThreadPool(processes=None)
        color_thread = pool.apply_async(self.color.color_search, [imgs])
        audio_thread = pool.apply_async(self.audio.audio_search, [audio_filename])
        semantic_thread = pool.apply_async(self.resnet.semantic_search, [imgs])
        color_similarity = color_thread.get()
        audio_similarity = audio_thread.get()
        semantic_similarity = semantic_thread.get()

        # color_similarity = self.color.search(imgs)
        # audio_similarity = self.audio.search(audio_filename)
        # semantic_similarity = self.resnet.search(imgs)

        if not weights:
            weights = [1, 1, 1, 1]
        similarities = collections.defaultdict(list)
        for name in sorted(color_similarity.keys()):
            print("Name {} Color {} Audio {} Semantic {}".format(name, sum(color_similarity[name]) / len(
                color_similarity[name]), sum(audio_similarity[name]) / len(audio_similarity[name]),
                                                                 sum(semantic_similarity[name]) / len(
                                                                     semantic_similarity[name])))
            for t in range(len(color_similarity["flowers"])):
                color_simi = color_similarity[name][t]
                semantic_simi = semantic_similarity[name][t]
                audio_simi = audio_similarity[name][t]
                motion_simi = 0
                simi = (weights[0] * color_simi + weights[1] * motion_simi + weights[2] * audio_simi + weights[
                    3] * semantic_simi) / sum(weights)
                similarities[name].append(simi)
        scores = []
        for name in similarities:
            scores.append((name, sum(similarities[name]) / len(similarities[name])))
        scores.sort(key=lambda x: x[1], reverse=True)

        res = []
        for name, score in scores:
            # res.append({"dir": name, "score": score, "data": similarities[name]})
            res.append({"dir": name, "score": score, "data": None})
        return res


if __name__ == '__main__':
    dir = "data/dataset"
    color_dir = "feature/color"
    semantic_dir = "feature/resnet_resize"
    audio_dir = "feature/mfcc"
    engine = VideoSearchEngine(dir, color_dir, semantic_dir, audio_dir)
    # print(engine.search_folder("data/query/first"))
    print(engine.search_folder("data/test/ellenshow3", extension='jpg'))
