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
    items = "  ".join(["|"*game_state.board[i] + " "*([3,5,7][i] - game_state.board[i])
                       for i in range(3)])
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


def evaluate(game_state):
    if game_state.winner == PLAYER_A:
        return {PLAYER_A: 1,
                PLAYER_B: -1}
    elif game_state.winner == PLAYER_B:
        return {PLAYER_A: -1,
                PLAYER_B: 1}
    else:
        return {PLAYER_A: 0,
                PLAYER_B: 0}



from search_node import RandomOfBestChooser, GameAdapter


# TODO: This needs to go away.
def strip_self(func):
    def inner(*args, **kwargs):
        return func(*args[1:], **kwargs)
    return inner


class Nim(RandomOfBestChooser, GameAdapter):
    starting_state = strip_self(starting_state)
    evaluate_func = strip_self(evaluate)
    is_finished_func = strip_self(is_finished)
    all_legal_moves_func = strip_self(all_legal_moves)
    make_move_func = strip_self(make_move)
    node_key_func = strip_self(textual_repr)

    def __repr__(self):
        return textual_repr(self.state)

