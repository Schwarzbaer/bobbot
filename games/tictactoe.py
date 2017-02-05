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


# AI adapters


from search_node import SearchNode


# TODO: Most of this note can be genericed away by passing StateNode type and
#   functions to __init__ as a type.
class TicTacToeBaseSearchNode(SearchNode):
    def __init__(self, state=None, known_predecessors=None):
        if state is None:
            state = starting_state()
        if known_predecessors is None:
            known_predecessors = set()
        super().__init__(state, known_predecessors)

    def expand(self):
        """
        Returns all successor states for this state. It doesn't store them in
        this state object, as the search tree might find that it has already
        found the successor state before, and updates that instance with data
        from the instance generated here. Either way, the successor with the
        most complete set of information available (be it created here or by
        merging the one created here with the existing one) is indicated to
        this instance via :post_expansion_insertion:.
        """
        # TODO: This computes each move twice. Optimize!
        # TODO: Didn't I just say that we shouldn't store here?
        move_to_successor = {move: TicTacToe(state=make_move(self.state, move),
                                             known_predecessors={self})
                             for move in all_legal_moves(self.state)}
        self.moves = {move: state.node_key() for move, state in move_to_successor.items()}
        self.is_expanded = True
        return move_to_successor.values()

    def post_expansion_insertion(self, old, new):
        self.successors.update(old)
        self.successors.update(new)
    
    def is_finished(self):
        # TODO: Cache this?
        return is_finished(self.state)

    def merge(self, other_instance):
        if not self.is_expanded and other_instance.is_expanded:
            self.successors = other_instance.successors
            self.is_expanded = True
        self.known_predecessors.add(*other_instance.known_predecessors)

    def node_key(self):
        return ''.join([player_symbol(self.state.board[(x,y)])
                        for x in range(3)
                        for y in range(3)])

    def __repr__(self):
        return self.node_key()


import random


class TicTacToe(TicTacToeBaseSearchNode):
    def __init__(self, state=None, known_predecessors=None):
        super().__init__(state, known_predecessors)
        if not self.is_finished():
            self.score = {PLAYER_X: 0,
                          PLAYER_O: 0}
        elif is_winner(self.state, PLAYER_X):
            self.score = {PLAYER_X: 1,
                          PLAYER_O: -1}
        elif is_winner(self.state, PLAYER_O):
            self.score = {PLAYER_X: -1,
                          PLAYER_O: 1}
        else:
            self.score = {PLAYER_X: -0.5,
                          PLAYER_O: -0.5}

    def backpropagate_score(self):
        for node in self.known_predecessors:
            node.update_score()

    def post_expansion_insertion(self, old, new):
        super().post_expansion_insertion(old, new)
        if old or new:
            self.update_score()

    def merge(self, other_instance):
        super().merge(other_instance)
        if self.successors:
            self.update_score()
        
    def update_score(self):
        active_player = self.state.active_player
        has_been_updated = False
        for player in self.score:
            successor_scores = [successor.score[player] for successor in self.successors.values()]
            if player == active_player:
                new_score = max(successor_scores)
            else:
                new_score = min(successor_scores)
            if new_score != self.score[player]:
                self.score[player] = new_score
                has_been_updated = True
        if has_been_updated:
            self.backpropagate_score()

    def find_best_move(self):
        possible_moves = {move: self.successors[key].score[self.state.active_player]
                          for move, key in self.moves.items()}
        best_score = max(possible_moves.values())
        best_moves = [move for move in possible_moves if possible_moves[move] == best_score]
        return random.choice(best_moves)

    def __repr__(self):
        return "{}|Move {}, Score {: 2.1f}/{: 2.1f}, {} successors".format(
            self.node_key(),
            player_symbol(self.state.active_player),
            self.score[PLAYER_X],
            self.score[PLAYER_O],
            len(self.successors)
        )
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

