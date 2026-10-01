import socket
import json
import time
import random

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("NODE-02 connected. Sending telemetry...")

temperature = 24.7
battery = 91.0

try:
    while True:
        # Simulate changing sensor readings
        temperature += random.uniform(-0.3, 0.3)
        battery = max(0, battery - 0.01)

        telemetry = {
            "type": "telemetry",
            "node": "NODE-02",
            "temperature": round(temperature, 2),
            "battery": round(battery, 2),
            "status": "BAD"
        }

        message = json.dumps(telemetry) + "\n"
        client.sendall(message.encode())

        print(f"Sent: {message.strip()}")

        time.sleep(3)

except KeyboardInterrupt:
    print("\nNODE-02 stopping...")

finally:
    client.close()
    print("Disconnected.")