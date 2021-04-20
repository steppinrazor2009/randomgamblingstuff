import random

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
        for x in range(5):
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

HIGH_CARD = 0
JOB = 1
TWOPAIR = 2
THREE = 3
STRAIGHT = 4
FLUSH = 5
FULLHOUSE = 6
FOUR = 7
STRAIGHTFLUSH = 8
ROYALFLUSH = 9

HAND_STRINGS = ["High card", "JOB", "Two pair", "Three of a kind",
    "Straight", "Flush", "Full House", "Four of a kind",
    "Straight flush", "Royal flush"]

PAYOUTS = [0,5,10,15,20,30,45,125,250,4000]

SUITS = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

class PokerHand():
    
    def __init__(self):
        pass

    def get_values(self, hand, threshhold = 0):
        ret = []
        for card in hand.cards:
            if(card.value >= threshhold):
                ret.append(card.value)
        return ret

    def get_card_values(self, cards, threshhold = 0):
        ret = []
        for card in cards:
            if(card.value >= threshhold):
                ret.append(card.value)
        return ret
    
    def get_suits(self, hand):
        ret = []
        for card in hand.cards:
            ret.append(card.suit)
        return ret

    def get_multiples(self, values, find):
        ret = 0
        for i in values:
            if i == find:
                ret += 1
        return ret

    def filter_high_cards(self, cards, threshhold):
        output = []
        for x in range(0,len(cards)):
            if(cards[x].value >= threshhold):
                output.append(cards[x])
        return output            
    
    def eval_hand(self, hand):
        if self.is_royal(hand):
            return ROYALFLUSH
        elif self.is_straight_flush(hand):
            return STRAIGHTFLUSH
        elif self.is_four(hand):
            return FOUR
        elif self.is_full_house(hand):
            return FULLHOUSE
        elif self.is_flush(hand):
            return FLUSH
        elif self.is_straight(hand):
            return STRAIGHT
        elif self.is_three(hand):
            return THREE
        elif self.is_two_pair(hand):
            return TWOPAIR
        elif self.is_job(hand):
            return JOB
        else:
            return HIGH_CARD

    def find_high_cards(self, hand):
        output = []
        return output
            
    def find_job(self, hand):
        output = []
        values = self.get_values(hand, 11)
        for i in range(0,5):
            for x in range(i+1,5):
                if hand.cards[i].value == hand.cards[x].value:
                    output.append(i)
                    output.append(x)
                    break
            if len(output) > 0:
                break
        return output

    def find_pair(self, hand):
        output = []
        values = self.get_values(hand)
        for i in range(0,5):
            for x in range(i+1,5):
                if hand.cards[i].value == hand.cards[x].value:
                    output.append(i)
                    output.append(x)
                    break
            if len(output) > 0:
                break
        return output

    def find_two_pair(self, hand):
        output = []
        values = self.get_values(hand)
        for i in range(0,5):
            for x in range(i+1,5):
                if hand.cards[i].value == hand.cards[x].value:
                    output.append(i)
                    output.append(x)
                    break
            if len(output) > 0:
                break
        for i in range(output[0]+1,5):
            for x in range(i+1,5):
                if hand.cards[i].value == hand.cards[x].value:
                    output.append(i)
                    output.append(x)
                    break
            if len(output) > 2:
                break
            
        return output

    def find_three(self, hand):
        output = []
        values = self.get_values(hand)
        for i in range(0,5):
            if self.get_multiples(values, hand.cards[i].value) == 3:
                output.append(i)
                for x in range(i+1,5):
                    if hand.cards[i].value == hand.cards[x].value:
                        output.append(x)
                break
        return output    

    def find_four(self, hand):
        output = []
        values = self.get_values(hand)
        for i in range(0,5):
            if self.get_multiples(values, hand.cards[i].value) == 4:
                output.append(i)
                for x in range(i+1,5):
                    if hand.cards[i].value == hand.cards[x].value:
                        output.append(x)
                break
        return output  

    def find_straight(self, hand):
        return [0,1,2,3,4]

    def find_flush(self, hand):
        return [0,1,2,3,4]

    def find_full_house(self, hand):
        return [0,1,2,3,4]

    def find_straight_flush(self, hand):
        return [0,1,2,3,4]
    
    def find_royal(self, hand):
        return [0,1,2,3,4]

    def is_job(self, hand):
        ret = False
        values = self.get_values(hand, 11)
        pairs = 0
        for i in values:
            if self.get_multiples(values, i) == 2:
                pairs += 1
        if pairs == 2:
            ret = True                
        return ret

    def is_pair(self, hand):
        ret = False
        values = self.get_values(hand)
        pairs = 0
        for i in values:
            if self.get_multiples(values, i) == 2:
                pairs += 1
        if pairs == 2:
            ret = True                
        return ret

    def sort_cards(self, cards):
        return sorted(cards)

    def is_spread_five(self, values):
        ret = False
        mini = min(values)
        maxi = max(values)
        unis = (len(values) >= len(set(values)))
        ret = ((maxi - mini) <= 4) and unis
        return ret

    def suits_list(self, hand, suit):
        ret = []
        for i in range(0,5):
            if hand.cards[i].suit == suit:
                ret.append(hand.cards[i])
        return ret

    def is_four_to_a_straight_flush(self, hand):
        ret = False
        srt = hand.sorted_hand()
        for suit in SUITS:
            lst = self.get_card_values(self.suits_list(srt, suit))
            if len(lst) >= 4:
                if self.is_spread_five(lst):
                    ret = True
                    break
        return ret     

    def find_four_to_a_straight_flush(self, hand):
        ret = []
        srt = hand.sorted_hand()
        lst = []
        for suit in SUITS:
            lst = self.suits_list(srt, suit)
            if len(lst) >= 4:
                if self.is_spread_five([lst[0].value, lst[1].value, lst[2].value, lst[3].value]):
                    break
        for i in range(0, len(lst)):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)

    def is_four_to_a_royal(self, hand):
        ret = False
        if self.is_four_to_a_straight_flush(hand):
            if hand.sorted_hand().cards[0].value == 10 or hand.sorted_hand().cards[0].value == 11:
                ret = True
        return ret        

    

    def is_three_to_a_royal(self, hand):
        ret = False
        srt = hand.sorted_hand()
        for suit in SUITS:
            lst = self.get_card_values(self.filter_high_cards(self.suits_list(srt, suit), 10))
            if len(lst) >= 3:
                if self.is_spread_five(lst):
                    ret = True
                    break
        return ret          

    def find_three_to_a_royal(self, hand):
        ret = []
        srt = hand.sorted_hand()
        for suit in SUITS:
            lst = self.get_card_values(self.filter_high_cards(self.suits_list(srt, suit), 10))
            lst2 = self.filter_high_cards(self.suits_list(srt, suit), 10)
            if len(lst) >= 3:
                if self.is_spread_five(lst):
                    break
            if len(lst) == 5:
                if self.is_spread_five(lst):
                    break
        for i in range(0, len(lst2)):
            ret.append(hand.cards.index(lst2[i]))
        return sorted(ret)

    def find_four_to_a_royal(self, hand):
        return self.find_four_to_a_straight_flush(hand)

    def is_four_to_a_flush(self, hand):
        ret = False
        for suit in SUITS:
            lst = self.suits_list(hand, suit)
            if len(lst) >= 4:
                ret = True
                break
        return ret

    def find_four_to_a_flush(self, hand):
        ret = []
        for suit in SUITS:
            lst = self.suits_list(hand, suit)
            if len(lst) >= 4:
                break
        for i in range(0, len(lst)):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)
    
    def is_two_pair(self, hand):
        ret = False
        pairs = 0
        values = self.get_values(hand)
        for i in values:
            if self.get_multiples(values, i) == 2:
                pairs += 1
        if pairs == 4:
            ret = True
        return ret        

    def is_three(self, hand):
        ret = False
        values = self.get_values(hand)
        for i in values:
            if self.get_multiples(values, i) == 3:
                ret = True
        return ret

    def is_straight(self, hand):
        ret = True
        values = self.get_values(hand)
        for i in range(0,4):
            if values[i+1] != values[i] + 1:
                ret = False
        return ret

    def is_flush(self, hand):
        suits = self.get_suits(hand)
        return suits[0] == suits[1] == suits[2] == suits[3] == suits[4]    
    
    def is_full_house(self, hand):
        pair = False
        three = False
        values = self.get_values(hand)
        for i in values:
            if self.get_multiples(values, i) == 3:
                three = True
            if self.get_multiples(values, i) == 2:
                pair = True                
        return pair and three
    
    def is_four(self, hand):
        ret = False
        values = self.get_values(hand)
        for i in values:
            if self.get_multiples(values, i) == 4:
                ret = True
        return ret

    def is_straight_flush(self, hand):
        return self.is_straight(hand) and self.is_flush(hand)

    def is_royal(self, hand):
        return self.is_straight(hand) and self.is_flush(hand) and hand.sorted_hand().cards[4].value == 14

    def is_outside_straight(self, hand):
        ret = False
        srt = hand.sorted_hand()
        values = self.get_values(srt)
        for x in range(0,2):
            if (values[0+x] + 3) == (values[1+x] + 2) == (values[2+x] + 1) == (values[3+x]):
                ret = True
                break
        return ret

    def find_outside_straight(self, hand):
        ret = []
        winners = []
        srt = hand.sorted_hand()
        values = self.get_values(srt)
        for x in range(0,2):
            if (srt.cards[0+x].value + 3) == (srt.cards[1+x].value + 2) == (srt.cards[2+x].value + 1) == (srt.cards[3+x].value):
                winners.append(srt.cards[0+x])
                winners.append(srt.cards[1+x])
                winners.append(srt.cards[2+x])
                winners.append(srt.cards[3+x])
                break
        for i in range(0, len(winners)):
            ret.append(hand.cards.index(winners[i]))
        return sorted(ret)   

    def is_suited_high_cards(self, hand):
        ret = False
        for suit in SUITS:
            lst = self.filter_high_cards(self.suits_list(hand, suit), 11)
            if len(lst) >= 2:
                ret = True
                break
        return ret

    def find_suited_high_cards(self, hand):
        ret = []
        for suit in SUITS:
            lst = self.filter_high_cards(self.suits_list(hand, suit), 11)
            if len(lst) >= 2:
                break
        for i in range(0, len(lst)):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)          

    def is_to_a_straight_flush(self, hand, howmany):
        ret = False
        srt = hand.sorted_hand()
        for suit in SUITS:
            lst = self.get_card_values(self.suits_list(srt, suit))
            if len(lst) >= howmany:
                if self.is_spread_five(lst):
                    ret = True
                    break
        return ret     

    def find_to_a_straight_flush(self, hand, howmany):
        ret = []
        srt = hand.sorted_hand()
        for suit in SUITS:
            lst = self.suits_list(srt, suit)
            lst2 = self.get_card_values(self.suits_list(srt, suit))
            if len(lst) >= howmany:
                if self.is_spread_five(lst2):
                    break
        for i in range(0, len(lst)):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)

    def is_unsuited_high_cards(self, hand):
        ret = False
        lst = self.filter_high_cards(hand.cards, 11)
        if len(lst) >= 2:
            ret = True
        return ret

    def find_unsuited_high_cards(self, hand):
        ret = []
        lst = sorted(self.filter_high_cards(hand.cards, 11))
        for i in range(0, 2):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)       

    def is_suited_ten_plus_face(self, hand):
        ret = False
        for suit in SUITS:
            lst = self.filter_high_cards(self.suits_list(hand, suit), 10)
            if len(lst) >= 2:
                ret = True
                break
        return ret

    def find_suited_ten_plus_face(self, hand):
        ret = []
        for suit in SUITS:
            lst = self.filter_high_cards(self.suits_list(hand, suit), 10)
            if len(lst) >= 2:
                break
        for i in range(0, len(lst)):
            ret.append(hand.cards.index(lst[i]))
        return sorted(ret)

    def is_high_card(self, hand):
        ret = False
        lst = self.filter_high_cards(hand.cards, 11)
        if len(lst) >= 1:
            ret = True
        return ret

    def find_high_card(self, hand):
        ret = []
        lst = self.filter_high_cards(hand.cards, 11)
        if len(lst) >= 1:
            ret.append(hand.cards.index(lst[0]))
        return ret        

class Hand():
    """
    Implement a vp hand
    """

    def __init__(self):
        self.cards = []
        
    def __str__(self):
        ret = ""
        for c in self.cards:
            if ret != "":
                ret = ret + "\n" 
            ret = ret + str(c)
        return ret

    def add_card(self, card):
        self.cards.append(card)

    def replace_card(self, oc, nc):
        self.cards[oc] = nc
        
        
    def clear(self):
        self.cards = []

    def sorted_hand(self):
        ret = Hand()
        tmp = sorted(self.cards)
        for card in tmp:
            ret.cards.append(card)
        return ret

class Game():
    def __init__(self):
        self.deck = Deck()
        self.hand = Hand()

    def draw_hand(self):
        self.deck.refresh()
        self.hand = self.deck.get_hand()

    def draw(self, drawcards):
        pass

    def autoplay(self):
        draw_hand()

    def basic_strategy(self, hand):
        ret = []
        ph = PokerHand()
        if(ph.is_royal(hand)):
            return ph.find_royal(hand)
        if(ph.is_straight_flush(hand)):
            return ph.find_straight_flush(hand)
        if(ph.is_four(hand)):
            return ph.find_four(hand)        
        if(ph.is_four_to_a_royal(hand)):
            return ph.find_four_to_a_royal(hand)        
        if(ph.is_full_house(hand)):
            return ph.find_full_house(hand)        
        if(ph.is_flush(hand)):
            return ph.find_flush(hand)        
        if(ph.is_straight(hand)):
            return ph.find_straight(hand)        
        if(ph.is_three(hand)):
            return ph.find_three(hand)
        if(ph.is_to_a_straight_flush(hand, 4)):
            return ph.find_to_a_straight_flush(hand, 4)               
        if(ph.is_two_pair(hand)):
            return ph.find_two_pair(hand)
        if(ph.is_job(hand)):
            return ph.find_job(hand)
        if(ph.is_three_to_a_royal(hand)):
            return ph.find_three_to_a_royal(hand)
        if(ph.is_four_to_a_flush(hand)):
            return ph.find_four_to_a_flush(hand)
        if(ph.is_pair(hand)):
            return ph.find_pair(hand)
        if(ph.is_outside_straight(hand)):
            return ph.find_outside_straight(hand)
        if(ph.is_suited_high_cards(hand)):
            return ph.find_suited_high_cards(hand)
        if(ph.is_to_a_straight_flush(hand, 3)):
            return ph.find_to_a_straight_flush(hand, 3)
        if(ph.is_unsuited_high_cards(hand)):
            return ph.find_unsuited_high_cards(hand)
        if(ph.is_suited_ten_plus_face(hand)):
            return ph.find_suited_ten_plus_face(hand)
        if(ph.is_high_card(hand)):
            return ph.find_high_card(hand)
        #Discard everything
        return ret
        
    def get_discards(self, holdcards):
        ret = []
        for x in range(5):
            if not(x in holdcards):
                ret.append(x)
        return ret

    def get_outcome(self):
        ph = PokerHand()
        return ph.eval_hand(self.hand)

VERBOSE = False
SHOW_WINS = True
G = Game()
        
def simulate_one_hand():
    G.draw_hand()
    holdcards = G.basic_strategy(G.hand)
    discards = G.get_discards(holdcards)
    for x in discards:
        G.hand.replace_card(x, G.deck.get_card())
    if VERBOSE: print(G.hand)
    outcome = G.get_outcome()
    if VERBOSE: print(str(HAND_STRINGS[outcome]))
    pay = PAYOUTS[outcome]
    if VERBOSE: print("Pays: ", str(pay))
    return pay

def simulate_br_play(bankroll, maxgames, denom):
    output = []
    games = 0
    coinin = 0
    while bankroll > 0 and games < maxgames:
        bankroll -= (denom * 5)
        outcome = simulate_one_hand()
        if outcome >= (250):
            if SHOW_WINS: print("BIG WIN of ", str(outcome), " with:")
            if SHOW_WINS: print(G.hand)
        bankroll = bankroll + (outcome * denom)
        games += 1
        coinin = coinin + (denom * 5)
    print("\tGames:\t\t", str(games))
    print("\tCoin-in:\t", str(coinin))
    print("\tBankroll:\t", str(bankroll))
    print("\t==============================")
    output.append(games)
    output.append(coinin)
    output.append(bankroll)
    return output

def play_until_royal():
    games = 0
    br = 0
    while True:
        br = br - 5
        outcome = simulate_one_hand()
        games += 1
        br = br + outcome
        if outcome > (125):
            if SHOW_WINS: print("BIG WIN of ", str(outcome), " with:")
            if SHOW_WINS: print(G.hand)
            if outcome > 250:
                break
    print("\tGames:\t\t", str(games))
    print("\tExpense:\t\t", str(br))
    ev = (br * 100) / (games * 5)
    print("\tEV:\t\t", format(ev, ".2f"))

def simulate_sessions(sessions, bankroll, maxgames, denom):
    totalgames = 0
    totalcoinin = 0
    totalbankroll = 0
    busts = 0
    for x in range(sessions):
        outcome = simulate_br_play(bankroll, maxgames, denom)
        totalgames = totalgames + outcome[0]
        totalcoinin = totalcoinin + outcome[1]
        totalbankroll = totalbankroll + outcome[2]
        if(outcome[2] <= 0): busts += 1
    print("==============================")
    print("Average Games:\t\t", format(totalgames/sessions,".2f"))
    print("Average Coin-in:\t", format(totalcoinin/sessions,".2f"))
    print("Average Bankroll:\t", format(totalbankroll/sessions,".2f"))
    print("Busted:\t", str(busts), " times")
    print("RoR:\t", format((busts/sessions) * 100,".2f"), "%")


#simulate_sessions(50, 1000, 2400, 1)
play_until_royal()

   
