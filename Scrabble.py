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

    def fill_racks(self):
        self.next_move()
        if(self.racks == [[]]):
            for j in range(self.number_of_players):
                rack = []
                for i in range(7):
                    rack.append(random.choice(string.ascii_lowercase))
                self.racks.append(rack)

    def import_board(self, file):
        self.board = list(csv.reader(
            open(file)))

    def next_move(self):
        self.current_player += 1

        if(self.current_player > self.number_of_players):
            self.current_player = 1


@app.route("/", methods=['POST', 'GET'])
def startGame():
    global game
    if(game.number_of_players != 0):
        return redirect('/nextMove')
    if request.method == "POST":
        tmp = request.form['number_of_players']
        if(tmp != ""):
            game.number_of_players = int(tmp)
            game.fill_racks()
            return redirect('/nextMove')
        else:
            return redirect('/')
    else:
        return render_template('starting_board.html', letter_values=game.letter_values)


@app.route("/nextMove", methods=['POST', 'GET'])
def nextMove():
    global game
    if request.method == "POST":
        game.fill_racks()
        data = request.get_data()
        print(data)
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)
    else:
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)


if (__name__ == "__main__"):
    game = Game()
    game.board = [['-'for _ in range(15)] for _ in range(15)]
    game.import_board("board.csv")
    app.run()
