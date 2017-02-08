#!/usr/bin/env python3

if __name__ == '__main__':
    from bobbot.games.nim import NimAdapter
    from bobbot.search_node import RandomOfBestChooser
    from bobbot.search_tree import FullExpansionMixin, NaivePruningMixin, BaseAI
    
    Nim = type('TicTacToe', (NimAdapter, RandomOfBestChooser), {})
    AI = type('AI', (FullExpansionMixin, NaivePruningMixin, BaseAI), {})
    ai = AI(Nim(), debug=True)
    
    ai.play()

