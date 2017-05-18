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
    Game = type('Game', (MinMaxScoringMixin, NimAdapter), {})
    AI = type('AI', (OneStepSearchMixin, FullExpansionMixin, BaseAI), {})
    ai = AI(Game())
    ai.expand_search_tree()
    # FIXME: I've written half the API for this...
    assert ai.current_state.score[PLAYER_A] == 1
    assert ai.current_state.score[PLAYER_B] == -1


def test_unknown_scoring():
    Game = type('Game', (MinMaxScoringMixin, TicTacToeAdapter), {})
    AI = type('AI', (ForwardSweepingMixin, BaseAI), {})
    ai = AI(Game(), search_depth=2)
    ai.expand_search_tree()
    # With a search depth of 2, there should be no known end state in
    # Tic Tac Toe.
    assert ai.current_state.score[PLAYER_X] == 0
    assert ai.current_state.score[PLAYER_O] == 0


def test_draw_scoring():
    Game = type('Game', (MinMaxScoringMixin, TicTacToeAdapter), {})
    AI = type('AI', (ForwardSweepingMixin, BaseAI), {})
    ai = AI(Game(), search_depth=4)
    ai.make_move((1, 1))
    ai.make_move((0, 2))
    ai.make_move((2, 2))
    ai.make_move((0, 0))
    ai.make_move((0, 1))
    ai.make_move((2, 1))
    ai.expand_search_tree()
    # At this point, minmax play yields draws.
    assert ai.current_state.score[PLAYER_X] == -0.5
    assert ai.current_state.score[PLAYER_O] == -0.5
