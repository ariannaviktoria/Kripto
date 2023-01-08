import random
import math
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

