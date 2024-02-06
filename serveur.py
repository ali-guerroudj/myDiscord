import socket
ADDR = '127.0.0.1'
PORT = 45123

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind((ADDR,PORT))
server.listen(5)
print(f"[info] server started with IP {ADDR} on port {PORT}.")

while True:
    communication_socket, dest_ip = server.accept()
    print(f"[info] {dest_ip} esteblished a connection to the server.")
    message = communication_socket.recv(5).decode('utf-8')
    print(f"[Message from {dest_ip[0]} : {dest_ip[1]} {message}]")

