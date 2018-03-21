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
		central_card = None
		central_cardv = None
		result = []
		resultv = [] #The v suffix stands for value: Only the value of the card is taken.
		#Entire process
		while True:
			#Card to build for
			while True:
				print(self.hand)
				selection = input("Enter (1-%d) the card you want to build for: " % len(self.hand))

				#Safeguards
				if not selection:
					continue
				selection = int(selection)
				if selection > len(self.hand):
					continue

				central_card = self.hand[selection-1]
				central_cardv = Deck().card_values(central_card[1])
				print("You have selected " , central_card)

				break

			#Card to play to construct build.
			while True:
				print(self.hand)
				selection = input("Enter (1-%d) the card you want to build with: " % len(self.hand))

				#Safeguards
				if not selection:
					continue
				selection = int(selection)
				if selection > len(self.hand):
					continue
				build_card = self.hand[selection-1]
				if build_card == central_card:
					print("Cannot use the same card as the one you are building for.")
					continue

				build_cardv = Deck().card_values(build_card[1])
				print("You have selected ", build_card)
				result.append(build_card)
				resultv.append(build_cardv)

				break








class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())