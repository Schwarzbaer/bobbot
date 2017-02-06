Bob the bot
-----------

A set of classes to easily weave AIs from for simple, deterministic games of total information. Each
of these three adjectives is subject for later removal.


The idea here is that you write a set of functions that describe the rules and states of your game,
plug them into a SearchNode class (that represents the current and possible future states of the
game being played), add functions to guess how good a given state is for a given player (learning
algorithms might be added in the future to free you from that chore), and... you're done.


Currently Bob is able to play games that are simple enough to solve (create a complete exploration
of the game's possible states) before starting to play it.


TODO
----

* Code cleanup
  * Extract generic search node classes out of Tic Tac Toe
  * Make search tree and search nodes use weakref dicts to let the GC prune the state tree.
    * Also provide explicit pruning.
* Algorithms
  * Alpha-Beta pruning
  * Quiescence search
  * Expectiminimax
  * Principal variation search
  * Monte Carlo tree search
  * AlphaGo (meaning: machine learning algorithms for expansion guidance and state evaluation)
* Games
  * Nim
  * [Black Hole](http://nestorgames.com/rulebooks/BLACKHOLE_EN.pdf) (check license first)
  * [Order and Chaos](https://en.wikipedia.org/wiki/Order_and_Chaos) (check license first)
  * Nine Men's Morrow
  * Checkers
  * Hnefatafl
  * Chess
  * Go

