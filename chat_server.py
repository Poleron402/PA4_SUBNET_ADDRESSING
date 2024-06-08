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
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
server_port = 12000
clients = {}

def connection_handler(connection_socket, addr):
    while True:
        try:
            message = connection_socket.recv(1024).decode()
            if not message:
                break
            if message == "bye":
                exit_message = message + "\n" + clients[connection_socket] + " has left the chat."
                for client in clients.keys():
                    if client != connection_socket:
                        client.send(exit_message.encode())
                connection_socket.close()
                clients.pop(connection_socket)
                break
            else:
                message_to_send = str(clients[connection_socket]) + ": " + message
                for client in clients.keys():
                    if client != connection_socket:
                        client.send(message_to_send.encode())
        except Exception as e:
            log.error("Error handling client " + clients[connection_socket] + ": " + str(e))
            connection_socket.close()
            clients.pop(connection_socket)
            break

    connection_socket.close()

    # Check if all clients have disconnected
    if not clients:
        server_shutdown_event.set()

def main():
    global server_shutdown_event
    server_shutdown_event = threading.Event()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(3)
    print("Server is ready to receive on port", server_port)

    while True:
        if server_shutdown_event.is_set():
            break
        try:
            server_socket.settimeout(1.0)
            try:
                connection_socket, address = server_socket.accept()
            except socket.timeout:
                continue
            username = connection_socket.recv(1024)
            clients[connection_socket] = username.decode()
            log.info(f"Connected to {username.decode()} at {address}")
            client_thread = threading.Thread(target=connection_handler, args=(connection_socket, address))
            client_thread.start()
        except OSError:
            break

    server_socket.close()
    log.info("Server has been shut down")

if __name__ == "__main__":
    main()
