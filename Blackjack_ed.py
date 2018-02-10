import simplegui
import random

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

in_play = False
in_stand = False
in_game = False
outcome = ""
score = 0

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos,flag):
        global in_stand
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if flag:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0], pos[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0], pos[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i])+" "
        return ans	

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        ace_flag = 0
        i = 0
        while i < len(self.cards):
            hand_value += VALUES[self.cards[i].rank]
            if self.cards[i].rank == 'A':
                ace_flag += 1     
            i += 1   
                
        if ace_flag == 0:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                hand_value += 10
                return hand_value
            else:
                return hand_value
        return self.hand_value
        
    def draw(self, canvas, pos,type):
        i = 0
        flag = False
        if type == "d" and not in_stand:
            flag = True
        else:
            flag = False
        while i < len(self.cards):
            if i > 0:
                flag = False
            self.cards[i].draw(canvas,[72*i+86,pos[1]],flag) 
            i += 1
        
class Deck:
    def __init__(self):
        self.card_list = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.card_list.append(Card(SUITS[i],RANKS[j]))

    def shuffle(self):
        random.shuffle(self.card_list)

    def deal_card(self):
        ans = 	random.choice(self.card_list) 
        popped = self.card_list.pop(self.card_list.index(ans))
        return ans
    
    def __str__(self):
        ans = "Deck contains "
        for i in range(len(self.card_list)):
            ans += str(self.card_list[i])+" "
        return ans

def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score, in_stand, in_game

    if in_game:
        score -= 1
        outcome = "Dealer wins!!"
    outcome = ""
    in_stand = False
    in_game = True
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()  
    deck.shuffle()
    
    i = 1
    
    while i <= 4:
        dealt_card = deck.deal_card()
        if i % 2 == 0:            
            player_hand.add_card(dealt_card)
        else:
            dealer_hand.add_card(dealt_card)
        i += 1
    
    in_play = True

def hit():
    global in_play, outcome, score, in_stand, in_game
    if not in_play:
        outcome = "Dealer won!!"
        in_stand = True
        in_game = False
    else:
        next_card = deck.deal_card()
        player_hand.add_card(next_card)
        
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "Dealer won!!"
            in_stand = True
            in_game = False
            score -= 1
    
def stand():
    global score, outcome, in_stand, in_game
    in_stand = True
    if not in_play:
        outcome = "Dealer won!!"
        in_stand = True
        in_game = False
    else:
        while dealer_hand.get_value() <= 17:
            next_card = deck.deal_card()
            dealer_hand.add_card(next_card)
        if dealer_hand.get_value() > 21:
            outcome = "You won!!"
            in_stand = True
            in_game = False
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "Dealer won!!"
                in_stand = True
                in_game = False
                score -= 1
            else:
                outcome = "You won!!"
                in_stand = True
                in_game = False
                score += 1

def draw(canvas):
    global player_hand, dealer_hand, score, outcome, in_game
    canvas.draw_text("Blackjack", (50,75), 64, "Black")
    canvas.draw_text("Score: "+str(score), (350,75), 48, "Black")
    canvas.draw_text("Dealer", (50,175), 40, "Black")
    canvas.draw_text("Player", (50,375), 40, "Black")
    canvas.draw_text(outcome, (350,175), 40, "Black")
    if in_game:
        canvas.draw_text("Hit/Stand?", (350,375), 25, "Black")
    else:
        canvas.draw_text("New Deal?", (350,375), 25, "Black")
    dealer_hand.draw(canvas,[300,248],"d")
    player_hand.draw(canvas,[300,448],"p")

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()