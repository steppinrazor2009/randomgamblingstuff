import math, random

SYMBOL_STRINGS = ["Buffalo", "Eagle", "Stag", "Wolf"]
'''
#92%
SYMBOL_5PAYS = [5000, 500, 52, 5]
SYMBOL_4PAYS = [1000, 100, 10, 2]
SYMBOL_3PAYS = [500, 50, 5, 1]
'''

'''
#95%
SYMBOL_5PAYS = [5000, 500, 50, 5]
SYMBOL_4PAYS = [1000, 100, 15, 2]
SYMBOL_3PAYS = [500, 50, 5, 1]
'''


#90%
SYMBOL_5PAYS = [5000, 500, 46, 5]
SYMBOL_4PAYS = [1000, 100, 10, 2]
SYMBOL_3PAYS = [500, 50, 5, 1]


class Symbols():
    #Wild = 0
    Buffalo = 0
    Eagle = 1
    Stag = 2
    Wolf = 3


    def symbol_name(val):
        return SYMBOL_STRINGS[val]

class Reel:
    def __init__(self, symbols = []):
        self.symbols = symbols
        self.On = 0

    def copy(self):
        ret = Reel(self.symbols)
        ret.On = self.On
        return ret

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def add_symbols(self, symbols):
        for symbol in symbols:
            self.add_symbol(symbol)
        
    def __str__(self):
        return Symbols.symbol_name(self.symbols[self.On])

    def spin(self):
        self.On = random.randint(0,len(self.symbols) - 1)
        
class Machine:
    def __init__(self, reels = []):
        self.reels = reels

    def add_reel(self, reel):
        self.reels.append(reel)

    def __str__(self):
        ret = ""
        for reel in self.reels:
            ret = ret + str(reel) + "\t"
        return ret

    def get_results(self):
        ret = []
        for reel in self.reels:
            ret.append(reel.symbols[reel.On])
        return ret

    def spin_reels(self):
        for reel in self.reels:
            reel.spin()

    def win_amt(self, symbol, inarow):
        if inarow == 5:
            return SYMBOL_5PAYS[symbol]
        elif inarow == 4:
            return SYMBOL_4PAYS[symbol]
        elif inarow == 3:
            return SYMBOL_3PAYS[symbol]
        else:
            return 0

    def find_win(self):
        ret = 0
        results = self.get_results()
        inarow = 1
        first = results[0]
        for i in range(1, len(results)):
            if results[i] == first:
                inarow += 1
            else:
                break
        if inarow >= 3:
            ret = self.win_amt(first, inarow)

        if VERBOSE: print(self.get_results())
        return ret

def build_machine():
    reel1 = Reel()
    reel1.add_symbol(Symbols.Buffalo)
    reel1.add_symbols([Symbols.Eagle, Symbols.Eagle, Symbols.Eagle, Symbols.Eagle, Symbols.Eagle])
    reel1.add_symbols([Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag, Symbols.Stag])
    reel1.add_symbols([Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf, Symbols.Wolf])

    reel2 = reel1.copy()
    reel3 = reel2.copy()
    reel4 = reel2.copy()
    reel5 = reel2.copy()
    m = Machine([reel1, reel2, reel3, reel4, reel5])
    return m

def spin_sl(machine, br, unitsize):
    bankroll = br
    spins = 0
    slinc = round(br / 2)
    sl = round(br / 2)
    while bankroll >= sl + unitsize:
        spins += 1
        machine.spin_reels()
        bankroll = bankroll - unitsize
        win = machine.find_win()
        if win > 0:
            if win > 500:
                print(machine)
            bankroll = bankroll + (win * unitsize)
        if bankroll > (sl + (slinc*2)):
            sl = sl + slinc
    return [bankroll, spins]

def just_spend(machine, br, unitsize):
    bankroll = br
    spins = 0
    slinc = round(br / 2)
    sl = round(br / 2)
    while bankroll >= unitsize:
        spins += 1
        machine.spin_reels()
        bankroll = bankroll - unitsize
        win = machine.find_win()
        if win > 0:
            if win > 500:
                print(machine)
            bankroll = bankroll + (win * unitsize)
    return [bankroll, spins]

def spin_bigwin(machine):
    win = 0
    spins = 0
    while win <= 1000:
        spins += 1
        machine.spin_reels()
        win = machine.find_win()
    print(spins)
    print(machine)

def find_wins(symbols, sym):
    inarow = 1
    for i in range(1, len(symbols)):
        if symbols[i] == sym:
            inarow += 1
        else:
            break
    return inarow  

def get_odds(m):
    totalchances = len(m.reels[0].symbols) * len(m.reels[1].symbols) * len(m.reels[2].symbols) * len(m.reels[3].symbols) * len(m.reels[4].symbols)
    totalpays = 0
    wins = 0
    tests = 0
    sums = []
    for i in range(4):
        counts = [0,0,0]
        thiscount = 0
        symwins = 0
        symtests = 0
        for symbol1 in m.reels[0].symbols:
            if i == symbol1:
                thiscount += 1
        for symbol2 in m.reels[1].symbols:
            for symbol3 in m.reels[2].symbols:
                for symbol4 in m.reels[3].symbols:
                    for symbol5 in m.reels[4].symbols:
                        cnt = find_wins([i, symbol2, symbol3, symbol4, symbol5], i)
                        symtests += 1
                        if cnt > 2:
                            counts[cnt-3] = counts[cnt-3] + 1
                            symwins += 1
        for x in range(len(counts)):
            counts[x] = counts[x] * thiscount
        symwins = symwins * thiscount
        symtests = symtests * thiscount
        wins = wins + symwins
        
        tests = tests + symtests
                            
                            
        print("FOR ", SYMBOL_STRINGS[i], ":")
        print(counts)
        probs = []
        for x in range(len(counts)):
            probs.append(round(counts[x]/totalchances, 8))
        print(probs)

        pays = []
        pays.append(round(SYMBOL_3PAYS[i] * probs[0], 8))
        pays.append(round(SYMBOL_4PAYS[i] * probs[1], 8))
        pays.append(round(SYMBOL_5PAYS[i] * probs[2], 8))

        print(pays)
        totalpays = totalpays + sum(pays)
            
        sums.append(sum(probs) * 100)
    print(totalpays)    

def run_sim(sess, br, bet, m):
    totalspins = 0
    wins = 0
    sessions = sess
    bigwin = 0
    totalbr = 0
    bankroll = br
    betsize = bet
    bigloss = bankroll
    for x in range(sessions):
        output = spin_sl(m, bankroll, betsize)
        if output[0] > bigwin:
            bigwin = output[0]
        if output[0] < bigloss:
            bigloss = output[0]        
        totalspins = totalspins + output[1]
        if output[0] > bankroll:
            wins += 1
        totalbr = totalbr + output[0]
    print("BANKROLL:\t\t", str(bankroll))
    print("BET:\t\t\t", str(betsize))
    print(sessions, "SESSIONS\n---------------------------------")

    print("AVG SPINS/SESSION:\t", format(totalspins / sessions, ".2f"))
    print("WINS:\t\t\t", str(wins))
    print("BIGGEST WIN:\t\t", str(bigwin))
    print("BIGGEST LOSS:\t\t -", str(bankroll - bigloss))
    print("AVG TIER POINTS:\t", format(((totalspins / sessions)*betsize) / 5,".2f"))

def avg_spins(sessions, br, bet):
	totalspins = 0
	highspins = 0
	lowspins = 0

	for x in range(sessions):
		output = just_spend(m, 1000, 3)
		totalspins += output[1]
		if output[1] > highspins:
			highspins = output[1]
		if (lowspins <= 0) or (lowspins > output[1]):
			lowspins = output[1]
		#print("SPINS:\t\t\t", str(output[1]))
		
	print("AVG SPINS:\t\t\t", str(totalspins/sessions))
	print("HIGH SPINS:\t\t\t", str(highspins))
	print("LOW SPINS:\t\t\t", str(lowspins))


VERBOSE = False

m = build_machine()
#get_odds(build_machine())
#run_sim(1000, 4000, 100, build_machine())
avg_spins(100, 1000, 3)


