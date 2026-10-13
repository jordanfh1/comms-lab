import socket
import json
import threading
import time

HOST = "127.0.0.1"
PORT = 5000
HEARTBEAT_TIMEOUT = 10

def handle_node(connection, address):
    node_id = None
    last_heartbeat = None
    offline_reported = None
    buffer = ""

    connection.settimeout(1)

    print(f"Connection opened: {address}")

    try:
        with connection:
            while True:
                try:
                    data = connection.recv(1024)
                except socket.timeout:
                    data = None

                if data == b"":
                    break

                if data:
                    buffer += data.decode("utf-8")

                    while "\n" in buffer:
                        raw_message, buffer = buffer.split("\n", 1)

                        if not raw_message:
                            continue

                        message = json.loads(raw_message)
                        node_id = message.get("node", "UNKNOWN")
                        message_type = message.get("type")
                        
                        if message_type == "heartbeat":
                            last_heartbeat = time.monotonic()

                            if offline_reported:
                                print(f"{node_id} is ONLINE again")

                            offline_reported = False
                            print(
                                f"{node_id}: heartbeat "
                                f"#{message.get('sequence', '?')}"
                            )

                        elif message_type == "telemetry":
                            print(
                                f"{node_id}: "
                                f"{message['temperature']}°C, "
                                f"battery {message['battery']}%, "
                                f"status {message['status']}"
                            )

                if last_heartbeat is not None:
                    elapsed = time.monotonic() - last_heartbeat

                    if elapsed > HEARTBEAT_TIMEOUT and not offline_reported:
                        print(
                            f"WARNING: {node_id} OFFLINE "
                            f"(no heartbeat for {elapsed:.1f}s)"
                        )
                        offline_reported = True

    except (ConnectionResetError, json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"Connection error from {address}: {error}")

    finally:
        print(f"{node_id or address} disconnected")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"NODE-01 listening on {HOST}:{PORT}")

try:
    while True:
        connection, address = server.accept()

        thread = threading.Thread(
            target=handle_node,
            args=(connection, address),
            daemon=True
        )
        thread.start()

except KeyboardInterrupt:
    print("\nNODE-01 shutting down.")

finally:
    server.close()
