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
  * Improve [documentation](http://www.sphinx-doc.org/en/stable/ext/example_google.html)
  * Packaging
* Code features
  * Make search tree and search nodes use weakref dicts to let the GC prune the state tree.
  * Make search tree write to disk / DB to solve games and / or build opening libraries.
  * multiprocessing
    * ...to let it run in the background, to not block the interface
    * ...for pondering
* Algorithms
  * Alpha-Beta pruning
  * [Proof-number search](https://en.wikipedia.org/wiki/Proof-number_search)
  * Conspiracy number search
    [Conspiracy Numbers](https://chessprogramming.wikispaces.com/Conspiracy+Numbers)
    [An Analysis of the Conspiracy Numbers Algorithm](https://webdocs.cs.ualberta.ca/~jonathan/publications/ai_publications/icn.pdf)
    [Sibling Conspiracy Number Search](http://www.aaai.org/ocs/index.php/SOCS/SOCS15/paper/viewFile/11040/10641)
  * [Best-first search](https://en.wikipedia.org/wiki/Best-first_search)
  * Quiescence search
  * Expectiminimax
  * Principal variation search
    [NegaScout](https://chessprogramming.wikispaces.com/NegaScout)
  * [Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
    [Monte Carlo Tree Search for Game AI](https://spin.atomicobject.com/2015/12/12/monte-carlo-tree-search-algorithm-game-ai/)
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


Other Links
-----------

* [SP.268 Coursenotes](http://web.mit.edu/sp.268/www/coursenotes.html)
* [Chess with Different Armies](http://www.chessvariants.com/unequal.dir/cwda.html) (ask for permission before copying)
* [Papers by Rémi Coulom](https://scholar.google.de/citations?user=qxMvlisAAAAJ&hl=en)
* [Constructing a Kamisado playing agent](http://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand13/Group4Per/report/17-setterquist-skeppstedt.pdf)
* [Temporal difference learning](https://en.wikipedia.org/wiki/Temporal_difference_learning) (works well for Backgammon)

