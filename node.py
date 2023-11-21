import sys
import socket
import threading
import json
import time
import queue

import helpers.config as config
import helpers.counter as counter

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
Responses = queue.PriorityQueue()

def listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP_address, Port)
    server_socket.bind(server_address)

    server_socket.listen(100)  # number of accepted connections

    while True:
        client_socket, client_address = server_socket.accept()
        data = client_socket.recv(1024)
        if len(data) == 0:
            break
        if data:
            process_message(data.decode(), client_socket)
    client_socket.close()
        


def process_message(message, client):  # This is called whenever the server recieves a message
    global Responses
    # Decode message
    processed_message = json.loads(message)
    # Handle Client Requests
    if (processed_message["Type"] == "Client"):
        destination = config.service_dict[processed_message["Service"]]
        id = MessageID.inc()
        Responses.put((id, client))
        send_message(config.routing[Identifier][destination], json.dumps(
            {
                "SourceNode": Identifier,
                "DestinationNode": destination,
                "MessageID": id,
                "Type": "Request",
                "Message": processed_message["Message"]
            }
        ))
    elif (processed_message["DestinationNode"] != Identifier):
        send_message(config.routing[Identifier]
                     [processed_message["DestinationNode"]], message)
    else:
        # Handle All other requests
        if (processed_message["Type"] == "Request"):
            response = config.functions[Identifier](processed_message)
            destination = response["SourceNode"]
            response["SourceNode"] = Identifier
            response["DestinationNode"] = destination
            response["Type"] = "Response"
            send_message(config.routing[Identifier][destination], json.dumps(response))
        
        elif (processed_message["Type"] == "Response"):
            if Responses.qsize() != 0 and processed_message["MessageID"] == Responses.queue[0][0]:
                send_message("NaN", processed_message["Message"], Responses.get()[1])
            print(f"Recieved Response From {processed_message['SourceNode']}\n\tMessageID : {processed_message['MessageID']}\n\tType : {processed_message['Type']}\n\tMessage : {processed_message['Message']}")
        
        else:
            print(
                f"Unknown Request From {processed_message['SourceNode']}\n\tMessageID : {processed_message['MessageID']}\n\tType : {processed_message['Type']}\n\tMessage : {processed_message['Message']}")


def send_message(node_ID, message, client = None):
    if (node_ID == Identifier):
        process_message(message, client)
    else:
        # Don't forget to encode the message as a JSON object!
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if client != None:
            client_socket = client
        else:
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
    if (Identifier == "Node1"):
        destination = "Node4"
    elif (Identifier == "Node2"):
        destination = "Node3"
    elif (Identifier == "Node3"):
        destination = "Node2"
    else:
        destination = "Node1"

    send_message(config.routing[Identifier][destination], json.dumps(
        {
            "SourceNode": Identifier,
            "DestinationNode": destination,
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
