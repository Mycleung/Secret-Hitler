# Secret Hitler
### (In Python)

This is a quick day-hack project to write the board game Secret Hitler (http://www.secrethitler.com) in Python.

The idea is for additional players to implement their own `HitlerPlayer` and pit their AI players against each other.

Currently the only implemented player is the `DumbPlayer`, which plays completely randomly.

### Usage

The game is currently configured to analyse the win-rates when the game is played by ten `DumbPlayer`s. It plays 10,000 games and prints out the number of victories due to each win condition. It will also print out the total number of Liberal:Fascist wins.

Run with `python HitlerGame.py`
