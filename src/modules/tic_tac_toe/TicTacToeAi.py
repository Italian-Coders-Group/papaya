from core.abc.games.player import Player
from typing import List, Tuple, Dict


class TicTacToeAI(Player):

    def __init__(self, user, symbol, sign):

        self.user = user
        self.symbol = symbol
        self.sign = sign

    def makeMove(self, gameData: Dict) -> int:

        grid = gameData['grid']

        possibleMoves = []
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == '':
                    possibleMoves.append(from2Dto1D((i, j)))
        move = 0

        # Check for possible winning move to take or to block opponents winning move
        for sign in ['o', 'x']:
            for possibleMove in possibleMoves:
                boardCopy = [[],
                             [],
                             []]
                for y, row in enumerate(grid):
                    for x, cell in enumerate(row):
                        boardCopy[y].append(cell)
                posY, posX = from1Dto2D(possibleMove)
                boardCopy[posY][posX] = sign
                if check_for_win(boardCopy, sign):
                    move = possibleMove
                    return from1Dto2D(move)

        # Try to take one of the corners
        cornersOpen = []
        for i in possibleMoves:
            if i in ['1', '3', '7', '9']:
                cornersOpen.append(i)
        if len(cornersOpen) > 0:
            move = choice(cornersOpen)
            return from1Dto2D(move)

        # Try to take the center
        if 5 in possibleMoves:
            move = 5
            return from1Dto2D(move)

        # Take any edge
        edgesOpen = []
        for i in possibleMoves:
            if i in ['2', '4', '6', '8']:
                edgesOpen.append(i)

        if len(edgesOpen) > 0:
            move = choice(edgesOpen)

        return move
