# Mini-project #6 - Blackjack
# this project has to be run in codeskulptor.org
# An online version could be found here: http://www.codeskulptor.org/#user43_NgkE6j4U0U_0.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
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
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        res = 'Hand contains'
        for card in self.cards:
            res += ' ' + str(card)
        return res

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video

        hand_value = 0
        has_aces = 0
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_aces += 1
        if has_aces:
            if hand_value + 10 <= 21:
                hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for index, card in enumerate(self.cards):
            card.draw(canvas, [pos[0] + 100 * index, pos[1]])


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop(random.randrange(0, len(self.deck)))

    def __str__(self):
        # return a string representing the deck
        res = 'Deck contains'
        for card in self.deck:
            res += ' ' + str(card)
        return res


# define event handlers for buttons
def deal():
    global outcome, score, prompt, in_play, deck, player, dealer

    if in_play:
        outcome = "Player lost this round"
        in_play = False
        score -= 1
    else:
        outcome = ''
    prompt = "Hit or Stand ?"
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()

    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True


def hit():
    # replace with your code below
    global outcome, score, prompt, in_play

    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You've busted"
            in_play = False
            score -= 1
            prompt = "New deal ?"
        else:
            prompt = "Hit or Stand ?"


def stand():
    # replace with your code below
    global outcome, in_play, score, prompt

    if in_play:
        in_play = False
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() >= 21:
            outcome = "Dealer's busted"
            in_play = False
            score += 1
        else:
            if player.get_value() <= dealer.get_value():
                outcome = "Dealer wins"
                in_play = False
                score -= 1
            else:
                outcome = "Player wins"
                in_play = False
                score += 1

        prompt = "NEW deal ?"


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    canvas.draw_text('Blackjack', [213, 50], 36, 'Black')
    canvas.draw_text(prompt, [300, 180], 24, 'Black')
    canvas.draw_text(outcome, [300, 380], 24, 'Black')
    canvas.draw_text('Score : ' + str(score), [50, 100], 24, 'Black')

    canvas.draw_text('Player', [50, 180], 24, 'Black')
    player.draw(canvas, [50, 220])
    canvas.draw_text('dealer', [50, 380], 24, 'Black')
    if in_play:
        dealer.draw(canvas, [50, 420])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + 36, 420 + 48], CARD_BACK_SIZE)
    else:
        dealer.draw(canvas, [50, 420])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
