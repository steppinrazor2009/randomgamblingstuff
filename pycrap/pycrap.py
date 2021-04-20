import random, sys, argparse, math

r = random.Random()
points = [4,5,6,8,9,10]
verbose = False

roll_results = ["Front Line Loser", "Front Line Winner","Point Set","Winner","Seven Out","Other"]

def round_down(num):
    return num - (num%5)

def oddspayout(num):
    if(num == 4 or num == 10):
        return 2
    if(num == 5 or num == 9):
        return 1.5
    if(num == 6 or num == 8):
        return 1.2

def placepayout(num):
    if(num == 4 or num == 10):
        return 1.95
    if(num == 5 or num == 9):
        return 1.4
    if(num == 6 or num == 8):
        return (7/6)

def hardwaypayout(num):
    if(num == 4 or num == 10):
        return 7
    if(num == 6 or num == 8):
        return 9


def adjustplace(amt, pt):
    ret = 0
    if(pt == 5 or pt == 9):
        ret = amt * 5
    elif(pt == 6 or pt == 8):
        ret = amt * 6
    else:
        ret = amt * 4
    return ret

def findopposite(num):
    if(num == 4):
        return 10
    elif(num == 5):
        return 9
    elif(num == 6):
        return 8
    elif(num == 8):
        return 6
    elif(num == 9):
        return 5
    elif(num == 10):
        return 4
    else:
        return 0


class Bet:
    def __init__(self, amt):
        self.Type = "Bet"
        self.Amount = amt
        self.Active = False
    def SetUp(self):
        pass
    def Resolve(self):
        pass


class ParlayHardway(Bet):
    def __init__(self, amt, num):
        Bet.__init__(self, amt)
        self.Type = "ParlayHardway"
        self.Point = num
        self.Amount = amt
        self.Active = True
        self.adjamt = self.Amount
        self.Multiplier = 1
        self.wins = 0
    def SetUp(self):
        self.adjamt = self.Amount
        if verbose: print("Hardway bet now on hard " + str(self.Point) + " for " + str(self.adjamt * self.Multiplier))
 
    def Resolve(self, rv, res, hard):
        payout = 0
        if self.adjamt > 100:
            self.adjamt = 100
        #seven out
        if res == 4:
            if verbose: print("Hardway bet on " + str(self.Point) + " Loses " + str(self.adjamt * self.Multiplier))
            payout = self.adjamt * self.Multiplier * -1
            self.wins = 0
            self.adjamt = self.Amount
        #point set
        elif res == 2:
            if verbose: print("Hardway bet now on hard " + str(self.Point) + " for " + str(self.adjamt * self.Multiplier))
        #hard rolled
        elif rv == self.Point and hard:
            if verbose: print("Hardway bet on " + str(self.Point) + " Wins " + str(self.adjamt * self.Multiplier * hardwaypayout(rv)))
            payout = self.adjamt * self.Multiplier * hardwaypayout(rv)
            self.wins += 1
            self.adjamt = self.adjamt + (self.adjamt * self.Multiplier * hardwaypayout(rv))
        #soft rolled
        elif rv == self.Point and not hard:
            if verbose: print("Hardway bet on " + str(self.Point) + " Loses " + str(self.adjamt * self.Multiplier))
            payout = self.adjamt * self.Multiplier * -1
            self.wins = 0
            self.adjamt = self.Amount
        #point made
        elif res == 3:
            if verbose: print("Hardway bet now OFF hard " + str(self.Point))
        return payout


class AggPlace(Bet):
    def __init__(self, amt, pt):
        Bet.__init__(self, amt)
        self.Type = "AggPlace"
        self.Point = pt
        self.Active = False
        self.OddsAmount = 0
        self.adjamt = 0
        self.Multiplier = 1
        self.wins = 0
        self.aggMultiplier = 1
    def SetUp(self, pv, am=1):
        if self.Point != pv:
            self.adjamt = adjustplace(self.Amount, self.Point)
            if verbose: print("Place bet now on " + str(self.Point) + " for " + str(self.adjamt * self.Multiplier) + " (wins:" + str(self.wins) + ")")
            self.wins = 0
            self.Multiplier = 1
            self.aggMultiplier = am
            self.Active = True
        else:
            self.Active = False
            self.aggMultiplier = 1
    def Resolve(self, rv, p):
        payout = 0
        #was comeout roll
        if(p == rv):
            if self.Point != p:
                if verbose: print("Place bet back up on " + str(self.Point) + " for " + str(self.adjamt * self.Multiplier) + " (wins:" + str(self.wins) + ")")
                payout = 0
            else:
                if verbose: print("Place bet off of " + str(self.Point))
                payout = 0
                self.Active = False
        #win
        elif(rv == self.Point):
            if verbose: print("Place on " + str(self.Point) + " Wins " + str(placepayout(self.Point) * self.adjamt * self.Multiplier) + " (wins:" + str(self.wins + 1) + ")")
            self.wins += 1
            payout = placepayout(self.Point) * self.adjamt * self.Multiplier
            if(self.wins == 3):
                self.wins = 0
                self.Multiplier += 1
                if verbose: print("Upping Place bet on " + str(self.Point) + " to " + str(self.adjamt * self.Multiplier))
        #seven out
        elif(rv == 7):
            if verbose: print("Place bet on " + str(self.Point) + " Loses " + str(self.adjamt * self.Multiplier))
            self.Active = False
            payout = self.adjamt * -1 * self.Multiplier
            self.wins = 0
            self.Multiplier = 1
            self.aggMultiplier = 1
        #front line won
        if(p == 0 and rv != 7 and rv != 2 and rv != 3 and rv != 12):
            if verbose: print("Place bet on " + str(self.Point) + " for " + str(self.adjamt * self.Multiplier) + " is now OFF")
        return payout        
        


class PassBet345(Bet):
    def __init__(self, amt):
        Bet.__init__(self, amt)
        self.Type = "PassBet345"
        self.Point = 0
        self.Active = True
        self.OddsAmount = 0
        self.aggMultiplier = 1

    def Resolve(self, rv, p, am=1):
        self.aggMultiplier = am
        #comeout roll
        if(self.Point == 0):
            #seven winner
            if(rv == 7):
                if verbose: print("Passline Wins " + str(self.Amount * self.aggMultiplier))
                return self.Amount * self.aggMultiplier
            #point set
            elif(rv in points):
                self.Point = rv
                if verbose: print("Pass Bet Now On " + str(rv))
                if(rv == 4 or rv == 10):
                    self.OddsAmount = self.Amount * 3 * self.aggMultiplier
                if(rv == 5 or rv == 9):
                    self.OddsAmount = self.Amount * 4 * self.aggMultiplier
                if(rv == 6 or rv == 8):
                    self.OddsAmount = self.Amount * 5 * self.aggMultiplier                  
                return 0
            #craps
            else:
                if verbose: print("Passline Loses " + str(self.Amount * self.aggMultiplier))
                return self.Amount * -1 * self.aggMultiplier
        #not comeout
        else:
            #hit point
            if(rv == self.Point):
                self.Point = 0
                if verbose: print("Passline Wins " + str(self.Amount * self.aggMultiplier))
                if verbose: print("Passline Odds Wins " + str(self.OddsAmount * oddspayout(rv) * self.aggMultiplier))
                return (self.OddsAmount * oddspayout(rv) * self.aggMultiplier) + (self.Amount * self.aggMultiplier)

            #seven out
            elif(rv == 7):
                self.Point = 0
                if verbose: print("Passline Loses " + str(self.Amount * self.aggMultiplier))
                if verbose: print("Passline Odds Loses " + str(self.OddsAmount * self.aggMultiplier))
                return (self.Amount * self.aggMultiplier + self.OddsAmount * self.aggMultiplier) * -1                
            else:
                return 0



class Die:
    def __init__(self):
        self.Value = 0
    def Roll(self):
        global r
        self.Value = r.randint(1,6)
        return self.Value

      
class Game:
    def __init__(self, br):
        self.Bankroll = br
        self.Dice = [Die(), Die()]
        self.Point = 0
        self.RollValue = 0
        self.result = 0
    def Roll(self):
        global points
        d1 = self.Dice[0].Roll()
        d2 = self.Dice[1].Roll()
        self.RollValue = d1 + d2
        if verbose: print("Roll: " + str(self.RollValue))
    
        #comeout roll
        if(self.Point == 0):
            #point number
            if self.RollValue in points:
                self.Point = self.RollValue
                self.result = 2
                if verbose: print("Point is now: " + str(self.Point))
            #seven winner
            elif self.RollValue == 7:
                if verbose: print("Seven Winner!")
                self.result = 1
            #craps
            else:
                if verbose: print("Craps, line away.")
                self.result = 0
        #not comeout roll - seven out
        elif self.RollValue == 7:
            self.Point = 0
            if verbose: print("Seven out!")
            self.result = 4
        #made point
        elif self.RollValue == self.Point:
            self.Point = 0
            if verbose: print("Winner front line!")
            self.result = 3
        #some other number
        else:
            self.result = 5
        
        return self.RollValue


class RunGame:
    def __init__(self, br, b):
        self.game = Game(br)
        self.Bets = b
        self.Rolls = 0
        self.AggMultiplier = 1
        
    def Roll(self, am=1):
        global points
        self.AggMultiplier = am
        self.Rolls += 1
        self.game.Roll()
        self.come = True        
                
        for bet in self.Bets:
            if(bet.Active):
                if(bet.Type == "PassBet345"):
                    self.game.Bankroll += int(bet.Resolve(self.game.RollValue, self.game.Point, self.AggMultiplier))
                elif bet.Type == "ParlayHardway":
                    hard = self.game.Dice[0].Value == self.game.Dice[1].Value
                    self.game.Bankroll += int(bet.Resolve(self.game.RollValue, self.game.result, hard))
                else:
                    self.game.Bankroll += int(bet.Resolve(self.game.RollValue, self.game.Point))
            else:
                if(bet.Type == "ComeBet345"):
                    if(self.game.Point > 0):
                        if(self.come):
                            bet.SetUp(0)
                            self.come = False
                if(bet.Type == "PassBet345"):
                    if self.game.RollValue in points:
                        bet.SetUp(self.game.RollValue)

                if(bet.Type == "PlaceOpposite"):
                    if(self.game.Point > 0):
                        bet.SetUp(self.game.Point)
                if(bet.Type == "AggPlaceOpposite"):
                    if(self.game.Point > 0):
                        bet.SetUp(self.game.Point, self.game.Bankroll)
                if(bet.Type == "AggPlace"):
                    if(self.game.Point > 0):
                        bet.SetUp(self.game.Point)
 

    def DoRolls(self, rolls):
        for x in range(0,rolls):
            if(self.game.Bankroll > 0):
                self.Roll()
                if verbose: print(str(self.game.Bankroll) + "\n")
            else:
                #print("Bust at " + str(x) + " rolls.")
                break

    def stoploss(self, BANKROLL, r=400):
        rolls = 0
        stoploss = (BANKROLL / 2)
        breakpoint = (BANKROLL / 2)
        overallmultiplier = 1
        while self.game.Bankroll > stoploss and self.Rolls < r:
            if self.game.Bankroll >= (stoploss + (breakpoint * 1.5)):
                stoploss = stoploss  + breakpoint
        
            overallmultiplier = math.floor(self.game.Bankroll / BANKROLL)
            if overallmultiplier < 1:
                overallmultiplier = 1

            if overallmultiplier > 2:
                #print("MULTIPLIER AT " + str(overallmultiplier))
                #print("BANKROLL AT " + str(self.game.Bankroll))
                pass
            self.Roll(overallmultiplier)
            rolls += 1
            if verbose: print(str(self.game.Bankroll) + "\n")

    def GoalOrNothing(self, goal):
        rolls = 0
        while self.game.Bankroll < goal:
            if(self.game.Bankroll > 0):
                self.Roll()
                rolls += 1
                if verbose: print(self.game.Bankroll)
            else:
                if verbose: print("Bust at " + str(rolls) + " rolls.")
                break
        if(self.game.Bankroll >= goal):
            if verbose: print("Hit target win goal of " + str(goal) + " after " + str(rolls) + " rolls.")


    def RollsOrNothing(self, rs):
        rolls = 0
        while(rolls < rs):
            if(self.game.Bankroll > 0):
                self.Roll()
                rolls += 1
                if verbose: print(self.game.Bankroll)
            else:
                #print("Bust at " + str(rolls) + " rolls.")
                break
        if(rolls >= rs):
            #print("Hit target rolls of " + str(rolls) + " with " + str(self.game.Bankroll) + " bankroll.")
            pass




verbose = False

def main():
    parser = argparse.ArgumentParser(description = 'Craps simulator')
    parser.add_argument('-bankroll', type=int, help='starting bankroll', default=1000)
    args = parser.parse_args()
    busts = 0
    wins = 0
    winbr = 0
    downs = 0
    downbr = 0
    rolls = 0
    bank = 500
    games = 4
    dorolls = 800
    br = 0

    #bs = [PassBet345(5), AggPlace(5, 6), AggPlace(5, 8)]
    #bs = [PassBet345(5), ComeBet345(5), ComeBet345(5)]
    bs = [ParlayHardway(5, 8),ParlayHardway(5, 6),ParlayHardway(5, 4),ParlayHardway(5, 10)]
    for y in range(0,games):
        rg = RunGame(bank, bs)
        #rg.DoRolls(dorolls)
        rg.stoploss(bank, dorolls)
        if verbose: print("---------------\nGAME END\n---------------")
        #print(rg.game.Bankroll)
        #rg.GoalOrNothing(2000)
        #rg.RollsOrNothing(dorolls)
        if(rg.game.Bankroll <= 0):
            busts += 1
            downbr += rg.game.Bankroll
        elif(rg.game.Bankroll < bank):
            downs += 1
            downbr += rg.game.Bankroll
        else:
            wins += 1
            winbr += rg.game.Bankroll
        rolls += rg.Rolls
        br += rg.game.Bankroll
    print(str(games) + " Sessions\t-\t" + str(bank) + " Bankroll")
    print("------------------------------------------------")
    print("Wins:\t\t\t" + str(wins))
    try:
        print("Avg Win:\t\t" + format((winbr/wins) - bank, ".2f"))
    except:
        pass
    print("Avg Rolls/Session:\t" + format(rolls /games, ".2f"))
    print("Total Time:\t\t" + format(rolls /100, ".2f") + " hrs")
    print("Down:\t\t\t" + str(downs))
    print("Bust:\t\t\t" + str(busts))
    try:
        print("Avg Loss:\t\t" + format((downbr/(downs + busts)) - bank, ".2f"))
    except:
        pass
    print("Avg End Bankroll:\t" + format(br/games, ".2f"))
    print("RoR:\t\t\t" + format((busts/games) * 100, ".2f") + "%")
    print("Total win/loss:\t\t" + "+"*(br - (games*bank) > 0) + (str(br - (games*bank))))
    
if __name__ == "__main__":
    main()
