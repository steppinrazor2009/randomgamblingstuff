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

    ranks = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('Jack', 10), ('Queen', 10), ('King', 10),('Ace', 1)]
    suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

    def __init__(self, decks):
        self.cards = []
        self.decks = decks
        for x in range(self.decks):
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

    def cards_left(self):
        return len(self.cards)

    def shuffle(self):
        
        self.cards = []
        for x in range(self.decks):
            for r in self.ranks:
                for s in self.suits:
                    c = Card()
                    c.value = r[1]
                    c.rank = r[0]
                    c.suit = s
                    self.cards.append(c)
        random.shuffle(self.cards)        
    
    def get_card(self):
        return self.cards.pop()


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
    def __init__(self):
        self.deck = Deck(8)
        self.banker = Hand()
        self.player = Hand()
        self.needshuffle = False

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

    def deal(self):
        self.player.clear()
        self.banker.clear()
        if self.needshuffle:
            self.deck.shuffle()
        self.player.add_card(self.deck.get_card())
        self.banker.add_card(self.deck.get_card())
        self.player.add_card(self.deck.get_card())
        self.banker.add_card(self.deck.get_card())
        if self.deck.cards_left() < 52:
            self.needshuffle = True

        #natural
        if self.player.get_score() >= 8 or self.banker.get_score() >= 8:
            return None
        #player draws
        elif self.player.get_score() <= 5:
            player3rd = self.deck.get_card()
            self.player.add_card(player3rd)
            if self.bank_third(player3rd.value):
                self.banker.add_card(self.deck.get_card())
        #player stands
        else:
            #banker draws
            if self.banker.get_score() <= 5:
                self.banker.add_card(self.deck.get_card())

    def compare(self):
        if self.player.get_score() > self.banker.get_score():
            return "Player"
        elif self.banker.get_score() > self.player.get_score():
            return "Banker"
        else:
            return "Tie"
    

VERBOSE = False
G = Game()


def bet_ties(bet, bankroll):
    games = 0
    gamessincetie = 0
    br = bankroll
    betting = False
    while 0 < br < (bankroll * 2):
        games += 1
        if VERBOSE: print("Last Tie: ", str(gamessincetie), " games ago.")
        if gamessincetie >= 50:
            betting = True
            br = br - bet

        G.deal()
        winner = G.compare()
        
        if winner == "Tie":
            if betting:
                br = br + (bet * 8)
            gamessincetie = 0
        else:
            gamessincetie += 1
        if VERBOSE: print(winner, " wins!")
        if VERBOSE: print("Bankroll:\t", str(br))

        betting = False
    if VERBOSE: print("Games:\t", str(games))
    return br

def bet_player(bet, bankroll, hands):
    games = 0
    br = bankroll
    while 0 < br and games < hands and br < (bankroll * 2):
        games += 1

        G.deal()
        winner = G.compare()
        
        if winner == "Player":
            br = br + bet
        elif winner == "Banker":
            br = br - bet

        if VERBOSE: print(winner, " wins!")
        if VERBOSE: print("Bankroll:\t", str(br))
    if VERBOSE: print("Games:\t", str(games))
    return [games, br]

def simulate_sessions(sessions, bankroll, bet):
    totalbr = 0
    wins = 0
    totalwin = 0
    losses = 0
    totalloss = 0
    for x in range(sessions):
        br = bet_ties(bet,bankroll)
        if br > bankroll:
            wins += 1
            totalwin = totalwin + br
        else:
            losses += 1
            totalloss = (totalloss + (bankroll - br))
        print("\tGame BR(end): ", str(br))
        totalbr = totalbr + br
    print("Wins:\t\t", str(wins))
    print("Avg win:\t", format((totalwin/wins) - bankroll, ".2f"))
    print("Losses:\t\t", str(losses))
    print("Avg loss:\t", format((totalloss/losses), ".2f"))

def simulate_sessions2(sessions, bankroll, bet, games):
    totalbr = 0
    wins = 0
    totalwin = 0
    losses = 0
    totalloss = 0
    totalgames = 0
    for x in range(sessions):
        ret = bet_player(bet,bankroll, games)
        totalgames = totalgames + ret[0]
        br = ret[1]
        if br > bankroll:
            wins += 1
            totalwin = totalwin + br
        else:
            losses += 1
            totalloss = (totalloss + (bankroll - br))
        print("\tGame BR(end): ", str(br))
        totalbr = totalbr + br
    print("Wins:\t\t", str(wins))
    print("Avg win:\t", format((totalwin/wins) - bankroll, ".2f"))
    print("Losses:\t\t", str(losses))
    print("Avg loss:\t", format((totalloss/losses), ".2f"))
    print("Avg hands:\t", format((totalgames/sessions), ".2f"))

simulate_sessions2(100, 1000000, 50, 5000)
