import os
import glob
import shutil
from utils import generate_video


def query_preprocess():
    output_dir = "/Users/jiarongqiu/Desktop/CS576/Final/output_videos/"

    dir = "/data/dataset/"
    subs = ["flowers", "interview", "movie", "musicvideo", "sports", "starcraft", "traffic"]
    for sub in subs:
        generate_video(dir, sub, output_dir)

    dir = "data/query/"
    subs = ["first", "second"]+["Q3", "Q4", "Q5"]+["HQ1", "HQ2", "HQ4"]
    for sub in subs:
        generate_video(dir, sub, output_dir)

def test_preprocess():
    dir = "data/test"
    videos = sorted(glob.glob(os.path.join(dir, "*.flv")))
    duration = 30
    for video in videos:
        name = os.path.basename(video).split('.')[0]
        folder = os.path.join(dir,name)
        shutil.rmtree(folder)
        os.mkdir(folder)
        cmd = "ffmpeg -i {} -s 352x288 -y -r 30 -t {} {}/{}%03d.jpg".format(video,duration,folder,name)
        print(cmd)
        os.system(cmd)
        cmd = "ffmpeg -i {} -y -t {} {}/{}.wav".format(video,duration,folder,name)
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    # query_preprocess()
    test_preprocess()
