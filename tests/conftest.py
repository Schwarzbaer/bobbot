#!/usr/bin/env python3

import pytest

from bobbot.search_tree import BaseAI
from bobbot.search_tree import FullExpansionMixin, BoundedExpansionMixin
from bobbot.search_tree import OneStepSearchMixin
from bobbot.search_tree import ForwardSweepingMixin
from bobbot.search_tree import NaivePruningMixin
from bobbot.search_node import MinMaxScoringMixin
from bobbot.search_node import (ChooseFirstMoveMixin, ChooseRandomMoveMixin,
    ChooseRandomMoveFromBestMixin)
from bobbot.games.tictactoe import TicTacToeAdapter


@pytest.fixture
def tictactoe():
    TicTacToe = type('TicTacToe',
                     (MinMaxScoringMixin,
                      ChooseRandomMoveFromBestMixin,
                      TicTacToeAdapter,
                     ),
                     {})
    AI = type('AI',
              (ForwardSweepingMixin,
               NaivePruningMixin,
               BaseAI,
              ),
              {})
    ai = AI(TicTacToe(), debug=True, search_depth=2)
    return ai
