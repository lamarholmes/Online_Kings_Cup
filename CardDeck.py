import random
import json


class CardDeck:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.players = []
        self.whoWent = None
        self.last_played = None
        self.pulled = {
            'Clubs': [],
            'Spades': [],
            'Diamonds': [],
            'Hearts': []
        }
        self.deck = {
            'Clubs': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
            'Spades': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
            'Diamonds': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace'],
            'Hearts': [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']
        }

    def pull(self):
        card = {}
        house = random.choice(list(self.deck.keys()))
        card[house] = random.choice(self.deck[house])
        while card[house] in self.pulled[house]:
            card[house] = random.choice(self.deck[house])
        self.pulled[house].append(card[house])
        self.last_played = card
        return card

    def deckEmpty(self):
        if len(self.pulled['Clubs']) == 13 and len(self.pulled['Spades']) == 13 and len(self.pulled['Diamonds']) == 13 and len(self.pulled['Hearts']) == 13:
            return True
        return False

    def connected(self):
        return self.ready

    def addPlayer(self, playerid):
        self.players.append(playerid)

    def whosTurn(self):
        turn = self.players[0]
        self.players.append(turn)
        self.players.pop(0)
        return turn

    def myTurn(self, playerid):
        player_up = self.players[0]
        if playerid == player_up:
            return True
        return False

    def newGame(self):
        self.pulled = {
            'Clubs': [],
            'Spades': [],
            'Diamonds': [],
            'Hearts': []
        }

    def cardPlayed(self, playerid):
        self.whoWent = playerid

    def clearWent(self):
        self.whoWent = None

    def load_card(self, card):
        self.pulled.update(card)
