from chessPlayer_lib import *
from random import choice

def chessPlayer(board, player):
	oCanList = []
	root = treeNode(board)
	noError = root.genCandidate(player, 3)

	for child in root.candidate:
		oCanList += [[child.move, child.worth]]

	childMove = choice(root.candidate)
	move = [childMove.move, childMove.worth]

	tree = root.getLevelOrder()

	return([noError, move, oCanList, tree])