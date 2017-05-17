from bobbot.search_tree import BaseAI, PlayerInterface
from bobbot.search_tree import OneStepSearchMixin
from bobbot.search_tree import FullExpansionMixin
from bobbot.search_tree import ForwardSweepingMixin
from bobbot.search_tree import NaivePruningMixin
from bobbot.games.nim import NimAdapter
from bobbot.games.tictactoe import TicTacToeAdapter
from bobbot.games.tictactoe import PLAYER_X
from bobbot.games.tictactoe import PLAYER_O


# TODO
# search_tree: CurrentStateExpansionMixin, BoundedExpansionMixin
# search_node: BackpropagationScoringMixin, MinMaxScoringMixin, choosers

def test_expand_implicitly_on_move():
    ai = BaseAI(TicTacToeAdapter())
    assert ai.num_states() == 1
    ai.make_move((0, 0)) # This adds all nine possible successors
    assert ai.num_states() == 10


def test_player_interface():
    AI = type('AI',
              (PlayerInterface, BaseAI),
              {})
    ai = AI(TicTacToeAdapter())
    assert ai.active_player() == PLAYER_X
    assert len(ai.all_legal_moves()) == 9
    ai.make_move((0, 0))
    assert ai.active_player() == PLAYER_O
    assert len(ai.all_legal_moves()) == 8
    ai.make_move((0, 2))
    assert ai.active_player() == PLAYER_X
    assert len(ai.all_legal_moves()) == 7
    ai.make_move((1, 0))
    assert ai.active_player() == PLAYER_O
    assert len(ai.all_legal_moves()) == 6
    ai.make_move((1, 2))
    assert ai.active_player() == PLAYER_X
    assert len(ai.all_legal_moves()) == 5
    ai.make_move((2, 0))
    assert ai.active_player() == None
    assert ai.winner() == PLAYER_X
    assert ai.is_finished()
    assert len(ai.all_legal_moves()) == 0


def test_full_expansion_mixin():
    AI = type('AI',
              (PlayerInterface,
               FullExpansionMixin,
               OneStepSearchMixin,
               BaseAI),
              {})
    ai = AI(NimAdapter())
    assert ai.num_states() == 1
    ai.expand_search_tree()
    # There's heaps with 3, 5 and 7 items, so the heaps have 4, 6 and
    # 8 states, respectively. Except for a few of them, these states
    # can be those of either player. Those exceptions are the starting
    # state, and those states where only one item has been taken from
    # each pile (001, 010, 100, 011, 101, 110, 111). The end state has
    # two states, as there are two possible winners.
    possible_states = (4 * 6 * 8) * 2 - (1 + 7)
    assert ai.num_states() == possible_states


def test_forward_sweeping_mixin():
    AI = type('AI',
              (ForwardSweepingMixin, BaseAI),
              {})
    ai = AI(TicTacToeAdapter(), search_depth=1)
    ai.expand_search_tree()
    assert ai.num_states() == 1 + 9
    ai = AI(TicTacToeAdapter(), search_depth=2)
    ai.expand_search_tree()
    assert ai.num_states() == 1 + 9 + 9*8
    # ai = AI(TicTacToeAdapter(), search_depth=3)
    # ai.expand_search_tree()
    # assert ai.num_states() == 1 + 9 + 9*8 + FIXME


def test_naive_pruning_mixin():
    AI = type('AI',
              (NaivePruningMixin, BaseAI),
              {})
    ai = AI(TicTacToeAdapter())
    ai.make_move((0, 0))
    assert ai.num_states() == 1
    ai.make_move((0, 2))
    assert ai.num_states() == 1
    ai.make_move((1, 0))
    assert ai.num_states() == 1
    ai.make_move((1, 2))
    assert ai.num_states() == 1
