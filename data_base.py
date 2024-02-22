import mysql.connector

# Se connecter à la base de données
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="conan",
    database="mydiscord"
)

# Créer un curseur pour exécuter des requêtes SQL
cursor = conn.cursor()

# Exécuter une requête de sélection (Read)
cursor.execute("SELECT * FROM votre_table")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Exécuter une requête d'insertion (Create)
insert_query = "INSERT INTO votre_table (colonne1, colonne2) VALUES (%s, %s)"
values = ("valeur1", "valeur2")
cursor.execute(insert_query, values)
conn.commit()

# Exécuter une requête de mise à jour (Update)
update_query = "UPDATE votre_table SET colonne1 = %s WHERE colonne2 = %s"
new_value = ("nouvelle_valeur", "ancienne_valeur")
cursor.execute(update_query, new_value)
conn.commit()

# Exécuter une requête de suppression (Delete)
delete_query = "DELETE FROM votre_table WHERE colonne = %s"
value_to_delete = ("valeur_a_supprimer",)
cursor.execute(delete_query, value_to_delete)
conn.commit()

# Fermer le curseur et la connexion à la base de données
cursor.close()
conn.close()

