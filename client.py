import socket
import json

from helpers.config import IP, PORT, Nodes, services


while True:
    message = input("Enter a message to send to the server or . to quit\n")

    if message == ".":
        break
        
    temp = json.dumps(
        {
            "Type": "Client",
            "Service" : services[1],
            "Message": message
        }
    )
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (IP, PORT + 1)
    client_socket.connect(server_address)

    client_socket.send(temp.encode())

    data = client_socket.recv(1024).decode()
    print("Recieved :", data)

client_socket.close()