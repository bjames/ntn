from flask import Flask, render_template

import os
import config

app = Flask(__name__)

note_dir = os.fspath(config.renderer_config["output_directory"])
notes = [file for file in os.listdir(note_dir)]

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/<path>')
def posts(path):

    return os.open(f"{note_dir}{path}.html").read()


if __name__ == '__main__':

    app.run()