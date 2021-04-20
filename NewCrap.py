import random, sys, argparse, math, collections
from enum import Enum
from copy import deepcopy

r = random.Random()
r.seed()
points = [4,5,6,8,9,10]
fieldnumbers = [2,3,4,9,10,11,12]

def FindOpenCome(bets):
	comebets = []
	for bet in bets:
		if isinstance(bet, ComeBet):
			if bet.Active and bet.Number:
				comebets.append(bet.Number)
	for bet in bets:
		if isinstance(bet, ComeOddsBet):
			if bet.Active:
				if bet.Number in comebets:
					comebets.remove(bet.Number)
	return comebets

def FindComeAmt(num, bets):
	for bet in bets:
		if isinstance(bet, ComeBet):
			if bet.Number == num:
				return bet.BetAmount
	return 0

def AddLists(l1, l2):
	retval = []
	if len(l1) == len(l2):
		for x in range(0, len(l1)):
			retval.append(l1[x]+l2[x])
	return retval

def OddsPayout(num):
	if(num == 4 or num == 10):
		return 2
	if(num == 5 or num == 9):
		return 1.5
	if(num == 6 or num == 8):
		return 1.2

def PlacePayout(num):
	if(num == 4 or num == 10):
		return 2
	if(num == 5 or num == 9):
		return 7.0 / 5
	if(num == 6 or num == 8):
		return 7.0 / 6

def FieldPayout(num):
	if(num in fieldnumbers):
		if num == 12:
			return 3
		elif num == 2:
			return 2
		else:
			return 1
	return 0   

def HardwayPayout(num):
	if(num == 4 or num == 10):
		return 8
	if(num == 6 or num == 8):
		return 10		

def OddsAmount(num, bet, multiple):
	if multiple != 0:
		return multiple * bet
	if(num == 4 or num == 10):
		return 3 * bet
	if(num == 5 or num == 9):
		return 4 * bet
	if(num == 6 or num == 8):
		return 5 * bet

def CallRoll(ro):

	if ro.po == PossibleOutcome.SEVENWINNER:
		print("Seven Winner!")
	elif ro.po == PossibleOutcome.SEVENOUT:
		print("Seven out!")
	elif ro.po == PossibleOutcome.CRAPSLOSER:
		print("Craps, line away.")
	elif ro.po == PossibleOutcome.POINTWINNER:
		print("Winner front line!")
	elif ro.po == PossibleOutcome.POINTSET:
		print("Point is now: " + str(ro.roll) + ".")
	elif ro.po == PossibleOutcome.ELEVENWINNER:
		print("Yo-leven! Winner!")
	elif ro.po == PossibleOutcome.OTHER:
		#print("Roll is: " + str(ro.roll) + ".")
		pass

def GetOpposite(num):
	if num == 6:
		return 8
	if num == 8:
		return 6
	if num == 5:
		return 9
	if num == 9:
		return 5
	if num == 4:
		return 10
	if num == 10:
		return 4

class Die:
	def __init__(self):
		self.Value = 0
	def Roll(self):
		self.Value = r.randint(1,6)
		return self.Value

class PossibleOutcome(Enum):
	SEVENWINNER = 1
	SEVENOUT = 2
	CRAPSLOSER = 3
	POINTWINNER = 4
	POINTSET = 5
	ELEVENWINNER = 6
	OTHER = 7

class GameState(Enum):
	ON = 1
	OFF = 2
	 
class RollOutcome:
	def __init__(self, po, roll, hard):
		self.po = po
		self.roll = roll
		self.hard = hard

class Game:
	def __init__(self):
		self.Dice = [Die(), Die()]
		self.Point = 0
		self.State = GameState.OFF
		self.RollValue = 0


	def DoRoll(self):
		d1 = self.Dice[0].Roll()
		d2 = self.Dice[1].Roll()
		return d1 + d2	   

	def Roll(self):
		self.RollValue = self.DoRoll()
		#while self.RollValue != 8:
		#	self.RollValue = self.DoRoll()

		hard = (self.Dice[0].Value == self.Dice[1].Value)
		if verbose and hard: print("HARD") 
		if verbose: print("Roll: " + str(self.RollValue) + "\n========")
	
		#comeout roll
		if(self.State == GameState.OFF):
			#point number
			if self.RollValue in points:
				self.Point = self.RollValue
				self.State = GameState.ON
				return RollOutcome(PossibleOutcome.POINTSET, self.RollValue, hard)
			#seven winner
			elif self.RollValue == 7:
				return RollOutcome(PossibleOutcome.SEVENWINNER, self.RollValue, hard)
			#eleven winner
			elif self.RollValue == 11:
				return RollOutcome(PossibleOutcome.ELEVENWINNER, self.RollValue, hard)				
			#craps
			else:
				return RollOutcome(PossibleOutcome.CRAPSLOSER, self.RollValue, hard)
		#not comeout roll - seven out
		elif self.RollValue == 7:
			self.Point = 0
			self.State = GameState.OFF
			return RollOutcome(PossibleOutcome.SEVENOUT, self.RollValue, hard)
		#made point
		elif self.RollValue == self.Point:
			self.Point = 0
			self.State = GameState.OFF
			return RollOutcome(PossibleOutcome.POINTWINNER, self.RollValue, hard)
		#some other number
		else:
			return RollOutcome(PossibleOutcome.OTHER, self.RollValue, hard)

class GenericBet():
	def __init__(self, bet, number=0):
		self.BetAmount = bet
		self.OriginalAmount = bet
		self.Number = number
		self.Active = False
		self.On = False
		self.Wins = 0
		self.BetsMade = 0
		self.BetsLost = 0
		self.BetsWon = 0
		self.BetReturn = 0
		self.BetWagered = 0

	def Deactivate(self):
		self.Active = False
		self.BetAmount = 0
		self.Number = 0		
		self.On = False

	def SetUp(self, amt=-1, num=0):
		self.BetsMade += 1
		self.Active = True
		#odds bet
		if amt != -1:
			self.BetAmount = amt
		else:
			self.BetAmount = self.OriginalAmount
		self.Number = num
		self.BetReturn += self.BetAmount * -1
		self.BetWagered += self.BetAmount
		if verbose: print("SETUP FOR: " + str(self.BetAmount))
		return self.BetAmount * -1
		
	def SetUpHot(self, mult, num=0):
		self.BetsMade += 1
		self.Active = True
		if mult < 5: mult = 5
		self.BetAmount = self.OriginalAmount * mult
		self.Number = num
		self.BetReturn += self.BetAmount * -1
		self.BetWagered += self.BetAmount
		return self.BetAmount * -1

	def Resolve(self, ro):
		return 0

class FieldBet(GenericBet):
	def Resolve(self, ro):
		if self.Active:
			self.Active = False
			if ro.roll in fieldnumbers:
				self.BetsWon += 1
				self.BetReturn += self.BetAmount + (self.BetAmount * FieldPayout(ro.roll))
				return self.BetAmount * FieldPayout(ro.roll)
			else:
				self.BetAmount = self.OriginalAmount
				self.BetsLost += 1
				self.Wins = 0
		return 0

class PassBet(GenericBet):
	def Resolve(self, ro):
		if self.Active:
			if(ro.po == PossibleOutcome.POINTWINNER):
				self.Active = False
				self.BetsWon += 1
				self.BetReturn +=  self.BetAmount * 2
				return self.BetAmount * 2
			elif(ro.po == PossibleOutcome.SEVENWINNER):
				self.Active = False
				self.BetsWon += 1
				self.BetReturn +=  self.BetAmount * 2
				return self.BetAmount * 2
			elif(ro.po == PossibleOutcome.ELEVENWINNER):
				self.Active = False
				self.BetsWon += 1
				self.BetReturn +=  self.BetAmount * 2
				return self.BetAmount * 2
			elif(ro.po == PossibleOutcome.SEVENOUT):
				self.Active = False
				self.hot = False
				self.BetsLost += 1
				self.BetAmount = self.OriginalAmount
			elif(ro.po == PossibleOutcome.CRAPSLOSER):
				self.Active = False
				self.BetsLost += 1
			elif ro.po == PossibleOutcome.POINTSET:
					self.Number = ro.roll
		return 0

	def BetType(self):
		return "Pass"

	def __str__(self):
		if self.Active:
			return "Pass Bet on " + str(self.Number) + ": " + str(self.BetAmount)
		else:
			return "Pass Bet Off"

class ComeBet(GenericBet):
	def Resolve(self, ro):
		if self.Active:
			if(self.On):
				if(ro.roll == 7):
					self.Active = False
					self.On = False
					if verbose: print("COME BET ON " + str(self.Number) + " LOSES")
					self.BetsLost += 1
					self.Number = 0
					self.BetAmount = self.OriginalAmount
				if(ro.roll == self.Number and self.On):
					self.Active = False
					self.On = False
					if verbose: print("COME BET ON " + str(self.Number) + " WON " + str(self.BetAmount * 2))
					self.BetsWon += 1
					self.Number = 0
					self.BetReturn +=  self.BetAmount * 2
					return self.BetAmount * 2
			else:
				if(ro.roll == 7 or ro.roll == 11):
					if verbose: print("COME BET WON " + str(self.BetAmount * 2) + " FROM 7/11")
					self.BetsWon += 1
					self.Active = False
					self.On = False
					self.Number = 0
					retval = self.BetAmount * 2
					self.BetReturn +=  self.BetAmount * 2
					self.BetAmount = self.OriginalAmount
					return retval
				elif(ro.roll == 2 or ro.roll == 3 or ro.roll == 12):
					self.Active = False
					self.Number = 0
					self.BetsLost += 1
					if verbose: print("COME BET LOST FROM CRAP ROLL")
				elif ro.roll in points:
					self.Number = ro.roll
					self.On = True
		return 0

	def BetType(self):
		return "Come"

	def __str__(self):
		if self.Active:
			return "Come Bet on " + str(self.Number) + ": " + str(self.BetAmount)
		else:
			return "Come Bet Off"

class OddsBet(GenericBet):
	def Resolve(self, ro):
		payout = 0
		if self.Active:
			#print(self.Number)
			if(ro.roll == self.Number):
				self.BetsWon += 1
				payout = (self.BetAmount * OddsPayout(ro.roll)) + self.BetAmount
				self.BetReturn += payout
				self.Deactivate()
			elif(ro.roll == 7): 
				self.BetsLost += 1
				self.Deactivate()
		return payout

	def BetType(self):
		return "Odds"

	def __str__(self):
		if self.Active:
			return "Odds Bet on " + str(self.Number) + ": " + str(self.BetAmount)
		else:
			return "Odds Bet Off"		

class ComeOddsBet(GenericBet):
	def Resolve(self, ro):
		payout = 0
		if self.Active:
			if(ro.roll == self.Number):
				if ro.po == PossibleOutcome.POINTSET:
					if verbose: print("COME ODDS ON " + str(self.Number) + " RETURN " + str(self.BetAmount))
					payout = self.BetAmount
					self.BetWagered -= self.BetAmount
				else:
					payout = (self.BetAmount * OddsPayout(ro.roll)) + self.BetAmount
					if verbose: print("COME ODDS ON " + str(ro.roll) + " WINS " + str(payout))
					self.BetsWon += 1
				self.Deactivate()
			elif(ro.roll == 7):
				if ro.po == PossibleOutcome.SEVENWINNER:
					if verbose: print("COME ODDS ON " + str(self.Number) + " RETURN " + str(self.BetAmount))
					payout = self.BetAmount
					self.BetWagered -= self.BetAmount
				else:
					if verbose: print("COME ODDS ON " + str(self.Number) + " LOSES")
					self.BetsLost += 1
					payout = 0
				self.Deactivate()
		self.BetReturn += payout
		return payout

	def BetType(self):
		return "Come Odds"

	def __str__(self):
		if self.Active:
			return "Come Odds Bet on " + str(self.Number) + ": " + str(self.BetAmount)
		else:
			return "Come Odds Bet Off"	

class PlaceBet(GenericBet):
	def Resolve(self, ro):
		retval = 0
		if self.Active:
			if ro.roll == 7:
				self.BetsLost += 1
				self.BetAmount = self.OriginalAmount
				self.Active = False
				self.Wins = 0
				if verbose: print("PLACE " + str(self.Number) + " LOSES")
			elif ro.roll == self.Number:
				self.Wins += 1
				self.BetsWon += 1
				retval = (self.BetAmount * PlacePayout(ro.roll)) + self.BetAmount
				self.Active = False
				self.BetReturn += retval
				if verbose: print("PLACE " + str(self.Number) + " WINS: " + str(retval) + "\t(Total " + str(self.Wins) + " wins)")
			elif ro.po == PossibleOutcome.POINTWINNER:
				self.Active = False
				self.Wins = 0
				self.BetReturn += self.BetAmount
				retval = self.BetAmount
				if verbose: print("TAKING DOWN PLACE" + str(self.Number))
				self.BetWagered -= self.BetAmount
		return retval

	def BetType(self):
		return "Place " + str(self.Number)

	def __str__(self):
		if self.Active:
			return "Place Bet on " + str(self.Number) + ": " + str(self.BetAmount)
		else:
			return "Place Bet on " + str(self.Number) + " off"

class HardwayBet(GenericBet):
	def Resolve(self, ro):
		retval = 0
		if self.Active:
			if ro.roll == self.Number:
				if ro.hard:
					self.Wins += 1
					if verbose: print("\tHARD " + str(self.Number) + " WINS: " + str(self.BetAmount * HardwayPayout(ro.roll)) + "\t(Total " + str(self.Wins) + " wins)")
					retval = self.BetAmount * HardwayPayout(ro.roll)
					self.BetsWon += 1	
					self.BetReturn += retval
					self.Active = False
					#print("RESOLVE: " + str(self.BetReturn))
				elif not ro.hard:
					self.Active = False
					self.Wins = 0
					if verbose: print("\tHARD " + str(self.Number) + " LOSES")		
					self.BetsLost += 1			
					#print("RESOLVE: " + str(self.BetReturn))
			elif ro.roll == 7:
				self.Active = False
				self.BetsLost += 1
				self.Wins = 0
				if verbose: print("\tHARD " + str(self.Number) + " LOSES")
				#print("RESOLVE: " + str(self.BetReturn))

		return retval

def simpPlay(incbets):
	maxrolls = 100000000
	rolls = 0
	currentbr = 500
	g = Game()
	keepgoing = False

	while (rolls < maxrolls) or keepgoing:
		keepgoing = False
		comesetup = False
		for bet in incbets:
			#if theres a pass bet
			if isinstance(bet, PassBet):
				if(g.State == GameState.OFF):
					currentbr += bet.SetUp()
					passamt = bet.BetAmount
			#if theres an odds bet
			if isinstance(bet, OddsBet):
				if not bet.Active and g.State == GameState.ON:
					currentbr += bet.SetUp(OddsAmount(ro.roll, passamt, bet.OriginalAmount), ro.roll)
			#comebet
			if isinstance(bet, ComeBet):
				if(g.State == GameState.ON and not bet.Active and not comesetup):
					currentbr += bet.SetUp()
					comeamt = bet.BetAmount					
					comesetup = True
			#come odds bet
			if isinstance(bet, ComeOddsBet):
				if not bet.Active:
					opencomes = FindOpenCome(incbets)
					if opencomes:
						currentbr += bet.SetUp(OddsAmount(opencomes[0], comeamt, bet.OriginalAmount), opencomes[0])
			#place bet
			if isinstance(bet, PlaceBet):
				if g.State == GameState.ON and not bet.Active:
					if(g.Point != bet.Number):
						currentbr += bet.SetUp(-1, bet.Number)



			if verbose:
				print(bet)

		#roll
		ro = g.Roll()
		rolls += 1

		#payoff bets
		for bet in incbets:
			if bet.Active:
				currentbr += bet.Resolve(ro)		
			if bet.Active:
				keepgoing = True

	#print("BR:\t" + str(currentbr))
	return [currentbr, incbets]

def PlayGame(incbets, startbr, hwfreq, fbfreq, placepress, maxrolls):
	currentbr = startbr
	g = Game()

	bets = incbets
	playout = False
	rolls = 0
	rollssince7out = 0
	hotshooter = False
	bethard = False
	betfield = False
	passamt = 0
	comesetup = False
	sevenouts = 0
	handlength = 0
	slinc = startbr / 2
	stoploss = 0
	while((currentbr > stoploss) and ((rolls < maxrolls) or playout)):
		
		if currentbr > (startbr * 1.5):
			if stoploss == 0:
				stoploss = startbr
			else:
				if currentbr > (stoploss + slinc):
					stoploss += slinc

		if verbose:
			if(g.State == GameState.ON):
				print("POINT IS : " + str(g.Point))

		if rollssince7out > 20 or currentbr > startbr * 4:
			hotshooter = True

		bethard = False
		betfield = False
		bethard = (r.randint(1,hwfreq) == 1)
		betfield = (r.randint(1,fbfreq) == 1)
		
		comesetup = False

		#set up bets
		if(rolls < maxrolls):
			for bet in bets:
				#if theres a pass bet
				if isinstance(bet, PassBet):
					if(g.State == GameState.OFF):
						if hotshooter:
							currentbr += bet.SetUpHot(currentbr // startbr)
						else:
							currentbr += bet.SetUp()
						passamt = bet.BetAmount
				#playin the field
				elif isinstance(bet, FieldBet):
					if betfield:
						if hotshooter:
							currentbr += bet.SetUpHot(currentbr // startbr)
						else:
							currentbr += bet.SetUp()
						if verbose: print("\tFIELD BET SET UP FOR " + str(bet.BetAmount))
				#HARDWAYS BOYS!!!!
				elif isinstance(bet, HardwayBet):
					if bethard or (bet.Wins > 0):
						if not bet.Active:
							#press HW
							if bet.Wins > 0:
								betamt = bet.BetAmount * 2
								if betamt > 500: betamt = 500
								currentbr += bet.SetUp(betamt, bet.Number)
								if verbose: print("\t\tPressing HARD" + str(bet.Number) + " to " + str(bet.BetAmount))
							else:
								currentbr += bet.SetUp(-1, bet.Number)
								if verbose: print("\tHARD " + str(bet.Number) + " SET UP FOR " + str(bet.BetAmount))

				#comebet
				elif isinstance(bet, ComeBet):
					if(g.State == GameState.ON and not bet.Active and not comesetup):
						if hotshooter:
							currentbr += bet.SetUpHot(currentbr // startbr)
						else:
							currentbr += bet.SetUp()
						comeamt = bet.BetAmount					
						comesetup = True
				#PLACE
				elif isinstance(bet, PlaceBet):
					if g.State == GameState.ON:
						if not bet.Active:
							if(g.Point != bet.Number):
								if bet.Wins > placepress:
									betamt = bet.BetAmount * 2
									currentbr += bet.SetUp(betamt, bet.Number)
									if verbose: print("\t\tPressing PLACE" + str(bet.Number) + " to " + str(bet.BetAmount))
								elif hotshooter:
									currentbr += bet.SetUpHot(currentbr // startbr, bet.Number)
								else:
									currentbr += bet.SetUp(-1, bet.Number)
									if verbose: print("\tPLACE" + str(bet.Number) + " SET UP FOR " + str(bet.BetAmount))				
	
		#roll
		ro = g.Roll()
		rolls += 1
		if ro.po == PossibleOutcome.SEVENOUT:
			rollssince7out = 0
			hotshooter = False
			passamt = 0
			sevenouts += 1
		else:
			rollssince7out += 1

		if verbose:
			CallRoll(ro)

		#payoff bets
		for bet in bets:
			if bet.Active:
				currentbr += bet.Resolve(ro)

		#set up odds
		if(rolls < maxrolls):
			for bet in bets:
				#if theres an odds bet
				if isinstance(bet, OddsBet):
					if ro.po == PossibleOutcome.POINTSET and not bet.Active:
						currentbr += bet.SetUp(OddsAmount(ro.roll, passamt, bet.OriginalAmount), ro.roll)
				elif isinstance(bet, ComeOddsBet):
					if not bet.Active:
						opencomes = FindOpenCome(bets)
						if(ro.roll in opencomes):
							comeamt = FindComeAmt(ro.roll, bets)
							currentbr += bet.SetUp(OddsAmount(ro.roll, comeamt, bet.OriginalAmount), ro.roll)

		#print active bet list
		if verbose: print("\tACTIVE BETS\n\t===========")
		playout = False
		for bet in bets:
			if bet.Active:
				playout = True
				if verbose:
					outstr = "\t" + bet.__class__.__name__
					try:
						outstr = outstr + " on " + str(bet.Number)
					except:
						pass
					outstr = outstr + " for " + str(bet.BetAmount)
					print(outstr)

		if verbose: print("BR (AFTER ROLL): " + str(currentbr) + "\n")
	
	#bet totals
	totalbetswon = []
	totalbetslost = []
	totalbetreturn = []
	totalbetwagers = []
	for bet in bets:
		totalbetswon.append(bet.BetsWon)
		totalbetslost.append(bet.BetsLost)
		totalbetreturn.append(bet.BetReturn)
		totalbetwagers.append(bet.BetWagered)

	return [currentbr, rolls, totalbetswon, totalbetslost, sevenouts, totalbetreturn, totalbetwagers]

verbose = False
#thebets = [PassBet(5), OddsBet(0), PlaceBet(12, 8), PlaceBet(12, 6), HardwayBet(5, 8), HardwayBet(5, 6), HardwayBet(5, 4), HardwayBet(5, 10)]
#thebets = [PassBet(5), OddsBet(0)]
#thebets = [PassBet(5), OddsBet(0), ComeBet(5), ComeOddsBet(0), ComeBet(5), ComeOddsBet(0)]
thebets = [PlaceBet(30, 8), PlaceBet(30, 6)]
winners = 0
losers = 0

for i in range(0,0):

	totalbr = 0
	betslost = []
	betswon = []
	betreturn = []
	betwager = []
	hands = 0
	totalrolls = 0
	ruin = 0
	win = 0
	highbr = 0
	double = 0
	sims = 100
	maxrolls = 400
	sbr = 500.0
	
	debug = False
	winners = 0
	losers = 0


	for x in range(0, len(thebets)):
		betslost.append(0.0)
		betswon.append(0.0)
		betreturn.append(0.0)
		betwager.append(0.0)

	for x in range(0,sims):
		tmp = PlayGame(deepcopy(thebets), sbr, 25, 25, 3, maxrolls)
		if tmp[0] <= 0: ruin += 1
		if tmp[0] >= sbr: win += 1
		if tmp[0] >= (sbr * 2): double += 1
		totalbr += tmp[0]
		totalrolls += tmp[1]
		if tmp[0] > highbr:
			highbr = tmp[0]
		betswon = AddLists(tmp[2], betswon)
		betslost = AddLists(tmp[3], betslost)
		betreturn = AddLists(tmp[5], betreturn)
		betwager = AddLists(tmp[6], betwager)
		hands += tmp[4] + 1

	print("AVG BR:\t\t" + format(totalbr / sims, ".2f"))
	print("AVG Rolls:\t" + format(totalrolls / sims, ".2f"))
	print("WIN:\t\t" + str(win) + "\t(" + format(win / sims * 100, ".2f") + "%)")
	print("OVERALL:\t" + format(totalbr - (sims * sbr), ".2f"))
	print("RUIN:\t\t" + str(ruin) + "\t(" + format(ruin / sims * 100, ".2f") + "%)")
	print("DOUBLE:\t\t" + str(double) + "\t(" + format(double / sims * 100, ".2f") + "%)")
	print("HIGH:\t\t" + format(highbr, ".2f"))
	print("ROLLS/HAND:\t" + format((totalrolls / sims)/(hands / sims), ".2f"))
	print("BETS:\n========")
	for x in range(0, len(thebets)):
		outval = "\t" + thebets[x].__class__.__name__
		try:
			if thebets[x].Number != 0: outval += str(thebets[x].Number)
		except:
			pass
		if len(thebets[x].__class__.__name__) < 8:
			outval += "\t"	
		outval += "\t" + format(betswon[x], ".2f") + " / " + format((betswon[x] + betslost[x]), ".2f")
		betamt = thebets[x].BetAmount
		if(betswon[x] + betslost[x]) < 1000: outval += "\t"
		if isinstance(thebets[x], OddsBet) or isinstance(thebets[x], ComeOddsBet):
			if thebets[x].OriginalAmount == 0:
				betamt = "345X"
			else:
				betamt = str(thebets[x].OriginalAmount) + "X"
			outval += "\t" + str(betamt)
		else:
			outval += "\t$" + str(betamt)
		try:
			percentage = ((betswon[x] / (betswon[x] + betslost[x])) * 100)
			outval += "\t(" + format(percentage, ".2f") + "% win rate)"
			#if percentage < 10: outval += "\t"
		except:
			pass

		outval += "\t$" + format(betreturn[x] / (betswon[x] + betslost[x]), ".4f") + " he per bet"
		if (betreturn[x] / (betswon[x] + betslost[x])) >= 0: outval += "\t"
		#outval += "\t\t" + format(betwager[x] , ".4f") + " : " + format(betreturn[x] , ".4f") + " house edge"
		print(outval)


val = simpPlay(thebets)
totalwager=0
for x in val[1]:
	ret = x.BetReturn / x.BetWagered
	totalwager += x.BetWagered
	printvals = [x.BetType() + "(" + str(x.BetsMade) + "):", x.BetReturn, ret]
	print("{0[0]:<35}{0[1]:<25}{0[2]:<25}".format(printvals))
print("RESULT:\t", str(val[0]))


'''
49.29% - pass
40.61% - odds
45.45% - place 6/8


'''