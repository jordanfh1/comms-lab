import socket
import json

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"NODE-01 listening on {HOST}:{PORT}")

while True:
    connection, address = server.accept()
    print (f"Connected by {address}")

    with connection:
        buffer = ""

        while True:
            data = connection.recv(1024)

            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)

                if not message:
                    continue

                telemetry = json.loads(message)

                print("\n--- TELEMETRY RECEIVED ---")
                print(f"Node:        {telemetry['node']}")
                print(f"Temperature: {telemetry['temperature']}C")
                print(f"Battery:     {telemetry['battery']}%")
                print(f"Status:      {telemetry['status']}")

            print("Connection closed. Waiting for another node...")