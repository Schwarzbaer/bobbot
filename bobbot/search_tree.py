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
        """Run the expansion of the search tree. By default, this
        will just step the expansion algorithm once.
        
        Returns:
            bool: True if any wrapping expand_search_tree should
                interrupt its loop, False if that's irrelevant.
        """
        self.step_search_tree_expansion()

    def step_search_tree_expansion(self):
        """Run a single iteration of the expansion algorithm
        Returns:
            bool: True if any node has actually be expanded, False
                otherwise.
        """
        raise NotImplementedError

    def expand_single_node(self, node):
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
        return (len(old) + len(new) > 0)

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
        raise NotImplementedError


# Expansion


class OneStepSearchMixin:
    """
    Expands every unexpanded node in the search tree.
    """
    def step_search_tree_expansion(self):
        expansion_happened = False
        for node in [node for node in self.search_tree.values() if not node.is_expanded]:
            expansion_happened = self.expand_single_node(node) or expansion_happened
        return expansion_happened


# Expansion Control


class FullExpansionMixin:
    """
    Run another mixin's expand_search_tree over and oder again until
    the search tree is fully expanded. Do also inherit from i.e.
    OneStepSearchMixin.
    """
    def expand_search_tree(self):
        expansion_happened = False
        while any(not node.is_expanded for node in self.search_tree.values()):
            expansion_happened = self.step_search_tree_expansion() or expansion_happened


class BoundedExpansionMixin:
    """Runs another mixin's expand_search until that has pushed the number of
    nodes in the search tree beyond the given limit, or until this loop has
    taken longer than the given limit, or the expansion yields no new nodes,
    possibly because the search tree already is fully expanded.
    
    Note that these limits are checked only after each expansion step, so they
    will not apply exactly when the limit is hit, only thereafter, and that it
    is up to the other mixin to terminate its expansions every now and then.
    For example, putting the FullExpansionMixin between this and the actual
    mixin doing the expansion would nullify this mixin's functionality
    completely.
    
    Also note that when using a node limit, a pruning mixin should be used,
    otherwise further expansions are guaranteed to only run for one cycle
    each.
    """
    def __init__(self, *args, time_limit=0, node_limit=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_limit = time_limit
        self.node_limit = node_limit
    
    def expand_search_tree(self):
        start_time = datetime.now()
        limit_exceeded = False
        while not limit_exceeded:
            expansion_happened = self.step_search_tree_expansion()
            if self.node_limit and len(self.search_tree) >= self.node_limit:
                limit_exceeded = True
            if self.time_limit and (datetime.now() - start_time).total_seconds() >= self.time_limit:
                limit_exceeded = True
            if not expansion_happened:
                limit_exceeded = True


# Combined expansion and expansion Control


# FIXME: This is not quite Iterative Deepening, but there must be a
# better known name for it.
class ForwardSweepingMixin:
    """
    """

    def __init__(self, *args, search_depth=0, **kwargs):
        assert search_depth > 0
        super().__init__(*args, **kwargs)
        self.search_depth = search_depth

    def expand_search_tree(self):
        # FIXME: What's the setdefault here?
        # FIXME: The recurring +1 smells bad.
        self.search_layers = {layer: set() for layer in range(self.search_depth + 1)}
        self.search_layers[0] = {self.current_state}
        self.search_layers.setdefault(set)
        known_nodes = {self.current_state}
        for depth in range(1, self.search_depth + 1):
            print("processiong layer {} following {} nodes".format(depth, len(self.search_layers[depth - 1])))
            # FIXME: This loop is b0rked
            for node in self.search_layers[depth - 1]:
                # FIXME: Filter out nodes that have been previously encountered
                candidates = set(node.get_successors().values()) - known_nodes
                self.search_layers[depth].update(candidates)
                known_nodes.update(candidates)
        self.current_layer = 0
        while self.step_search_tree_expansion() and self.current_layer < self.search_depth:
            self.current_layer += 1

    def step_search_tree_expansion(self):
        # FIXME: SearchNode.is_expanded should probably be a function.
        for node in [node for node in self.search_layers[self.current_layer] if not node.is_expanded]:
            self.expand_single_node(node)


# Pruning


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
                            for node_key in self.search_tree[expansion].get_successors()
                            if node_key not in transitive_hull)
        nodes_to_delete = set(self.search_tree.keys()) - transitive_hull
        for key in nodes_to_delete:
            del self.search_tree[key]
        # FIXME: This requires nodes to also know predecessor node key, not just their objects.
        # for node in self.search_tree.values():
        #     node.remove_predecessors(nodes_to_delete)
        post_prune_size = len(self.search_tree)
        if self.debug:
            print("Search tree size: {} (after move) - {} (pruned) = {}".format(
                post_move_size,
                post_move_size - post_prune_size,
                post_prune_size)
            )

