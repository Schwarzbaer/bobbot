#!/usr/bin/env python3

from bobbot.games.tictactoe import TicTacToeAdapter
from bobbot.search_tree import BaseAI
from bobbot.search_tree import (FullExpansionMixin, BoundedExpansionMixin, OneStepSearchMixin,
    NaivePruningMixin)
from bobbot.search_node import ChooseFirstMove, ChooseRandomMove, ChooseRandomMoveFromBest


TicTacToe = type('TicTacToe', (TicTacToeAdapter, ChooseRandomMoveFromBest), {})
AI = type('AI', (BoundedExpansionMixin, OneStepSearchMixin, NaivePruningMixin, BaseAI), {})
ai = AI(TicTacToe(), debug=True, time_limit=3, node_limit=1000)


if __name__ == '__main__':
    ai.play()

