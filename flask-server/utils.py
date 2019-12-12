import numpy as np
import cv2
import subprocess
import os
import time
import glob


def read_image_folder(folder,extension,width=352,height=288):
    if extension == "rgb":
        img_paths = sorted(glob.glob(os.path.join(folder,"*."+extension)))
        res = []
        for img_path in img_paths:
            img = read_image(img_path,width,height)
            res.append(img)
        return res
    elif extension == "jpg":
        img_paths = sorted(glob.glob(os.path.join(folder, "*." + extension)))
        res = []
        for img_path in img_paths:
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            res.append(img)
        return res

    else:
        raise ValueError("Unknown extension {}".format(extension))


def read_image(path, width, height, mode='RGB'):
    with open(path, 'rb') as fr:
        img = np.fromfile(fr, dtype=np.uint8)
        img = img.reshape((3, height, width))
        img = np.transpose(img, (1, 2, 0))
        if mode == 'RGB':
            pass
        elif mode == 'BGR':
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif mode == 'YCrCb':
            img = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
        img = img.astype(np.uint8)
        return img


def images2video(frames, filename):
    capSize = (352, 288)  # this is the size of my source video
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, capSize, 1)

    for frame in frames:
        out.write(frame)
    out.release()


def read_video(folder, width, height,mode="RGB"):
    frames = []
    names = sorted([name for name in os.listdir(folder) if 'rgb' in name])
    for name in names:
        img_path = os.path.join(folder, name)
        frame = read_image(img_path, width, height,mode)
        frames.append(frame)
    print("Found {:d} frames".format(len(frames)))
    return frames


def merge_audio_video(video, audio, output):
    cmd = "ffmpeg -i {} -i {} -c:a aac -vcodec libx264 -y -strict experimental -loglevel quiet {}".format(video, audio, output)
    subprocess.call(cmd, shell=True)


def generate_video(dir, name, output_dir):
    folder = os.path.join(dir, name)
    frames = read_video(folder, 352, 288,mode="BGR")
    audio = os.path.join(folder, "{}.wav".format(name))
    tmp = os.path.join(output_dir, "tmp.mp4")
    output = os.path.join(output_dir, "{}.mp4".format(name))
    images2video(frames, tmp)
    merge_audio_video(tmp, audio, output)
    os.system("rm {}".format(tmp))
    print("Generate video {}".format(folder))






def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


if __name__ == '__main__':
    # query_preprocess()
    imgs = read_image_folder("data/test/ellenshow1","jpg")
