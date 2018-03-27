from random import shuffle
import itertools

class Card:
	SUIT = ["Spades","Diamonds","Hearts","Clubs"]
	RANK = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]

	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank
		self.for_build = False


	def rank_value(self,acevalue = None):
		ROYALTY = {"Jack":11,"Queen":12,"King":13}
		if isinstance(self.rank,int):
			return self.rank
		if self.rank == "Ace":
			if acevalue:
				value = acevalue
			else:
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
			return ROYALTY[self.rank]

	def card_name(self):
		return str(self.rank) + " of " + self.suit

	@staticmethod
	def show_hand(group):
		representation = []
		for card in group:
			representation.append(Card.card_name(card))
		return representation
			

class Deck:
	def __init__(self):
		
		self.cards = []

		self.populate()
		shuffle(self.cards) #Shuffles cards

	def populate(self):
		#Creates deck of cards
		for i in Card.SUIT:
			for j in Card.RANK:
				self.cards.append(Card(i,j))

	def draw_card(self):
		return self.cards.pop()

	def deal_player(self,player):
		for i in range(0,4):
			player.hand.append(self.draw_card())

class Player():
	
	def __init__(self,name="",is_pc = False):

		self.name = name
		self.hand = []
		self.points = 0
		self.pack = PlayerPack()
		self.has_build = False
		self.is_pc = is_pc

	def build(self,table):
		#Entire process
		while True:
			start_over = False
			central_card = None
			central_cardv = None
			result = []
			resultv = [] #The v suffix stands for value: Only the value of the card is taken.
			quit = False

			print("You have entered the build function. If at any time you want to get out, enter 'q'.\n")
			#Card to build for
			while True:
				print("Your hand: ",Card.show_hand(self.hand))
				print("Cards in table: ", Card.show_hand(table.in_game))
				print("")
				selection = input("Enter (1-%d) the card you want to build for: " % len(self.hand))



				#Safeguards
				if not selection:
					continue
				if selection.lower() == 'q':
					quit = True
					break
				try:
					selection = int(selection)
				except ValueError:
					continue
				if selection <= 0:
					continue
				if selection > len(self.hand):
					continue



				central_card = self.hand[selection-1]
				central_cardv = Card.rank_value(central_card)
				print("You have selected %s and its value is %d" % (Card.card_name(central_card),central_cardv))
				print("")
				break

			#Card to play to construct build.
			while True:
				if quit:
					break

				print("If you want to start over, enter 'x'.")
				print(Card.show_hand(self.hand))
				selection = input("Enter (1-%d) the card you want to build with: " % len(self.hand))



				#Safeguards
				if not selection:
					continue
				if selection.lower() == 'q':
					quit = True
					break
				if selection.lower() == 'x':
					start_over = True
					break
				try:
					selection = int(selection)
				except ValueError:
					continue
				
				if selection > len(self.hand):
					continue
				if selection <= 0:
					continue



				build_card = self.hand[selection-1]
				if build_card == central_card:
					print("Cannot use the same card as the one you are building for.")
					continue

				build_cardv = Card.rank_value(build_card)

				if build_cardv >= central_cardv:
					print ("Cannot use card with same or more value than the one you are building for.")
					continue

				print("You have selected ", Card.card_name(build_card))
				result.append(build_card)
				resultv.append(build_cardv)

				break

			#Choose card from table to build with
			while True:
				if quit:
					break
				if start_over:
					break

				build_sum = 0
				for i in resultv:
					build_sum += i

				while True:
					if build_sum == central_cardv:
						finish = input("You have a valid build! Do you want to choose it? Enter \"y\" for YES, \"x\" to start over, \"q\" to quit. ")

						if not finish:
							continue

						elif finish.lower() == 'y':
							print("Your build is %s for the card %s" % (Card.show_hand(result),Card.card_name(central_card)))
							self.has_build = True
							central_card.for_build = True
							self.hand.remove(result[0])
							for unit in result[1:]:
								table.in_game.remove(unit)
							print("Your hand: ",Card.show_hand(self.hand),"Cards in table: ",Card.show_hand(table.in_game))
							return result, central_card

						elif finish.lower() == 'q':
							quit = True
							break

						elif finish.lower() == 'x':
							start_over = True
							break

						else:
							continue
					
					print("Your build card is: ",  Card.card_name(central_card))
					print(Card.show_hand(table.in_game))
					print("Current build: %s. The added value is: %d" % (Card.show_hand(result),build_sum))
					
					selection = input("Select a card (1-%d) from the table to build with. " % len(table.in_game))
					


					#Safeguards
					if not selection:
						continue
					if selection.lower() == 'q':
						quit = True
						break
					if selection.lower() == 'x':
						start_over = True
						break
					try:
						selection = int(selection)
					except ValueError:
						continue

					if selection > len(table.in_game):
						continue
					if selection <= 0:
						continue




					build_card = table.in_game[selection-1]
					build_cardv = Card.rank_value(build_card)

					if build_card in result:
						print("Cannot use card more than one time.")
						continue

					if build_sum + build_cardv > central_cardv:
						print("This card makes the build surpass the build card.")
						continue

					result.append(build_card)
					resultv.append(build_cardv)
					break

					
				if start_over == True:
					break
				if quit:
					break

			if quit:
				break
			if start_over:
				continue

	def trail(self,table):

		if not self.is_pc:
			print("You have entered the trail function. If at any time you want to get out, enter 'q'.\n")
		while True:
			selection = 0
			if not self.is_pc:
				print(Card.show_hand(self.hand))
				selection = input("Enter (1-%d) the card you want leave on the table: " % len(self.hand))
				print("")

			else:
				selection = 1

			if not self.is_pc:
				if not selection:
					continue
				if selection.lower() == "q":
					break
				
				try:
					selection = int(selection)
				except ValueError:
					continue

				if selection > len(self.hand):
					continue
				if selection <= 0:
					continue

			trail_card = self.hand[selection-1]

			if not self.is_pc:

				print("You have selected %s. " % Card.card_name(trail_card))

				selection2 = input("Are you sure? Enter \"y\" to proceed. ")

				if not selection2:
					continue
				elif selection2.lower() == "q":
					break
				elif selection2.lower() == 'y':
					table.in_game.append(trail_card)
					self.hand.remove(trail_card)

					print(Card.show_hand(self.hand))
					print(Card.show_hand(table.in_game))
					break
				else:
					continue

			else:

				table.in_game.append(trail_card)
				self.hand.remove(trail_card)
				break

	def capture(self,table):
		print("You have entered the capture function. If at any time you want to get out, enter 'q'.\n")
		tab_combs = self.all_comb2(table)
		possible_cap = []

		#Make sure aces are included for single capture
		for card in self.hand:
			card_value = Card.rank_value(card,14)
			for group in tab_combs:
				if len(group)>1:
					continue
				for unit in group:
					if Card.rank_value(unit,14) == card_value:
						possible_cap.append([group,card])

		#Only for captures of more than 1 card.
		for card in self.hand:
			card_value = Card.rank_value(card,14)
			for group in tab_combs:
				if len(group) == 1:
					continue
				added_value = 0
				for unit in group:
					added_value += Card.rank_value(unit,1)
				if card_value == added_value:
					possible_cap.append([group,card])

		i = 1
		for obj in possible_cap:
			print("Number %d: " % i, Card.show_hand(obj[0]),"with " + Card.card_name(obj[1]))
			i += 1

		while True:

			if not possible_cap:
				print("There are no possible captures.")
				break
			elif len(possible_cap) == 1:
				print("Only 1 possible capture.")
				selection = 1
			else:
				selection = input("Select (1-%d) the capture you want to make: " % len(possible_cap))

			if selection.lower() == 'q':
				break

			if not selection:
				continue

			try:
				selection = int(selection)
			except ValueError:
				continue

			if selection > len(possible_cap) or selection <= 0:
				print("Number must be between 1 and %d." % len(possible_cap))
				continue

			cap_obj = possible_cap[selection-1]

			print("You have selected: ")
			print(Card.show_hand(cap_obj[0]),"with " + Card.card_name(cap_obj[1]))

			confirm = input("Enter 'y' to confirm selection: ")

			if confirm.lower() == 'y':
				for i in cap_obj[0]:
					self.pack.pack.append(i)
					table.in_game.remove(i)
				self.pack.pack.append(cap_obj[1])
				self.hand.remove(cap_obj[1])
			else:
				continue

			print("Capture successfully made!")

			break



	def all_comb(self,table):
		"""Gets all the possible combinations for one player card and all the table's cards"""
		all_comb = []
		for L in range(1,len(table.in_game)+1):
			all_comb.append(itertools.combinations(table.in_game,L))

		result = []
		for e in all_comb:
			for value in e:
				result.append(list(value))

		result2 = []
		for group in result:
			for card in self.hand:
				group.append(card)
				result2.append(tuple(group))
				group.remove(card)

		return result2

	def all_comb2(self,table):
		"""Gets all the possible combinations for all the table's cards"""
		all_comb = []
		for L in range(1,len(table.in_game)+1):
			all_comb.append(itertools.combinations(table.in_game,L))

		result = []
		for e in all_comb:
			for value in e:
				result.append(list(value))

		return result

	def build2(self,table):

		if not self.is_pc:
			print("You have entered the build function. If at any time you want to get out, enter 'q'.\n")
		combs = self.all_comb(table)
		possible_combs = []

		for e in self.hand:
			for group in combs:
				build_sum = 0
				if e not in group:
					for unit in group:
						build_sum += Card.rank_value(unit,1)
					if build_sum == Card.rank_value(e,14):
						if group not in possible_combs:
							possible_combs.append([group,e])

		if not self.is_pc:
			no = 1
			for i in possible_combs:
				print("Number %d: " % no, Card.show_hand(i[0]),"with " + Card.card_name(i[1]))
				no += 1

		while True:
			selection = 0
			if not possible_combs:
				if not self.is_pc:
					print("There are no possible builds.")
				break

			if len(possible_combs) == 1:
				if not self.is_pc:
					print("There is only one possible selection.")
				selection = 1

			else:
				if not self.is_pc:
					selection = input("Select (1-%d) the build you want to make: " % len(possible_combs))

					if selection.lower() == 'q':
						break

			if self.is_pc:
				selection = 1

			try:
				selection = int(selection)
			except ValueError:
				continue

			if selection <= 0 or selection > len(possible_combs):
				print("Selection must be between 1 and %d." % len(possible_combs))
				continue

			sel_build = possible_combs[selection-1]

			if not self.is_pc:
				print("You have selected: ")
				print(Card.show_hand(sel_build[0]),"with " + Card.card_name(sel_build[1]))

				confirm = input("Enter 'y' to confirm selection.")

			if self.is_pc:
				confirm = 'y'
			result = []
			if confirm.lower() == 'y':
				for i in sel_build[0]:
					result.append(i)
					if i in table.in_game:
						table.in_game.remove(i)
					if i in self.hand:
						self.hand.remove(i)
			else:
				continue

			table.build.append(result)
			if not self.is_pc:
				print("Build successfully made!")
			sel_build[1].for_build = True
			self.has_build = True
			break


class PlayerPack():
	def __init__(self):
		self.pack = []
		self.card_qty = len(self.pack)
		self.sweep = 0
		self.aces = 0
		self.spades = 0
		self.has_ten_diamonds = False
		self.has_two_spades = False

	def aces_qty(self):
		for card in self.pack:
			if card.rank == "Ace":
				self.aces += 1

	def spades_qty(self):
		for card in self.pack:
			if card.suit == "Spades":
				self.spades += 1

	def own_ten_diamonds(self):
		for card in self.pack:
			if card_name(card) == "10 of Diamonds":
				self.has_ten_diamonds = True
				break

	def own_two_spades(self):
		for card in self.pack:
			if card_name(card) == "2 of Spades":
				self.has_two_spades = True
				break

	def get_score(self):
		self.aces = self.aces_qty()
		self.spades = self.spades_qty()
		self.has_ten_diamonds = self.own_ten_diamonds()
		self.has_two_spades = self.own_two_spades()


class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())


############## Game Logic #######################

print("Get ready to play CASINOOOOOO! Make sure you have read and understood \n\
the rules of the game.")

human = Player(input("Enter your name here: "))

print("Hi, %s! Let's get things moving!" % human.name)

def play_casino(player=None,cpu1=None,cpu2=None,cpu3=None):
	
	if not player:
		print("Starting up!")
		player = human
		cpu1 = Player("cpu1")
		cpu2 = Player("cpu2")
		cpu3 = Player("cpu3")
		table1 = Table()
		deck1 = Deck()
		table1.start_game(deck1)

	people = (player,cpu1,cpu2,cpu3)

	gameplay = {1: "build2(table1)", 2: "capture(table1)", 3: "trail(table1)"}

	winner = []
	for person in people:
		if person.points >= 21:
			winner.append(person)

	if winner:
		if len(winner) == 1:
			print("We have a winner!! Congratulations %s!!" % winner[0].name)
		else:
			print("We have multiple winners!")
			for w in winner:
				print("Congratulations, %s!!" % w.name)

	if not player.hand:
		for person in people:
			deck1.deal_player(person)

	for person in people:
		if person == people[0]:
			for k,v in gameplay.items():
				print("%s: %s" % (k,v))
			while True:
				not_played = len(person.hand)
				slct = input("How would you like to play?")

				try:
					slct = int(slct)
				except ValueError:
					continue

				if slct not in gameplay.keys():
					continue
			
				if slct == 1:
					person.build2(table1)
				elif slct == 2:
					person.capture(table1)
				else:
					person.trail(table1)

				if len(person.hand) == not_played:
					continue
				else:
					break




# play_casino()