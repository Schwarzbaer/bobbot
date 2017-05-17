import pytest

from bobbot.games import tictactoe


def test_starting_state():
    state_0 = tictactoe.starting_state()
    assert not tictactoe.is_finished(state_0)
    assert state_0.active_player == tictactoe.PLAYER_X
    all_initial_moves = set([(x, y) for x in range(3) for y in range(3)])
    assert set(tictactoe.all_legal_moves(state_0)) == all_initial_moves


def test_alternating_players():
    state_0 = tictactoe.starting_state()
    assert state_0.active_player == tictactoe.PLAYER_X
    state_1 = tictactoe.make_move(state_0, (0,0))
    assert state_1.active_player == tictactoe.PLAYER_O


def test_cannot_choose_field_twice():
    state_0 = tictactoe.starting_state()
    state_1 = tictactoe.make_move(state_0, (0,0))
    with pytest.raises(ValueError):
        tictactoe.make_move(state_1, (0,0))


def test_win():
    state_0 = tictactoe.starting_state()
    state_1 = tictactoe.make_move(state_0, (0,0))
    state_2 = tictactoe.make_move(state_1, (0,1))
    state_3 = tictactoe.make_move(state_2, (1,0))
    state_4 = tictactoe.make_move(state_3, (1,1))
    state_5 = tictactoe.make_move(state_4, (2,0))
    assert tictactoe.is_finished(state_5)
    assert tictactoe.all_legal_moves(state_5) == []
    assert tictactoe.winner(state_5) == tictactoe.PLAYER_X


def test_draw():
    state_0 = tictactoe.starting_state()
    state_1 = tictactoe.make_move(state_0, (1,1))
    state_2 = tictactoe.make_move(state_1, (2,0))
    state_3 = tictactoe.make_move(state_2, (2,2))
    state_4 = tictactoe.make_move(state_3, (0,0))
    state_5 = tictactoe.make_move(state_4, (1,0))
    state_6 = tictactoe.make_move(state_5, (1,2))
    state_7 = tictactoe.make_move(state_6, (2,1))
    state_8 = tictactoe.make_move(state_7, (0,1))
    state_9 = tictactoe.make_move(state_8, (0,2))
    assert tictactoe.is_finished(state_9)
    assert tictactoe.all_legal_moves(state_9) == []
    assert tictactoe.winner(state_9) is None
