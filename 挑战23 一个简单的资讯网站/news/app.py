import json
import os
from flask import Flask
from flask import render_template


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    text = {}
    path = '/home/shiyanlou/files'
    for file in os.listdir(path):
        with open(os.path.join(path, file)) as f_obj:
            text.setdefault(
                'titles', []).append(json.load(f_obj)['title'])
    return render_template('index.html', text=text)


@app.route('/files/<filename>')
def file(filename):
    json_file = '/home/shiyanlou/files/%s.json' % filename
    try:
        with open(json_file) as f_obj:
            text = json.load(f_obj)
    except FileNotFoundError:
        return render_template('404.html'), 404
    else:
        return render_template('file.html', text=text)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
