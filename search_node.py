class SearchNode:
    def __init__(self, state, known_predecessors):
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

