import pygame
from network import Network
import json

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kings Cup Client")

meaning = {
    "Ace": "Waterfall",
    2: "You",
    3: "Me",
    4: "Women",
    5: "Drive",
    6: "Men",
    7: "Heaven",
    8: "Date",
    9: "Rhyme",
    10: "Categories",
    "Jack": "Social",
    "Queen": "Questions",
    "King": "Kings Cup"
}

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Aerial", 30)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, CardDeck, p):
    win.fill((128, 128, 128))

    if not (CardDeck.connected()):
        font = pygame.font.SysFont("Aerial", 60)
        text = font.render("No other players connected yet", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        checkAgain.draw(win)
    else:
        font = pygame.font.SysFont("Aerial", 40)
        text = font.render("Kings Cup", 1, (0, 255, 255))
        win.blit(text, (250, 150))

        font2 = pygame.font.SysFont("Aerial", 20)
        # get clubs
        clubs = font2.render(f"Clubs: {json.dumps(CardDeck.pulled['Clubs'])}", 1, (0, 255, 255))
        win.blit(clubs, (20, 80))
        # get spades
        spades = font2.render(f"Spades: {json.dumps(CardDeck.pulled['Spades'])}", 1, (0, 255, 255))
        win.blit(spades, (20, 100))
        # get hearts
        hearts = font2.render(f"Hearts: {json.dumps(CardDeck.pulled['Diamonds'])}", 1, (0, 255, 255))
        win.blit(hearts, (20, 120))
        # get diamonds
        diamonds = font2.render(f"Diamonds: {json.dumps(CardDeck.pulled['Hearts'])}", 1, (0, 255, 255))
        win.blit(diamonds, (20, 140))

        font3 = pygame.font.SysFont("Aerial", 20)
        card_deck = font3.render(f"Game id: {CardDeck.id}", 1, (255, 0, 0))
        win.blit(card_deck, (290, 40))

        last_card = font.render(f"last card played: {CardDeck.last_played}", 1, (0, 255, 255))
        win.blit(last_card, (200, 350))

        if CardDeck.last_played:
            font4 = pygame.font.SysFont("Aerial", 60)
            card_meaning = font4.render(meaning[list(CardDeck.last_played.values())[0]], 1, (0, 255, 255))
            win.blit(card_meaning, (250, 250))

        if CardDeck.whoWent is None:
            move = CardDeck.whosTurn()
            if p == move:
                go_text = font.render(f"Your Pull", 1, (0, 255, 255))
                win.blit(go_text, (300, 400))
                btn.draw(win)
            else:
                wait_text = font.render(f"Waiting for player {move} to pull", 1, (0, 255, 255))
                win.blit(wait_text, (300, 400))

    pygame.display.update()


btn = Button("Pull Card", 50, 500, (0, 0, 0))

checkAgain = Button("Check Again", 50, 500, (0, 0, 0))


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            cardDeck = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if cardDeck.connected():
            redrawWindow(win, cardDeck, player)
            pygame.time.delay(500)
            try:
                if cardDeck.deckEmpty():
                    cardDeck = n.send("reset")
                else:
                    cardDeck = n.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Aerial", 20)
            text = font.render(f"Game id: {cardDeck.id}", 1, (255, 0, 0))
            win.blit(text, (290, 40))

            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                font2 = pygame.font.SysFont("Aerial", 30)
                if cardDeck.myTurn(player):
                    if btn.click(pos) and cardDeck.connected():
                        n.send("pull_card")
                        card_pulled = cardDeck.last_played
                        card_text = font2.render(json.dumps(card_pulled), 1, (0, 255, 255))
                        print(card_pulled)
                        win.blit(card_text, (250, 400))



                else:
                    n.send("get")

                if checkAgain.click(pos) and cardDeck.connected():
                    n.send("get")


        redrawWindow(win, cardDeck, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("Aerial", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (200, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("quit")
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
