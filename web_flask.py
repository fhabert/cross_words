import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
import main
import random
import requests

app = Flask(__name__)
app.secret_key = "PaRiS"

@app.route('/', methods=['GET', 'POST'])
def home():
    mots = main.initiliaze_game()
    return render_template("base.html", board=mots.mat, rows_count=len(mots.mat), cols_count=len(mots.mat[0]), 
                                pos_h=mots.words_pos_h, pos_v=mots.words_pos_v, def_v=mots.def_v, 
                                def_h=mots.def_h, len_def_h=len(mots.def_h), len_def_v=len(mots.def_v))


@app.route('/redo', methods=['POST'])
def redo():
    mots = main.initiliaze_game()
    return render_template("base.html", board=mots.mat, rows_count=len(mots.mat), cols_count=len(mots.mat[0]),
                            pos_h=mots.words_pos_h, pos_v=mots.words_pos_v, def_v=mots.def_v, def_h=mots.def_h,
                            len_def_h=len(mots.def_h), len_def_v=len(mots.def_v))

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        list_mots = list(zip(data["mots"], data["defs"]))
        mots = main.initiliaze_game(list_mots)
        # return redirect('/')
        return render_template("base.html", board=mots.mat, rows_count=len(mots.mat), cols_count=len(mots.mat[0]),
                                pos_h=mots.words_pos_h, pos_v=mots.words_pos_v, def_v=mots.def_v, def_h=mots.def_h,
                                len_def_h=len(mots.def_h), len_def_v=len(mots.def_v))
    elif request.method == "GET":
        return render_template("generate.html")


if __name__ == '__main__':
    app.run(debug=True)