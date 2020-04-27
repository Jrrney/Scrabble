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

        cleanMove = [x for x in move if (
            x[0] != "-" and x[1] >= 0 and x[1] <= 14 and x[2] >= 0 and x[2] <= 14)]

        previous = cleanMove[0]
        vertical = True
        word = ""

        if(cleanMove[1][1] == cleanMove[0][1]):
            vertical = False
        elif(cleanMove[1][2] == cleanMove[0][2]):
            vertical = True
        else:
            return False

        if(vertical):
            cleanMove.sort(key=lambda cleanMove: cleanMove[1])
        else:
            cleanMove.sort(key=lambda cleanMove: cleanMove[2])

        for item in cleanMove:
            word += (item[0])
            if(vertical):
                if(item[2] != previous[2]):
                    return False
            else:
                if(item[1] != previous[1]):
                    return False

        # if(dictionary.is_word(word)==False)

        tmpBoard = self.board

        if(vertical):
            tmpBoard = transpose(tmpBoard)

        anchors = get_anchors(self.board, self.dictionary)
        cross_checks = get_cross_checks(self.board, self.dictionary)
        return True

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
            number = int(tmp)
            if(number > 0):
                game.number_of_players = number
                game.fill_racks()
                return redirect('/nextMove')
        return redirect('/')
    else:
        return render_template('starting_board.html', letter_values=game.letter_values)


@app.route("/nextMove", methods=['POST', 'GET'])
def nextMove():
    global game
    if request.method == "POST":
        move = json.loads(request.get_data())
        value = game.validate_move(move)
        print(value)
        game.fill_racks()
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)
    else:
        return render_template('game_board.html', board=game.board, letter_values=game.letter_values, current_player=game.current_player, racks=game.racks)


if (__name__ == "__main__"):
    dictionaryFile = "DictionaryENG.txt"
    boardFile = "board.csv"
    game = Game(import_dictionary(dictionaryFile, ""), None)

    game.import_board(boardFile)
    app.run()
