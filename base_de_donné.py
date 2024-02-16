import mysql.connector

class ChatDatabase:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user="root",
            password="wxop45az",
            database="mydiscord"
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        # Crée la table pour stocker les messages
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def insert_message(self, user_id, content):
        # Insère un message dans la table
        self.cursor.execute("""
            INSERT INTO messages (user_id, content)
            VALUES (%s, %s)
        """, (user_id, content))
        self.connection.commit()

    def get_messages(self, limit=10):
        # Récupère les derniers messages
        self.cursor.execute("""
            SELECT user_id, content, timestamp
            FROM messages
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        # Ferme la connexion à la base de données
        self.cursor.close()
        self.connection.close()

# Exemple d'utilisation
if __name__ == "__main__":
    db = ChatDatabase(host="localhost", user="root", password="wxop45az", database="mydiscord")
    db.create_table()
    db.insert_message(user_id=1, content="Salut tout le monde !")
    db.insert_message(user_id=2, content="Bonjour !")
    messages = db.get_messages(limit=5)
    for message in messages:
        print(f"{message[2]} - User {message[0]}: {message[1]}")
    db.close()
