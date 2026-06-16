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

# handling client
def handle_client(client):
    try:
        # handling authentication
        client.sendall(b"USERNAME")
        username = client.recv(1024).decode()
        usernames[client] = username
        clients.append(client)

        print(f"connecting {username}")
        broadcast(f"{username} joined\n".encode(), client)

        while True:
            data = client.recv(1024)

            if not data:
                break

            # handling file transfer
            if data.startswith(b"FILE|"):
                broadcast(data, client)

                size = int(client.recv(1024).decode())
                broadcast(str(size).encode(), client)

                received = 0
                while received < size:
                    chunk = client.recv(min(1024, size - received))
                    if not chunk:
                        break
                    received += len(chunk)
                    broadcast(chunk, client)

            else:
                msg = f"{username}: {data.decode()}\n"
                print(msg.strip())
                broadcast(msg.encode(), client)

    except:
        pass

    remove_client(client)

# starting server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("listening...")

    while True:
        client, _ = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()