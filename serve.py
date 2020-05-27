from flask import Flask, render_template, send_from_directory
from render import render_all

import os

app = Flask(__name__)

# TODO as we get closer migrate to https://flask.palletsprojects.com/en/1.1.x/config/
app.config.from_pyfile("config.py")

notes = render_all()

@app.route("/")
def hello():

    return render_template("index.html", notes=notes)

@app.route("/<path:filename>")
def posts(filename):

    return render_template("note.html", filename=filename)

@app.template_global()
def rendered(filename):
    fullpath = os.path.join(app.config["RENDERER_CONFIG"]["output_directory"], f"{filename}.html")
    with open(fullpath, 'r') as f:
        return f.read()

if __name__ == '__main__':

    app.run()