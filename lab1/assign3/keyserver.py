import socket
import pickle
 
class Client:
    def __init__(self, client_id, public_key):
        self.client_id = client_id
        self.public_key = public_key

def main():
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('localhost', 16100))
    serv.listen(2)
    clients = []

    while True:
        print("Waiting for connection..")
        conn, addr = serv.accept()
        data = pickle.loads(conn.recv(1024))
        if data[0] == "CONNECT":
            clients.append(Client(data[1],data[2]))
            print("New client connected...") 
        if data[0] == "GET_KEY":
            for client in clients:
                if data[1] == client.client_id:
                    conn.sendall(pickle.dumps(client.public_key))
                    break
            
if __name__ == '__main__':
    main()