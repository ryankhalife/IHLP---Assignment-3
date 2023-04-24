import pickle
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

print('\nConnected to server\n')

client_hand = client_socket.recv(1024).decode()
print('Your hand is:', client_hand, '\n')

for i in range(1, 14):
    server_msg = client_socket.recv(1024).decode()
    
    print('The server advertised card ({:s}, Spades)' .format(server_msg))
    client_card = input('Play a card: ')
    client_socket.send(client_card.encode())

    server_msg = client_socket.recv(4096)
    try:
        server_msg = server_msg.decode()
    except UnicodeDecodeError as e:
        data =  pickle.loads(server_msg)
        

    while server_msg == 'Invalid card':
        print(server_msg)
        client_card = input('Play a card: ')
        client_socket.send(client_card.encode())
        server_msg = client_socket.recv(4096)
        try:
            server_msg = server_msg.decode()
        except UnicodeDecodeError as e:
            data =  pickle.loads(server_msg)

    print('\n', '-' * 20,'\n')
    print('The server advertised card ({:d}, Spades)' .format(data[0]))
    print('Client 1 sent card ({:d}, Hearts)' .format(data[1]))
    print('Client 2 sent card ({:d}, Diamonds)' .format(data[2]))
    print('Client 3 sent card ({:d}, Clubs)' .format(data[3]))
    print('Round winner(s):', data[4], '\n')
    print('-' * 20,'\n')

    if i != 13:
        print('Your hand is:', data[5], '\n')

winners_str = client_socket.recv(1024).decode()
print('Game over')
print('Winner(s):', winners_str)

 
   