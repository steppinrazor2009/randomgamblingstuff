import random, math

class Card():
	"""
	Implement a basic playing card
	"""
	def __init__(self, value=1, rank="Ace", suit="Spades"):
		"""
		:param value: blackjack value of card
		:param rank: type of card (e.g. King)
		:param suit: {Diamonds, Hearts, Spades, Clubs}
		"""
		self.value = value
		self.rank = rank
		self.suit = suit

	def __str__(self):
		return self.rank + " of " + self.suit

class Deck():
	""" Implement a standard 52-card deck """

	ranks = [('Ace', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('Jack', 10), ('Queen', 10), ('King', 10)]
	suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

	def __init__(self):
		self.cards = []
		for r in self.ranks:
			for s in self.suits:
				c = Card()
				c.rank = r[0]
				c.value = r[1]
				c.suit = s
				self.cards.append(c)

	def __str__(self):
		ret = ""
		for c in self.cards:
			ret = ret + "\n" + str(c)
		return ret

class CardStack():
	"""
	Implement a variable-sized show
	"""

	def __init__(self, num_decks=1):
		"""
		Build stack of decks and shuffle
		:param num_decks: number of decks to use
		"""
		self.reshuffle = False
		self.stack = []
		for i in range(num_decks):
			deck = Deck()
			for card in deck.cards:
				self.stack.append(card)
		random.shuffle(self.stack)
		self.runningcount = 0
		self.decksremaining = num_decks
		self.truecount = 0

	def set_decks_remaining(self):
		self.decksremaining = math.floor(len(self.stack) / 52)

	def do_count(self, val):
		if 1 < val <= 7:
			self.runningcount += 1
		elif val == 1 or val == 10:
			self.runningcount -= 1
		self.set_decks_remaining()
		if self.decksremaining < 1:
			self.decksremaining = 1
		self.truecount = math.floor(self.runningcount / self.decksremaining)

	def shuffle(self, num_decks):
		self.stack = []
		for i in range(num_decks):
			deck = Deck()
			for card in deck.cards:
				self.stack.append(card)
		random.shuffle(self.stack)
		self.runningcount = 0
		self.truecount = 0
		self.decksremaining = num_decks

	def draw(self):
		if len(self.stack) <= 70:
			self.reshuffle = True
		ret = self.stack.pop()
		self.do_count(ret.value)
		return ret

	def __len__(self):
		return len(self.stack)

	def __str__(self):
		ret = ""
		for c in self.stack:
			ret = ret + "\n" + str(c)
		return ret

class Hand():
	"""
	Implement a blackjack hand. Hands keep track of player bets
	"""

	def __init__(self, startingcards=[]):
		self.cards = []
		self.values = []
		self.Splitaces = False
		self.Doubleup = False
		self.Surrender = False
		self.Bust = False
		if startingcards:
			for card in startingcards:
				self.add_card(card)

	def add_card(self, card):
		self.cards.append(card)
		self.__update_values()

	def __update_values(self):
		"""
		Calculate value of hand
		"""
		v = [0]
		has_ace = False

		# two values for hands with aces
		for card in self.cards:
			v[0] += card.value
			if card.rank == 'Ace':
				has_ace = True

		# hand is soft if below 12
		if has_ace:
			if v[0] < 12:
				v.append(v[0] + 10)

		if v[0] > 21:
			self.Bust = True

		self.values = v

	def __str__(self):
		ret = str([str(card) for card in self.cards])
		if self.Bust:
			return ret + '\n\tBUSTED'
		else:
			if len(self.values) == 2:
				is_player_soft = True
				player_value = self.values[1]
			else:
				player_value = self.values[0]
			return ret + '\n\t' + str(player_value)

class Game():
	"""
	Implement a blackjack game
	"""

	def __init__(self, num_decks=8):
		self.num_decks = num_decks
		self.hands = []
		self.dealer = Hand()
		self.cardstack = CardStack(num_decks)
		self.rounds = 0
		self.decks = num_decks

	def play(self, roundstoplay, bankroll, bet):
		"""
		Play a game of blackjack
		"""
		br = bankroll
		hands = 0
		wagered = 0

		while self.rounds < roundstoplay:
			self.deal_cards()

			bj = False
			if (21 in self.hands[0].values) or (21 in self.dealer.values):
				if 21 in self.hands[0].values:
					bj = True
			elif self.should_surrender(self.hands[0], self.dealer.cards[0]):
				self.hands[0].Surrender = True
			else:
				#play it out
				self.determine_splits()

				unbusted = False				
				for hand in self.hands:
					if hand.Splitaces:
						#DO NOTHING, CANT DRAW ON ACE
						pass
					elif self.should_double(hand, self.dealer.cards[0]):
						hand.Doubleup = True
						hand.add_card(self.cardstack.draw()) 
					else:
						while self.should_hit(hand, self.dealer.cards[0]) and not hand.Bust:
							hand.add_card(self.cardstack.draw())
					if not hand.Bust:
						unbusted = True

				if unbusted:
					while self.dealer_should_hit():
						self.dealer.add_card(self.cardstack.draw())

			#check wins
			for hand in self.hands:
				win = self.did_i_win(hand, bet)
				if win > 0 and bj:
					win = win * 1.5
				br += win
				hands += 1
				wagered += bet
				if hand.Doubleup:
					wagered += bet

			if VERBOSE: print(self)

			self.hands = []
			self.dealer = Hand()
			self.rounds += 1

		return [hands, wagered, br]

	def did_i_win(self, hand, bet):
		ret = 0

		dealer_value = get_value(self.dealer)
		player_value = get_value(hand)

		if hand.Surrender:
			if VERBOSE: print("Player Surrenders")
			ret = bet * -.5			
		elif hand.Bust:
			if VERBOSE: print("Dealer Wins")
			ret = bet * -1
		elif self.dealer.Bust:
			if VERBOSE: print("Player Wins")
			ret = bet
		elif player_value > dealer_value:
			if VERBOSE: print("Player Wins")
			ret = bet
		elif dealer_value > player_value:
			if VERBOSE: print("Dealer Wins")
			ret = bet * -1
		else:
			if VERBOSE: print("Push")
			ret = 0

		if hand.Doubleup:
			ret = ret * 2

		return ret

	def should_surrender(self, hand, dealerup):
		if len(hand.values) == 1:
			if get_value(hand) == 16:
				if dealerup.value == 10:
					return True
		return False

	def should_double(self, hand, dealerup):
		doubleup = False
		player_value = get_value(hand)
		#soft
		if len(hand.values) == 2:
			if player_value in [16, 17, 18]:
				if dealerup.value in [2, 3, 4, 5, 6]:
					doubleup = True
		#hard number
		else:
			if player_value == 9:
				if dealerup.value in [2, 3, 4, 5, 6]:
					doubleup = True
			elif player_value in [10, 11]:
				if player_value > dealerup.value:
					doubleup = True
		return doubleup

	def should_hit(self, hand, dealerup):
		hit = False
		player_value = get_value(hand)

		#soft numbers
		if len(hand.values) == 2:
			if player_value in [13, 14, 15, 16, 17]:
				hit = True
		#hard number
		else:
			if player_value in [4, 5, 6, 7, 8, 9, 10, 11]:
				hit = True
			if player_value in [12, 13, 14, 15, 16]:
				if dealerup.value in [7, 8, 9, 10, 1]:
					hit = True

		return hit

	def player_turn(self, hand, dealerup):
			
		bust = False
		stand = False

		if hand.splitaces:
			return hand
		if hand.Doubleup:
			hand.add_card(self.cardstack.draw())
			return hand

			#soft numbers
			if(is_player_soft):
			#12 row
				if(player_value == 12):
					if(5 <= dealerup.value <= 6):
						#double here
						doubleup = True
			#13-14 rows
				if(13 <= player_value <= 14):
					if(5 <= dealerup.value <= 6):
						doubleup = True
			#15-16 rows
				if(15 <= player_value <= 16):
					if(4 <= dealerup.value <= 6):
						doubleup = True
			#17 row
				if(player_value == 17):
					if(3 <= dealerup.value <= 6):
						doubleup = True
			#18 row
				if(player_value == 18 and (3 <= dealerup.value <= 6)):
					doubleup = True
				else:
					stand = True
			#hard number
			else:
			#4-8 rows
				if(4 <= player_value <= 8):
					pass
			#9 row
				if(player_value == 9):
					if(3 <= dealerup.value <= 6):
						#double here
						doubleup = True
			#10 row
				if(player_value == 10):
					if(2 <= dealerup.value <= 9):
						doubleup = True
			#11 row
				if(player_value == 11):
					if(2 <= dealerup.value <= 10):
						doubleup = True
			#12 row
				if(player_value == 12):
					if(4 <= dealerup.value <= 6):
						stand = True
			#13-16 row
				if(13 <= player_value <= 16):
					if(dealerup.value <= 6):
						stand = True
				if player_value == 16 and dealerup.value == 10 and len(h.cards) == 2:
					stand = True
					h.surrender = True
			#17+ row
				if(player_value >= 17):
					stand = True

			if doubleup:
				self.double_up()
				h.doubleup = True
				self.add_player_card(h)
			elif not stand:							
				self.add_player_card(h)

	def new_player_turn(self, dealerup):
			
		for h in self.hands:
			if len(self.hands) > 1:
				if VERBOSE: print("HANDS:\t" + str(len(self.hands)))
			is_player_soft = False
			doubleup = False
			stand = False
			while not h.splitaces and not doubleup and not stand:
				if len(h.values) == 2:
					is_player_soft = True
					player_value = h.values[1]
				else:
					player_value = h.values[0]				
				if VERBOSE: print("PV:\t" + str(player_value) + "\t\tDU:" + str(dealerup.value) + "\t\tSOFT:\t" + str(is_player_soft) + "\t\tSTAND:\t" + str(stand))
				#soft numbers
				if(is_player_soft):
				#12 row
					if(player_value == 12):
						if(5 <= dealerup.value <= 6):
							#double here
							doubleup = True
				#13-14 rows
					if(13 <= player_value <= 14):
						if(5 <= dealerup.value <= 6):
							doubleup = True
				#15-16 rows
					if(15 <= player_value <= 16):
						if(4 <= dealerup.value <= 6):
							doubleup = True
				#17 row
					if(player_value == 17):
						if(3 <= dealerup.value <= 6):
							doubleup = True
				#18 row
					if(player_value == 18 and (3 <= dealerup.value <= 6)):
						doubleup = True
					else:
						stand = True
				#hard number
				else:
				#4-8 rows
					if(4 <= player_value <= 8):
						pass
				#9 row
					if(player_value == 9):
						if(3 <= dealerup.value <= 6):
							#double here
							doubleup = True
				#10 row
					if(player_value == 10):
						if(2 <= dealerup.value <= 9):
							doubleup = True
				#11 row
					if(player_value == 11):
						if(2 <= dealerup.value <= 10):
							doubleup = True
				#12 row
					if(player_value == 12):
						if(4 <= dealerup.value <= 6):
							stand = True
				#13-16 row
					if(13 <= player_value <= 16):
						if(dealerup.value <= 6):
							stand = True
					if player_value == 16 and dealerup.value == 10 and len(h.cards) == 2:
						stand = True
						h.surrender = True
				#17+ row
					if(player_value >= 17):
						stand = True

				if doubleup:
					self.double_up()
					h.doubleup = True
					self.add_player_card(h)
				elif not stand:							
					self.add_player_card(h)

	def dealer_should_hit(self):
		if get_value(self.dealer) < 17:
			return True
		else:
			return False

	def deal_cards(self):
		"""
		Deal initial cards following casino order
		"""
		if self.cardstack.reshuffle:
			self.cardstack.shuffle(self.decks)
			self.cardstack.reshuffle = False
		self.hands = [Hand()]
		for i in range(2):
			self.hands[0].add_card(self.cardstack.draw())
			self.dealer.add_card(self.cardstack.draw())

	def __str__(self):
		ret =  "Player :\n"
		for h in self.hands:
			ret += "\t" + str(h) + "\n"
		ret += "Dealer:\n\t" + str(self.dealer) + "\n"
		ret += "-----------------------\n"
		return ret

	def determine_splits(self):
		checkcount = 0
		dosplit = False
		dealerup = self.dealer.cards[0]
		newhands = self.hands
		while checkcount < len(newhands):
			#PAIR
			if newhands[checkcount].cards[0].rank == newhands[checkcount].cards[1].rank:
				if(newhands[checkcount].cards[0].value in [2, 3, 6, 7, 9]):
					if(2 <= dealerup.value <= 6):
						dosplit = True
				if(newhands[checkcount].cards[0].value in [8, 1]):
					#split here
					dosplit = True
			if dosplit:
				if VERBOSE: print("SPLITTING:\t" + str(newhands[checkcount].cards[0]) + "\t" + str(newhands[checkcount].cards[1]))
				firsthand = Hand([newhands[checkcount].cards[1], self.cardstack.draw()])
				secondhand = Hand([newhands[checkcount].cards[0], self.cardstack.draw()])
				if newhands[checkcount].cards[1].value == 1:
					firsthand.Splitaces = True
					secondhand.Splitaces = True
				newhands.append(firsthand)
				newhands[checkcount] = secondhand
				dosplit = False
			checkcount += 1

		self.hands = newhands

def get_value(hand):
	value = hand.values[0]
	if len(hand.values) == 2 and hand.values[1] <= 21:
		value = hand.values[1]
	return value

VERBOSE = False
SLOWPLAY = False


g = Game(8)
val = g.play(10000000, 1000, 10)

betreturn = val[2] - 1000
betwagered = val[1]
ret = betreturn / betwagered
printvals = ["Result:\t" + str(betreturn), "HE:\t" + str(ret)]
print(val[0])
print(val[1])
print("{0[0]:<35}{0[1]:<35}".format(printvals))
