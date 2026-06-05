import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clients = []
usernames = {}

# broadcasting data
def broadcast(data, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(data)
            except:
                remove_client(client)

# removing client
def remove_client(client):
    if client in clients:
        print(f"disconnecting {usernames[client]}")
        clients.remove(client)
        del usernames[client]
        client.close()

