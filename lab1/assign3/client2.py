import socket
import pickle
import random
import string
import crypto

client_id = "CLIENT2"

def generateSecret(k):
    letters = string.ascii_letters
    secret = ''.join(random.choice(letters) for i in range(k))
    return secret

def generateKeyPair():
    prk = crypto.generate_private_key()
    puk = crypto.generate_public_key(prk)
    return prk,puk

def encrypt_mh(public_key, message):
    message = message.encode('utf-8')
    encrypted_message = crypto.encrypt_mh(message, public_key)
    return encrypted_message

def decrypt_mh(private_key, encrypted_message):
    message = crypto.decrypt_mh(encrypted_message, private_key)
    message = message.decode('utf-8')
    return message

def receive_from_server(sock):
    data = sock.recv(1024)
    sock.close()
    return pickle.loads(data)

def send_to_server(obj, receive=False):
    byt = pickle.dumps(obj)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost',16100))
    sock.sendall(byt)
    if receive:
        return receive_from_server(sock)
    sock.close()


def main():
    #private_key,public_key = generateKeyPair()
    private_key= ((5, 6, 12, 39, 85, 190, 528, 1338), 2661, 1112)
    public_key= (238, 1350, 39, 792, 1385, 1061, 1716, 357)
    send_to_server(["CONNECT",client_id,public_key])
    
    partner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    partner_socket.bind((client_id,17160))
    partner_socket.listen(1)
    print("waiting for partner")
    conn, addr = partner_socket.accept()
    print("partner accepted")
    data = pickle.loads(conn.recv(1024))
    partner_public_key = None
    if data[0] == "HELLO":
        print("received HELLO")
        partner_id = decrypt_mh(private_key,data[1])
        partner_public_key = send_to_server(["GET_KEY",partner_id],True)
        encrypted_id = encrypt_mh(partner_public_key,client_id)
        conn.sendall(pickle.dumps(["ACK",encrypted_id]))
    else:
        conn.close()
        print("NOT HELLO")
        exit()
    secret2 = generateSecret(5)
    data = pickle.loads(conn.recv(1024))
    secret1 = decrypt_mh(private_key,data)
    print("secret 1 received")

    byt = pickle.dumps(encrypt_mh(partner_public_key,secret2))
    conn.sendall(byt)
    print("secret 2 sent")

    commonkey = secret1 + secret2

    card_deck = crypto.generate_card_deck(commonkey)
    offset = 0
    print("card deck generated")
    while True:
        print("Waiting for message...")
        data = pickle.loads(conn.recv(1024))
        if data[1] != offset:
            print("Offset is different, closing.")
            conn.close()
            exit()
        received_message = crypto.decrypt_solitaire(card_deck,data[0])

        if received_message == "BYE":
            print("Received BYE, client closing...")
            conn.close()
            exit()
        else:
            print("Received: ",received_message)
        
        offset += len(received_message)
        message = input('Message: ')
        encrypted_message = crypto.encrypt_solitaire(card_deck,message)
        byt = pickle.dumps([encrypted_message,offset])
        conn.sendall(byt)
        offset += len(message)
        


if __name__ == '__main__':
    main()