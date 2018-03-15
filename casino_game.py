class Deck:
	def __init__(self):
		
		self.cards = []

		self.populate()

	def populate(self):

		symbol = ["Spade","Diamond","Heart","Club"]
		number = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]

		for i in symbol:
			for j in number:
				self.cards.append([i,j])

		return self.cards

class Player():
	def __init__(self,name):

		self.name = name
		self.hand = []

class Table():
	def __init__(self):

		self.in_game = []
		self.build = []
	