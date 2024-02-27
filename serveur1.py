import socket
import threading

HOST = '127.0.0.1'
PORT = 45678

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((HOST, PORT)) # On passe un tuple avec nos informations

server.listen() # on n'autorise la connexion simultanées sur le serveur 

clients = []
surnoms = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            surnom = surnoms[clients.index(client)]
            print(f"{surnom} dit : {message.decode('utf-8')}")
            broadcast(f"{surnom} dit : {message}".encode("utf-8"))

        except:
            index = clients.index(client)
            clients.remove(client)
            surnom = surnoms[index]
            surnoms.remove(surnom)
            break  

def recevoir():
    while True:
        client , adress = server.accept()
        print(f"Connecté avec {str(adress)}")

        client.send("SURNOM".encode("utf-8")) # le encode(utf-8) signifie qu'on veux convertir les donnees envoyeez en bits pour qu'elles soient lisible pour nous.
        surnom = client.recv(1024)

        surnoms.append(surnom)
        clients.append(client)

        print(f"Surnom du client : {surnom}")
        broadcast(f"{surnom} \n".encode("utf-8"))
        client.send("".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("En attente de connexion ...") 
recevoir()
