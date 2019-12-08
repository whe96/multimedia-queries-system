import numpy as np
import cv2
import subprocess
import os


def read_image(path, width, height, BGR_mode=False):
    with open(path, 'rb') as fr:
        img = np.fromfile(fr, dtype=np.uint8)
        img = img.reshape((3, height, width))
        img = np.transpose(img, (1, 2, 0))
        if BGR_mode:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img.astype(np.uint8)
        return img


def images2video(frames, filename):
    capSize = (352, 288)  # this is the size of my source video
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, capSize, 1)

    for frame in frames:
        out.write(frame)
    out.release()


def read_video(folder, width, height):
    frames = []
    names = sorted([name for name in os.listdir(folder) if 'rgb' in name])
    for name in names:
        img_path = os.path.join(folder, name)
        frame = read_image(img_path, width, height)
        frames.append(frame)
    print("Found {:d} frames".format(len(frames)))
    return frames


def merge_audio_video(video, audio, output):
    cmd = "ffmpeg -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(video, audio, output)
    subprocess.call(cmd, shell=True)


def generate_video(dir, name, output_dir):
    folder = os.path.join(dir, name)
    frames = read_video(folder, 352, 288)
    audio = os.path.join(folder, "{}.wav".format(name))
    tmp = os.path.join(output_dir, "tmp.mp4")
    output = os.path.join(output_dir, "{}.mp4".format(name))
    images2video(frames, tmp)
    merge_audio_video(tmp, audio, output)
    os.system("rm {}".format(tmp))
    print("Generate video {}".format(folder))

def preprocess():
    output_dir = "/Users/jiarongqiu/Desktop/CS576/Final/output_videos/"

    dir = "/Users/jiarongqiu/Desktop/CS576/Final/database_videos/"
    subs = ["flowers","interview","movie","musicvideo","sports","starcraft","traffic"]
    for sub in subs:
        generate_video(dir, sub, output_dir)

    dir = "/Users/jiarongqiu/Desktop/CS576/Final/query/"
    subs = ["first", "second"]
    for sub in subs:
        generate_video(dir, sub, output_dir)

    dir = "/Users/jiarongqiu/Desktop/CS576/Final/query_videos_2/SeenExactMatch"
    subs = ["Q3", "Q4", "Q5"]
    for sub in subs:
        generate_video(dir, sub, output_dir)

    dir = "/Users/jiarongqiu/Desktop/CS576/Final/query_videos_2/SeenInexactMatch"
    subs = ["HQ1", "HQ2", "HQ4"]
    for sub in subs:
        generate_video(dir, sub, output_dir)


if __name__ == '__main__':
    preprocess()
