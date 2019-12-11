from flask import Flask, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os
import random

from main import VideoSearchEngine
from utils import generate_video

app = Flask(__name__)
CORS(app)

dirr = "data/dataset"
color_dir = "feature/color"
semantic_dir = "feature/resnet_resize"
audio_dir = "feature/mfcc"
engine = VideoSearchEngine(dirr, color_dir, semantic_dir, audio_dir)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/queries')
def get_queries():
    q = './queries'
    f = filter(lambda x: os.path.isdir(os.path.join(q, x)), os.listdir(q))
    folders = sorted([str(folder) for folder in f])
    for folder in folders:
        generate_video(dir="./queries", name=folder, output_dir="./static/")
    return jsonify({'folders': folders})

@app.route('/results/<dirr>/<color>/<motion>/<sound>/<semantic>')
def get_results(dirr, color, motion, sound, semantic):
    results = engine.search_folder("./queries/"+dirr, 
        weights=[int(color), int(motion), int(sound), int(semantic)])

    #result_dirs = ['flowers', 'interview', 'movie', 'musicvideo', 'traffic']
    #similarities = [[random.randint(0,100) for _ in range(200)] for i in range(5)]
    #results = [{'dir': r, 'data': s, 'score': 95}
    #    for r, s in zip(result_dirs, similarities)]
    return jsonify(results)
