# Importation des modules
import socket
import threading
import mysql.connector

# Établir une connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sirinepupuce1",  # Changez-le par votre mot de passe MySQL
    database="mydiscord",
)

# Vérifier si la connexion a réussi
if conn.is_connected():
    print("Connexion à la base de données réussie.")

# Fonction pour insérer un utilisateur dans la base de données lors de l'inscription
def insert_user(first_name, last_name, email, password):
    cursor = conn.cursor()
    sql = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (first_name, last_name, email, password))
    conn.commit()  # Assurez-vous de commettre les modifications
    cursor.close()
    print("Utilisateur inséré dans la base de données.")

# Fonction pour gérer les connexions des clients
def handle_client(client_socket, client_address):
    print(f"[Info] {client_address} connected.")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith("REGISTER"):  # Vérifier si le message est une demande d'inscription
                    # Séparer les informations de l'utilisateur
                    _, first_name, last_name, email, password = message.split("|")
                    insert_user(first_name, last_name, email, password)  # Insérer l'utilisateur dans la base de données
                    client_socket.sendall("Inscription réussie !".encode('utf-8'))
                else:
                    print(f"[Message from {client_address}] {message}")
                    # Votre logique de gestion de chat ici...
            else:
                print(f"[Info] {client_address} disconnected.")
                break
        except ConnectionResetError:
            print(f"[Info] {client_address} forcibly disconnected.")
            break

    client_socket.close()

# Adresse IP et port du serveur
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000  # Nouveau port

# Création du socket serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen(5)

print(f"[Info] Server started with IP {SERVER_IP} on port {SERVER_PORT}.")

try:
    # Boucle d'attente des connexions des clients
    while True:
        client_socket, client_address = server.accept()
        
        # Démarrer un thread pour gérer la connexion client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

except KeyboardInterrupt:
    # Fermer la connexion à la base de données
    conn.close()
    print("Connexion à la base de données fermée.")
    print("Server stopped.")








