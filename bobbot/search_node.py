class SearchNode:
    def __init__(self, state=None, known_predecessors=None):
        if state is None:
            state = self._starting_state()
        if known_predecessors is None:
            known_predecessors = set()
        self.state = state
        self.is_expanded = False
        self.successors = {} # {key: state} to keep a ref to the successor
        self.moves = {} # {move: key}
        assert isinstance(known_predecessors, set), "{!r} is not a set".format(known_predecessors)
        self.known_predecessors = known_predecessors
    
    def expand(self):
        raise NotImplementedError("Game's SearchNode doesn't implement .expand()")
    
    def post_expansion_insertion(self, old, new):
        """
        Gets called after this node has been expanded and its new successors
        have been inserted into the search tree. :old: contains nodes that
        were already present in the search tree, but have been updated through
        .merge(). new contains nodes that haven't been known before. The format
        of both is {node_key: node}
        """
        pass
    
    def is_finished(self):
        """
        Is the game in a state from which it can't be continued, either because
        a player won or it resulted in a draw?
        """
        raise NotImplementedError("Game's SearchNode doesn't implement .is_finished()")
    
    def merge(self, other_instance):
        """
        This node has been re-discovered through expansion of a game state,
        and the resulting information should be added to this instance.
        """
        raise NotImplementedError("Game's SearchNode doesn't implement .merge()")
    
    def node_key(self):
        raise NotImplementedError("Game's SearchNode doesn't implement .node_key()")

    def get_successor(self, move):
        return self.successors[self.moves[move]]


class GameAdapter(SearchNode):
    def _starting_state(self):
        return self.starting_state()

    def starting_state(self):
        raise NotImplementedError("Game does not implement .starting_state()")

    def _active_player(self):
        return self.active_player(self.state)

    def active_player(self, game_state):
        raise NotImplementedError("Game does not implement .active_player()")

    def _is_finished(self):
        return self.is_finished(self.state)

    def is_finished(self, game_state):
        raise NotImplementedError("Game does not implement .is_finished()")

    def _all_legal_moves(self):
        return self.all_legal_moves(self.state)

    def all_legal_moves(self, game_state):
        raise NotImplementedError("Game does not implement .all_legal_moves()")

    def _make_move(self, move):
        return self.make_move(self.state, move)

    def make_move(self, game_state, move):
        raise NotImplementedError("Game does not implement .make_move()")

    def _node_key(self):
        return self.node_key(self.state)

    def node_key(self, game_state):
        raise NotImplementedError("Game does not implement .node_key()")

    def _evaluate(self):
        return self.evaluate(self.state)

    def evaluate(self, game_state):
        raise NotImplementedError("Game does not implement .evaluate()")

    def __repr__(self):
        return self._node_key()


# TODO: The reference to TicTacToe needs to go.
class ExpandingSearchNode(SearchNode):
    """
    Requires .all_legal_moves(), .make_move() to be implemented.
    """
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
        # TODO: Can I be sure that there aren't any more kwargs?
        move_to_successor = {move: self.__class__(state=self._make_move(move),
                                                  known_predecessors={self})
                             for move in self._all_legal_moves()}
        self.moves = {move: state._node_key() for move, state in move_to_successor.items()}
        self.is_expanded = True
        return move_to_successor.values()

    def post_expansion_insertion(self, old, new):
        self.successors.update(old)
        self.successors.update(new)

    def merge(self, other_instance):
        if not self.is_expanded and other_instance.is_expanded:
            self.successors = other_instance.successors
            self.is_expanded = True
        self.known_predecessors.add(*other_instance.known_predecessors)


class EvaluatingSearchNode(ExpandingSearchNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = self._evaluate()

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
        has_been_updated = False
        for player in self.score:
            successor_scores = [successor.score[player] for successor in self.successors.values()]
            if player == self._active_player():
                new_score = max(successor_scores)
            else:
                new_score = min(successor_scores)
            if new_score != self.score[player]:
                self.score[player] = new_score
                has_been_updated = True
        if has_been_updated:
            self.backpropagate_score()


#
# CHOOSERS
# These SearchNodes implement .find_best_move() and require .score to be implemented.
#


import random


class ChooseRandomMove(EvaluatingSearchNode):
    def find_best_move(self):
        return random.choice(self.moves)


class ChooseFirstMove(EvaluatingSearchNode):
    def find_best_move(self):
        return sorted(self.moves)[0]


class ChooseRandomMoveFromBest(EvaluatingSearchNode):
    def find_best_move(self):
        possible_moves = {move: self.successors[key].score[self._active_player()]
                          for move, key in self.moves.items()}
        best_score = max(possible_moves.values())
        best_moves = [move for move in possible_moves if possible_moves[move] == best_score]
        return random.choice(best_moves)

