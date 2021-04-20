import random, sys, math
verbose = False
bankroll = 500
rolls = 500
r = random.Random()
betamt = 25

class Die:
    def __init__(self):
        self.Value = 0
    def Roll(self):
        global r
        self.Value = r.randint(1,6)
        return self.Value

class Game:
    def __init__(self, br, rolls, betamt):
        if verbose:
            print(f"New Game Starting!\tBankroll: {br}")
            print("***************************************")
        self.Bankroll = br
        self.InitialBankroll = br
        self.StopLoss = 0
        self.Rolls = rolls
        self.BetAmount = betamt
        self.Dice = [Die(), Die()]
        self.Bets = []
        self.Bets.append(HardwayBet(betamt, 4))
        self.Bankroll -= 25
        self.Bets.append(HardwayBet(betamt, 10))
        self.Bankroll -= 25
        self.Bets.append(HardwayBet(betamt, 6))
        self.Bankroll -= 25
        self.Bets.append(HardwayBet(betamt, 8))
        self.Bankroll -= 25
        self.RollNumber = 0
        if verbose: print()
    def Roll(self):
        d1 = self.Dice[0].Roll()
        d2 = self.Dice[1].Roll()
        self.RollValue = d1 + d2
        #if verbose: print(f"\tRoll: {self.RollValue} ({d1}:{d2})")
        return [d1, d2]
    def Play(self):
        for i in range(0, self.Rolls):
            if self.Bankroll > (self.StopLoss + self.InitialBankroll):
                self.StopLoss = self.StopLoss + self.InitialBankroll
            self.RollNumber += 1
            if verbose: print(f"Round: {i + 1}\tBankroll: {self.Bankroll}")
            res = self.Roll()
            winloss = 0
            for bet in self.Bets:
                ret = bet.Resolve(res)
                self.Bankroll += ret
                winloss += ret
                if ret != 0:
                    #if verbose: print(f"\t\t{bet.Name}:\t{ret}")
                    pass
            if verbose: print(f"\tRoll: {self.RollValue} ({res[0]}:{res[1]})\t{winloss}")
            if winloss > 0:
                for bet in self.Bets:
                    bet.Increase(self.BetAmount)
                    self.Bankroll -= self.BetAmount
            elif winloss < 0:
                if self.Bankroll < self.StopLoss:
                    if verbose: print(f"STOP!!")
                    break
            if verbose: print(f"New Bankroll: {self.Bankroll}")
            if verbose: print()
        if verbose: print(f"Game Over - Bankroll: {self.Bankroll}")
        return [self.Bankroll, self.RollNumber]
        
class HardwayBet:
    def __init__(self, amt, num):
        self.Amount = amt
        self.InitialAmount = amt
        self.Number = num
        self.Name = "Hard" + str(num)
        if verbose: print(f"Bet Added: {self.Name} for ${self.Amount}")
    def Resolve(self, roll):
        if roll[0] + roll[1] == 7:
            self.Amount = self.InitialAmount
            return self.InitialAmount * -1
        elif roll[0] + roll[1] == self.Number:
            if roll[0] == roll[1]:
                if self.Number in [4, 10]:
                    return self.Amount * 7
                elif self.Number in [6, 8]:
                    return self.Amount * 9
            else:
                self.Amount = self.InitialAmount
                return self.InitialAmount * -1
        else:
            return 0
    def Increase(self, amt):
        self.Amount += amt
        if verbose: print(f"\t{self.Name} increased from ${self.Amount - amt} to ${self.Amount}")

wins = 0
winbr = 0
losses = 0
lossbr = 0
for i in range(1, 50001):
    game = Game(bankroll, rolls, betamt)
    res = game.Play()
    if res[0] < 0:
        losses += 1
        lossbr = lossbr - bankroll
    elif res[0] > bankroll:
        winbr += res[0]
        wins += 1
    if res[0] > 7000:
        print(f"BIG WIN: Game #{i}:\t{res[0]}\t({res[1]} rolls)")
print(f"Wins: {wins}")
print(f"\tWon:\t{winbr}")
print(f"Losses: {losses}")
print(f"\tLost:\t{lossbr}")
