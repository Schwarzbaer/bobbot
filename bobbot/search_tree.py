class BaseAI:
    def __init__(self, current_state, debug=False):
        self.current_state = current_state
        self.debug = debug

    def choose_move(self):
        self.expand_search_tree()
        chosen_move = self.current_state.find_best_move()
        return chosen_move

    def make_move(self, move):
        self.current_state = self.current_state.get_successor(move)

    def play(self):
        if self.debug:
            print(self.current_state, end="\n")
            print("Nodes in the search tree: {}".format(len(self.search_tree)))
        while not self.current_state.is_finished():
            self.make_move(self.choose_move())
            if self.debug:
                print(self.current_state, end="\n")
                print("Nodes in the search tree: {}".format(len(self.search_tree)))

    def expand_search_tree(self):
        raise NotImplemented(".expand_search_tree() not implemented")

    def find_best_move(self):
        raise NotImplemented(".find_best_move() not implemented")
    

class OneStepSearchMixin:
    def __init__(self, starting_state, *args, **kwargs):
        super().__init__(starting_state, *args, **kwargs)
        self.search_tree = dict()
        self.add_node(starting_state)
    
    def expand_search_tree(self):
        for node in [node for node in self.search_tree.values() if not node.is_expanded]:
            # TODO: Does it really even make sense to distinguish between these after
            #   adding/merging them to/with the search tree?
            old = {}
            new = {}
            for successor in node.expand():
                is_new = self.add_node(successor)
                # FIXME: Ugly copypaste.
                if is_new:
                    new[successor.node_key()] = successor
                else:
                    old[successor.node_key()] = self.search_tree[successor.node_key()]
            node.post_expansion_insertion(old, new)
    
    def add_node(self, node):
        """
        Adds the node to the search tree if it isn't present already, or causes
        a merge with the already present instance of it otherwise.
        """
        if node.node_key() not in self.search_tree:
            self.search_tree[node.node_key()] = node
            return True
        else:
            self.search_tree[node.node_key()].merge(node)
            return False


class FullExpansionMixin(OneStepSearchMixin):
    def expand_search_tree(self):
        while any(not node.is_expanded for node in self.search_tree.values()):
            super().expand_search_tree()


class NaivePruningMixin:
    def make_move(self, move):
        super().make_move(move)
        post_move_size = len(self.search_tree)
        transitive_hull = set()
        frontier = set([self.current_state.node_key()])
        while frontier:
            expansion = frontier.pop()
            transitive_hull.add(expansion)
            frontier.update(node_key
                            for node_key in self.search_tree[expansion].successors.keys() # FIXME: accesses SearchNode internals
                            if node_key not in transitive_hull)
        nodes_to_delete = set(self.search_tree.keys()) - transitive_hull
        for key in nodes_to_delete:
            del self.search_tree[key]
            # TODO: Remove these as predecessors from still-existing nodes, too
            # TODO: ...which will also require to add such methods to search nodes.
        post_prune_size = len(self.search_tree)
        if self.debug:
            print("Search tree size: {} (after move) - {} (pruned) = {}".format(
                post_move_size,
                post_move_size - post_prune_size,
                post_prune_size)
            )

