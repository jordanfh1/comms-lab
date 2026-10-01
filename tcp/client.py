import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

weather = "Temp: 21.4C, Wind: 13MPH, Rain: false, Sun: Bright"

message = "Hello from NODE-02, "
client.sendall(message.encode() + weather.encode())

client.close()