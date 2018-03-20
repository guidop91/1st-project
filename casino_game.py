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
			while True:
				try:
					value = int(input("Would you like to have the Ace to be a 1 or a 14? "))
				except ValueError:
					print("Not a valid number.")
					continue

				if value != 14 and value !=1:
					print("Must enter either 1 or 14")
				else:
					break
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
	
	def __init__(self,name=""):

		self.name = name
		self.hand = []
		self.points = 0
		self.pack = []
		self.has_build = False

	def build(self,table):
		result = []
		#Entire process
		while True:
			#Card to build for
			while True:
				print(self.hand)
				selection = input("Enter (1-%d) the card you want to build for: " % len(self.hand))

				if not selection:
					continue

				selection = int(selection)
				if selection > len(self.hand):
					continue

				card1 = self.hand[selection-1]
				card1m = Deck().card_values(card1[1])
				print("You have selected " , card1)

				result.append(card1)






class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())