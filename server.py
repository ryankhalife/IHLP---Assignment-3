import random
import socket
import pickle

CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
HOST = 'localhost'
PORT = 5000

clients_hands = [CARD_VALUES.copy() for _ in range(3)]

server_hand = CARD_VALUES.copy()
random.shuffle(server_hand)

score = [[0 for _ in range(3)] for _ in range(14)]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(3)

print('\nServer is listening...\n')

clients_sockets = []
for i in range(3): #Sending cards to clients
    client_socket, client_address = server_socket.accept()
    clients_sockets.append(client_socket)
    print('Client', i+1, 'connected')
    client_socket.send(str(clients_hands[i]).encode())

print('\nGame Started')

for i in range(1, 14): #Playing the game
    server_card = server_hand.pop()
    clients_cards = []
 
    for client_socket in clients_sockets: #Getting clients cards
        client_socket.send(str(server_card).encode())
        try:
            client_card = int(client_socket.recv(1024).decode())
        except ValueError as e:
            client_card = -1
        while client_card not in clients_hands[clients_sockets.index(client_socket)]:
            client_socket.send('Invalid card'.encode())
            try:
                client_card = int(client_socket.recv(1024).decode())
            except ValueError as e:
                client_card = -1
        clients_cards.append(client_card)
        clients_hands[clients_sockets.index(client_socket)].remove(client_card)

    winners = [i for i, x in enumerate(clients_cards) if x == max(clients_cards)]
    winners_str = ', '.join(['Client ' + str(winner + 1) for winner in winners])

    for client_socket in clients_sockets: #Sending round information to clients
        data = pickle.dumps([server_card, clients_cards[0], clients_cards[1], clients_cards[2], winners_str, clients_hands[clients_sockets.index(client_socket)]])
        client_socket.send(data)

    for j in range(3): #Updating score card
        if j in winners:
            score[i][j] = score[i-1][j] + server_card
        else:
            score[i][j] = score[i-1][j]

    #Printing current scores to server
    print('\n','-' * 20, '\n')
    print('Round', i)
    for j in range(3):
        print('Client', j+1, 'score:', score[i][j])

#Getting winner(s) and sending to clients
winners = [i for i, x in enumerate(score[13]) if x == max(score[13])]
winners_str = ', '.join(['Client ' + str(winner + 1) for winner in winners])
for client_socket in clients_sockets:
    client_socket.send(winners_str.encode())





        


    

