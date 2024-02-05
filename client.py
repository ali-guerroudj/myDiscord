import socket
import threading

host = '127.0.0.1'
port = 1234

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try :
        client.connect((host,port))
        print(f"connecte avec succes")

    except:
        print(f"unable to connect to server  {host} {port}")


if __name__ == '__main__':
    main()            
