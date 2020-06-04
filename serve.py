from flask import Flask, render_template, send_from_directory, request
from render import render_all

from datetime import datetime

import os

app = Flask(__name__)

# TODO as we get closer migrate to https://flask.palletsprojects.com/en/1.1.x/config/
app.config.from_pyfile("config.py")

notes, tag_set = render_all()

@app.route("/")
def index():

    return render_template("index.html", notes=notes, tag_set=tag_set)

@app.route("/tags")
def tags():

    tag = request.args.get("tag")

    matching_articles = [note for note in notes if tag in note.tags]

    return render_template("index.html", notes=matching_articles, tag_set=tag_set)

@app.route(f"/{app.config['NOTES_DIR']}/<path:filename>")
def posts(filename):

    return render_template("note.html", filename=filename)

# This leads to HTTP 500s consider moving
@app.template_global()
def rendered(filename):
    fullpath = os.path.join(app.config["RENDERER_CONFIG"]["output_directory"], f"{filename}.html")
    with open(fullpath, 'r') as f:
        return f.read()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow(),
            'public_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

if __name__ == '__main__':

    app.run("0.0.0.0")