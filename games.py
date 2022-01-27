import numpy as np 

class TTTGame(object):
	
	def __init__(self):		
		self.board = np.empty(9, dtype='object')		

	def printBoard(self):
		#using NumPad layout 
		for row in range(2,-1,-1):
			print("|", self.board[0+3*row], self.board[1+3*row], self.board[2+3*row], "|")
		print('---------')

	def makeMove(self, move, player):
		if move in self.getValidMoves():
			self.board[move-1] = player
		else:
			print("Invalid Move!")

	def getValidMoves(self):
		#return array of possible moves
		result = np.where(self.board == '-')
		return result[0]+1

	def evaluateBoard(self, player):
		#return True/False if game is over, and final score if game over is True
		game_over = False
		score = 0

		#check for draw
		if len(self.getValidMoves()) == 0:
			game_over = True
			score = 0

		rows = np.array([(1,2,3),(4,5,6),(7,8,9)])-1
		cols = np.array([(1,4,7),(2,5,8),(3,6,9)])-1
		diags = np.array([(1,5,9),(3,5,7)])-1

		#check for win
		for row in rows:
			if self.board[row[0]] == self.board[row[1]] == self.board[row[2]] != '-':
				game_over = True
				if self.board[row[0]] == player:
					score = 1
				else:
					score = -1
				break
		for col in cols:
			if self.board[col[0]] == self.board[col[1]] == self.board[col[2]] != '-':
				game_over = True
				if self.board[col[0]] == player:
					score = 1
				else:
					score = -1
				break
		for diag in diags:
			if self.board[diag[0]] == self.board[diag[1]] == self.board[diag[2]] != '-':
				game_over = True
				if self.board[diag[0]] == player:
					score = 1
				else:
					score = -1
				break

		return game_over, score

	def getPlayerMove(self, player):
		#get human input move and check that it is valid
		print('You are playing the', player, "\b's")
		move = int(input("Input Move (Layout Matches Numpad): "))

		if move in self.getValidMoves():
			valid = True
		else:
			valid = False
			print('Invalid Move, Try Again!')

		return move, valid

	def resetGame(self):
		self.board.fill('-')
		print("CONTROLS:\nThe game uses the Numpad layout shown below to enter moves")
		print("| 7 8 9 |")
		print("| 4 5 6 |")
		print("| 1 2 3 |")
		print('---------\n')

	def undoMove(self, move):
		self.board[move-1] = '-'

class Connect4Game(object):
	
	def __init__(self):	
		self.rows = 6
		self.cols = 7
		self.win_count = 4	
		self.board = np.empty((self.rows, self.cols), dtype='object')

	def resetGame(self):
		self.board.fill('-')
		print("CONTROLS:\nEnter the number of the desired column to drop your piece.\n")

	def printBoard(self):
		print("   1   2   3   4   5   6   7")
		print(np.flip(self.board, axis=0),'\n'*2)

	def getValidMoves(self):
		empty = np.where(self.board == '-')
		moves = np.unique(empty[1])+1

		#sort moves optimally
		order = [4,3,5,2,6,1,7]
		sorted_moves = []
		for num in order:
			if num in moves:
				sorted_moves.append(num)

		return sorted_moves

	def makeMove(self, move, player):
		#search from the bottom to find the first empty space
		if move in self.getValidMoves():
			for i, row in enumerate(self.board):
				if row[move-1] == '-':
					self.board[i][move-1] = player
					#print(f"{player} move made at ({i},{move-1})")
					break
		else:
			print("Invalid Move!")

	def undoMove(self, move):
		#search from the top to find the first non empty space
		for i, row in enumerate(np.flip(self.board, axis=0)):
			if row[move-1] != "-":
				self.board[self.rows-1-i][move-1] = "-"
				break

	def getPlayerMove(self, player):
		#get human input move and check that it is valid
		print('You are playing the', player, "\b's")
		move = int(input("Input Move: "))

		if move in self.getValidMoves():
			valid = True
		else:
			valid = False
			print('Invalid Move, Try Again!')

		return move, valid

	def evaluateBoard(self, player):
		#return True/False if game is over, and final score if game over is True
		game_over = False
		score = 0

		#check for draw
		if len(self.getValidMoves()) == 0:
			game_over = True
			score = 0

		#check for win
		#horizontal
		for row in self.board:
			for i in range(self.cols-3):
				if row[i] == row[i+1] == row[i+2] == row[i+3] != "-":
					game_over = True
					if row[i] == player:
						score = 1000
					else:
						score = -1000
					break
		#vertical
		for row in range(self.rows-3):
			for col in range(self.cols):
				if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != "-":
					game_over = True
					if self.board[row][col] == player:
						score = 1000
					else:
						score = -1000
					break 
		#diagonal up-right
		for row in range(self.rows-3):
			for col in range(self.cols-3):
				if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != "-":
					game_over = True
					if self.board[row][col] == player:
						score = 1000
					else:
						score = -1000
					break 
		#diagonal up-left
		for row in range(self.rows-3):
			for col in range(self.cols-4, self.cols):
				if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] != "-":
					game_over = True
					if self.board[row][col] == player:
						score = 1000
					else:
						score = -1000
					break 

		return game_over, score	

	def estimateBoard(self, player, opponent):

		score = 0

		#horizontal
		for row in self.board:
			for i in range(self.cols-3):
				subrow = list(row[i:i+4])
				if subrow.count(player) == 2 and subrow.count('-') == 2:
					score += 2
				if subrow.count(player) == 3 and subrow.count('-') == 1:
					score += 3

		#vertical
		for row in range(self.rows-3):
			for col in range(self.cols):
				subrow = [self.board[row][col], self.board[row+1][col], self.board[row+2][col], self.board[row+3][col]]
				if subrow.count(player) == 2 and subrow.count('-') == 2:
					score += 2
				if subrow.count(player) == 3 and subrow.count('-') == 1:
					score += 3

		#diagonal up-right
		for row in range(self.rows-3):
			for col in range(self.cols-3):
				subrow = [self.board[row][col], self.board[row+1][col+1], self.board[row+2][col+2], self.board[row+3][col+3]]
				if subrow.count(player) == 2 and subrow.count('-') == 2:
					score += 2
				if subrow.count(player) == 3 and subrow.count('-') == 1:
					score += 3

		#diagonal up-left
		for row in range(self.rows-3):
			for col in range(self.cols-4, self.cols):
				subrow = [self.board[row][col], self.board[row+1][col-1], self.board[row+2][col-2], self.board[row+3][col-3]]
				if subrow.count(player) == 2 and subrow.count('-') == 2:
					score += 2
				if subrow.count(player) == 3 and subrow.count('-') == 1:
					score += 3

		return score


# REWORK SO IT LOOKS AT 4 AND SEES IF ITS POSSIBLE CONNECT count 2 empty 2 player or 1 empty 3 player

# player = 'X'

# row = ['X', 'X', 'X', '-', 'O', 'X', 'X']
# score = 0

# for i in range(3):
# 	subrow = row[i:i+4]
# 	if subrow.count(player) == 2 and subrow.count('-') == 2:
# 		score += 2
# 	if subrow.count(player) == 3 and subrow.count('-') == 1:
# 		score += 3

# print(score)