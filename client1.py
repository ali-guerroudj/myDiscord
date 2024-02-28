import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import emoji

HOST = '127.0.0.1'
PORT = 45678

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()
        self.surnom = simpledialog.askstring("Surnom", "Donnez votre surnom s'il vous plaît", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recevoir_thread = threading.Thread(target=self.recevoir)

        gui_thread.start()
        recevoir_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.config(bg="cyan")

        self.chat_label = tkinter.Label(self.win, text="Chat", bg="cyan")
        self.chat_label.configure(font="arial 12")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message", bg="cyan")
        self.msg_label.config(font="arial 12")
        self.msg_label.pack(padx=20, pady=5)

        self.saisit = tkinter.Text(self.win, height=3)
        self.saisit.pack(padx=20, pady=5)

        self.btn_envoie = tkinter.Button(self.win, text="Envoyer", command=self.ecrire)
        self.btn_envoie.config(font="arial 12")
        self.btn_envoie.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def ecrire(self):
        message = f"{self.surnom} : {self.saisit.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.saisit.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def recevoir(self):
      messages_recus = set()  # Utiliser un ensemble pour éviter les doublons
      while self.running:
        try:
            message = self.sock.recv(1024)
            if message == "SURNOM":
                self.sock.send(self.surnom.encode("utf-8"))
            else:
                if self.gui_done:
                    message_text = message.decode("utf-8")
                    if message_text not in messages_recus:
                        self.text_area.config(state="normal")

                        self.text_area.tag_configure("right", justify="right")
                        self.text_area.insert(tkinter.END, message_text + "\n", "right")

                        self.text_area.tag_configure("left", justify="left")
                        self.text_area.insert(tkinter.END, "\n", "left")

                        message_with_emoji = self.emoji_replace(message_text)
                        self.text_area.insert(tkinter.END, message_with_emoji)
                        self.text_area.insert(tkinter.END, "\U0001F60A")
                        self.text_area.insert(tkinter.END, "\U00002764")
                        self.text_area.insert(tkinter.END, "\U0001F44D")
                        self.text_area.yview(tkinter.END)
                        self.text_area.config(state="disabled")
                        messages_recus.add(message_text)  # Ajouter le message à l'ensemble des messages reçus
        except ConnectionAbortedError:
            break
        except Exception as e:
            print("Erreur:", e)
            self.sock.close()
            break

    def emoji_replace(self, text):
        # Remplace les alias d'emoji par les caractères correspondants
        return emoji.demojize(text, delimiters=('', ''))


Client = Client(HOST, PORT)



         

        