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

	@staticmethod
	def added_value(group):
		added_value = 0
		for card in group:
			added_value += Card.rank_value(card,1)
		return added_value
			

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

class Player(PlayerPack):
	
	def __init__(self,name="",is_pc = False):

		self.name = name
		self.hand = []
		self.points = 0
		self.is_pc = is_pc
		#Point restrictions for winning
		self.eighteen_rest = False
		self.nineteen_rest = False
		self.twenty_rest = False
		PlayerPack.__init__(self)

	def trail(self,table):
		permission = True
		for group in table.build:
			if self == group["Owner"]:
				print("Cannot use trail function if you have a build. Use either capture or make another build.")
				permission = False
				break
		
		for card1 in table.in_game:
			for card2 in self.hand:
				if Card.rank_value(card1,1) == Card.rank_value(card2,1):
					print("Cannot use trail function if a card in table is same value as a card in hand.")
					permission = False
					break
		


		while permission:

			if not self.is_pc:
				print("You have entered the trail function. If at any time you want to get out, enter 'q'.\n")

			selection = 0

			if not self.is_pc:
				if len(self.hand)==1:
					print("You can only choose one card.")
					selection = 1
				else:
					print(Card.show_hand(self.hand))
					selection = input("Enter (1-%d) the card you want leave on the table: " % len(self.hand))
					print("")

			else:
				selection = 1

			if selection != 1:
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
				if card_value == Card.added_value(group):
					possible_cap.append([group,card])

		#For build capture.
		for card in self.hand:
			card_value = Card.rank_value(card,14)
			for group in table.build:
				if card_value == Card.added_value(group["Build"]):
					build_cap.append([group["Build"],card])

		if not self.is_pc:
			i = 1
			for obj in possible_cap:
				print("Number %d: " % i, Card.show_hand(obj[0]),"with " + Card.card_name(obj[1]))
				i += 1
			for obj in build_cap:
				print("Number %d: " % i, Card.show_hand(obj[0]),"with " + Card.card_name(obj[1]) + ". BUILD")
				i += 1

		possible_cap.extend(build_cap)
		while True:
			
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
					self.pack.append(i)
					if i in table.in_game:
						table.in_game.remove(i)
						continue
					for group in table.build:
						if i in group["Build"]:
							table.build.remove(group)

				self.pack.append(cap_obj[1])
				self.hand.remove(cap_obj[1])

				if not table.in_game and not table.build:
					print("%s has sweeped the table!" % self.name)
					self.sweep += 1
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
				if e not in group:
					if Card.added_value(group) == Card.rank_value(e,14):
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

		#The combination method returns an object that contains the possible combinations. 
		#The object is iterable. It contains a list of tuples of those combinations.
		result = []
		for e in all_comb:
			for value in e:
				result.append(list(value))

		result2 = []
		for group in result:
			for card in self.hand:
				group.append(card)
				result2.append(tuple(group)) #Make what I add to result2 unique and unalterable, so when 
				group.remove(card)           #I remove it, the result2 is not affected.

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


class Table():
	def __init__(self):

		self.in_game = []
		self.build = [] #Shows builds for cards in play

	def start_game(self,deck):
		#Draw initial cards for game start. 
		for i in range(0,4):
			self.in_game.append(deck.draw_card())



#################################################################################################################
########################################### Game Logic ##########################################################
#################################################################################################################



print("Get ready to play CASINOOOOOO! Make sure you have read and understood \n\
the rules of the game.\n\n")

# human = Player(input("Enter your name here: "))


player = Player("Human",True)
cpu1 = Player("cpu1",True)
cpu2 = Player("cpu2",True)
cpu3 = Player("cpu3",True)

# print("Hi, %s! Let's get things moving!" % human.name)

people = [player,cpu1,cpu2,cpu3]
table1 = Table()

def play_casino(player,cpu1,cpu2,cpu3,people):
	
	
	deck1 = Deck()
	table1.start_game(deck1)

	team1 = (player,cpu2)
	team2 = (cpu1,cpu3)
	teams = (team1,team2)

	gameplay = {1: "Build", 2: "Capture", 3: "Trail"}

	for team in teams:
		total_score = 0
		team_names = []
		for unit in team:
			total_score += unit.points
			team_names.append(unit.name)
		if total_score > 20:
			print("%s is the winning team. Congratulations!!" % team_names)
			return
		elif total_score == 18:
			for unit in team:
				unit.eighteen_rest = True
				if team.index(unit) == 0: #Only print this once per team
					print("Team %s gets a restriction for having 18 points." % team_names)
		elif total_score == 19:
			for unit in team:
				unit.nineteen_rest = True
				if team.index(unit) == 0:
					print("Team %s gets a restriction for having 19 points." % team_names)
		elif total_score == 20:
			for unit in team:
				unit.twenty_rest = True
				if team.index(unit) == 0:
					print("Team %s gets a restriction for having 20 points." % team_names)

	log = []
	while deck1.cards or player.hand or cpu1.hand or cpu2.hand or cpu3.hand:

		if not people[0].hand:
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
						log.append(gameplay[slct])
						break

			else:
				not_played = len(person.hand)

				person.capture(table1)

				if len(person.hand) < not_played:
					print("%s played capture.\n" % person.name)
					log.append("Capture")
					continue

				person.build2(table1)				

				if len(person.hand) < not_played:
					print("%s played build.\n" % person.name)
					log.append("Build")
					continue

				person.trail(table1)
				print("%s played trail.\n" % person.name)
				log.append("Trail")



	print("\nTHIS ROUND IS OVER\n")

	i = -1
	while True:
		if log[i] == "Capture":
			people[i%4].pack.extend(table1.in_game)
			table1.in_game = []
			print("%s was the last to capture, so gets all cards left in table.\n" % people[i%4].name)
			break
		else:
			i -= 1

	#Point reckoning

	spades_qty_comp = []
	sweep_comp = []
	pack_qty_comp = []

	for person in people:
		if not person.eighteen_rest and not person.twenty_rest:
			person.get_score()

			if person.has_two_spades:
				if not person.nineteen_rest:
					person.points += 1
					print("%s has the two of spades. He gets 1 point.\n" % person.name)
			if person.has_ten_diamonds:
				person.points += 2
				print("%s has the ten of diamonds. He gets 2 points.\n" % person.name)
			if person.aces:
				if not person.nineteen_rest:
					person.points += person.aces
					print("%s gets %d points for his aces.\n" %(person.name,person.aces))

		spades_qty_comp.append(person.spades)
		sweep_comp.append(person.sweep)
		pack_qty_comp.append(person.card_qty)

	#Get points for sweeps. Player with min. sweeps reduces the other player sweeps.
	sweeps_redux = min(sweep_comp)

	print("SWEEPS")
	if sweeps_redux >0:
		print("Everyone's sweeps get reduced by %d, the least amount from the players." % sweeps_redux)

	i = 0
	while i<len(sweep_comp):
		sweep_comp[i] -= sweeps_redux
		i += 1

	
	pos = 0
	for e in sweep_comp:
		print("%s has %d sweeps." % (people[pos].name, e))
		#If there's any restriction, no points are added.
		if not people[pos].eighteen_rest and not people[pos].nineteen_rest and not people[pos].twenty_rest:
			people[pos].points += e
		pos += 1
	print()


	#Compare player's card quantities
	most_cards = max(pack_qty_comp)

	if pack_qty_comp.count(most_cards)>1:
		print("There's a tie for most cards. No one gets points.\n")
	else:
		most_cards_holder = people[pack_qty_comp.index(most_cards)]
		#If nineteen or twenty point restriction is on, no points. Eighteen point restriction
		#calls for this condition to be met.
		if not most_cards_holder.nineteen_rest and not most_cards_holder.twenty_rest:
			print("%s has the most cards. He gets 3 points.\n" % most_cards_holder.name)
			most_cards_holder.points += 3
		else:
			print("The player with most cards has a restriction for points. No points added.")

	#Compare player's spade quantities.
	most_spades = max(spades_qty_comp)

	if spades_qty_comp.count(most_spades)>1:
		print("There's a tie for most spades. No one gets points.\n")
	else:
		most_spades_holder = people[spades_qty_comp.index(most_spades)]
		#If eighteen or nineteen restriction is on, no points. Twenty restriction
		#calls for this condition to be met. 
		if not most_spades_holder.eighteen_rest and not most_spades_holder.nineteen_rest:
			print("%s has the most spades. He gets 1 point.\n" % most_spades_holder.name)
			most_spades_holder.points += 1
		else:
			print("Player with most spades has a restriction for points. No points added.")


	#Point display
	print("----------SCOREBOARD----------")
	for team in teams:
		total_score = 0
		team_names = []
		for person in team:
			total_score += person.points
			team_names.append(person.name)
			person.pack = []
			person.card_qty = 0
			person.sweep = 0
			person.aces = 0
			person.spades = 0
			person.has_ten_diamonds = False
			person.has_two_spades = False

		print("%s has %d points." % (team_names,total_score))

	print("----------------------------------------------\n")

	#The firsts shall be the lasts
	first = people[0]
	people.remove(first)
	people.append(first)

	play_casino(player,cpu1,cpu2,cpu3,people)



play_casino(player,cpu1,cpu2,cpu3,people)