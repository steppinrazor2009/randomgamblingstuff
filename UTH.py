import random, math, itertools

HAND_STRINGS = ["High card", "Pair", "Two pair", "Three of a kind", "Straight", "Flush", "Full House", "Four of a kind", "Straight flush", "Royal flush"]

PAYOUTS = [0,5,10,15,20,30,45,125,250,4000]

BET_CHANCE = [1,2,3]

SUITS = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

def all_equal(lst):
    return len(set(lst)) == 1

def is_consecutive(lst):
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

def evaluate_hand(cards):
    ranks = [card.value for card in cards]
    suits = [card.suit for card in cards]

    if is_consecutive(ranks):
        return (
            4 if not all_equal(suits) else
            8 if max(ranks) < 14 else
            9
        )
    if all_equal(suits):
        return 5
    return {
        4 + 4 + 4 + 4 + 1: 7,
        3 + 3 + 3 + 2 + 2: 6,
        3 + 3 + 3 + 1 + 1: 3,
        2 + 2 + 2 + 2 + 1: 2,
        2 + 2 + 1 + 1 + 1: 1,
        1 + 1 + 1 + 1 + 1: 0,
    }[sum(ranks.count(r) for r in ranks)]

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

def compare_high_cards(h1, h2):
    for x in range(len(h1)):
        if h1[x] > h2[x]:
            return 1
        elif  h2[x] > h1[x]:
            return 2
    return 0

def compare_hands(hand1, hand2):
    h1v = evaluate_hand(hand1.cards)
    h2v = evaluate_hand(hand2.cards)
    if h1v > h2v:
        return 1
    elif h2v > h1v:
        return 2
    elif h1v == h2v:
        h1ranks = [card.value for card in hand1.cards]
        h2ranks = [card.value for card in hand2.cards]

        h1ranks.sort(reverse=True)
        h2ranks.sort(reverse=True)

        L1 = [list(v) for k,v in itertools.groupby(h1ranks)]
        L1.sort(key=len, reverse=True)
        L2 = [list(v) for k,v in itertools.groupby(h2ranks)]
        L2.sort(key=len, reverse=True)
        return(compare_high_cards(L1, L2))
    return 0

def basic_strategy_r1(hand):
    ranks = [card.value for card in hand.cards]
    ranks.sort(reverse=True)

    #pair
    if ranks[0] == ranks[1]:
        if ranks[0] >= 3:
            return True
        else:
            return False
    #has ace
    elif ranks[0] == 14:
        return True
    #has king
    elif ranks[0] == 13:
        #doesnt matter >=5
        if ranks[1] >= 5:
            return True
        #<5 check if suited
        else:
            if hand.cards[0].suit == hand.cards[1].suit:
                return True
            else:
                return False
    #has queen
    elif ranks[0] == 12:
        #doesnt matter >=8
        if ranks[1] >= 8:
            return True
        #6 or 7, check if suited
        elif ranks[1] >= 6:
            if hand.cards[0].suit == hand.cards[1].suit:
                return True
        else:
            return False    
    #has jack
    elif ranks[0] == 11:
        #doesnt matter if 10
        if ranks[1] == 10:
            return True
        #68 or 9, check if suited
        elif ranks[1] >= 8:
            if hand.cards[0].suit == hand.cards[1].suit:
                return True
        else:
            return False
                #nothing above 10
    return False

def basic_strategy_r2(hand, flop):
    hf = hand + flop
    hfranks = [card.value for card in hf.cards]
    hfsuits = [card.suit for card in hf.cards]
    playerranks = [card.value for card in hand.cards]
    playersuits = [card.suit for card in hand.cards]
    bh = best_hand(hf.cards)
    bestvalue = evaluate_hand(bh)
    #2 pair or better
    if bestvalue >= 2:
        return True
    #one pair
    if bestvalue >= 1:
        #dont bet on pocket deuces
        if hand.cards[0].value == 2 and hand.cards[1].value == 2:
            return False
        else:
            #store the pair value in L1[0]
            L1 = [list(v) for k,v in itertools.groupby(hfranks)]
            L1.sort(key=len, reverse=True)
            #its a 'hidden pair'
            if L1[0][0] in playerranks:
                return True
            else:
                return False
    
    L1 = [list(v) for k,v in itertools.groupby(hfsuits)]
    L2 = max(L1,key=len)
    #4 to a flush
    if len(L2) >= 4:
        for card in hand.cards:
            if L2[0] == card.suit:
                if card.value >= 10:
                    return True
    return False

def basic_strategy_r3(hand, flop):
    hf = hand + flop
    playerranks = [card.value for card in hand.cards]
    bh = best_hand(hf.cards)
    bhranks = [card.value for card in bh]
    bhranks.sort(reverse=True)
    bestvalue = evaluate_hand(bh)

    #2 pair or better
    if bestvalue >= 2:
        return True
    #one pair
    if bestvalue == 1:
        #store the pair value in L1[0]
        L1 = [list(v) for k,v in itertools.groupby(bhranks)]
        L1.sort(key=len, reverse=True)
        #its a 'hidden pair'
        if L1[0][0] in playerranks:
            return True
        else:
            return False
    return False

def trips_Payout(handvalue, bet):

    ret = 0
    if handvalue == 3:
        ret = bet * 4
    elif handvalue == 4:
        ret = bet * 5
    elif handvalue == 5:
        ret = bet * 8
    elif handvalue == 6:
        ret = bet * 9
    elif handvalue == 7:
        ret = bet * 31
    elif handvalue == 8:
        ret = bet * 41
    elif handvalue == 9:
        ret = bet * 51
    return ret

def blind_Payout(handvalue, bet):
    ret = bet
    if handvalue == 4:
        ret = bet * 2
    elif handvalue == 5:
        ret = (bet * 1.5) + bet
    elif handvalue == 6:
        ret = bet * 4
    elif handvalue == 7:
        ret = bet * 11
    elif handvalue == 8:
        ret = bet * 51
    elif handvalue == 9:
        ret = bet * 501
    return ret

def payout(hand, winner, qual, trips, ante, blind, play):
    handvalue = evaluate_hand(hand.cards)
    ret = trips_Payout(handvalue, trips)
    if verbose: print("TRIPS PAYS:\t" + str(ret - trips))

    if winner == 0:
        ret += ante + blind + play
        if verbose: 
            print("ANTE PUSHES")
            print("BLIND PUSHES")
            print("PLAY PUSHES")
        return ret
    if qual:
        if winner == 1:
            ret += (ante * 2)
            if verbose: print("ANTE PAYS:\t" + str(ante))
            ret += (play * 2)
            if verbose: print("PLAY PAYS:\t" + str(play))
            ret += blind_Payout(handvalue, blind)
            if verbose: print("BLIND PAYS:\t" + str(blind_Payout(handvalue, blind) - blind))
    else:
        if winner == 1:
            ret += ante
            if verbose: print("ANTE PUSHES")
            ret += (play * 2)
            if verbose: print("PLAY PAYS:\t" + str(play))
            ret += blind_Payout(handvalue, blind)
            if verbose: print("BLIND PAYS:\t" + str(blind_Payout(handvalue, blind) - blind))
        else:
            ret += ante
            if verbose: print("ANTE PUSHES")
    return ret

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

def play_round(trips, ante):
    tripsbet = trips
    antebet = ante
    blindbet = ante
    playbet = 0
    hasbet = 0

    #subtract bets from BR
    totalbets = tripsbet + antebet + blindbet

    #deal and execute basic strategy
    g = Game()
    g.deal_hand()
    if basic_strategy_r1(g.player):
        hasbet = 4
    g.deal_flop()
    if not hasbet:
        if basic_strategy_r2(g.player, g.board):
            hasbet = 2
    g.deal_turn()
    if not hasbet:
        if basic_strategy_r3(g.player, g.board):
            hasbet = 1

    #get best hands
    playerhand = g.player + g.board
    dealerhand = g.dealer + g.board
    playerbesthand = Hand(best_hand(playerhand.cards))
    dealerbesthand = Hand(best_hand(dealerhand.cards))

    #output vfor debug
    if verbose: 
        print(g)
        print("\n" + HAND_STRINGS[evaluate_hand(playerbesthand.cards)] + "\t-\t" + HAND_STRINGS[evaluate_hand(dealerbesthand.cards)])
        print("\nBETTING:\t" + str(hasbet) + "x")

    #if no play bet player folded
    if not hasbet:
        winner = 2
    else:
        winner = compare_hands(playerbesthand, dealerbesthand)

    #subtract bets from BR
    playbet = antebet * hasbet
    totalbets += playbet

    #dealer didnt qualify
    dealernotqual = evaluate_hand(dealerbesthand.cards) == 0
    if dealernotqual:
        if verbose: print("DEALER DIDNT QUALIFY")

    #calculate payouts amd change BR and HR
    totalpayout = payout(playerbesthand, winner, not dealernotqual, tripsbet, antebet, blindbet, playbet)
    hr = totalpayout - totalbets
    
    #output for debug
    if hasbet > 0:
        if winner == 1:
            if verbose: print("WINNER!")
        elif winner == 2:
            if verbose: print("LOSER!")
        else:
            if verbose: print("PUSH")
    else:
        if verbose: print("FOLD")
    if verbose: print("HANDRESULT:\t" + str(hr))

    return [hr, winner, totalbets]

def play_game(br, trips, ante, maxhands=140):
    bankroll = br
    tripsbet = trips
    antebet = ante
    hands = 0
    wins = 0

    while (bankroll > ((ante * 6) + trips)) and hands < maxhands:
        handresult = play_round(bankroll, trips, antebet)
        if handresult > 0: wins += 1
        bankroll += handresult
        hands += 1
    result = (br - bankroll) * -1
    #print("BANKROLL AFTER: " + str(result)
    #print("HANDS: " + str(hands))
    #print("WINS: " + str(wins))
    return [result, hands, wins]

def play_game_sl(br, trips, ante, maxhands=140):
    bankroll = br
    tripsbet = trips
    antebet = ante
    hands = 0
    wins = 0
    multiplier = 1
    stoploss = 0
    hardstop = False
    slinc = br / 2
    totalbet = 0

    while (bankroll > stoploss and hands < maxhands):

        if bankroll > (br * 1.5):
            if stoploss == 0:
                stoploss = br
            else:
                if bankroll > (stoploss + slinc):
                    stoploss += slinc

        if stoploss > br:
            multiplier = ((stoploss - br) / slinc) + 1

        handresult = play_round(trips * multiplier, antebet * multiplier)
        bankroll += handresult[0]
        if handresult[1] == 1: wins += 1
        totalbet += handresult[2]
        hands += 1

    result = (br - bankroll) * -1
    return [result, hands, wins, totalbet]

verbose = False

sims = 10000
br = 500
trips = 0
bet = 1
hands = 100

highresult = 0
totalresult = 0
totalhands = 0
totalwins = 0
totalamountbet = 0
for x in range(sims):
    res = play_game_sl(br, trips, bet, hands)
    totalresult += res[0]
    totalhands += res[1]
    totalwins += res[2]
    totalamountbet += res[3]
    if res[0] > highresult:
        highresult = res[0]
avgresult = totalresult / sims
avghands = totalhands / sims
avgwins = totalwins / sims
avgbet = totalamountbet / totalhands
he = avgresult / avghands * trips
print("AVG RESULT:\t" + format(avgresult, ".2f"))
print("AVG HANDS:\t" + format(avghands, ".2f"))
print("AVG WINS:\t" + format(avgwins, ".2f"))
print("LARGEST WIN:\t" + format(highresult, ".2f"))
print("AVERAGE BET:\t" + format(avgbet, ".2f"))