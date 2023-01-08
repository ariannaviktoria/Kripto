import string
import random
import crypto

def generateRandomString(length=8):
    letters = string.ascii_letters
    word = ''.join(random.choice(letters) for i in range(length))
    return word

def generateKeyPair():
    prk = crypto.generate_private_key()
    puk = crypto.generate_public_key(prk)
    return prk,puk

def main():
    private_key,public_key = generateKeyPair()
    message = "I said we workin' today!"
    encrypted_message = crypto.encrypt_mh(message.encode('utf-8'), public_key)
    decrypted_message = crypto.decrypt_mh(encrypted_message, private_key).decode('utf-8')
    if message == decrypted_message:
        print("OK")
    print(message," -- ", decrypted_message)
    
if __name__ == '__main__':
    main()