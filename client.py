import socket
TARGET_IP = '127.0.0.1'
TARGET_PORT = 45123

client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

client.connect((TARGET_IP , TARGET_PORT))
client.send(input(). encode('utf-8'))