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

* Project cleanup
  * Write tests
  * flake8 (or other linter)
  * Packaging
* Code features
  * Make search tree and search nodes use weakref dicts to let the GC prune the state tree.
  * multiprocessing
    * ...to let it run in the background, to not block the interface
    * ...for pondering
* Algorithms
  * Alpha-Beta pruning
  * Quiescence search
  * Expectiminimax
  * Principal variation search
  * Monte Carlo tree search
  * AlphaGo (meaning: machine learning algorithms for expansion guidance and state evaluation)
* Games
  * [Nim](https://en.wikipedia.org/wiki/Nim) (more variants)
  * [Black Hole](http://nestorgames.com/rulebooks/BLACKHOLE_EN.pdf) (check license first)
  * [Order and Chaos](https://en.wikipedia.org/wiki/Order_and_Chaos) (check license first)
  * [Nine Men's Morris](https://en.wikipedia.org/wiki/Nine_Men's_Morris)
  * [Fanorona](https://en.wikipedia.org/wiki/Fanorona)
  * [Ludus latrunculorum](https://en.wikipedia.org/wiki/Ludus_latrunculorum)
  * [Mancala](https://en.wikipedia.org/wiki/Mancala)
  * [Checkers](https://en.wikipedia.org/wiki/Draughts)
  * [Hnefatafl](https://de.wikipedia.org/wiki/Hnefatafl)
  * [Chess](https://en.wikipedia.org/wiki/Chess)
  * [Go](https://en.wikipedia.org/wiki/Go_(game))
  * [Arimaa](https://en.wikipedia.org/wiki/Arimaa)

