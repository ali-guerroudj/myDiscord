# Importation des modules
import socket
import threading
import mysql.connector

# Établir une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sirinepupuce1",  # Changez-le par votre mot de passe MySQL
    database="mydiscord"
)

# Vérifier si la connexion a réussi
if conn.is_connected():
    print("Connexion à la base de données réussie.")

# Fonction pour insérer un message dans la base de données
def insert_message(sender_address, message):
    cursor = conn.cursor()
    sql = "INSERT INTO historique (sender_address, message) VALUES (%s, %s)"
    cursor.execute(sql, (sender_address, message))
    conn.commit()  # Assurez-vous de commettre les modifications
    cursor.close()
    print(f"Message inserted into database: {message}")

# Fonction pour gérer les connexions des clients
def handle_client(client_socket, client_address):
    print(f"[Info] {client_address} connected.")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[Message from {client_address}] {message}")
                insert_message(client_address[0], message)  # Insérer le message dans la base de données
                broadcast(message)  # Diffuser le message à tous les clients
            else:
                print(f"[Info] {client_address} disconnected.")
                break
        except ConnectionResetError:
            print(f"[Info] {client_address} forcibly disconnected.")
            break

    client_socket.close()

# Fonction pour diffuser un message à tous les clients
def broadcast(message):
    for client in clients:
        try:
            client.sendall(message.encode('utf-8'))
        except:
            client.close()
            remove_client(client)

# Fonction pour retirer un client de la liste des clients
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Adresse IP et port du serveur
SERVER_IP = '127.0.0.1'
SERVER_PORT = 25565

# Création du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen(5)

print(f"[Info] Server started with IP {SERVER_IP} on port {SERVER_PORT}.")

# Liste des clients connectés
clients = []

try:
    # Boucle d'attente des connexions des clients
    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        
        # Démarrer un thread pour gérer la connexion client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

except KeyboardInterrupt:
    # Fermer la connexion à la base de données
    conn.close()
    print("Connexion à la base de données fermée.")
    print("Server stopped.")




