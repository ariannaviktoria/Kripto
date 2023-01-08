import socket
import pickle
import random
import string
import time

import crypto

client_id = "CLIENT1"

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

    private_key = ((5, 8, 17, 46, 94, 228, 712, 1725), 4986, 4253)
    public_key = (1321, 4108, 2497, 1184, 902, 2400, 1634, 2019)

    send_to_server(["CONNECT",client_id,public_key])

    print("Wait for client2 to start")
    time.sleep(5)
    print("No more waiting")

    partner_public_key = send_to_server(["GET_KEY","CLIENT2"],True)

    
    client_id_encrypted = encrypt_mh(partner_public_key,client_id)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('CLIENT2',17160))
    byt = pickle.dumps(["HELLO",client_id_encrypted])
    sock.sendall(byt)

    data = pickle.loads(sock.recv(1024))
    if data[0] == "ACK":
        print("received ACK")
        if decrypt_mh(private_key, data[1]) != "CLIENT2":
            print("Wrong response")
            sock.close()
            exit() 
    secret1 = generateSecret(5)
    secret1_encrypted = encrypt_mh(partner_public_key, secret1)
    byt = pickle.dumps(secret1_encrypted)
    sock.sendall(byt)
    print("secret 1 sent")

    secret2_encrypted = pickle.loads(sock.recv(1024))
    secret2 = decrypt_mh(private_key,secret2_encrypted)
    print("secret 2 received")
    commonkey = secret1 + secret2

    card_deck = crypto.generate_card_deck(commonkey)
    offset = 0
    print("card deck generated")
    
    while True:
        message = input('Message: ')
        encrypted_message = crypto.encrypt_solitaire(card_deck,message)
        byt = pickle.dumps([encrypted_message,offset])
        sock.sendall(byt)
        offset += len(message)
        data = pickle.loads(sock.recv(1024))
        if data[1] != offset:
            print("Offset is different, closing.")
            sock.close()
            exit()
        received_message = crypto.decrypt_solitaire(card_deck,data[0])

        if received_message == "BYE":
            print("Received BYE, client closing...")
            sock.close()
            exit()
        else:
            print("Received: ",received_message)
            offset += len(received_message)



if __name__ == '__main__':
    main()