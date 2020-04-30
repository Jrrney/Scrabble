from flask import Flask, render_template, url_for, request, redirect
from Trie import import_dictionary
from Scrabble_algorithm import get_anchors, get_cross_checks, transpose

import csv
import random
import string
import time
import json
import pickle

app = Flask(__name__)
app.config.from_pyfile('config.py')


class Game:
    board = [[[]for _ in range(15)] for _ in range(15)]
    dictionary = None
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

    def __init__(self, dictionary, letter_values):
        self.dictionary = dictionary
        if(letter_values != None):
            self.letter_values = letter_values

    def validate_move(self, move):

        tmp = json.loads(request.get_data())

        cleanMove = [x for x in tmp if (
            x[0] != "-" and x[1] >= 0 and x[1] <= 14 and x[2] >= 0 and x[2] <= 14)]

        if (len(cleanMove) == 0):
            return False

        if(len(cleanMove) > 1):
            if(cleanMove[1][1] == cleanMove[0][1]):
                vertical = False
            elif(cleanMove[1][2] == cleanMove[0][2]):
                vertical = True
            else:
                print("Bending word")
                return False

            if(vertical):
                cleanMove.sort(key=lambda cleanMove: cleanMove[1])
            else:
                cleanMove.sort(key=lambda cleanMove: cleanMove[2])

        for item in cleanMove:
            if(vertical):
                if(item[2] != cleanMove[0][2]):
                    print("Bending word")
                    return False
            else:
                if(item[1] != cleanMove[0][1]):
                    print("Bending word")
                    return False

        return True

    def fill_racks(self):
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

        self.fill_racks()

    def initiate_game(self, number_request):
        if(number_request != ""):
            number = int(number_request)
            if(number > 0):
                self.number_of_players = number
                self.next_move()
                return True
        return False


@app.route("/", methods=['POST', 'GET'])
def startGame():
    global game
    if(game.number_of_players != 0):
        return redirect('/nextMove')
    if request.method == "POST":
        if(game.initiate_game(request.form['number_of_players'])):
            return redirect('/nextMove')
        return redirect('/')
    else:
        return render_template('starting_board.html', letter_values=game.letter_values)


@app.route("/nextMove", methods=['POST', 'GET'])
def nextMove():
    global game
    if request.method == "POST":
        value = game.validate_move(request.get_data())
        print(value)
        game.next_move()
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)
    else:
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)


if (__name__ == "__main__"):
    dictionaryFile = "DictionaryENG.txt"
    boardFile = "board.csv"
    game = Game(import_dictionary(dictionaryFile, ""), None)

    game.import_board(boardFile)
    app.run()
