# SearchNode
# +- GameAdapter
# BackpropagationScoringMixin
# +- MinMaxScoringMixin
# ChooseRandomMoveMixin
# ChooseFirstMoveMixin
# ChooseRandomMoveFromBestMixin

from bobbot.search_tree import BaseAI, PlayerInterface
from bobbot.search_tree import OneStepSearchMixin
from bobbot.search_tree import FullExpansionMixin
from bobbot.search_tree import ForwardSweepingMixin
from bobbot.search_node import MinMaxScoringMixin
from bobbot.games.nim import NimAdapter
from bobbot.games.nim import PLAYER_A
from bobbot.games.nim import PLAYER_B
from bobbot.games.tictactoe import TicTacToeAdapter
from bobbot.games.tictactoe import PLAYER_X
from bobbot.games.tictactoe import PLAYER_O


def test_scoring():
    Game = type('Game',
                (MinMaxScoringMixin, NimAdapter),
                {})
    AI = type('AI',
              (OneStepSearchMixin, FullExpansionMixin, BaseAI),
              {})
    ai = AI(Game()) # Nim is a first-mover-wins game
    ai.expand_search_tree()
    # FIXME: I've written half the API for this...
    assert ai.current_state.score[PLAYER_A] == 1
    assert ai.current_state.score[PLAYER_B] == -1


# TODO: Test Tic tac Toe with partial sweep to assure that the score
# is 0/0
