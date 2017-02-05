from collections import namedtuple


# Types, constants and helpers


GameState = namedtuple('GameState', ['board', 'active_player', 'winner'])


PLAYER_A = 1
PLAYER_B = 2


def other_player(player):
    if player==PLAYER_A:
        return PLAYER_B
    else:
        return PLAYER_A


def player_symbol(state):
    return {PLAYER_A: "A",
            PLAYER_B: "B",
            None: "n/a"}[state]


def textual_repr(game_state):
    items = "  ".join(["|"*game_state.board[i] for i in range(3)])
    if is_finished(game_state):
        state = "Winner: {}".format(player_symbol(game_state.winner))
    else:
        state = "Move: {}".format(player_symbol(game_state.active_player))
    return items + " " + state


# Functional implementation of game rules


def starting_state():
    return GameState(board=(3, 5, 7), active_player=PLAYER_A, winner=None)


def is_winner(game_state, player):
    return game_state.winner == player


def is_finished(game_state):
    return game_state.board == (0, 0, 0)


def is_legal_move(game_state, take):
    return 0 <= take[0] <= 2 and take[1] <= game_state.board[take[0]]


def make_move(game_state, take):
    if not is_legal_move(game_state, take):
        raise ValueError("Illegal move")
    
    board = list(game_state.board)
    print(board, take)
    board[take[0]] = board[take[0]] - take[1]
    if all(board[i] == 0 for i in range(3)):
        next_player = None
        winner = game_state.active_player
    else:
        next_player = other_player(game_state.active_player)
        winner = None
    return GameState(board=tuple(board), active_player=next_player, winner=winner)
        

def all_legal_moves(game_state):
    return [(pos, take)
            for pos in range(3)
            for take in range(1, game_state.board[pos] + 1)]

