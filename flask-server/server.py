from flask import Flask, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/queries')
def get_queries():
    q = './queries'
    f = filter(lambda x: os.path.isdir(os.path.join(q, x)), os.listdir(q))
    folders = sorted([str(folder) for folder in f])
    return jsonify({'folders': folders})

@app.route('/results/<dirr>/<color>/<motion>/<sound>/<xxx>')
def get_results(dirr, color, motion, sound, xxx):
    result_dirs = ['flowers', 'interview', 'movie', 'musicvideo', 'traffic']
    similarities = [[i]*600 for i in range(5)]
    results = [{'dir': r, 'data': s} for r, s in zip(result_dirs, similarities)]
    return jsonify(results)
