#!/usr/bin/env python3

if __name__ == '__main__':
    from bobbot.games.tictactoe import TicTacToeAdapter
    from bobbot.search_node import RandomOfBestChooser
    from bobbot.search_tree import FullExpansionMixin, NaivePruningMixin, BaseAI
    
    TicTacToe = type('TicTacToe', (TicTacToeAdapter, RandomOfBestChooser), {})
    AI = type('AI', (FullExpansionMixin, NaivePruningMixin, BaseAI), {})
    ai = AI(TicTacToe(), debug=True)

    ai.play()

