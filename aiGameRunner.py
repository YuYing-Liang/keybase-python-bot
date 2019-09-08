from chessPlayer_lib import *
from chess_board_lib import *
from chessPlayer import *
from time import sleep

board = boardInit()
player = 20
while 1:
	printBoard(board)
	drawBoard(board)
	print(board)
	if incheck(board, player):
		print(player, ' Check')
		break
	move = chessPlayer(board, player)
	print(move[1][0])
	board = altBoard(board, move[1][0][0], move[1][0][1])
	if player == 10:
		player = 20
	else:
		player = 10
	input()
