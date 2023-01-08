"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <Mate Arianna Viktoria>
SUNet: <maim2049>

Replace this with a description of the program.
"""
import math
from ntpath import join
import utils
import string
import random

def console():
    
    return 

# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    encrypted_text=''
    for i in range(len(plaintext)):
        encrypted_text += chr((ord(plaintext[i]) + 3-65) % 26 + 65)
    return encrypted_text    
    
    #raise NotImplementedError  # Your implementation here
    

def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    decrypted_text=''
    for i in range(len(ciphertext)):
        decrypted_text += chr((ord(ciphertext[i]) + 23-65) % 26 + 65)
    return decrypted_text
    #raise NotImplementedError  # Your implementation here


# Vigenere Cipher
def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    encrypted_text=''
    if(len(plaintext) != len(keyword)):
        raise ValueError("The given keyword's length is not equal with the plaintext's length.")
    for i in range(len(plaintext)):
        encrypted_text += chr((ord(plaintext[i]) + ord(keyword[i]))%26 + ord('A'))
    return encrypted_text
    #raise NotImplementedError  # Your implementation here


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    decrypted_text=''
    if(len(ciphertext) != len(keyword)):
        raise ValueError("The given keyword's length is not equal with the plaintext's length.")
    for i in range(len(ciphertext)):
        decrypted_text += chr((ord(ciphertext[i]) - ord(keyword[i]) + 26) % 26 + ord('A'))
    return decrypted_text
    #raise NotImplementedError  # Your implementation here

def encrypt_scytale(plaintext, circumference):
    """Encrypt plaintext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    encrypted_text = [''] * int(circumference)
    for col in range(int(circumference)):
        index = col
        while index < len(plaintext):
           encrypted_text[col] += plaintext[index]
           index += int(circumference)          
    return ''.join(encrypted_text)
    #raise NotImplementedError  # Your implementation here


def decrypt_scytale(ciphertext, circumference):
    """Decrypt ciphertext using a Scytale cipher with a keyword.

    Add more implementation details here.
    """
    nr_col = int(math.ceil(len(ciphertext) / float(circumference)))      #column number
    decrypted_text = [''] * nr_col
    nr_row = int(circumference)  #row number
    nr_empty_place = (nr_row * nr_col) - len(ciphertext)        #last row's empty places
    
    column = 0
    row = 0
    for i in ciphertext:
        decrypted_text[column] += i
        column += 1 
        if (column == nr_col-1 and row >= nr_row - nr_empty_place) or (column == nr_col):
            column = 0  #new row
            row += 1
    return ''.join(decrypted_text)

   
def encrypt_railfence(plaintext, circumference):
    """Encrypt plaintext using a Railfence cipher with a keyword.

    Add more implementation details here.
    """
    encrypted_text = ""
    size = int(circumference)*2 - 2
    for i in range(int(circumference)):
        index = 0
        
        #first row
        if i == 0:
            while(index<len(plaintext)):
                encrypted_text += plaintext[index]
                index += size
        #last row
        elif i == int(circumference)-1:
            index = i
            while(index<len(plaintext)):
                encrypted_text += plaintext[index]
                index += size
        else:
            left = i
            right = size-i
            while(left < len(plaintext)):
                encrypted_text += plaintext[left]
                
                if right < len(plaintext):
                    encrypted_text += plaintext[right]
                
                left += size
                right += size
                            
    return encrypted_text
    #raise  NotImplementedError  # Your implementation here


def decrypt_railfence(chipertext, circumference):
    """Decrypt ciphertext using a Railfence cipher with a keyword.

    Add more implementation details here.
    """
    length = len(chipertext)
    decrypted_text = "." * length 
    size = 2 * int(circumference) - 2
    units = length // size
    rail_lengths = [0] * int(circumference)
    #Top
    rail_lengths[0] = units
    #Intermediate
    for i in range(1, int(circumference)-1):
        rail_lengths[i] = 2 * units
    #Bottom
    rail_lengths[int(circumference)-1] = units
    
    
    for i in range(length % size):
        if i<int(circumference):
            rail_lengths[i] += 1
        else:
            rail_lengths[size-i] += 1
    #print(rail_lengths)
    
     #replace top rail fence characters
    index = 0
    plus_index = 0
    for j in chipertext[:rail_lengths[0]]:
        decrypted_text = decrypted_text[:index] + j + decrypted_text[index+1:]
        index += size
        
    plus_index += rail_lengths[0]
    #replace between top and bottom
    for row in range(1,(int(circumference)-1)):
        left = row
        rigth = size - row
        l_char = True
        for d in chipertext[plus_index:plus_index + rail_lengths[row]]:
            if l_char:
                decrypted_text = decrypted_text[:left] + d + decrypted_text[left+1:]
                left += size
                l_char = not l_char
            else:
                decrypted_text = decrypted_text[:rigth] + d + decrypted_text[rigth+1:]
                rigth += size
                l_char = not l_char
        plus_index += rail_lengths[row]
    
    #replace bottom rail fence characters
    index = int(circumference)-1
    for j in chipertext[plus_index:]:
        decrypted_text = decrypted_text[:index] + j + decrypted_text[index+1:]
        index += size
  
    return decrypted_text

def encrypt_file(file_name, key):
    """ 
    Encrypts the bytes of a file using a key.\n
    Uses Vigenere cipher.\n
    Returns a set of bytes for a new file.
    """
    key=key.upper()
    result = []
    extension = file_name.split('.')[1]
    if(extension == []):
        extension_bytes = bytes([0])
    else:
        extension_bytes = bytes([len(extension)])
        extension_bytes += bytes(extension,'utf-8')        

    f = open(file_name,"rb")
    k=0
    file_bytes = f.read()
    
    for byte in file_bytes:
        num = byte
        if key[k].isalpha():
            num = num+ string.ascii_uppercase.index(key[k])
        else:
            num = num+ string.digits.index(key[k])
        num = num % 256
        result.append(num)
        k=(k+1)%len(key)

    f.close()
    return extension_bytes + bytes(result)


def decrypt_file(file_name, key):
    """ 
    Decrypts the bytes of a file using a key. \n
    Uses Vigenere cipher.\n
    Returns a set of bytes for the original file.
    """
    key=key.upper()
    result = []
    f = open(file_name,"rb")
    extension_length = int.from_bytes(f.read(1), "little")
    extension = f.read(extension_length).decode("utf-8")

    k=0
    file_bytes= f.read()
    for byte in file_bytes:
        num = byte
        if key[k].isalpha():
            num = num - string.ascii_uppercase.index(key[k])
        else:
            num = num - string.digits.index(key[k])
        if num<0:
            num = 256 + num
        result.append(num)
        k=(k+1)%len(key)
    f.close()
    return bytes(result),extension


#Merkle-Helman Knapsack

def generate_private_key(n=8):
    """
    :param n: Bitsize of message to send (defaults to 8)
    :type n: int

    :returns: 3-tuple private key `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    
    w=[]
    w.append(random.randint(1,10))
    for i in range(n-1):
        k=random.randint(sum(w) + 1, 2 * sum(w))
        w.append(k)
    if not(utils.is_superincreasing(w)):
        print("w sequence is not superincreasing!")
        return -1
    q=random.randint(sum(w) + 1, 2 * sum(w))
    r=random.randint(2, q-1)
    while not(utils.coprime(r, q)):
        r=random.randint(2, q-1)
    w_tuple=tuple(w)
    return (w_tuple, q, r)

def generate_public_key(private_key):
    """
    :param private_key: The private key created by generate_private_key.
    :type private_key: 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    :returns: n-tuple public key
    """
    w=private_key[0]
    q=private_key[1]
    r=private_key[2]
    b=[]
    for i in range(len(w)):
        b.append((r*w[i])%q)
    return tuple(b)

def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    :param message: The message to be encrypted.
    :type message: bytes
    :param public_key: The public key of the message's recipient.
    :type public_key: n-tuple of ints

    :returns: Encrypted message bytes represented as a list of ints.
    """
    c=[]
    for message_byte in message:
        bits=utils.byte_to_bits(message_byte)
        s=0
        for i in range(len(public_key)):
            s=s + (bits[i]*public_key[i])
        c.append(s)
    return c

def decrypt_mh(message, private_key):
    """
    :param message: Encrypted message chunks.
    :type message: list of ints
    :param private_key: The private key of the recipient (you).
    :type private_key: 3-tuple of w, q, and r

    :returns: bytearray of decrypted characters
    """
    w=private_key[0]
    n=len(w)
    q=private_key[1]
    r=private_key[2]
    s=utils.modinv(r, q)
    decrypted_message=[]
    for num in message:
        c=(num*s)%q
        X=[]
        for i in range(n):
            if c>=w[n-i-1]:
                c-=w[n-i-1]
                X.append(n-i-1)
        k=0
        for x in X:
            k=k + 2**(n-1-x)

        decrypted_message.append(k)
            
    return bytes(decrypted_message)


####################
# SOLITAIRE CIPHER #
####################

def generate_card_deck(key):
    card_deck = []
    for i in range(1,55):
        card_deck.append(i)
    
    for character in key:
        tripleCut(card_deck)
        countCut(card_deck)
        tripleCut(card_deck)

    return card_deck

def moveA(index,card_deck):
    card_deck[index]=card_deck[(index+1)%54]
    card_deck[(index+1)%54]=53

def moveB(index,card_deck):
    card_deck[index]=card_deck[(index+1)%54]
    card_deck[(index+1)%54]=card_deck[(index+2)%54]
    card_deck[(index+2)%54]=54

def tripleCut(card_deck):
    part1=[]
    part2=[]
    part3=[]

    i=0
    while(card_deck[i]!=53 and card_deck[i]!=54):
        part1.append(card_deck[i])
        i+=1
    part2.append(card_deck[i])
    i+=1
    while(card_deck[i]!=53 and card_deck[i]!=54):
        part2.append(card_deck[i])
        i+=1
    part2.append(card_deck[i])
    i+=1
    while(i<54):
        part3.append(card_deck[i])
        i+=1
    card_deck=part3+part2+part1

def countCut(card_deck):
    last_card=card_deck[53]
    pack=[]
    for i in range(last_card):
        pack.append(card_deck[i])
    for i in range(last_card,53):
        card_deck[i-last_card]=card_deck[i]
    k=0
    for pos in range(53-last_card,53):
        card_deck[pos]=pack[k]
        k+=1

def generate_keystream_value(card_deck):
    kv=0
    #1.Locate jokers and move them
    jokerA=card_deck.index(53)
    moveA(jokerA,card_deck)
    jokerB=card_deck.index(54)
    moveB(jokerB,card_deck)


    #2.Perform triple cut
    tripleCut(card_deck)
    #3.Perform count cut
    countCut(card_deck)

    #4.Return keystream number, if its a joker -> repeat
    first_card=card_deck[0]
    kv=card_deck[first_card%54]
    if (kv==53 or kv==54):
        return generate_keystream_value(card_deck)
    else:
        return kv

def solitaire_fix(text):
    string_list = list(text.upper())
    for i in range(len(text)):
        if not string_list[i] in string.ascii_letters:
            string_list[i] = 'X'
    return string_list

def encrypt_solitaire(card_deck,plaintext):
    ciphertext=""
    plaintext = solitaire_fix(plaintext)
    for character in plaintext:
        plain_number=string.ascii_uppercase.index(character)
        keystream_value=generate_keystream_value(card_deck)
        ciphertext+=string.ascii_uppercase[(plain_number+keystream_value)%26]
    return ciphertext

def decrypt_solitaire(card_deck,ciphertext):
    plaintext=""
    for character in ciphertext:
        cipher_number=string.ascii_uppercase.index(character)
        keystream_value=generate_keystream_value(card_deck)
        plain_number=cipher_number-keystream_value
        while(plain_number<0):
            plain_number+=26
        plaintext+=string.ascii_uppercase[plain_number]
    return plaintext