#!/usr/bin/env python3

from bobbot.search_tree import BaseAI
from bobbot.search_tree import FullExpansionMixin, BoundedExpansionMixin  # Expansion control
from bobbot.search_tree import OneStepSearchMixin  # Expansion step
from bobbot.search_tree import ForwardSweepingMixin # Combined Expansion control and step
from bobbot.search_tree import NaivePruningMixin  # Pruning
from bobbot.search_node import MinMaxScoringMixin  # Score backpropagation
from bobbot.search_node import (ChooseFirstMoveMixin, ChooseRandomMoveMixin,
    ChooseRandomMoveFromBestMixin)  # Move choosers
from bobbot.games.tictactoe import TicTacToeAdapter  # Actual game rules


TicTacToe = type('TicTacToe',
                 (MinMaxScoringMixin, ChooseRandomMoveFromBestMixin, TicTacToeAdapter),
                 {})
AI = type('AI',
          (ForwardSweepingMixin, NaivePruningMixin, BaseAI),
          {})
ai = AI(TicTacToe(), debug=True, search_depth=2)


if __name__ == '__main__':
    ai.play()

