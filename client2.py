import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import mysql.connector

class Channel:
    def __init__(self, name, is_text_channel, is_voice_channel):
        self.name = name
        self.is_text_channel = is_text_channel
        self.is_voice_channel = is_voice_channel

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def is_text_channel(self):
        return self.is_text_channel

    def set_text_channel(self, text_channel):
        self.is_text_channel = text_channel

    def is_voice_channel(self):
        return self.is_voice_channel

    def set_voice_channel(self, voice_channel):
        self.is_voice_channel = voice_channel

class ChatWindow:
    def __init__(self, channel, server_address, server_port, sender_name):
        self.channel = channel
        self.server_address = server_address
        self.server_port = server_port
        self.sender_name = sender_name  # Nom de l'expéditeur
        self.root = tk.Tk()
        self.root.title("Chat Naycir")
        
        self.chat_history = scrolledtext.ScrolledText(self.root, state='disabled', height=15, width=50)
        self.chat_history.grid(column=0, row=0, columnspan=2)
        
        self.message_entry = tk.Entry(self.root)
        self.message_entry.grid(column=0, row=1)
        
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(column=1, row=1)

        # Établir une connexion avec le serveur
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        
        # Démarrer un thread pour recevoir les messages du serveur
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        # Récupérer les messages précédemment enregistrés dans la base de données et les afficher
        self.display_previous_messages()

        self.root.mainloop()

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        
        # Envoyer le message et le nom de l'expéditeur au serveur
        self.client_socket.sendall(f"{self.sender_name}: {message}".encode('utf-8'))

        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, f"{self.sender_name}: {message}\n")
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.chat_history.configure(state='normal')
                    self.chat_history.insert(tk.END, f"{message}\n")
                    self.chat_history.configure(state='disabled')
                    self.chat_history.see(tk.END)
            except ConnectionAbortedError:
                break
            except ConnectionAbortedError:
                break

    def display_previous_messages(self):
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sirinepupuce1",
            database="mydiscord"
        )

        # Récupération des messages précédemment enregistrés dans la base de données
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM historique")
        messages = cursor.fetchall()
        cursor.close()
        conn.close()

        # Affichage des messages dans la fenêtre de chat
        for msg in messages:
            self.chat_history.configure(state='normal')
            self.chat_history.insert(tk.END, f"{msg[1]}: {msg[2]}\n")
            self.chat_history.configure(state='disabled')
            self.chat_history.see(tk.END)

# Utilisation de la classe ChatWindow
channel1 = Channel("Naycir", True, False)
chat_window1 = ChatWindow(channel1, '127.0.0.1', 25565, "Naycir")  # Remplacez par les informations de votre serveur et le nom de l'expéditeur

