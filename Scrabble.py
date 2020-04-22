from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

import csv
import random
import string
import time

import pickle

app = Flask(__name__)
app.config.from_pyfile('config.py')


class Game:
    board = [[[]for _ in range(15)] for _ in range(15)]
    number_of_players = 0
    current_player = 0
    racks = [[]]

    def import_board(self, file):
        self.board = list(csv.reader(
            open(file)))


@app.route("/", methods=['POST', 'GET'])
def startGame():
    if request.method == "POST":
        pass
    else:
        return render_template('starting_board.html')


@app.route("/nextMove", methods=['POST', 'GET'])
def nextMove():
    if request.method == "POST":
        pass
    else:
        return render_template('testing.html', board=game.board)


if (__name__ == "__main__"):
    game = Game()
    game.import_board("board.csv")
    app.run()
