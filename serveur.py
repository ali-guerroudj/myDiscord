import socket
import threading

host = '027.0.0.1'
port = 1234
LISTENER_LIMIT = 5

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((host , port))
        print(f"running the server on {host} {port}")

    except:
        print(f"unable to bind to host {host} and port {port}")

        server.listen(LISTENER_LIMIT)    

        while 1 :
            client, adress = server.accept()
            print(f"Successfully connected to client {adress[0]} {adress[1]}")

if __name__ == "__main__":
    main()


