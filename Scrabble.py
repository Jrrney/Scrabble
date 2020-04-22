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
    letter_values = {
        "a": 1,
        "b": 3,
        "c": 3,
        "d": 2,
        "e": 1,
        "f": 4,
        "g": 2,
        "h": 4,
        "i": 1,
        "j": 8,
        "k": 5,
        "l": 1,
        "m": 3,
        "n": 1,
        "o": 1,
        "p": 3,
        "q": 10,
        "r": 1,
        "s": 1,
        "t": 1,
        "u": 1,
        "v": 4,
        "w": 4,
        "x": 8,
        "y": 4,
        "z": 10,
    }

    def import_board(self, file):
        self.board = list(csv.reader(
            open(file)))


@app.route("/", methods=['POST', 'GET'])
def startGame():
    if request.method == "POST":
        pass
    else:
        return render_template('starting_board.html', letter_values=game.letter_values)


@app.route("/nextMove", methods=['POST', 'GET'])
def nextMove():
    if request.method == "POST":
        pass
    else:
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values)


if (__name__ == "__main__"):
    game = Game()
    game.import_board("board.csv")
    app.run()
