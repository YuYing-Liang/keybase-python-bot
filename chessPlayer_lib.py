from chess_board_lib import *
class treeNode:
	def __init__(self, board):
		"""
		|	Initializes class variables
		|	Arguments	   : board    | Data struct
		|	Class Variables: board    | Datastruct
		|				   : worth    | int value
		|				   : move 	  | list in the form [pos, move] or None
		|				   : mmValue  | 
		|				   : treeList | list of treeNode class objects
		"""
		self.board = list(board)
		self.worth = self.worthCalc()
		self.childList = []

		self.move = []
		self.candidate = []
		self.mmValue = None

	def worthCalc(self):
		"""
		|	Calculates the worth of the board based on 'Reinfeld Values'
		|	Arguments: None
		|	Returns  : Numeric sum of the 'worth' of piece on the board
		"""
		worthList = [100, 320, 330, 500, 900, 20000]  # Based on 'Reinfeld Values'
		#worthList = [5, 30, 30, 50, 90, 100000]
		worth = 0

		for pos, piece in enumerate(self.board):  # For every piece
			if piece == 0: continue  # If null piece, ignore
			pieceType = piece%10  # Finding piece type
			colour = piece - pieceType  # finding the colour
			if colour == 10: mult = 1  # if it should be plus or minus
			else: mult = -1  
			worth += mult*(worthList[pieceType] + self.evalPosMatrix(pos, pieceType, colour))  # Add the worth

		return(worth)

	def evalPosMatrix(self, pos, piece, colour):
		listIndex = int(colour/10)-1
		paMatrixBlack = [0,  0,  0,  0,  0,  0,  0,  0,
						 50, 50, 50, 50, 50, 50, 50, 50,
						 10, 10, 20, 30, 30, 20, 10, 10,
 						 5,  5, 10, 25, 25, 10,  5,  5,
 						 0,  0,  0, 20, 20,  0,  0,  0,
 						 5, -5,-10,  0,  0,-10, -5,  5,
						 5, 10, 10,-20,-20, 10, 10,  5,
 						 0,  0,  0,  0,  0,  0,  0,  0]
		paMatrixWhite = list(paMatrixBlack[::-1])

		knMatrixBlack = [-50,-40,-30,-30,-30,-30,-40,-50,
						 -40,-20,  0,  0,  0,  0,-20,-40,
						 -30,  0, 10, 15, 15, 10,  0,-30,
						 -30,  5, 15, 20, 20, 15,  5,-30,
						 -30,  0, 15, 20, 20, 15,  0,-30,
						 -30,  5, 10, 15, 15, 10,  5,-30,
						 -40,-20,  0,  5,  5,  0,-20,-40,
						 -50,-40,-30,-30,-30,-30,-40,-50]
		knMatrixWhite = list(knMatrixBlack[::-1])

		biMatrixBlack = [-20,-10,-10,-10,-10,-10,-10,-20,
						 -10,  0,  0,  0,  0,  0,  0,-10,
						 -10,  0,  5, 10, 10,  5,  0,-10,
						 -10,  5,  5, 10, 10,  5,  5,-10,
						 -10,  0, 10, 10, 10, 10,  0,-10,
						 -10, 10, 10, 10, 10, 10, 10,-10,
						 -10,  5,  0,  0,  0,  0,  5,-10,
						 -20,-10,-10,-10,-10,-10,-10,-20]
		biMatrixWhite = list(biMatrixBlack[::-1])

		roMatrixBlack = [ 0,  0,  0,  0,  0,  0,  0,  0,
						  5, 10, 10, 10, 10, 10, 10,  5,
						 -5,  0,  0,  0,  0,  0,  0, -5,
						 -5,  0,  0,  0,  0,  0,  0, -5,
						 -5,  0,  0,  0,  0,  0,  0, -5,
						 -5,  0,  0,  0,  0,  0,  0, -5,
						 -5,  0,  0,  0,  0,  0,  0, -5,
						  0,  0,  0,  5,  5,  0,  0,  0]
		roMatrixWhite = list(roMatrixBlack[::-1])

		quMatrixBlack = [-20,-10,-10, -5, -5,-10,-10,-20,
						 -10,  0,  0,  0,  0,  0,  0,-10,
						 -10,  0,  5,  5,  5,  5,  0,-10,
						  -5,  0,  5,  5,  5,  5,  0, -5,
						   0,  0,  5,  5,  5,  5,  0, -5,
						 -10,  5,  5,  5,  5,  5,  0,-10,
						 -10,  0,  5,  0,  0,  0,  0,-10,
						 -20,-10,-10, -5, -5,-10,-10,-20]
		quMatrixWhite = list(quMatrixBlack[::-1])

		kiMatrixBlack = [-30,-40,-40,-50,-50,-40,-40,-30,
						 -30,-40,-40,-50,-50,-40,-40,-30,
						 -30,-40,-40,-50,-50,-40,-40,-30,
						 -30,-40,-40,-50,-50,-40,-40,-30,
						 -20,-30,-30,-40,-40,-30,-30,-20,
						 -10,-20,-20,-20,-20,-20,-20,-10,
						  20, 20,  0,  0,  0,  0, 20, 20,
						  20, 30, 10,  0,  0, 10, 30, 20]
		kiMatrixWhite = list(kiMatrixBlack[::-1])


		matrixList = [[paMatrixWhite, paMatrixBlack], [knMatrixWhite, knMatrixBlack],
					  [biMatrixWhite, biMatrixWhite], [roMatrixWhite, roMatrixBlack],
					  [quMatrixWhite, quMatrixBlack], [kiMatrixWhite, kiMatrixBlack]]
		return(matrixList[piece][listIndex][pos])

	def returnByDepth(self):
		"""
		|	Is recursively run, returns a tree in list format and the mmValue 
		|	Arguments: None
		|	Returns  : A tree in list format [worth, board, [[worth1, board1, [...]], [worth2, board2, [...]]]]
		"""
		output = [self.worth, self.board, []]
		for obj in self.childList:
			output[2] +=  [obj.returnByDepth()]
		return(output)

	def genTree(self, player, depth):
		"""
		|	Generates a tree based on the current board, w/ depth limit
		|	Arguments: depth | the depth limit, current node is depth 0
		|	Arguments: player| the next turn of the tree
		|	Returns  : True or success
		"""
		self.childList = []  # Clearing previous entries
		if depth == 0 or incheck(self.board, player):  # Exit case
			return()

		# Defining Conditional Variables
		listIndex = int(player/10)-1
		playerList = [20, 10]
		modeList = [max, min]
		maxEvalList = [-99999999999999999999999, 99999999999999999999999]
		
		nextPlayer = playerList[listIndex]  # If white, next player is black
		mode = modeList[listIndex]  # Goal of white is to max black is to min
		maxEval  = maxEvalList[listIndex]  # Defining a value that will always be smaller for white, and larger for black
		
		# Recursivly calling genTree
		for pos in GetPlayerPositions(self.board, player):
			for move in GetRawPieceLegalMoves(self.board, player):
				child = treeNode(altBoard(self.board, pos, move))
				child.move = [pos, move]
				mmValue = child.genTree(nextPlayer, depth-1)
				self.childList += [child]

				maxEval = mode(maxEval, mmValue)  # AB pruning step

		self.mmValue = maxEval
		return(maxEval)

	def genTreeAB(self, player, depth, alpha=-99999999, beta=99999999):
		"""
		|	Generates a tree based on the current board, w/ depth limit and alpha beta pruning
		|	Arguments: depth | the depth limit, current node is depth 0
		|			   player| the next turn of the tree
		|			   alpha | value to evaulate ab
		|			   beta  | value to evaulate beta
		|	Returns  : True or success
		"""
		self.childList = []  # Clearing any pre existing values
		totalPosList = []
		if depth == 0 or incheck(self.board, player):  # exit case, if depth is 0 or less than 0
			return(self.worth)  # Return the value of the final node

		# Defining Conditional Variables
		listIndex = int(player/10)-1
		playerList = [20, 10]
		modeList = [max, min]
		maxEvalList = [-99999999, 99999999]
		endRow = [7, 0]

		nextPlayer = playerList[listIndex]  # If white, next player is black
		mode = modeList[listIndex]  # Goal of white is to max black is to min
		maxEval  = maxEvalList[listIndex]  # Defining a value that will always be smaller for white, and larger for black		
		
		# Generating a list of player positions
		for pos in GetPlayerPositions(self.board, player):
			for move in RawGetPieceLegalMoves(self.board, pos):
				totalPosList += [[pos, move]]

		# Recursivly calling genTreeAB using AB pruning
		for move in totalPosList:
			
			tile = self.board[move[0]]
			pieceType = tile%10
			colour = tile-pieceType
			row = int((move[1]-(move[1]%8))/8)

			end = endRow[int(colour/10)-1]
			if tile == colour and row == end:
				quBoard = list(self.board)
				quBoard[move[0]] = player+4
				childNode = treeNode(altBoard(quBoard, move[0], move[1]))
			else:

				childNode = treeNode(altBoard(self.board, move[0], move[1]))  # Recursive step
			
			childNode.move = move
			mmValue = childNode.genTreeAB(nextPlayer, depth-1, alpha, beta)
			self.childList += [childNode]
			#print(self.childList, nextPlayer)

			maxEval = mode(maxEval, mmValue)  # AB pruning step
			if player == 10: alpha = mode(alpha, mmValue)
			else: beta = mode(beta, mmValue)

			if beta<=alpha:
				break
		self.mmValue = maxEval
		return(maxEval)

	def genCandidate(self, player, depth, AB=1):
		"""
		|	Returns a list of candidate nodes using the minMax algorithm
		|	Arguments: player
		|	Retrurns : A list of treeNode 
		"""
		candidateMoves = []
		try:
			if AB == 1: self.genTreeAB(player, depth)
			else: self.genTree(player, depth)
		except:	
			return(False)
		else:
			for child in self.childList:
				if child.mmValue == self.mmValue:
					candidateMoves += [child]
			self.candidate = candidateMoves

			return(True)

	def getLevelOrder(self):
		output = []
		queue = []
		queue += [[True, [self.move, self.worth, self.childList]]]
		while (len(queue) > 0):
			if queue[0][0] != False:
				output += [[queue[0][1][0], queue[0][1][1]]]
				childList = queue[0][1][2]
				queue = queue[1:]
				for child in childList:
					queue += [[True, [child.move, child.worth, child.childList]]]
		return(output)

def GetPlayerPositions(board, player):
	"""
	|	Gives a list of player positions
	|	Arguments: board  | Data struct
	|			 : player |	10 white 20 black
	|	Returns  : A list of player positions
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	pawnList, knList, biList, roList, quList, kiList = [], [], [], [], [], []
	pieceTypeList = [pawnList, knList, biList,
					roList, quList, kiList]

	for i in range(0, numCol*numRow):
		# Finding out if it is Black or White, and what piece
		tile = board[i]
		pieceType = tile%10
		cPlayer = tile-(tile%10)

		# Adding the position
		if cPlayer == player:
			pieceTypeList[pieceType] += [i]
	posList = pawnList + knList + biList + roList + quList + kiList  # Adding the valid moves in order of piece worth
	return(posList)

def GetPieceLegalMoves(board, position):
	"""
	|	Returns a list of all legal positions - excludes moves that would jepordize king
	|	Arguments: board 	| Data structure
	|			 : position | int, index for board
	|	Returns  : A list of valid move positions
	"""
	# Defining Variables
	piece = board[position]
	pieceType = piece%10  # Finding piece type
	enemyList = [20, 10]
	
	ally = piece - pieceType
	enemy = enemyList[int((ally/10)-1)] # Finding Enemy and Ally
	
	moveList = []

	rawMoveList = RawGetPieceLegalMoves(board, position)  # Generating raw list of legal moves
	for move in rawMoveList:  # Filtering moves which would jepordize the king
		copyBoard = altBoard(board, position, move)
		kingPos = pieceFind(copyBoard, ally+5)  # Finding the king in this board
		if kingPos == (-1):  # If there is no king, assume it is an error case
			return(rawMoveList)
		if IsPositionUnderThreat(copyBoard, kingPos, ally) == False:
			moveList += [move]
	return(moveList)

def RawGetPieceLegalMoves(board, position):
	"""
	|	Returns a list of all legal positions - includes moves that would jepordize king
	|	Arguments: board 	| Data structure
	|			 : position | int, index for board
	|	Returns  : A list of valid move positions
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	piece = board[position]
	enemyList = [20, 10]
	helpFuncList = [pwnLegalMoves, knLegalMoves, biLegalMoves,
					roLegalMoves, quLegalMoves, kiLegalMoves]

	pType = piece%10  # Finding piece type
	ally = piece - pType
	enemy = enemyList[int((ally/10)-1)] # Finding Enemy and Ally
	moveList = []

	function = helpFuncList[pType]  # Selecting appropriate function

	# Finding list of allies and enemies
	allyList = GetPlayerPositions(board, ally)
	enemyList = GetPlayerPositions(board, enemy)

	# Calling function
	moveList = function(position, ally, allyList, enemyList)
	return(moveList)

def pwnLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the pawn
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	direcList = [1, -1]
	moveList = []

	direc = direcList[int((colour/10)-1)]  # Defining Direction

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	if row+direc in range(0, numRow, 1):  # If row outside accepted range
		fPos = (row+direc)*numCol + column
		if (fPos not in allyList and fPos not in enemyList):  # Not in allyList or enemyList
			moveList += [fPos]
		if (column + 1 in range(0, numCol, 1) and fPos+1 in enemyList):  # Looking at the right
			moveList += [fPos+1]
		if (column - 1 in range(0, numCol, 1) and fPos-1 in enemyList):  # Looking at the left
			moveList = [fPos-1] + moveList

	return(moveList)

def knLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the knight
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	direcList = [1, -1]
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for direc in direcList:  # For both directions
		xVector = direc  # Defining vector from origin
		yVector = 2
		for i in range(0, 4, 1):  # Rotating vector 4 times
			newRow = row + yVector  # If finding newRow and newCol
			newCol = column + xVector
			if newRow in range(0, numRow) and newCol in range(0, numCol):  # If the newRow and newCol is valid
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If there is no ally already in pos
					moveList += [newPos]
			xVector, yVector = yVector, -xVector  # Rotating vector by 90 degrees
	return(moveList)

def biLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the bishop
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 1, 1
	cnst = 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for i in range(0, 4, 1):  # 4 rotations
		while 1:  # For an undetermined time
			newRow = row + cnst*yVector  # Translating to row and col
			newCol = column + cnst*xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]  # Adding to move list
					if newPos in enemyList:  # If an enemy stopping here
						xVector, yVector = yVector, -xVector  # If an ally, rotate
						cnst = 1  # reset counter
						break
					cnst += 1  # If not stopped, increasing the constant
					continue  # Re-run while loop
			xVector, yVector = yVector, -xVector  # If an ally, rotate
			cnst = 1  # reset counter
			break  # stop while loop
	return(moveList)

def roLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the rook
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 0, 1
	cnst = 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for i in range(0, 4, 1):  # 4 rotations
		while 1:  # For an undetermined time
			newRow = row + cnst*yVector  # Translating to row and col
			newCol = column + cnst*xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]  # Adding to move list
					if newPos in enemyList:  # If an enemy stopping here
						xVector, yVector = yVector, -xVector  # If an ally, rotate
						cnst = 1  # reset counter
						break
					cnst += 1  # If not stopped, increasing the constant
					continue  # Re-run while loop
			xVector, yVector = yVector, -xVector  # If an ally, rotate
			cnst = 1  # reset counter
			break  # stop while loop
	return(moveList)

def quLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the queen
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	
	# Combination of bishop and rook legal moves
	moveList = []
	moveList += biLegalMoves(position, colour, allyList, enemyList)
	moveList += roLegalMoves(position, colour, allyList, enemyList)
	return(moveList)

def kiLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the king
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 0, 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for n in range(0, 2, 1):
		for i in range(0, 4, 1):
			newRow = row + yVector  # Translating to row and col
			newCol = column + xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]
			xVector, yVector = yVector, -xVector  # If an ally, rotate
		xVector, yVector = 1, 1  # starting again with a different vector
	return(moveList)

def IsPositionUnderThreat(board, position, player):
	"""
	|	Returns true or false depending on is the position is under threat
	|	Arguments: board    | Data Structure
	|			 : position | int between [0, 64)
	|			 : player   | int, 10 for white, 20 for black
	|	Returns  : Boolean
	"""
	# Defining variables
	numCol, numRow = 8, 8

	playerTypes = [20, 10]
	direcList = [1, -1]
	direc = direcList[int((player/10)-1)]
	funcList = [pwnLegalMoves, knLegalMoves, biLegalMoves,
				roLegalMoves, quLegalMoves, kiLegalMoves]
	enemy = playerTypes[int((player/10)-1)]
	allyList = GetPlayerPositions(board, player)
	enemyList = GetPlayerPositions(board, enemy)

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	if row+direc in range(0, numRow):
		for di in direcList:
			if column+di in range(0, numCol):
				if enemy == board[(row+direc)*numCol+(column+di)]:
					return(True)

	for piece in [2, 3]:
		posList = funcList[piece](position, player, allyList, enemyList)
		for pos in posList:
			if enemy+piece == board[pos] or enemy+4 == board[pos]:
				return(True)

	posList = funcList[1](position, player, allyList, enemyList)
	for pos in posList:
			if enemy+1 == board[pos]:
				return(True)

	posList = funcList[5](position, player, allyList, enemyList)
	for pos in posList:
			if enemy+5 == board[pos]:
				board[pos]
				return(True)
	return(False)

def pieceFind(board, piece):
	"""
	|	Returns an index of the piece
	|	Arguments: board | Data Structure
	|			 : piece | int between [0, 64)
	|	Returns  : integer, if <0 failure, if >=0 valid index
	"""
	counter = 0
	for i in range(0, len(board)):
		if board[i] == piece:
			return(i)
	return(-1)

def altBoard(board, pos, move):
	"""
	|	Returns a varient on the current board 
	|	Arguments: board | Data Structure
	|			 : pos   | Current position
	|			 : move  | Move piece to
	|	Returns  : board | Data Structure
	"""
	copyBoard = list(board)
	copyBoard[move] = copyBoard[pos]
	copyBoard[pos] = 0
	return(copyBoard)

def incheck(board, player):
	kingPos = pieceFind(board, player+5)
	if IsPositionUnderThreat(board, kingPos, player) and len(GetPieceLegalMoves(board, kingPos)) == 0:
		return(True)
	return(False)
'''
	def candidateMoves(self, player, depth, AB=1):
		"""
		|	Returns a list of candidate nodes using the minMax algorithm
		|	Arguments: player
		|	Retrurns : A list of treeNode 
		"""
		candidateMoves = []
		if AB == 1: self.genTreeAB(player, depth)
		else: self.genTree(player, depth)
		for child in self.childList:
			if child.mmValue == self.mmValue:
				candidateMoves += [child]
		self.noOfMovesRating(player, candidateMoves)
		candidateMoves = self.pawnAnalysis(player, candidateMoves)
		return(candidateMoves)

	def noOfMovesRating(self, player, candidateMoves):
		for candiate in candidateMoves:
			count = 0
			board = candiate.board
			for pos in GetPlayerPositions(board, player):
				for move in GetPieceLegalMoves(board, pos):
					if board[pos] != player + 5:
						count += 1
					else:
						count -= 1
			candiate.rating += count


	def pawnAnalysis(self, player, canMoves):
		"""
		|	Returns a list of reduced candiate nodes based on some analysis of pawn structures
		|	Refernces Structures from article: https://thechessworld.com/articles/endgame/7-basic-pawn-structure-you-must-know/
		|	Arguments: player
		|	Retrurns : A list of treeNode 
		"""

		ratingList = []
		candidateMoves = []
		pawnList = [pos for pos in GetPlayerPositions(self.board, player) if self.board[pos] == player]
		for child in canMoves:
			r = max(child.passedDown(player, pawnList), child.isolatedPawn(player, pawnList),
				     child.connectedPawn(player, pawnList), child.doubledPawns(player, pawnList))
			self.rating += r
			ratingList += [self.rating]
		maxRating = max(ratingList)
		for i, rating in enumerate(ratingList):
			if rating == maxRating:
				candidateMoves += [canMoves[i]]
		return(candidateMoves)
	
	def passedDown(self, player, pawnList):  # Max rating of 2, min of 0
		numCol, numRow = 8, 8
		index = int(player/10)-1
		endRowList = [7, 0]
		endRow =  endRowList[index]

		for pawn in pawnList:
			col = pawn%numCol
			row = int((pawn-col)/numCol)
			rating = abs(row-endRow)
			if rating <= 1: return(5)
			if rating == 2: return(2)
			else: return(0)

	def isolatedPawn(self, player, pawnList):  # Max rating of 0, min of -2
		numCol, numRow = 8, 8
		rating = 0
		
		for pawn in pawnList:
			col = pawn%numCol
			row = int((pawn-col)/numCol)
			upRow, downRow = row+1, row-1
			rightCol, leftCol = col+1, col-1

			for surrRow in [upRow, downRow]:
				if surrRow in range(0, numRow):
					for surrCol in [rightCol, leftCol]:
						if surrCol in range(0, numCol):
							tilePos = surrRow*numCol + surrCol
							tile = self.board[tilePos]
							if tile == 0:
								rating -= (1/4)
		if rating <= -2:
			return(-2)
		return(rating)
	def connectedPawn(self, player, pawnList):  # Max rating of 2, min of 0
		numCol, numRow = 8, 8
		rating = 0
		
		for pawn in pawnList:
			col = pawn%numCol
			row = int((pawn-col)/numCol)
			rightCol, leftCol = col+1, col-1

			for surrCol in [rightCol, leftCol]:
				if surrCol in range(0, numCol):
					tilePos = row*numCol + surrCol
					tile = self.board[tilePos]
					if tile == player:
						rating += 1
		if rating >= 2:
			return(2)
		return(rating)

	def doubledPawns(self, player, pawnList):  # Max rating of 0, min of -2
		numCol, numRow = 8, 8
		rating = 0
		
		for pawn in pawnList:
			col = pawn%numCol
			row = int((pawn-col)/numCol)
			upRow, downRow = row+1, row-1

			for surrRow in [upRow, downRow]:
				if surrRow in range(0, numRow):
					tilePos = surrRow*numCol + col
					tile = self.board[tilePos]
					if tile == 0:
						rating -= 1
		return(rating)
	'''