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

#Encrypt decrypt files
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


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here

#Solitaire chipher

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

#Blum-Blum-Shub

def keys_for_blum_blum_shub(p, q):
    seed = random.randint(100000000,999999999)
    p = good_prime()
    q = good_prime()
    return seed, p, q

def good_prime():
    while True:
        n = random.randint(12345, 987654)
        prim = True
        gyok = math.sqrt(n)
        for i in range(2, gyok + 1):
            if n % i == 0:
                prim = False
        if prim == True and n % 4 == 3:
            break
    return n
