import string
import random
import crypto
def generateRandomString(length=8):
    letters = string.ascii_letters
    word = ''.join(random.choice(letters) for i in range(length))
    return word

def main():
    card_deck_1 = crypto.generate_card_deck("aaaa")
    card_deck_2 = card_deck_1.copy()
    message = "hello is it me you're looking for?"
    encrypted_message = crypto.encrypt_solitaire(card_deck_1,message)
    print(encrypted_message)
    if card_deck_1 == card_deck_2:
        print("DS")
    print(crypto.decrypt_solitaire(card_deck_2,encrypted_message))
    
if __name__ == '__main__':
    main()