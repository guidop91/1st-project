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
		possible_builds = []
		result = []
		for card1 in self.hand:
			#This is the card we want to make a build for.
			card1m = Deck().card_values(card1[1])
			for card2 in self.hand:
				#This is the potential card for a build to be made with.
				print("Building for ", card1)
				if card1 == card2:
					continue

				#These only hold the value of the card, Jack -> 11, Queen -> 12, etc.
				card2m = Deck().card_values(card2[1])
				result.append(card2)

				for card3 in table.in_game:
					#These are the cards taken from the table to make the build.
					card3m = Deck().card_values(card3[1])
					addition = 0

					for entry in result:
						addition += Deck().card_values(entry[1])

					if addition + card3m == card1m:
						result.append(card3)
						possible_builds.append(result)
						result = []
						break

					if addition + card3m < card1m:
						result.append(card3)

					result = []

		print(possible_builds)




class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())