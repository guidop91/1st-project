from random import shuffle
import itertools

class Card:
	SUIT = ["Spades","Diamonds","Hearts","Clubs"]
	RANK = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]

	def __init__(self,suit,rank):
		self.suit = suit
		self.rank = rank

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
		self.is_pc = is_pc

	def trail(self,table):
		permission = True
		for group in table.build:
			if self == group["Owner"]:
				print("Cannot use trail function if you have a build. Use either capture or make another build.")
				permission = False
		
		
		while permission:

			if not self.is_pc:
				print("You have entered the trail function. If at any time you want to get out, enter 'q'.\n")

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
					break
				else:
					continue

			else:

				table.in_game.append(trail_card)
				self.hand.remove(trail_card)
				break

	def capture(self,table):
		if not self.is_pc:
			print("You have entered the capture function. If at any time you want to get out, enter 'q'.\n")
		tab_combs = self.all_comb2(table)
		possible_cap = []
		build_cap = []

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

		#For build capture.
		for card in self.hand:
			card_value = Card.rank_value(card,14)
			for group in table.build:
				added_value = 0
				for unit in group["Build"]:
					added_value += Card.rank_value(unit,1)
				if card_value == added_value:
					build_cap.append([group["Build"],card])

		if not self.is_pc:
			i = 1
			for obj in possible_cap:
				print("Number %d: " % i, Card.show_hand(obj[0]),"with " + Card.card_name(obj[1]))
				i += 1
			for obj in build_cap:
				print("Number %d: " % i, Card.show_hand(obj[0]),"with " + Card.card_name(obj[1]) + ". BUILD")
				i += 1

		while True:
			possible_cap.extend(build_cap)
			if not possible_cap:
				if not self.is_pc:
					print("There are no possible captures.")
				break
			elif len(possible_cap) == 1:
				if not self.is_pc:	
					print("Only 1 possible capture.")
				selection = 1
			else:
				if not self.is_pc:
					selection = input("Select (1-%d) the capture you want to make: " % len(possible_cap))
				
					if selection.lower() == 'q':
						break
					if not selection:
						continue

				else:
					selection = len(possible_cap)

			try:
				selection = int(selection)
			except ValueError:
				continue

			if selection > len(possible_cap) or selection <= 0:
				print("Number must be between 1 and %d." % len(possible_cap))
				continue

			cap_obj = possible_cap[selection-1]

			if not self.is_pc:
				print("You have selected: ")
				print(Card.show_hand(cap_obj[0]),"with " + Card.card_name(cap_obj[1]))

			if not self.is_pc:
				confirm = input("Enter 'y' to confirm selection: ")
			else:
				confirm = 'y'

			if confirm.lower() == 'y':
				for i in cap_obj[0]:
					self.pack.pack.append(i)
					if i in table.in_game:
						table.in_game.remove(i)
						continue
					for group in table.build:
						if i in group["Build"]:
							table.build.remove(group)

				self.pack.pack.append(cap_obj[1])
				self.hand.remove(cap_obj[1])

				if not table.in_game and not table.build:
					print("%s has sweeped the table!" % self.name)
					self.pack.sweep += 1
			else:
				continue

			if not self.is_pc:
				print("Capture successfully made!")

			break

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

			#Make the build a dictionary, so we know who built it.

			res_dict = {}
			res_dict["Build"] = result
			res_dict["Owner"] = self

			table.build.append(res_dict)
			if not self.is_pc:
				print("Build successfully made!")
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


class PlayerPack():
	def __init__(self):
		self.pack = []
		self.card_qty = 0
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
			if Card.card_name(card) == "10 of Diamonds":
				self.has_ten_diamonds = True
				break

	def own_two_spades(self):
		for card in self.pack:
			if Card.card_name(card) == "2 of Spades":
				self.has_two_spades = True
				break

	def get_score(self):
		self.aces_qty()
		self.spades_qty()
		self.own_ten_diamonds()
		self.own_two_spades()
		self.card_qty = len(self.pack)


class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())


############## Game Logic #######################

# print("Get ready to play CASINOOOOOO! Make sure you have read and understood \n\
# the rules of the game.")

# human = Player(input("Enter your name here: "))

# print("Hi, %s! Let's get things moving!" % human.name)

def play_casino(player=None,cpu1=None,cpu2=None,cpu3=None):
	
	if not player:
		print("Starting up!")
		player = Player("Human1",True)
		cpu1 = Player("cpu1",True)
		cpu2 = Player("cpu2",True)
		cpu3 = Player("cpu3",True)
		table1 = Table()
		deck1 = Deck()
		table1.start_game(deck1)

	people = (player,cpu1,cpu2,cpu3)

	gameplay = {1: "Build", 2: "Capture", 3: "Trail"}

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

	while deck1.cards or player.hand or cpu1.hand or cpu2.hand or cpu3.hand:

		if not player.hand:
			for person in people:
				deck1.deal_player(person)

		for person in people:
			print("TABLE: ",Card.show_hand(table1.in_game))
			for group in table1.build:
				print("BUILD: ",Card.show_hand(group["Build"]))
			if not person.is_pc:
				print("Your hand: ", Card.show_hand(person.hand))
				for k,v in gameplay.items():
					print("%s: %s" % (k,v))
				while True:
					not_played = len(person.hand)
					slct = input("How would you like to play? ")

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

			else:
				not_played = len(person.hand)

				person.capture(table1)

				if len(person.hand) < not_played:
					print("%s played capture." % person.name)
					continue

				person.build2(table1)				

				if len(person.hand) < not_played:
					print("%s played build." % person.name)
					continue

				person.trail(table1)
				print("%s played trail." % person.name)


	spades_qty_comp = []
	sweep_comp = []
	pack_qty_comp = []

	for person in people:

		person.pack.get_score()

		if person.pack.has_two_spades:
			person.points += 1
		if person.pack.has_ten_diamonds:
			person.points += 2

		if person.pack.aces:
			person.points += person.pack.aces

		spades_qty_comp.append(person.pack.spades)
		sweep_comp.append(person.pack.sweep)
		pack_qty_comp.append(person.pack.card_qty)

	#Get points for sweeps. Player with min. sweeps reduces the other player sweeps.
	sweeps_redux = min(sweep_comp)

	i = 0
	while i<len(sweep_comp):
		sweep_comp[i] -= sweeps_redux
		i += 1

	for e in sweep_comp:
		pos = 0
		people[pos].points += e
		pos += 1



	#Compare player's card quantities
	print(pack_qty_comp)
	most_cards = max(pack_qty_comp)
	print(most_cards)

	if pack_qty_comp.count(most_cards)>1:
		print("There's a tie for most cards. No one gets points.")
	else:
		most_cards_holder = people[pack_qty_comp.index(most_cards)]
		print("%s has the most cards. He gets 3 points." % most_cards_holder.name)
		most_cards_holder.points += 3

	#Compare player's spade quantities.
	print(spades_qty_comp)
	most_spades = max(spades_qty_comp)
	print(most_spades)

	if spades_qty_comp.count(most_spades)>1:
		print("There's a tie for most spades. No one gets points.")
	else:
		most_spades_holder = people[spades_qty_comp.index(most_spades)]
		print("%s has the most spades. He gets 1 point." % most_spades_holder.name)
		most_spades_holder.points += 1

	for person in people:
		print("%s has %d points." % (person.name,person.points))






play_casino()