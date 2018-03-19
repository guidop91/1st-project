from random import shuffle

class Deck:
	def __init__(self):
		
		self.cards = []

		self.populate()
		shuffle(self.cards) #Shuffles cards



	@staticmethod
	def card_values(card):
		royalty = {"Jack":11,"Queen":12,"King":13}
		if isinstance(card,int):
			return card
		if card == "Ace":
			control = False
			while not control:
				value = int(input("Would you like to have the Ace to be a 1 or a 14? "))

				if value != 14 and value !=1:
					print("Must enter either 1 or 14")
				else:
					control = True
			return value
		else:
			return royalty[card]



	def populate(self):
		#Creates deck of cards
		symbol = ["Spade","Diamond","Heart","Club"]
		number = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]

		for i in symbol:
			for j in number:
				self.cards.append(tuple([i,j]))

	def draw_card(self):
		return self.cards.pop()

	def deal_player(self,player):
		for i in range(0,4):
			player.hand.append(self.draw_card())

class Player():
	has_build = False
	def __init__(self,name=""):

		self.name = name
		self.hand = []
		self.points = 0
		self.pack = []

	def build(self,table):
		


class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())