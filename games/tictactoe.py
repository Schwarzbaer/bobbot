from collections import namedtuple


# Types, constants and helpers


GameState = namedtuple('GameState', ['board', 'active_player'])

PLAYER_X = 1
PLAYER_O = 2

def player_symbol(state):
    return {PLAYER_X: "X",
            PLAYER_O: "O",
            None: " "}[state]


def textual_repr(game_state):
    b = game_state.board
    return (" {} | {} | {}\n"
            "---+---+---\n"
            " {} | {} | {}\n"
            "---+---+---\n"
            " {} | {} | {}\n"
            "Move: {}".format(player_symbol(b[(0,0)]),
                              player_symbol(b[(1,0)]),
                              player_symbol(b[(2,0)]),
                              player_symbol(b[(0,1)]),
                              player_symbol(b[(1,1)]),
                              player_symbol(b[(2,1)]),
                              player_symbol(b[(0,2)]),
                              player_symbol(b[(1,2)]),
                              player_symbol(b[(2,2)]),
                              player_symbol(game_state.active_player)))

# Functional implementation of game rules


def starting_state():
    board = {(x,y): None for x in range(3) for y in range(3)}
    active_player = PLAYER_X
    return GameState(board=board, active_player=active_player)


def is_winner(game_state, player):
    row = any([all([game_state.board[(b_column, b_row)] == player
                    for b_column in range(3)])
               for b_row in range(3)])
    column = any([all([game_state.board[(b_column, b_row)] == player
                       for b_row in range(3)])
                  for b_column in range(3)])
    diagonal_a = all([game_state.board[(b, b)] == player for b in range(3)])
    diagonal_b = all([game_state.board[(b, 2-b)] == player for b in range(3)])
    
    return any([row, column, diagonal_a, diagonal_b])


def is_finished(game_state):
    player_won = is_winner(game_state, PLAYER_X) or is_winner(game_state, PLAYER_O)
    board_full = all([field is not None for field in game_state.board.values()])
    return player_won or board_full


def is_legal_move(game_state, coord):
    assert len(coord) == 2, "Not a coord tuple"
    assert (0 <= coord[0] <= 2) and (0 <= coord[1] <= 2), "Value out of range"
    return not is_finished(game_state) and game_state.board[coord] is None


def make_move(game_state, coord):
    if not is_legal_move(game_state, coord):
        raise ValueError("Illegal move")
        
    successor_board = {c: s for c, s in game_state.board.items()}
    successor_board[coord] = game_state.active_player
    tentative_successor_game_state = GameState(board=successor_board,
                                               active_player=None)
    if is_finished(tentative_successor_game_state):
        successor_active_player = None
    elif game_state.active_player == PLAYER_X:
        successor_active_player = PLAYER_O
    else:
        successor_active_player = PLAYER_X
    return GameState(board=successor_board,
                     active_player=successor_active_player)


def all_legal_moves(game_state):
    return [coord
            for coord in [(x,y) for x in range(3) for y in range(3)]
            if is_legal_move(game_state, coord)]


def evaluate(game_state):
    if not is_finished(game_state):
        return {PLAYER_X: 0,
                PLAYER_O: 0}
    elif is_winner(game_state, PLAYER_X):
        return {PLAYER_X: 1,
                PLAYER_O: -1}
    elif is_winner(game_state, PLAYER_O):
        return {PLAYER_X: -1,
                PLAYER_O: 1}
    else:
        return {PLAYER_X: -0.5,
                PLAYER_O: -0.5}


def node_key(game_state):
    return ''.join([player_symbol(game_state.board[(x,y)])
                    for x in range(3)
                    for y in range(3)])

# AI adapters


from search_node import RandomOfBestChooser, GameAdapter


# TODO: This needs to go away.
def strip_self(func):
    def inner(*args, **kwargs):
        return func(*args[1:], **kwargs)
    return inner


class TicTacToe(RandomOfBestChooser, GameAdapter):
    starting_state = strip_self(starting_state)
    evaluate_func = strip_self(evaluate)
    is_finished_func = strip_self(is_finished)
    all_legal_moves_func = strip_self(all_legal_moves)
    make_move_func = strip_self(make_move)
    node_key_func = strip_self(node_key)

    def __repr__(self):
        board_repr = textual_repr(self.state)
        value_repr = "State valuation: {: 2.1f}/{: 2.1f}".format(self.score[PLAYER_X], 
                                                                 self.score[PLAYER_O])
        successor_value_reprs = ["{: 2.1f}/{: 2.1f}".format(successor.score[PLAYER_X],
                                                            successor.score[PLAYER_O])
                                 for successor in self.successors.values()]
        return "".join([board_repr, "\n",
                        value_repr, " (",
                        ", ".join(successor_value_reprs),
                        ")"])

