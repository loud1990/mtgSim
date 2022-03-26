# This program will simmulate a game of magic the gathering
import copy
import enum
import random

import numpy as np


# Have an enum for each type of card
import self as self


class CardType(enum.Enum):
    CREATURE = 1
    INSTANT = 2
    SORCERY = 3
    LAND = 4
    PLANESWALKER = 5
    ENCHANTMENT = 6
    ARTIFACT = 7
    TRIBAL = 8


class DeckStrategy(enum.Enum):
    AGGRO = 1
    MIDRANGE = 2
    COMBO = 3
    CONTROL = 4
    OTHER = 5


class Triggers(enum.Enum):
    NA = 0
    PROWESS = 1


class Card:
    type = CardType.CREATURE
    cmc = 1
    cost = "R"
    name = "Monastery Swiftspear"
    tapped = False
    summoningSick = True
    deckStrategy = DeckStrategy.AGGRO
    power = 1
    toughness = 2
    text = "Prowess"
    triggers = Triggers.PROWESS

    # instance attribute
    def __init__(self, type, cmc, cost, name, tapped, strat, power, toughness, text, triggers):
        self.type = type
        self.cmc = cmc
        self.cost = cost
        self.name = name
        self.tapped = tapped
        self.deckStrategy = strat
        self.power = power
        self.toughness = toughness
        self.text = text
        self.triggers = triggers

    def print_card(self):
        return (self.name, self.type, self.cost, "T" if self.tapped else "U", (self.power, self.toughness) if self.type == CardType.CREATURE else '')


class Player:
    # instance attribute
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.hand = []
        self.sideboard = []
        self.onThePlay = True
        self.graveyard = []
        self.exile = []
        self.board = []
        self.life = 20
        self.opponentCardsInHandKnown = []
        self.opponentCardsInDeckKnown = []


# instantiate the Player class
# Assign Decks to players here
play1 = Player("Lou")
play2 = Player("Opponent")

# Create some test cards
lightningBolt = Card(CardType.INSTANT, 1, "R", "Lightning Bolt", False, DeckStrategy.OTHER, 0, 0, "Deal 3 damage to any target", Triggers.NA)
monasterySwiftspear = Card(CardType.CREATURE, 1, "R", "Monastery Swiftspear", False, DeckStrategy.AGGRO, 1, 2, "Prowess", Triggers.PROWESS)
mountain = Card(CardType.LAND, 0, "NA", "Mountain", False, DeckStrategy.AGGRO, 0, 0, "", Triggers.NA)

llanowarElves = Card(CardType.CREATURE, 1, "G", "Llanowar Elves", False, DeckStrategy.MIDRANGE, 1, 1, "T, Add G", Triggers.NA)
forest = Card(CardType.LAND, 0, "NA", "Forest", False, DeckStrategy.MIDRANGE, 0, 0, "", Triggers.NA)
preyUpon = Card(CardType.INSTANT, 1, "G", "Prey Upon", False, DeckStrategy.MIDRANGE, 0, 0, "Target creature you control fights target creature", Triggers.NA)

# Add the cards to the deck
for i in range(0, 20):
    play1.deck.append(copy.deepcopy(lightningBolt))
    play1.deck.append(copy.deepcopy(monasterySwiftspear))
    play1.deck.append(copy.deepcopy(mountain))
    play2.deck.append(copy.deepcopy(llanowarElves))
    play2.deck.append(copy.deepcopy(forest))
    play2.deck.append(copy.deepcopy(preyUpon))

# Add cards to the sideboard here
for i in range(0, 5):
    play1.sideboard.append(copy.deepcopy(lightningBolt))
    play1.sideboard.append(copy.deepcopy(monasterySwiftspear))
    play1.sideboard.append(copy.deepcopy(mountain))
    play2.sideboard.append(copy.deepcopy(lightningBolt))
    play2.sideboard.append(copy.deepcopy(monasterySwiftspear))
    play2.sideboard.append(copy.deepcopy(mountain))


def print_player_deck(playerX):
    print(playerX.name, "'s Deck")
    print_line_break()
    for j in range(0, len(playerX.deck)):
        return playerX.deck[j].name


def print_player_sideboard(playerX):
    for k in range(0, len(playerX.sideboard)):
        print(playerX.sideboard[k].name)


def print_line_break():
    print("===============================================")


# Shuffle the decks
def shuffle_player_deck(playerX):
    print("Shuffling", playerX.name, " deck!")
    np.random.shuffle(playerX.deck)


# Put hand back into deck
def put_hand_in_deck(playerx):
    print("Shuffling hand back into deck")
    print_line_break()
    print("Hand size is ", len(playerx.hand))
    for i in range(0, len(playerx.hand)):
        playerx.deck.append(playerx.hand.pop())


# Draw opening hand
def draw_opening_hand(playerx):
    print(playerx.name, "drawing seven")
    for h in range(0, 7):
        playerx.hand.append(playerx.deck.pop())


shuffle_player_deck(play1)
shuffle_player_deck(play2)

# Put game loop here

print("PREGAME ACTIONS")
print_line_break()

# Flip coin to see who goes first, player 1 will choose for now
print("Guess heads by entering 1 or tails by entering 2 for the coin flip.")
answer = input()
answer = int(answer)
if answer == 1:
    print("You guessed heads")
elif answer == 2:
    print("You guessed tails")
else:
    print("That is not a valid response. Try again")

flip = random.choice([1,2])
if flip == 1:
    print("The coin landed on heads")
else:
    print("The coin landed on tails")
if answer == flip:
    print("Congrats! You guessed correctly! You will go first")
    play1.onThePlay = True
    play2.onThePlay = False
else:
    print("Sorry your guess was wrong. You will go second")
    play1.onThePlay = False
    play2.onThePlay = True

# Shuffle up decks
print("Shuffling decks...")
shuffle_player_deck(play1)
shuffle_player_deck(play1)
shuffle_player_deck(play2)

# Dish out opening hands
print("Each player draws their top seven cards for their opening hands")
print_line_break()

tempCardA = copy.deepcopy(llanowarElves)
tempCardB = copy.deepcopy(lightningBolt)
for h in range(0,7):
    tempCardA = play1.deck.pop()
    play1.hand.append(tempCardA)
    tempCardB = play2.deck.pop()
    play2.hand.append(tempCardB)


def print_player_hand(playerH):
    print(playerH.name,"'s hand")
    print_line_break()
    for m in range(0, len(playerH.hand)):
        print(playerH.hand[m].print_card())


print_player_hand(play1)
print_player_hand(play2)

# Keep or mulligan
print_line_break()
keeping = False
yesorno = "Y"
if play1.onThePlay:
    # Player 1 must choose first, loop through redraws until they have a hand they like
    while not keeping:
        print("Do you want to keep your hand (Y or N),", play1.name,"?")
        yesorno = input()
        if yesorno == "Y":
            keeping = True
        else: # Put cards from hand back into deck, shuffle deck, draw seven again
            put_hand_in_deck(play1)
            shuffle_player_deck(play1)
            draw_opening_hand(play1)
            print_player_hand(play1)

    keeping = False
    # Now player 2 chooses
    while not keeping:
        print("Do you want to keep your hand (Y or N),", play2.name,"?")
        yesorno = input()
        if yesorno == "Y":
            keeping = True
        else: # Put cards from hand back into deck, shuffle deck, draw seven again
            put_hand_in_deck(play2)
            shuffle_player_deck(play2)
            draw_opening_hand(play2)
            print_player_hand(play2)
else:
    while not keeping:
        print("Do you want to keep your hand (Y or N),", play2.name, "?")
        yesorno = input()
        if yesorno == "Y":
            keeping = True
        else:
            put_hand_in_deck(play2)
            shuffle_player_deck(play2)
            draw_opening_hand(play2)
            print_player_hand(play2)

    keeping = False
    # Player 1 must choose now
    while not keeping:
        print("Do you want to keep your hand (Y or N),", play1.name, "?")
        yesorno = input()
        if yesorno == "Y":
            keeping = True
        else:  # Put cards from hand back into deck, shuffle deck, draw seven again
            put_hand_in_deck(play1)
            shuffle_player_deck(play1)
            draw_opening_hand(play1)
            print_player_hand(play1)


# Now both players have hands they like, let's start the game
