import sys
import socket
import threading
import json
import time


# Airport Name, Port, Conn1Name, Conn1Port, Conn2Name. . . 
if len(sys.argv) < 4: 
    print ("Correct usage: IP, Port, HubID, Connection1IP, Connection1Port, Connection1ID, Connection2IP, Connection2Port, Connection2ID,...")
    exit()


IP_address = sys.argv[1]
Port = int(sys.argv[2]) 
Identifier = sys.argv[3] # ID = IATA


# Process cmd Args
connection_lookup = {}
connection_list = []
for i in range(4, len(sys.argv), 3):
    connection_list.append((sys.argv[i], int(sys.argv[i + 1]), sys.argv[i + 2]))
    connection_lookup[sys.argv[i + 2]] = (sys.argv[i], int(sys.argv[i + 1]))


# Process incoming connections
def listen():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (IP_address, Port)
        server_socket.bind(server_address)

        server_socket.listen(100) # number of accepted connections

        while True:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024)
            if data:
                process_message(data.decode())
                client_socket.close()
                    

server_thread = threading.Thread(target=listen, daemon=True)
server_thread.start()


def process_message(message): # This is called whenever the server recieves a message
    # Decode message
    processed_message = json.loads(message)
    print(processed_message["message"])


def send_message(destination_IP, destination_port, message): 
    # Don't forget to encode the message as a JSON object!
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((destination_IP, destination_port))
    client_socket.sendall(message.encode())


print(IP_address, " at ", Port, " is Online as ", Identifier)
# Wait for other threads to start
time.sleep(0.5)


# send some messages
for connection in connection_list:
    send_message(connection[0], connection[1], json.dumps({"message": f"Hello from {Identifier}"}))


# Keep window alive
while(True):
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Closing Program")
        sys.exit(0)








 


 

