# Scrabble
The game of Scrabble.

Back-end Python implementation contains REST API in Flask framework.
Front-end is design as HTML + CSS website.

Code also contains an algorithm to play the game. Further used as an AI opponent

## Scrabble algorithm

*For now move evaluation is based on **length of the word**, not offical Scrabble rules*

## Lexicon
Lexicon used by algorithm is implemented as a Trie - a kind of search tree where the keys are letters of the alphabet. 
Each node has "isTerminal" marker to distingiush if path from the root to that node forms a complete word. 
This kind of structure makes search for words very efficient. Whole lexicone in this form has **370 104 wors**.

Credit for the dictionary used in the Trie: [github.com/dwyl](https://github.com/dwyl)  

## Algorithm implementation 
Implementation is based on a paper by Andrew W. Appel and Guy J. Jacobson

It takes an anchor square and uses a recursive formula to extend the word to the right and left from there. 
This way all possible across moves are generated. Down moves are generated simply by the transposition of the board.

Important terms:
* Anchor: potential square to look for a new word (square adjecent to filled square)
* Cross-Check: When making an across play, the
new tiles must also form down words whenever they are directly above or below tiles already on
the board. Therefore some squares have limited Cross-Check set of letters allowed to be placed there. 
