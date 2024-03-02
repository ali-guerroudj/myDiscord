import socket
import threading
import mysql.connector
from mysql.connector import Error

# Connexion à la base de données MySQL
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="conan",
        database="mydiscord",
        auth_plugin='mysql_native_password'
    )
    print("Connecté à la base de données MySQL")
except Error as e:
    print(f"Erreur lors de la connexion à MySQL: {e}")

# Fonction pour diffuser un message à tous les clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Fonction pour gérer les messages des clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            surnom = surnoms[clients.index(client)]
            print(f"{surnom} dit : {message.decode('utf-8')}")
            broadcast(f"{surnom} dit : {message}".encode("utf-8"))

            # Sauvegarde du message dans la base de données
            cursor = db_connection.cursor()
            sql_insert_query = "INSERT INTO messages (utilisateur_id, salon_id, message) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert_query, (1, 1, message.decode('utf-8')))  # Remplacez 1, 1 par les vrais ID utilisateur et salon
            db_connection.commit()
            cursor.close()

        except:
            index = clients.index(client)
            clients.remove(client)
            surnom = surnoms[index]
            surnoms.remove(surnom)
            break  

# Fonction pour recevoir les connexions des clients
def recevoir():
    while True:
        client, address = server.accept()
        print(f"Connecté avec {str(address)}")

        client.send("SURNOM".encode("utf-8"))
        surnom = client.recv(1024)

        surnoms.append(surnom)
        clients.append(client)

        print(f"Surnom du client : {surnom}")
        broadcast(f"{surnom} connecté au serveur\n".encode("utf-8"))
        client.send("Connecté au serveur".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("En attente de connexion ...")

HOST = '127.0.0.1'
PORT = 45678

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
surnoms = []

recevoir()