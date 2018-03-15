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
				self.cards.append([i,j])

		return self.cards

	def draw_card(self):
		return self.cards.pop()

class Player():
	def __init__(self,name):

		self.name = name
		self.hand = []

class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play