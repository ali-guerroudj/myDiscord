import mysql.connector
from mysql.connector import connect, Error


# Connexion à la base de données MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="conan",
    database="mydiscord",
    auth_plugin='mysql_native_password'
)

# Classe User pour gérer les utilisateurs
class User:
    def __init__(self, nom, prenom, email, mot_de_passe):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mot_de_passe = mot_de_passe

    def sign_up(self):
        cursor = mydb.cursor()
        sql = "INSERT INTO users (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)"
        val = (self.nom, self.prenom, self.email, self.mot_de_passe)
        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "utilisateur inséré.")


# Classe ChatRoom pour gérer les salons de discussion
class ChatRoom:
    def __init__(self, nom_du_salon):
        self.nom_du_salon = nom_du_salon

    def create_chat_room(self):
        cursor = mydb.cursor()
        sql = "INSERT INTO channels (nom_du_salon) VALUES (%s)"
        val = (self.nom_du_salon,)
        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "salon créé.")


# Classe Message pour gérer les messages dans les salons
class Message:
    def __init__(self, utilisateur_id, salon_id, message):
        self.utilisateur_id = utilisateur_id
        self.salon_id = salon_id
        self.message = message

    def send_message(self):
        cursor = mydb.cursor()
        sql = "INSERT INTO messages (utilisateur_id, salon_id, message) VALUES (%s, %s, %s)"
        val = (self.utilisateur_id, self.salon_id, self.message)
        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "message envoyé.")


# Exemple d'utilisation
if __name__ == "__main__":
    # Créer un nouvel utilisateur
    new_user = User("John", "Doe", "john@example.com", "motdepasse123")
    new_user.sign_up()

    # Créer un nouveau salon de discussion
    new_chat_room = ChatRoom("General")
    new_chat_room.create_chat_room()

    # Envoyer un message dans le salon de discussion
    new_message = Message(1, 1, "Bonjour tout le monde !")
    new_message.send_message()

    # Fermer la connexion à la base de données
    mydb.close()
