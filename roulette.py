import random, math

COLORS = ["Black", "Red", "Green"]
TYPES = ["Odd", "Even", "Zero"]
COLUMNS = [[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34], [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35], [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]]

class Wheel():
	def __init__(self):
		self.values = [[0, '0', 'Green', 'Zero'], [28, '28', 'Black', 'Even'], [9, '9', 'Red', 'Odd'], [26, '26', 'Black', 'Even'], [30, '30', 'Red', 'Even'], [11, '11', 'Black', 'Odd'],
					[7, '7', 'Red', 'Odd'], [20, '20', 'Black', 'Even'], [32, '32', 'Red', 'Even'], [17, '17', 'Black', 'Odd'], [5, '5', 'Red', 'Odd'], [22, '22', 'Black', 'Even'],
					[34, '34', 'Red', 'Even'], [15, '15', 'Black', 'Odd'], [3, '3', 'Red', 'Odd'], [24, '24', 'Black', 'Even'], [36, '36', 'Red', 'Even'], [13, '13', 'Black', 'Odd'],
					[1, '1', 'Red', 'Odd'], [-1, '00', 'Green', 'Zero'], [27, '27', 'Red', 'Odd'], [10, '10', 'Black', 'Even'], [25, '25', 'Red', 'Odd'], [29, '29', 'Black', 'Odd'],
					[12, '12', 'Red', 'Even'], [8, '8', 'Black', 'Even'], [19, '19', 'Red', 'Odd'], [31, '31', 'Black', 'Odd'], [18, '18', 'Red', 'Even'], [6, '6', 'Black', 'Even'],
					[21, '21', 'Red', 'Odd'], [33, '33', 'Black', 'Odd'], [16, '16', 'Red', 'Even'], [4, '4', 'Black', 'Even'], [23, '23', 'Red', 'Odd'], [35, '35', 'Black', 'Odd'],
					[14, '14', 'Red', 'Even'], [2, '2', 'Black', 'Even']]

	def spin_wheel(self):
		return random.choice(self.values)

class GenericBet():
	def __init__(self):
		self.BetsMade = 0
		self.BetsLost = 0
		self.BetsWon = 0
		self.BetReturn = 0
		self.BetWagered = 0

class NumberBet(GenericBet):
	def __init__(self, amount, number):
		self.bet_amount = amount
		self.number = number
		GenericBet.__init__(self)	

	def payout_bet(self, spin_result):
		if spin_result[0] == self.number:
			return self.bet_amount * 35
		else:
			return self.bet_amount * -1

	def __str__(self):
		return "$" + str(self.bet_amount) + " Straight up on " + str(self.number)

class OddOrEvenBet(GenericBet):
	def __init__(self, amount, oetype):
		self.bet_amount = amount
		self.oetype = oetype	
		GenericBet.__init__(self)	

	def payout_bet(self, spin_result):
		if spin_result[3] == self.oetype:
			return self.bet_amount
		else:
			return self.bet_amount * -1
	
	def __str__(self):
		return "$" + str(self.bet_amount) + " on " + str(self.oetype)

class BlackOrRedBet(GenericBet):
	def __init__(self, amount, color):
		self.bet_amount = amount
		self.color = color	
		GenericBet.__init__(self)	

	def payout_bet(self, spin_result):
		if spin_result[2] == self.color:
			return self.bet_amount
		else:
			return self.bet_amount * -1
	
	def __str__(self):
		return "$" + str(self.bet_amount) + " on " + str(self.color)

class ColumnBet(GenericBet):
	def __init__(self, amount, column):
		self.bet_amount = amount
		self.column = column	
		GenericBet.__init__(self)	

	def payout_bet(self, spin_result):
		if spin_result[0] in COLUMNS[self.column - 1]:
			return self.bet_amount * 2
		else:
			return self.bet_amount * -1
	
	def __str__(self):
		return "$" + str(self.bet_amount) + " on Column " + str(self.column)

class DozenBet(GenericBet):
	def __init__(self, amount, dozen):
		self.bet_amount = amount
		self.dozen = dozen	
		GenericBet.__init__(self)	

	def payout_bet(self, spin_result):
		if spin_result[0] in range(((self.dozen - 1) * 12) + 1, (self.dozen * 12) + 1):
			return self.bet_amount * 2
		else:
			return self.bet_amount * -1
	
	def __str__(self):
		return "$" + str(self.bet_amount) + " on Dozen " + str(self.dozen)

class Game():
	def __init__(self):
		self.wheel = Wheel()

	def play(self, rounds):
		br = 1000
		for x in range(rounds):
			spin_result = self.wheel.spin_wheel()
			for bet in BETS:
				payout = bet.payout_bet(spin_result)
				bet.BetsMade += 1
				bet.BetWagered += bet.bet_amount
				bet.BetReturn += payout
				if payout > 0:
					bet.BetsWon += 1
				else:
					bet.BetsLost += 1

				br += payout
		return br

#BETS = [NumberBet(10, -1), OddOrEvenBet(10, "Odd"), BlackOrRedBet(10, "Black"), ColumnBet(10, 1), DozenBet(10, 1)]
BETS = [NumberBet(25, 5), NumberBet(25, 15), NumberBet(25, 20), NumberBet(25, 27)]
g = Game()
result = g.play(2)
print("BR:\t" + str(result))
for bet in BETS:
	ret = bet.BetReturn / bet.BetWagered
	pctwin = bet.BetsWon / bet.BetsMade
	printvals = ["\t" + str(bet) + ":", pctwin, ret]
	print("{0[0]:<35}{0[1]:>15}{0[2]:>20}".format(printvals))
