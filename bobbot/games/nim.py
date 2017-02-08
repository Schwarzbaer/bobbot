from collections import namedtuple

from bobbot.search_node import GameAdapter


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
    nim_sum = game_state.board[0] ^ game_state.board[1] ^ game_state.board[2]
    return items + " " + state + ", Nim sum: " + str(nim_sum)


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


def node_key(game_state):
    board_repr = ''.join([str(heapsize) for heapsize in game_state.board])
    player_repr = player_symbol(game_state.active_player)
    return board_repr + player_repr



def evaluate_if_end_state(game_state):
    if game_state.winner == PLAYER_A:
        return {PLAYER_A: 1,
                PLAYER_B: -1}
    elif game_state.winner == PLAYER_B:
        return {PLAYER_A: -1,
                PLAYER_B: 1}
    else:
        return {PLAYER_A: 0,
                PLAYER_B: 0}


def evaluate_by_nim_sum(game_state):
    def other_player(player):
        return {PLAYER_A: PLAYER_B,
                PLAYER_B: PLAYER_A}[player]
    nim_sum = game_state.board[0] ^ game_state.board[1] ^ game_state.board[2]
    if game_state.active_player is None:
        return evaluate_if_end_state(game_state)
    if nim_sum == 0:
        return {game_state.active_player: -1,
                other_player(game_state.active_player): 1}
    else:
        return {game_state.active_player: 1,
                other_player(game_state.active_player): -1}


class NimAdapter(GameAdapter):
    def starting_state(self):
        return starting_state()

    def evaluate(self):
        return evaluate_by_nim_sum(self.state)

    def is_finished(self):
        return is_finished(self.state)

    def all_legal_moves(self):
        return all_legal_moves(self.state)

    def make_move(self, move):
        return make_move(self.state, move)

    def node_key(self):
        return node_key(self.state)

    def __repr__(self):
        return textual_repr(self.state)

