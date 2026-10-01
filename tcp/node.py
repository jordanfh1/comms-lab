import socket

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"NODE-01 listening on {HOST}:{PORT}")

connection, address, = server.accept()

print(f"Connection received from {address}")

while True:
    data = connection.recv(1024)

    if not data:
        break 

    print(f"Received: {data.decode()}")

    connection.close()