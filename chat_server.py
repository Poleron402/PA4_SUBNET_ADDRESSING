#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "OtterAI"
__credits__ = [
    "Anthony Suvorov",
    "Aryeh Freud",
    "Eric Rodriguez",
    "Polina Mejia"
]

import socket
import threading
# Configure logging
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
server_port = 12000
clients = {}  # dictionary to store client sockets
# global client_counter
def connection_handler(connection_socket, addr):
    while True:  # loop to handle client messages
        try:
            message = connection_socket.recv(1024).decode()  # receive message from client
            if not message:
                break
            if message == "bye":  # if client sends 'bye', close connection
                # Inform other client and close connection
                exit_message = message+"\n"+clients[connection_socket]+" has left the chat."

                for client in clients.keys():  # loop through clients
                    if client != connection_socket:  # if client is not the one leaving
                        client.send(exit_message.encode())  # send exit message
                connection_socket.close()  # close connection
                # remove client from clients dictionary - prevents server from sending to a client that has left
                clients.pop(connection_socket)
                break
            else:
                # Forward the message to the other client with the client's name
                message_to_send = str(clients[connection_socket])+": " + message
                for client in clients.keys():  # loop through clients
                    if client != connection_socket:  # if client is not the one sending the message
                        client.send(message_to_send.encode())  # send message
        #If there is an issue with a client, we inform the user and remove the client from list, closing the socket
        except Exception as e:
            log.error("Error handling client "+ clients[connection_socket]+": "+str(e))
            connection_socket.close()
            clients.pop(connection_socket)
            break
    connection_socket.close()


def main():
    #setting up a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(3)  # Allow two clients
    print("Server is ready to receive on port", server_port)
    #client counter needed to assign names X and Y depending on when they were connected to server
    client_counter = 0
    
    while True:
        #try except to handle unexpected errors
        try:
            #accepting connections to the server sockets, incrementing the count and assigning usernames
            connection_socket, address = server_socket.accept()
            username = connection_socket.recv(1024)
            clients[connection_socket] = username.decode()
            log.info(f"Connected to {username.decode()} at {address}") # set client id
            #  start thread to handle client
            client_thread = threading.Thread(target=connection_handler, args=(connection_socket, address))
            client_thread.start()
        except OSError:
            break
    #had trouble getting to this part of the code, 
    server_socket.close()
    log.info("Server has been shut down")
        
        
    # server_socket.close()
if __name__ == "__main__":
    main()
