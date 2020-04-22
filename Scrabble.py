from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

import csv
import random
import string
import time

import pickle

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route("/", methods=['POST', 'GET'])
def startGame():
    if request.method == "POST":
        pass
    else:
        return render_template('starting_board.html')


if (__name__ == "__main__"):
    app.run()
