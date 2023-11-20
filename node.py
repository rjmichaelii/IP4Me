import sys
import socket
import threading
import json
import time
import config
import counter

# Process CMD Argument
if len(sys.argv) < 2:
    print("Correct usage: HubID")
    exit()

# Get Node Info
IP_address = config.Nodes[sys.argv[1]][0]
Port = config.Nodes[sys.argv[1]][1]
Identifier = sys.argv[1]

# Message Counter
MessageID = counter.AtomicCounter()


def listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP_address, Port)
    server_socket.bind(server_address)

    server_socket.listen(100)  # number of accepted connections

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024)
        if data:
            process_message(data.decode())
            client_socket.close()


def process_message(message):  # This is called whenever the server recieves a message
    # Decode message
    processed_message = json.loads(message)
    print(processed_message)
    if (processed_message["NodeID"] != Identifier):
        send_message(config.routing[Identifier]
                     [processed_message["NodeID"]], message)


def send_message(node_ID, message):
    if (node_ID == Identifier):
        process_message(message)
    else:
        # Don't forget to encode the message as a JSON object!
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(config.Nodes[node_ID])
        client_socket.sendall(message.encode())


# Start thread for recieving TCP Server
server_thread = threading.Thread(target=listen, daemon=True)
server_thread.start()

# Announce that server is started
print(IP_address, " at ", Port, " is Online as ", Identifier)

# Wait for other Nodes to start
time.sleep(0.5)
try:
    # send some messages
    destination = "Node4"
    send_message(config.routing[Identifier][destination], json.dumps(
        {
            "NodeID": destination,
            "MessageID": MessageID.inc(),
            "Type": "Request",
            "Message": f"Hello from {Identifier}"
        }
    ))
except Exception as e:
    print("ERROR", e)

# Keep window alive
while (True):
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Closing Program")
        sys.exit(0)
