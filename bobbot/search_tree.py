from datetime import datetime


class BaseAI:
    def __init__(self, current_state, debug=False):
        self.debug = debug
        self.search_tree = dict()
        self.current_state = current_state
        self.add_node(current_state)

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
        while not self.current_state._is_finished():
            self.make_move(self.choose_move())
            if self.debug:
                print(self.current_state, end="\n")
                print("Nodes in the search tree: {}".format(len(self.search_tree)))

    def expand_search_tree(self):
        raise NotImplementedError(".expand_search_tree() not implemented")

    def add_node(self, node):
        """
        Adds the node to the search tree if it isn't present already, or causes
        a merge with the already present instance of it otherwise.
        """
        if node._node_key() not in self.search_tree:
            self.search_tree[node._node_key()] = node
            return True
        else:
            self.search_tree[node._node_key()].merge(node)
            return False

    def find_best_move(self):
        raise NotImplementedError(".find_best_move() not implemented")
    

class OneStepSearchMixin:
    """
    Expends every unexpanded node in the search tree.
    """
    def expand_search_tree(self):
        expansion_happened = False
        for node in [node for node in self.search_tree.values() if not node.is_expanded]:
            # TODO: Does it really even make sense to distinguish between these after
            #   adding/merging them to/with the search tree?
            old = {}
            new = {}
            for successor in node.expand():
                is_new = self.add_node(successor)
                # FIXME: Ugly copypaste.
                if is_new:
                    new[successor._node_key()] = successor
                else:
                    old[successor._node_key()] = self.search_tree[successor._node_key()]
            node.post_expansion_insertion(old, new)
            expansion_happened = expansion_happened or (len(old) + len(new) > 0)
        return expansion_happened
    

class FullExpansionMixin:
    """
    Run another mixin's expand_search_tree over and oder again until
    the search tree is fully expanded. Do also inherit from i.e.
    OneStepSearchMixin.
    """
    def expand_search_tree(self):
        expansion_happened = False
        while any(not node.is_expanded for node in self.search_tree.values()):
            expansion_happened = super().expand_search_tree() or expansion_happened
        return expansion_happened


class BoundedExpansionMixin:
    """
    """
    def __init__(self, *args, time_limit=0, node_limit=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_limit = time_limit
        self.node_limit = node_limit
    
    def expand_search_tree(self):
        start_time = datetime.now()
        limit_exceeded = False
        while not limit_exceeded:
            expansion_happened = super().expand_search_tree()
            if self.node_limit and len(self.search_tree) >= self.node_limit:
                limit_exceeded = True
            if self.time_limit and (datetime.now() - start_time).total_seconds() >= self.time_limit:
                limit_exceeded = True
            if not expansion_happened:  # Tree is fully expanded
                limit_exceeded = True
            


class NaivePruningMixin:
    """
    Prunes the search tree after make_move(), so that only states
    that are still reachable are kept in it.
    """
    def make_move(self, move):
        super().make_move(move)
        post_move_size = len(self.search_tree)
        transitive_hull = set()
        frontier = set([self.current_state._node_key()])
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

