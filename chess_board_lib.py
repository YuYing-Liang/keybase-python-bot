from PIL import Image
def boardInit():
	numRow = 8
	numCol = 8
	board = [0]*(numCol*numRow)

	for xi in range(numCol):
		addPiece(board, 1, 0, xi, 1)  # White, Pawn, xPos, row 1
		addPiece(board, 2, 0, xi, 6)  # Black, Pawn, xPos, row 6

	# Placing Rooks
	addPiece(board, 1, 3, 0, 0)  # White, Rook, col 0, row 0
	addPiece(board, 1, 3, 7, 0)  # White, Rook, col 7, row 0

	addPiece(board, 2, 3, 0, 7)  # Black, Rook, col 0, row 7
	addPiece(board, 2, 3, 7, 7)  # Black, Rook, col 7, row 7

	# Placing Knights
	addPiece(board, 1, 1, 1, 0)  # White, Knight, col 1, row 0
	addPiece(board, 1, 1, 6, 0)  # White, Knight, col 6, row 0

	addPiece(board, 2, 1, 1, 7)  # Black, Knight, col 1, row 7
	addPiece(board, 2, 1, 6, 7)  # Black, Knight, col 6, row 7

	# Placing Bishops
	addPiece(board, 1, 2, 2, 0)  # White, Bishops, col 2, row 0
	addPiece(board, 1, 2, 5, 0)  # White, Bishops, col 5, row 0
		
	addPiece(board, 2, 2, 2, 7)  # Black, Bishops, col 2, row 7
	addPiece(board, 2, 2, 5, 7)  # Black, Bishops, col 5, row 7

	# Placing Queen and King
	addPiece(board, 1, 4, 3, 0),  # White, Queen, col 3, row 0
	addPiece(board, 1, 5, 4, 0)   # White, King, col 4, row 0
	
	addPiece(board, 2, 4, 3, 7),  # Black, Queen, col 3, row 7
	addPiece(board, 2, 5, 4, 7)   # Black, King, col 4, row 7

	return(board)

def addPiece(board, colour, piece, x, y):
	numCol = 8
	numRow = 8

	board[y*numCol + x] = int(str(colour) + str(piece))
	return(board)

def drawBoard(board):
	"""
	Prints the Board with images
	Arguments: None
	Returns: Completion State
	"""
	chessBoard = Image.open("img/board.png")
	numCol, numRow = 8, 8
	playerList = ['w', 'b']
	pieceList = ['Pawn', 'Knight', 'Bishop', 'Castle', 'Queen', 'King']
	for position in range(0, numRow*numCol, 1):
		row = int((position-position%numCol)/numCol)
		column = position%numCol
		tile = board[position]

		xPos = 47+5+column*67
		yPos = (numRow-row-1)*67+5

		if tile != 0:
			pType = tile % 10  # Finding piece type
			player = tile - pType
			imgPath = "img/"+playerList[int((player/10)-1)]+pieceList[pType]+".png"
			piece = Image.open(imgPath)
			chessBoard.paste(piece, (xPos, yPos), piece)
	chessBoard.save("tempBoard.png")


def printBoard(board):
	"""
	|	Prints the Board in a Readable Format.
	|	Arguments: None
	|	Returns: Completion State
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	playerList = ['W', 'B']
	pieceList = ['P', 'N', 'B', 'R', 'Q', 'K']
	outputString = "  ╚"+("═"*4+"╧")*7+"═"*4+"╝"
	rowString = "1" +  " ║"
	for position in range(0, numRow*numCol, 1):
		row = int((position-position%numCol)/numCol)
		column = position%numCol
		tile = board[position]

		if row%2 != 0 and column%2 != 0:
			whiteSpace = " "
			#rowString += str(position)[0] + "░░" + str(position)[1]
		elif row%2 != 0 and column%2 == 0:
			whiteSpace = "█"
			#rowString += str(position)[0] + "▓▓" + str(position)[1]
		elif row%2 == 0 and column%2 != 0:
			whiteSpace = "█"
			#rowString += str(position)[0] + "▓▓" + str(position)[1]
		elif row%2 == 0 and column%2 == 0:
			whiteSpace = " "
			#rowString += str(position)[0] + "░░" + str(position)[1]

		if tile == 0:
			rowString += whiteSpace + "%02d" % position + whiteSpace
		else:
			pType = tile%10  # Finding piece type
			player = tile - pType
			#rowString += whiteSpace + playerList[int((player/10)-1)] + pieceList[pType] + whiteSpace
			posString = "%02d" % position
			#rowString += posString[0] + playerList[int((player/10)-1)] + pieceList[pType] + posString[1]
			rowString += playerList[int((player/10)-1)] + pieceList[pType] + posString 
		if column != numCol-1:
			rowString += "│"
		else:
			rowString += "║\n"
			if row != 0:
				outputString = "  ╟" + ("─"*4+ "┼")*7 + "─"*4 + "╢" + "\n" + outputString
			outputString = rowString + outputString
			rowString = str(row+2) + " ║"
	outputString = "  ╔"+("═"*4+"╤")*7+"═"*4+"╗\n" + outputString
	outputString = "    A    B    C    D    E    F    G    H\n" + outputString
	print(outputString)