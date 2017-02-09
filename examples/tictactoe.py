#!/usr/bin/env python3

if __name__ == '__main__':
    from bobbot.games.tictactoe import TicTacToeAdapter
    from bobbot.search_tree import BaseAI
    from bobbot.search_tree import OneStepSearchMixin, FullExpansionMixin, NaivePruningMixin
    from bobbot.search_node import ChooseFirstMove, ChooseRandomMove, ChooseRandomMoveFromBest
    
    TicTacToe = type('TicTacToe', (TicTacToeAdapter, ChooseFirstMove), {})
    AI = type('AI', (OneStepSearchMixin, NaivePruningMixin, BaseAI), {})
    ai = AI(TicTacToe(), debug=True)

    ai.play()

