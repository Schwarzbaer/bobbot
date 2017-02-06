#!/usr/bin/env python3

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
        # TODO: ...and clean the search tree

    def play(self):
        if self.debug:
            print(self.current_state, end="\n")
        while not self.current_state.is_finished():
            self.make_move(self.choose_move())
            if self.debug:
                print(self.current_state, end="\n")

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


if __name__ == '__main__':
    #from games.tictactoe import TicTacToe
    #TTT = type('TicTacToeAI', (FullExpansionMixin, BaseAI), {})
    #ai = TTT(TicTacToe(), debug=True)
    from games.nim import Nim
    N = type('TicTacToeAI', (FullExpansionMixin, BaseAI), {})
    ai = N(Nim(), debug=True)
    ai.play()

