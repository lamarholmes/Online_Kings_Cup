import socket
from _thread import *
import pickle
from CardDeck import CardDeck

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = set()
games = {}
idCount = 0

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Great! Server is started and waiting for someone to connect")


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.newGame()
                    elif data != "get":
                        game.pull()
                        game.clearWent()
                        game.whosTurn()

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount -1)//2
    if idCount % 2 == 1:
        games[gameId] = CardDeck(gameId)
        games[gameId].players.append(p)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p += 1
        games[gameId].players.append(p)

    start_new_thread(threaded_client, (conn, p, gameId))
