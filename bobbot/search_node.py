class SearchNode:
    def __init__(self, state=None, known_predecessors=None):
        if state is None:
            state = self.starting_state()
        if known_predecessors is None:
            known_predecessors = set()
        self.state = state
        self.is_expanded = False
        self.successors = {} # {key: state} to keep a ref to the successor
        self.moves = {} # {move: key}
        assert isinstance(known_predecessors, set), "{!r} is not a set".format(known_predecessors)
        self.known_predecessors = known_predecessors
    
    def expand(self):
        raise NotImplemented("Game's SearchNode doesn't implement .expand()")
    
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
        raise NotImplemented("Game's SearchNode doesn't implement .is_finished()")
    
    def merge(self, other_instance):
        """
        This node has been re-discovered through expansion of a game state,
        and the resulting information should be added to this instance.
        """
        raise NotImplemented("Game's SearchNode doesn't implement .merge()")
    
    def node_key(self):
        raise NotImplemented("Game's SearchNode doesn't implement .node_key()")

    def get_successor(self, move):
        return self.successors[self.moves[move]]


class GameAdapter(SearchNode):
    def starting_state(self):
        raise NotImplemented("Game does not implement .starting_state()")

    def evaluate(self):
        raise NotImplemented("Game does not implement .evaluate()")

    def is_finished(self):
        raise NotImplemented("Game does not implement .is_finished()")

    def all_legal_moves(self):
        raise NotImplemented("Game does not implement .all_legal_moves()")

    def make_move(self, move):
        raise NotImplemented("Game does not implement .make_move()")

    def node_key(self):
        raise NotImplemented("Game does not implement .node_key()")

    def __repr__(self):
        return self.node_key()


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
        move_to_successor = {move: self.__class__(state=self.make_move(move),
                                                  known_predecessors={self})
                             for move in self.all_legal_moves()}
        self.moves = {move: state.node_key() for move, state in move_to_successor.items()}
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
        self.score = self.evaluate()

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


#
# CHOOSERS
# These SearchNodes implement .find_best_move() and require .score to be implemented.
#


import random

# TODO: Abstract out active_player
class RandomOfBestChooser(EvaluatingSearchNode):
    def find_best_move(self):
        possible_moves = {move: self.successors[key].score[self.state.active_player]
                          for move, key in self.moves.items()}
        best_score = max(possible_moves.values())
        best_moves = [move for move in possible_moves if possible_moves[move] == best_score]
        return random.choice(best_moves)
