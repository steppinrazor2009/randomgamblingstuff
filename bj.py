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

	def __init__(self, bet=1):
		self.cards = []
		self.values = []
		self.valid_moves = []
		self.bet = bet
		self.splitaces = False
		self.doubleup = False
		self.surrender = False

	def clear(self):
		self.cards = []
		self.values = []
		self.valid_moves = []
		self.bet = 0

	def update_split(self):
		self.__update_values()
		
	def add_card(self, card):
		"""
		Update properties when card is added
		:param card: type Card
		"""
		self.cards.append(card)
		self.__update_values()
		self.__update_valid_moves()

	def __update_valid_moves(self):
		"""
		Update self.valid_moves to set of possible moves
		"""

		moves = ['Stay']

		# case for 21
		for value in self.values:
			if value > 21:
				self.valid_moves = 'Bust'
				return
			if value == 21:
				if len(self.cards) == 2:
					self.valid_moves = 'Blackjack'
					return
				self.valid_moves = '21'
				return
		moves.append('Hit')

		if len(self.cards) <= 2:
			moves.append('Double')

		if len(self.cards) == 2:
			if self.cards[0].rank == self.cards[1].rank:
				moves.append('Split')

		self.valid_moves = moves

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

		self.values = v

	def __str__(self):
		ret = str([str(card) for card in self.cards])
		if self.valid_moves == 'Bust':
			return ret + '\n\tBUSTED'
		else:
			if len(self.values) == 2:
				is_player_soft = True
				player_value = self.values[1]
			else:
				player_value = self.values[0]
			return ret + '\n\t' + str(player_value)

class Player():
	def __init__(self):
		self.chips = BANKROLL
		self.basebet = BET
		self.overallmultiplier = 1
		self.multiplier = 1
		self.double = False

	def __str__(self):
		return 'Player has ' + str(self.chips) + ' bankroll'

	def place_bet(self):
		self.chips -= self.basebet * self.multiplier
		return self.basebet * self.multiplier

class Game():
	"""
	Implement a blackjack game
	"""

	def __init__(self, num_decks=8):
		# positions is list of players and their hands
		self.positions = []
		self.num_decks = num_decks
		self.player = Player()
		self.hands = []
		self.dealer = Hand()
		self.cardstack = CardStack(num_decks)
		self.chips = 0
		self.rounds = 0
		self.decks = num_decks
		self.betamts = 0

	def play(self, roundstoplay, bankroll, bet):
		"""
		Play a game of blackjack
		"""
		br = bankroll
		hands = 0
		wagered = 0
		while self.rounds < roundstoplay:
			self.deal_cards()
			if(self.dealer.valid_moves != 'Blackjack'):
				self.new_player_turn(self.dealer.cards[0])
			
			self.dealer_turn()
			self.print_status()
			result = self.new_determine_wins(bet)
			br += result
			if VERBOSE: print("Result: " + str(result))
			if VERBOSE: print("Bankroll: " + str(br))

			for h in self.hands:
				wagered += bet
				if h.doubleup:
					wagered += bet
				hands += 1

			self.clear_hands()
			self.rounds += 1
			if SLOWPLAY:
				input("Press a key to continue...")

		return [hands, wagered, br]
			
	def playsl(self):
		"""
		Play a game of blackjack
		"""
		stoploss = (BANKROLL / 2)
		breakpoint = (BANKROLL / 2)
		while self.player.chips > stoploss:
			if self.player.chips >= (stoploss + (breakpoint * 2)):
				stoploss = stoploss  + breakpoint
				
			#if self.cardstack.truecount >= 0:
			#    self.player.multiplier = self.cardstack.truecount + 1
			#    if VERBOSE: print("MULTIPLIER NOW AT " + str(self.player.multiplier))
			#self.player.multiplier = 1

			self.player.multiplier = 2

			if (self.player.multiplier * self.player.basebet) > 100:
				self.player.multiplier = (100 / self.player.basebet)

			overallmultiplier = math.floor(self.player.chips / BANKROLL)
			if overallmultiplier < 1:
				overallmultiplier = 1
			self.player.overallmultiplier = overallmultiplier

			if VERBOSE: print("\nBetting: " + str(self.player.basebet * self.player.overallmultiplier * self.player.multiplier))
			
			self.deal_cards()
			if(self.dealer.valid_moves != 'Blackjack'):
				self.player_turn(self.dealer.cards[0])
			
			self.dealer_turn()
			self.print_status()
			self.determine_wins()
				
			if VERBOSE: print("Bankroll: " + str(self.player.chips))
			if VERBOSE: print("Stop/Loss: " + str(stoploss))
			if VERBOSE: print("TRUE COUNT: ", str(self.cardstack.truecount))

			self.clear_hands()
			self.rounds += 1
			if SLOWPLAY:
				input("Press a key to continue...")

	def determine_wins(self):
		ret = 0
		double = 1
		if self.player.double:
			double = 2
		self.betamts = self.betamts + self.player.basebet * self.player.multiplier * double
		if len(self.dealer.values) == 2:
			dealer_value = max(self.dealer.values[0], self.dealer.values[1])
		else:
			dealer_value = self.dealer.values[0]
		for h in self.hands:
			if len(h.values) == 2:
				player_value = max(h.values[0], h.values[1])
			else:
				player_value = h.values[0]
				
			if self.dealer.valid_moves == 'Blackjack':
				if h.valid_moves == 'Blackjack':
					if VERBOSE: print("Push")
				else:
					if VERBOSE: print("Dealer Wins")
					self.player.chips -= self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
			else:
				if h.valid_moves == 'Blackjack':
						if VERBOSE: print("Player Wins")
						self.player.chips += self.player.basebet * self.player.multiplier * 1.5 * double * self.player.overallmultiplier
				else:
					if self.dealer.valid_moves == 'Bust':
						if h.valid_moves == 'Bust':
							if VERBOSE: print("Dealer Wins")
							self.player.chips -= self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
						else:
							if VERBOSE: print("Player Wins")
							self.player.chips += self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
					else:
						if h.valid_moves == 'Bust':
							if VERBOSE: print("Dealer Wins")
							self.player.chips -= self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
						else:
							if dealer_value == player_value:
								if VERBOSE: print("Push")
							elif dealer_value > player_value:
								if VERBOSE: print("Dealer Wins")
								self.player.chips -= self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
							else:
								if VERBOSE: print("Player Wins")
								self.player.chips += self.player.basebet * self.player.multiplier * double * self.player.overallmultiplier
					
	def new_determine_wins(self, bet):
		ret = 0

		if len(self.dealer.values) == 2:
			dealer_value = max(self.dealer.values[0], self.dealer.values[1])
		else:
			dealer_value = self.dealer.values[0]


		for h in self.hands:
			betamt = bet
			if h.doubleup:
				betamt = bet * 2
			if len(h.values) == 2:
				player_value = max(h.values[0], h.values[1])
			else:
				player_value = h.values[0]
				
			if h.surrender:
				ret -= (bet / 2)

			if dealer_value


			elif self.dealer.valid_moves == 'Blackjack':
				if h.valid_moves == 'Blackjack':
					if VERBOSE: print("Push")
					ret += 0
				else:
					if VERBOSE: print("Dealer Wins")
					ret -= bet
			else:
				if h.valid_moves == 'Blackjack':
						if VERBOSE: print("Player Wins")
						ret += bet * 1.5
				else:
					if self.dealer.valid_moves == 'Bust':
						if h.valid_moves == 'Bust':
							if VERBOSE: print("Dealer Wins")
							ret -= betamt
						else:
							if VERBOSE: print("Player Wins")
							ret += betamt
					else:
						if h.valid_moves == 'Bust':
							if VERBOSE: print("Dealer Wins")
							ret -= betamt
						else:
							if dealer_value == player_value:
								if VERBOSE: print("Push")
								ret += 0
							elif dealer_value > player_value:
								if VERBOSE: print("Dealer Wins")
								ret -= betamt
							else:
								if VERBOSE: print("Player Wins")
								ret += betamt

		return ret

	def double_up(self):
		self.player.double = True
		if VERBOSE: print("DOUBLING UP!")

	def clear_hands(self):
		self.hands = []
		self.dealer.clear()

	def add_player_card(self, h):
		card = self.cardstack.draw()
		h.add_card(card)        

	def split(self, handtosplit, card1, card2):
		newhand = Hand()
		newhand.add_card(handtosplit.cards[1])
		newhand.add_card(card2)
		handtosplit.cards[1] = card1
		handtosplit.update_split()
		self.hands.append(newhand)

	def new_player_turn(self, dealerup):
		checkcount = 0
		dosplit = False
		while checkcount < len(self.hands):
			#PAIR
			if self.hands[checkcount].cards[0].rank == self.hands[checkcount].cards[1].rank:
				#2 - 3 row
				if(2 <= self.hands[checkcount].cards[0].value <= 3):
					if(dealerup.value <= 8):
						#split here
						dosplit = True
				#4 row
				if(self.hands[checkcount].cards[0].value == 4):
					if(5 <= dealerup.value <= 6):
						#split here
						dosplit = True
				#6 row
				if(self.hands[checkcount].cards[0].value == 6):
					if(dealerup.value <= 6):
						#split here
						dosplit = True
				#7 row
				if(self.hands[checkcount].cards[0].value == 7):
					if(dealerup.value <= 7):
						#split here
						dosplit = True
				#9 row
				if(self.hands[checkcount].cards[0].value == 9):
					if(not(dealerup.value == 7 or dealerup.value == 10 or dealerup.value == 1)):
						#split here
						dosplit = True
				#8 and ace row
				if(self.hands[checkcount].cards[0].value == 8):
					#split here
					dosplit = True
				#8 and ace row
				if(self.hands[checkcount].cards[0].value == 1):
					#split here
					self.hands[checkcount].splitaces = True
					dosplit = True
			if dosplit:
				if VERBOSE: print("SPLITTING:\t" + str(self.hands[checkcount].cards[0]) + "\t" + str(self.hands[checkcount].cards[1]))
				self.split(self.hands[checkcount], self.cardstack.draw(), self.cardstack.draw())
				dosplit = False
			checkcount += 1

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

	def player_turn(self, dealerup):

		for x in range(2):
			for h in self.hands:
				#PAIR
				if h.cards[0].rank == h.cards[1].rank:
					#2 - 3 row
					if(2 <= h.cards[0].value <= 3):
						if(dealerup.value <= 8):
							#split here
							self.split(h, self.cardstack.draw(), self.cardstack.draw())
					#4 row
					if(h.cards[0].value == 4):
						if(5 <= dealerup.value <= 6):
							#split here
							self.split(h, self.cardstack.draw(), self.cardstack.draw())
					#6 row
					if(h.cards[0].value == 6):
						if(dealerup.value <= 6):
							#split here
							self.split(h, self.cardstack.draw(), self.cardstack.draw())
					#7 row
					if(h.cards[0].value == 7):
						if(dealerup.value <= 7):
							#split here
							self.split(h, self.cardstack.draw(), self.cardstack.draw())
					#9 row
					if(h.cards[0].value == 9):
						if(not(dealerup.value == 7 or dealerup.value == 10 or dealerup.value == 1)):
							#split here
							self.split(h, self.cardstack.draw(), self.cardstack.draw())                        
					#8 and ace row
					if(h.cards[0].value == 8 or h.cards[0].value == 1):
						#split here
						self.split(h, self.cardstack.draw(), self.cardstack.draw())

		for h in self.hands:
			while True:
				is_player_soft = False
				if len(h.values) == 2:
					is_player_soft = True
					player_value = h.values[1]
				else:
					player_value = h.values[0]
				
				if(is_player_soft):
				#soft numbers
				#12 row
					if(player_value == 12):
						if(5 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)       
				#13-14 rows
					if(13 <= player_value <= 14):
						if(5 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)                
				#15-16 rows
					if(15 <= player_value <= 16):
						if(4 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)                
				#17 row
					if(player_value == 17):
						if(3 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)                
				#18 row
					if(player_value == 18):
						if(3 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						elif( dealerup.value == 2 or dealerup.value == 7 or dealerup.value == 8):
							#stand
							break
						else:
							#just hit
							self.add_player_card(h)                           
				#19+ row
					if(player_value >= 19):
						#stand
						break


				else:
				#hard number
				#4-8 rows
					if(4 <= player_value <= 8):
						self.add_player_card(h)
				#9 row
					if(player_value == 9):
						if(3 <= dealerup.value <= 6):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)
				#10 row
					if(player_value == 10):
						if(2 <= dealerup.value <= 9):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)
				#11 row
					if(player_value == 11):
						if(2 <= dealerup.value <= 10):
							#double here
							self.double_up()
							self.add_player_card(h)
							break
						else:
							#just hit
							self.add_player_card(h)                        
				#12 row
					if(player_value == 12):
						if(4 <= dealerup.value <= 6):
							#stand
							break
						else:
							#just hit
							self.add_player_card(h)
				#13-16 row
					if(13 <= player_value <= 16):
						if(dealerup.value <= 6):
							#stand
							break
						else:
							#just hit
							self.add_player_card(h)
				#17+ row
					if(player_value >= 12):
						#stand
						break
		
	def dealer_turn(self):
		while True:
			is_dealer_soft = False
			if len(self.dealer.values) == 2:
				is_dealer_soft = True
				dealer_value = self.dealer.values[1]
			else:
				dealer_value = self.dealer.values[0]

			# stay if more than 17 or hard 17
			if dealer_value > 17 or (dealer_value == 17 and is_dealer_soft is False):
				break

			# hits on soft 17
			else:
				card = self.cardstack.draw()
				self.dealer.add_card(card)

	def deal_cards(self):
		"""
		Deal initial cards following casino order
		"""
		self.player.double = False
		if self.cardstack.reshuffle:
			self.cardstack.shuffle(self.decks)
			self.cardstack.reshuffle = False
		self.hands.append(Hand())
		for i in range(2):
			self.hands[0].add_card(self.cardstack.draw())
			self.dealer.add_card(self.cardstack.draw())

	def print_status(self):
		"""
		Print player hands, then print dealer hand
		"""
		if VERBOSE:

			print( 'Player : ')
			for h in self.hands:
				print('\t' + str(h))
			print( 'Dealer:\n\t' + str(self.dealer))
			print( '-----------------------')

VERBOSE = False
SLOWPLAY = False
BANKROLL = 1000
BET = 25
GAMES = 1
totalbr = 0
low = BANKROLL
winbr = 0
wins = 0
lossbr = 0
losses = 0
high = 0
bust = 0
totalhands = 0
totalbets = 0
finalbr = 0

'''
for x in range(GAMES):
	g = Game(8)
	g.playsl()
	totalbr += g.player.chips
	totalhands += g.rounds
	totalbets += g.betamts
	finalbr += g.player.chips
	if g.player.chips < low:
		low = g.player.chips
	if g.player.chips > high:
		high = g.player.chips
	if g.player.chips <= 0:
		bust += 1
	if g.player.chips >= BANKROLL:
		winbr += g.player.chips
		wins += 1
	if g.player.chips < BANKROLL:
		lossbr += g.player.chips
		losses += 1
print("AVG HANDS:\t" + format(totalhands / GAMES, ".2f"))
print("AVG BET:\t" + format(totalbets / totalhands, ".2f"))
avgbet = totalbets / totalhands
avghands = totalhands / GAMES
print("ADT:\t\t" + format(avgbet * avghands * .02, ".2f"), " ( 2 % )")
print("ACTUAL:\t\t" + format((BANKROLL - (totalbr / GAMES)), ".2f"), " (", format(((BANKROLL - (totalbr / GAMES))/(avgbet * avghands))*100, ".2f"), "% )")
print("WINS:\t\t" + str(wins))
print("LOSSES:\t\t" + str(losses))
print("LOW:\t\t" + format(low, ".2f"))
print("HIGH:\t\t" + format(high, ".2f"))
try:
	print("WINAVG:\t\t" + format((winbr / wins) - BANKROLL, ".2f"))
	print("LOSSAVG:\t" + format(BANKROLL - (lossbr / losses), ".2f"))
except:
	pass
print("BUST:\t\t" + str(bust))
print("RoR:\t\t" + format((bust/GAMES)*100, ".2f") + "%")

finalbr = finalbr - (GAMES * BANKROLL)
print("Outcome after " + str(GAMES) + " games: " + str(finalbr))
'''

g = Game(2)
val = g.play(1000, 1000, 10)
betreturn = val[2] - 1000
betwagered = val[1]
ret = betreturn / betwagered
printvals = ["Result:\t" + str(betreturn), "HE:\t" + str(ret)]
print(val[0])
print(val[1])
print("{0[0]:<35}{0[1]:<35}".format(printvals))