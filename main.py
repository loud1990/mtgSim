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


class GameState(enum.Enum):
    UNTAP = 0
    UPKEEP = 1
    DRAW = 2
    MAIN1 = 3
    BEGINCOMBAT = 4
    DECLAREATTACKERS = 5
    DECLAREBLOCKERS = 6
    FIRSTSTRIKEDAMAGE = 7
    COMBATDAMAGE = 8
    ENDCOMBAT = 9
    MAIN2 = 10
    ENDTURN = 11
    CLOSING = 12


class Card:
    '''
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
    id = 0
    '''
    # instance attribute
    def __init__(self, type, cmc, cost, name, tapped, strat, power, toughness, text, triggers, score):
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
        self.score = score

    def print_card(self):
        return (self.name, self.type, self.cost, "T" if self.tapped else "U",
                (self.power, self.toughness) if self.type == CardType.CREATURE else '', self.text)


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
        self.spellList = []
        self.life = 20
        # Set mana in mana pool to 0 for each color
        self.R = 0
        self.W = 0
        self.U = 0
        self.B = 0
        self.G = 0
        self.C = 0
        self.opponentCardsInHandKnown = []
        self.opponentCardsInDeckKnown = []

    def draw_card(self):
        self.hand.append(self.deck.pop())


# instantiate the Player class
# Assign Decks to players here
play1 = Player("Lou")
play2 = Player("Opponent")

# Create some test cards
lightningBolt = Card(CardType.INSTANT, 1, "R", "Lightning Bolt", False, DeckStrategy.OTHER, 0, 0,
                     "Deal 3 damage to any target", Triggers.NA, 0)
monasterySwiftspear = Card(CardType.CREATURE, 1, "R", "Monastery Swiftspear", False, DeckStrategy.AGGRO, 1, 2,
                           "Prowess", Triggers.PROWESS, 0)
mountain = Card(CardType.LAND, 0, "NA", "Mountain", False, DeckStrategy.AGGRO, 0, 0, "", Triggers.NA, 0)

llanowarElves = Card(CardType.CREATURE, 1, "G", "Llanowar Elves", False, DeckStrategy.MIDRANGE, 1, 1, "T, Add G",
                     Triggers.NA, 0)
forest = Card(CardType.LAND, 0, "NA", "Forest", False, DeckStrategy.MIDRANGE, 0, 0, "", Triggers.NA, 0)
preyUpon = Card(CardType.INSTANT, 1, "G", "Prey Upon", False, DeckStrategy.MIDRANGE, 0, 0,
                "Target creature you control fights target creature", Triggers.NA, 0)

# Add the cards to the deck
# These ids will keep track of the cards in each player's deck as the game goes along
playid1 = 0
playid2 = 0
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

flip = random.choice([1, 2])
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
for h in range(0, 7):
    tempCardA = play1.deck.pop()
    play1.hand.append(tempCardA)
    tempCardB = play2.deck.pop()
    play2.hand.append(tempCardB)


def print_player_hand(playerH):
    print(playerH.name, "'s hand")
    print_line_break()
    for m in range(0, len(playerH.hand)):
        print(m, playerH.hand[m].print_card())


print_player_hand(play1)
print_player_hand(play2)

# Keep or mulligan
print_line_break()
keeping = False
yesorno = "Y"
if play1.onThePlay:
    # Player 1 must choose first, loop through redraws until they have a hand they like
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

    keeping = False
    # Now player 2 chooses
    while not keeping:
        print("Do you want to keep your hand (Y or N),", play2.name, "?")
        yesorno = input()
        if yesorno == "Y":
            keeping = True
        else:  # Put cards from hand back into deck, shuffle deck, draw seven again
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

# How to keep track of game state, which player's turn, which player has priority, which phase of turn are we in, life
# totals, cards in hand, gy, ex, board state, triggers

# Set turn to player who is OnThePlay
# Player does not get to draw a card on the first turn of the game
firstTurn = True
gameNumber = 1
playerTurn = play1
if play2.onThePlay:
    playerTurn = play2

# Calculate deck mana requirements here for each player
# Calulate knowledge each player has of the other player's deck here if it's not game 1

def untapAll(plyr):
    for i in range(0, len(plyr.board)):
        plyr.board[i].tapped = False


def empty_mana(plyr):
    plyr.C = 0
    plyr.W = 0
    plyr.U = 0
    plyr.B = 0
    plyr.R = 0
    plyr.G = 0


def tap_all_lands(plyr):
    for i in range(0, len(plyr.board)):
        if plyr.board[i].type == CardType.LAND:
            print("Choose what type of mana to produce")


def print_battlefield(plyr1, plyr2):
    print_line_break()
    print(plyr1.name, "Battlefield")
    print_line_break()
    for obj in range(0, len(plyr1.board)):
        print(obj, plyr1.board[obj].name)

    print_line_break()
    print(plyr2.name, "Battlefield")
    print_line_break()
    for obj2 in range(0, len(plyr2.board)):
        print(plyr2.board[obj2].name)


def takeTurn(plyr1, plyr2, firstturn):

    empty_mana(plyr1)
    gmState = GameState.UNTAP
    # for every card on the board on this player's side, untap it
    untapAll(plyr1)

    gmState = GameState.UPKEEP
    # Search board for upkeep triggers, perform them

    gmState = GameState.DRAW
    # Draw a card if it isn't the first turn of the game
    if not firstturn:
        plyr1.draw_card()
    firstturn = False
    empty_mana(plyr1)

    gmState = GameState.MAIN1
    # Now we are able to play lands from our hand
    # Later, we will try to figure out what cards, deck, the opponent is playing/has in hand
    # Later, we will determine the optimal card to play first before deciding which land to play
    # We will also factor in the color requirements of the deck, such as RRW by turn 3
    # Present player with options 1: play a land - get list of all lands in hand with numbered options, take key input
    # 2 Tap a land for mana - get list of lands on board with numbered options, take key input
    # 3 Play a spell - get list of spells in hand with numbered options, take key input, check if player has enough mana
    # to pay for the spell
    # Options: 1 Play land 2 Cast spell 3 Move to combat
    print_battlefield(play1, play2)
    landPlayed = False
    playerAction = 98
    while not playerAction == 3:
        playerAction = int(input("What would you like to do? 1 Play land 2 Cast spell 3 Move to combat 4 tap land for mana"))
        if playerAction == 1:
            if landPlayed:
                print("You may only play one land per turn")
            else:
                print("Open up land options menu, then continue")
                print_player_hand(plyr1)
                landPicked = False
                while not landPicked:
                    landSelection = int(input("Which land would you like to play? Press 99 to cancel"))
                    if landSelection == 99:
                        break
                    for i in range(0, len(plyr1.hand)):
                        if landSelection == i:
                            if plyr1.hand[i].type == CardType.LAND:
                                plyr1.board.append(plyr1.hand.pop(i))
                                landPicked = True
                                landPlayed = True
                                break
                            else:
                                print("That is not a valid choice, try again")
                                break

        elif playerAction == 2:
            print("Open up spell cast options menu, then continue")
        elif playerAction == 3:
            print("Move on to combat")
        elif playerAction == 4:
            print("Tap lands for mana")
            print_battlefield(plyr1, plyr2)
            print("W:", plyr1.W, "U:", plyr1.U, "B:", plyr1.B, "R:", plyr1.R, "G:", plyr1.G, "C:", plyr1.C)
            landChoice = int(input("Press 99 to tap all lands, or press the land number to tap a single land:"))
            if landChoice == 99:
                tap_all_lands(plyr1)
            else:
                for i in range(0, len(plyr1.board)): # Check if choice is a land, check if land is tapped already, otherwise tap it and give the player the necessary mana
                    if plyr1.board[i].type == CardType.LAND:
                        if plyr1.board[i].tapped:
                            print("This land is already tapped!")
                        else:
                            plyr1.board[i].tapped = True
                            plyr1.R += 1
                    else:
                        print("This is not a valid land choice")



    print_battlefield(play1, play2)
    print_player_hand(play1)
    gmState = GameState.BEGINCOMBAT
    empty_mana(plyr1)

# We will turn our game into a loop later on
# def game_loop(plyr1, plyr2, gameNum):
takeTurn(play1, play2, True)
