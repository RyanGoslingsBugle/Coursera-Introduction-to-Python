# requires SimpleGUICS2Pygame module

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_str = "Hand contains"
        for card in self.hand:
            hand_str += (" " + str(card))
        return hand_str
            
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self): # computes the value of the hand
        value = 0
        ace_count = 0
        for card in self.hand:
            value += VALUES[str(card.get_rank())]
            if str(card.get_rank()) == 'A':
                ace_count += 1
        for i in range(ace_count):
            if (value + 11) <= 21:
                value += 10
        return value
   
    def draw(self, canvas, pos):
        for card in self.hand:	# draw a hand on the canvas, use the draw method for cards
            card.draw(canvas, pos)
            pos[0] += 100
        
# define deck class 
class Deck:
    def __init__(self): #create deck of card objects
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self): # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self): # deal a card object from the deck
        return self.deck.pop(-1)
    
    def __str__(self):# return a string representing the deck
        deck_str = "Deck contains"
        for card in self.deck:
            deck_str += (" " + str(card))
        return deck_str

deck = Deck()
player_hand = Hand()
dealer_hand = Hand()    
    
#define event handlers for buttons
def deal():
    global outcome, in_play, score, deck, player_hand, dealer_hand
    if in_play == True:
        outcome = "You forfeit. Deal again?"
        score -= 1
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        for i in range(2):
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
        in_play = True
        outcome = "Hit or stand?"

def hit(): #add card to player's hand while in play
    global outcome, in_play, score
    if in_play and (player_hand.get_value() <= 21):
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted. Deal again?"
            score -= 1
            in_play = False
       
def stand():
    global outcome, in_play, score
    if in_play:
        if player_hand.get_value() > 21:
            outcome = "You have busted. Deal again?"
            score -= 1
            in_play = False
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            if dealer_hand.get_value() > 21:
                outcome = "Dealer has busted. You win! Deal again?"
                score += 1
                in_play = False
            else: 
                if dealer_hand.get_value() >= player_hand.get_value():
                    outcome = "Dealer has won. Deal again?"
                    score -= 1
                    in_play = False
                else:
                    outcome = "Player has won. Deal again?"
                    score += 1
                    in_play = False

# draw handler    
def draw(canvas):
    player_hand.draw(canvas, [50, 482])
    dealer_hand.draw(canvas, [50, 20])
    if in_play == True:
        canvas.draw_image(card_back,
                          CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [50 + CARD_SIZE[0] / 2, 20 + CARD_SIZE[1] / 2], CARD_SIZE)
    canvas.draw_text(outcome, [250, 400], 20, "White", "sans-serif")
    canvas.draw_text("Blackjack", [250, 250], 26, "White", "serif")
    canvas.draw_text("Score: " + str(score), [250, 300], 20, "White", "sans-serif")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()