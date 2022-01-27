import numpy as np
from games import TTTGame, Connect4Game

class Agent(object):

	def __init__(self):		
		self.game = Connect4Game()
		self.agent = 'X'
		self.opponent = 'O'
		self.prunes = 0 
		self.prune_depths = 0
		self.MAX_DEPTH = 6

	def PlayGame(self):
		print('Starting Game!\n')	
		self.game.resetGame()

		game_over = False
		valid = False	

		#flip a coin to determine if human or computer goes first
		turn = np.random.randint(2)
		if turn == 0:
			print("Computer goes first!")
			self.agent = 'X'
			self.opponent = 'O'
		else:
			print("Human goes first!")
			self.agent = 'O'
			self.opponent = 'X'

		players = [self.agent, self.opponent]

		self.game.printBoard()

		while not game_over:
			#keep track of which player's turn it is
			player = players[turn%2]

			if player == self.agent:
				#MiniMax returns all the best moves (tied for best) and picks one randomly
				#this is done to make the games more varied instead of always the same move
				print("Thinking...", end='\r')
				moves = self.MiniMax()
				move = moves[np.random.randint(len(moves))]
				print("Computer's Move")
			else:
				#get a valid human input move
				while not valid:
					move, valid = self.game.getPlayerMove(player)
				valid = False

			#make the player's move and determine if the game is over
			self.game.makeMove(move, player)
			self.game.printBoard()

			if player == self.agent:
				print("Alpha/Beta Pruning Statistics:")
				if self.prunes > 0:
					print(self.prunes, "prunes with an average depth of", self.prune_depths/self.prunes)
				else:
					print("No prunes")
				print()

			game_over, score = self.game.evaluateBoard(player)
			#print(game_over, score)
			if game_over:
				if score == 1000:
					print('Player', player, 'wins!')
					break
				elif score == 0:
					print('It''s a draw!')
					break

			turn += 1


	def MiniMax(self):
		best_moves = [-1]
		best_score = -9999	

		alpha = -9999
		beta = 9999	

		depth = 0

		self.prunes = 0
		self.prune_depths = 0

		#run the MiniMax algorithm to get a list of the best moves
		for move in self.game.getValidMoves():
			self.game.makeMove(move, self.agent)
			score = self.Min(alpha, beta, depth+1)
			# print("Move", move, "score", score)
			if score > best_score:
				best_score = score
				best_moves = [move]
			elif score == best_score:
				#add any extra moves that are tied for the best
				best_moves.append(move)

			self.game.undoMove(move)

		# print(f"Best Moves: {best_moves} with score {best_score}")
		return best_moves

	def Min(self, alpha, beta, depth):

		#check if game is over, if not then continue MiniMax
		game_over, score = self.game.evaluateBoard(self.agent)
		if game_over:
			return score
		elif depth >= self.MAX_DEPTH:
			return self.game.estimateBoard(self.agent, self.opponent) - self.game.estimateBoard(self.opponent, self.agent)
		else:
			for move in self.game.getValidMoves():
				#print(f"Min at depth {depth}")
				self.game.makeMove(move, self.opponent)
				score = self.Max(alpha, beta, depth+1)
				self.game.undoMove(move)
				#update beta score and prune the rest of the branch if alpha >= beta
				if score < beta:
					beta = score				
				if alpha >= beta:
					#print("Prune at depth", depth, "with alpha/beta scores:", alpha, beta)
					self.prunes += 1
					self.prune_depths += depth
					break
			return beta

	def Max(self, alpha, beta, depth):

		game_over, score = self.game.evaluateBoard(self.agent)
		if game_over:
			return score
		elif depth >= self.MAX_DEPTH:
			return self.game.estimateBoard(self.agent, self.opponent) - self.game.estimateBoard(self.opponent, self.agent)
		else:
			for move in self.game.getValidMoves():
				#print(f"Max at depth {depth}")
				self.game.makeMove(move, self.agent)
				score = self.Min(alpha, beta, depth+1)
				self.game.undoMove(move)
				#update alpha score and prune the rest of the branch if alpha >= beta
				if score > alpha:
					alpha = score
				if alpha >= beta:
					#print("Prune at depth", depth, "with alpha/beta scores:", alpha, beta)
					self.prunes += 1
					self.prune_depths += depth
					break
			return alpha



agent = Agent()
agent.PlayGame()