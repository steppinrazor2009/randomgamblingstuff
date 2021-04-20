import random, math

BETS = {0 : "Banker", 1 : "Player", 2 : "Tie"}

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

	def __eq__(self, other):
		return (self.value == other.value and self.suit == other.suit)

	def __ne__(self, other):
		return not(self == other)

	def __lt__(self, other):
		return (self.value < other.value)

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

	def shuffle(self, num_decks):
		self.__init__(num_decks)

	def draw(self):
		if len(self.stack) <= 70:
			self.reshuffle = True
		ret = self.stack.pop()
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
	Implement a bacc hand
	"""

	def __init__(self):
		self.cards = []
		
	def __str__(self):
		ret = ""
		for c in self.cards:
			if ret != "":
				ret = ret + "\n" 
			ret = ret + "\t" + str(c)
		ret = ret + "\n\tScore: " + str(self.get_score())
		return ret

	def add_card(self, card):
		self.cards.append(card)

	def get_score(self):
		total = 0
		for card in self.cards:
			total = total + card.value
		return total % 10
		
	def clear(self):
		self.cards = []

class Game():
	def __init__(self, bet):
		self.deck = CardStack(8)
		self.banker = Hand()
		self.player = Hand()
		self.needshuffle = False
		self.bet = bet

	def bank_third(self, p3v):
		bscore = self.banker.get_score()
		if bscore <= 2:
			return True
		if bscore == 3:
			if p3v == 8:
				return False
			else:
				return True
		if bscore == 4:
			if p3v <= 1:
				return False
			elif p3v >= 8:
				return False
			else:
				return True            
		if bscore == 5:
			if p3v <= 3:
				return False
			elif p3v >= 8:
				return False
			else:
				return True            
		if bscore == 6:
			if p3v <= 5:
				return False
			elif p3v >= 8:
				return False
			else:
				return True
		if bscore == 7:
			return False

	def play(self):
		if self.deck.reshuffle:
			self.deck.shuffle(8)

		self.player.clear()
		self.banker.clear()
		self.player.add_card(self.deck.draw())
		self.banker.add_card(self.deck.draw())
		self.player.add_card(self.deck.draw())
		self.banker.add_card(self.deck.draw())

		#natural
		if self.player.get_score() >= 8 or self.banker.get_score() >= 8:
			pass
		#player draws
		elif self.player.get_score() <= 5:
			player3rd = self.deck.draw()
			self.player.add_card(player3rd)
			if self.bank_third(player3rd.value):
				self.banker.add_card(self.deck.draw())
		#player stands
		else:
			#banker draws
			if self.banker.get_score() <= 5:
				self.banker.add_card(self.deck.draw())

		ret = self.bet.payout(self.banker.get_score(), self.player.get_score())
		if VERBOSE:
			print("Banker:\t" + str(self.banker.get_score()))
			print("Player:\t" + str(self.player.get_score()))
			print("Result:\t" + str(ret))
			print()
		return ret

class Bet():
	def __init__(self, bet_on, amt):
		self.amount = amt
		self.bet_on = bet_on

	def payout(self, banker_score, player_score):
		result = compare(banker_score, player_score)
		if self.bet_on == result:
			if self.bet_on == 0:
				return self.amount * 0.95
			elif self.bet_on == 1:
				return self.amount
			else:
				return self.amount * 8
		else:
			if self.bet_on == 2:
				return self.amount * -1
			elif result == 2:
				return 0
			else:
				return self.amount * -1

def compare(banker_score, player_score):
	if player_score == banker_score:
		return 2
	else:
		return player_score > banker_score

VERBOSE = False
g = Game(Bet(1, 5))

rounds = 1000000
wins = 0
br = 0
for x in range(rounds):
	result = g.play()
	br += result
	if result > 0:
		wins += 1
betreturn = br
betwagered = rounds * 5
ret = betreturn / betwagered
printvals = ["Result:\t" + str(betreturn), "HE:\t" + str(ret)]
print(wins)
print("{0[0]:<35}{0[1]:<35}".format(printvals))

