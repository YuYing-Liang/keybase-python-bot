from chessPlayer_lib import *
from chess_board_lib import *

board = boardInit()
printBoard(board)
root = treeNode(board)
genPreCalc(root, 10, 6)