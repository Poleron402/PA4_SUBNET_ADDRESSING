#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "OtterAI"
__credits__ = [
    "Anthony Suvorov",
    "Aryeh Freud",
    "Eric Rodriguez",
    "Polina Mejia"
]

import socket as s
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.0.1'
server_port = 12000

# the function below is a thread that listens for messages from the server
def receive_messages(client_socket):
    while True:
        # receive server response
        server_response = client_socket.recv(1024)  
        # if server has closed the connection
        if not server_response:
            break
        # Decode server response from UTF-8 bytestream
        server_response_decoded = server_response.decode()
        # print server response
        print(server_response_decoded)  

def main():
    # Create socket 
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    try:
        # Establish TCP connection and send a username as a starting message
        username = input("Enter username: ")
        client_socket.connect((server_name, server_port))
        client_socket.send(username.encode())
    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")

    # Start the thread for receiving messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    # Welcome prompt
    print("Welcome to the chat, "+username+"\nTo send a message, type the message and click enter.")
    print("Input lowercase sentence: ")

    try:
        while True:
            # get user input
            user_input = input()  
            # Set data across socket to server
            client_socket.send(user_input.encode())
            # if user input is 'bye', break the loop
            if user_input.lower() == "bye":  
                print("\nDisconnecting from chat...\n")
                break
    # handle exception
    except Exception as e:
        log.exception("Error sending message: {}".format(e))
    finally:
        # Close socket prior to exit
        client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
