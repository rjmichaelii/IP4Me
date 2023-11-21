import socket
import json
import os 

from helpers.config import Nodes, services, service_dict

def getResponse(service, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(Nodes[service_dict[service]])

    client_socket.send(json.dumps(
        {
            "Type": "Client",
            "Service" : service,
            "Message": message
        }
    ).encode())

    data = client_socket.recv(1024).decode()

    client_socket.close()

    return data



def main(): 
    print_main_screen()
    handle_input()

def print_main_screen():
    clear_screen()
    print("-" * 50)
    print("Domain Client Application".center(50))
    print("Select from the following options".center(50))
    print("-" * 50)
    print(f"""1) Get Random Number
2) Lowercase your text
3) Uppercase your text
4) Get Random String
5) Exit""")
    print("-" * 50)

def handle_input():
    # Exception handling loop
    while True:
        try:
            user_input = int(input("Enter your choice (1-5): "))
            if user_input < 1 or user_input > 5:
                print("Error: Please enter a number between 1 and 5.")
            elif user_input == 5:
                print("Exiting program.")
                break
            else:
                clear_screen()
                getInput(services[user_input - 1])
                #break 
        except ValueError:
            print("Invalid input, please enter a number.")

def clear_screen():
    # Clear the screen based on the operating system
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for macOS and Linux
        os.system('clear')

def getInput(option_name):
    while True:
        if option_name == "Lowercase" or option_name == "Uppercase":
            user_input = input("Enter some text or '.' to return\n")
            if user_input == ".":
                break
            else:
                print(getResponse(option_name, user_input))
        elif option_name == "RandNum":
            user_input = input("Get random number? [Y/N]")
            if user_input.lower() == "y":
                print(getResponse(option_name, " "))
            else:
                break
        else:
            user_input = input("Get random String? [Y/N]")
            if user_input.lower() == "y":
                print(getResponse(option_name, " "))
            else:
                break
    clear_screen()
    print_main_screen()

if __name__ == "__main__":
    main()