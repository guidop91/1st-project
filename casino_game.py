from random import shuffle

class Deck:
	def __init__(self):
		
		self.cards = []

		self.populate()
		shuffle(self.cards) #Shuffles cards

	def populate(self):
		#Creates deck of cards
		symbol = ["Spade","Diamond","Heart","Club"]
		number = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]

		for i in symbol:
			for j in number:
				self.cards.append(tuple([i,j]))

		return self.cards

	def draw_card(self):
		return self.cards.pop()

	def deal_player(self,player):
		for i in range(0,4):
			player.hand.append(self.draw_card())
		return player.hand

class Player():
	has_build = False
	def __init__(self,name):

		self.name = name
		self.hand = []

	def build(self,table):
		print(table.in_game)
		possible = False
		finished = False

		while not possible and not finished:
			selection = input("Which card would you like to add to the build? Enter from\
				1 to %d in the order of the cards shown above, \n 1 being the first and\
				%d being the last." % (len(table.in_game),len(table.in_game)))


class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())
		return self.in_game