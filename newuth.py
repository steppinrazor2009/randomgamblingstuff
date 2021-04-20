import random, math, itertools


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

	ranks = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('Jack', 11), ('Queen', 12), ('King', 13),('Ace', 14)]
	suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

	def __init__(self):
		self.cards = []
		for r in self.ranks:
			for s in self.suits:
				c = Card()
				c.value = r[1]
				c.rank = r[0]
				c.suit = s
				self.cards.append(c)
		random.shuffle(self.cards)

	def __str__(self):
		ret = ""
		for c in self.cards:
			ret = ret + "\n" + str(c)
		return ret
	
	def get_hand(self):
		ret = Hand()
		for x in range(2):
			ret.add_card(self.cards.pop())
		return ret
			
	def get_card(self):
		return self.cards.pop()

	def refresh(self):
		self.cards = []
		for r in self.ranks:
			for s in self.suits:
				c = Card()
				c.rank = r[0]
				c.value = r[1]
				c.suit = s
				self.cards.append(c)
		random.shuffle(self.cards)

class Hand():
	def __init__(self, c=None):
		if c is None:
			c = []
		self.cards = c
		
	def __str__(self):
		ret = ""
		for c in self.cards:
			if ret != "":
				ret = ret + "\n" 
			ret = ret + str(c)
		return ret

	def add_card(self, card):
		self.cards.append(card)

	def clear(self):
		self.cards = []

	def sorted_hand(self):
		ret = Hand()
		tmp = sorted(self.cards)
		for card in tmp:
			ret.add_card(card)
		return ret

	def __add__(self, another_hand):
		newset = self.cards[:]
		for other_card in another_hand.cards:
			newset.append(other_card)
		return Hand(newset)        

HAND_STRINGS = ["High card", "Pair", "Two pair", "Three of a kind", "Straight", "Flush", "Full House", "Four of a kind", "Straight flush", "Royal flush"]

PAYOUTS = [0,5,10,15,20,30,45,125,250,4000]

BET_CHANCE = [1,2,3]

SUITS = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

class Game():
	def __init__(self):
		self.deck = Deck()
		self.player = Hand()
		self.dealer = Hand()
		self.board = Hand()

	def deal_hand(self):
		self.player = self.deck.get_hand()
		self.dealer = self.deck.get_hand()

	def deal_flop(self):
		for x in range(3):
			self.board.add_card(self.deck.get_card())

	def deal_turn(self):
		for x in range(2):
			self.board.add_card(self.deck.get_card())

	def __str__(self):
		ret = "PLAYER\n------\n"
		ret += str(self.player)
		ret += "\n\nDEALER\n------\n"
		ret += str(self.dealer)
		if len(self.board.cards) > 0:
			ret += "\n\nCARDS\n-----\n"
			ret += str(self.board)
		return ret      

	def play_hand(self, base_bet, trips_bet):
		self.__init__()
		
		g.deal_hand()
		g.deal_flop()
		g.deal_turn()
		
		playerbesthand = Hand(best_hand((g.player + g.board).cards))
		handvalue = evaluate_hand(playerbesthand.cards)
		ret = trips_Payout(handvalue, trips_bet)
		return ret

	def play(self, hands):
		br = 0
		wins = 0
		for x in range(hands):
			ret = self.play_hand(1, 1)
			if ret > 0:
				wins += 1
			br += ret
		return [br, wins]

def trips_Payout(handvalue, bet):
	if handvalue == 3:
		ret = bet * 3
	elif handvalue == 4:
		ret = bet * 4
	elif handvalue == 5:
		ret = bet * 7
	elif handvalue == 6:
		ret = bet * 8
	elif handvalue == 7:
		ret = bet * 30
	elif handvalue == 8:
		ret = bet * 40
	elif handvalue == 9:
		ret = bet * 50
	else:
		ret = bet * -1
	return ret

def best_hand(hand):
    def hand_score(cards):
        type_score = [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
        ].index(evaluate_hand(cards))
        return (type_score, sum(card.value for card in cards))

    if len(set(hand)) != len(hand):
        #raise ValueError('Duplicate card in hand')
        pass
    return max(itertools.combinations(hand, 5), key=hand_score)

def evaluate_hand(cards):
	ranks = [card.value for card in cards]
	suits = [card.suit for card in cards]
	if is_consecutive(ranks):
		if not all_equal(suits):
			return 4
		elif max(ranks) < 14:
			return 8
		else:
			return 9

	if all_equal(suits):
		return 5

	x = sum(ranks.count(r) for r in ranks)
	vals = {4 + 4 + 4 + 4 + 1: 7, 3 + 3 + 3 + 2 + 2: 6,	3 + 3 + 3 + 1 + 1: 3, 2 + 2 + 2 + 2 + 1: 2,	2 + 2 + 1 + 1 + 1: 1, 1 + 1 + 1 + 1 + 1: 0}
	return vals[x]

def all_equal(lst):
    return len(set(lst)) == 1

def is_consecutive(lst):
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1


g = Game()
games = 10000000
result = g.play(games)
br = result[0]


ret = br / games
pctwin = result[1] / games
printvals = ["\tTrips:", pctwin, ret]
print("{0[0]:<15}{0[1]:>15}{0[2]:>20}".format(printvals))

print(br)