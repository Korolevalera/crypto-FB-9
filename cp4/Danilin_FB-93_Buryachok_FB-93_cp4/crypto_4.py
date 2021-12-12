from random import randint

key_length = 256
key_start = pow(2, key_length - 1)
key_stop = pow(2, key_length) - 1

def quick_pow(a, b, m):
    ab = 1
    while b > 0:
        if b & 1:
            ab = (ab * a) % m
        b >>= 1
        a = (a ** 2) % m
    return ab

def get_ds(p):
    p -= 1
    s = 0
    while p % 2 == 0:
        p >>= 1
        s += 1
    return (p, s)

def strongly_prime(p, x, d, s):
    xd = quick_pow(x, d, p)
    if xd == 1 or xd == p - 1:
        return True
    xr = xd
    for r in range(1, s):
        xr = quick_pow(xr, 2, p)
        if xr == p - 1:
            return True
        if xr == 1:
            return False

def gcd(a, b):
    while a > 0 and b > 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b

def Millera_Rabina(p):
    d, s = get_ds(p)
    if not(strongly_prime(p, 2, d, s)) or not(strongly_prime(p, 3, d, s)) or not(strongly_prime(p, 5, d, s)) or not(strongly_prime(p, 7, d, s)):
        return False
    k = 0
    while k < 5:
        x = randint(2, p - 1)
        if gcd(x, p) > 1 or not(strongly_prime(p, x, d, s)):
            return False
        k += 1
    return True

def generate_prime():
    x = randint(key_start, key_stop)
    if not x & 1:
        x += 1
    for i in range(x, key_stop, 2):
        if Millera_Rabina(i):
            return i

def generate_e(fn):
    e = randint(2, fn - 1)
    while gcd(e, fn) > 1:
       e = randint(2, fn - 1)
    return e

def get_q(a, b):
    q = []
    while a > 0 and b > 0:
        if a > b:
            q.append(int(a / b))
            a %= b
        else:
            q.append(int(b / a))
            b %= a
    return q

def generate_d(e, fn):
    q = get_q(e, fn)
    result = []
    result.append(0)
    result.append(1)
    for i in range(len(q)):
        qi = -q[i]
        if qi < 0:
            qi += fn
        result.append(((qi * result[i + 1]) + result[i]) % fn)
    return result[len(q)]

def generate_keys():
    p = generate_prime()
    q = generate_prime()
    while p == q:
        q = generate_prime()
    n = p * q
    fn = (p - 1) * (q - 1)
    e = generate_e(fn)
    d = generate_d(e, fn)
    return (n, e, d)

def encrypt(m, e, n):
    return quick_pow(m, e, n)

def decrypt(c, d, n):
    return quick_pow(c, d, n)
    
def sign(m, d, n):
    return quick_pow(m, d, n)

def verify(m, s, e, n):
    return quick_pow(s, e, n) == m

def send_key(k, d0, n0, e1, n1):#A(d0,n0) B(e1, n1)
    k1 = encrypt(k, e1, n1)
    s = decrypt(k, d0, n0)
    s1 = encrypt(s, e1, n1)
    return (k1, s1)

def receive_key(ks, d0, n0, e1, n1):#A(e1,n1) B(d0,n0)
    k1 = ks[0]
    s1 = ks[1]
    k = decrypt(k1, d0, n0)
    s = decrypt(s1, d0, n0)
    if k != encrypt(s, e1, n1):
        print("SOMETHING WRONG WITH KEY")
    return k

def encode(string):
    return int(string.encode().hex(), 16)

def decode(int):
    return bytearray.fromhex(hex(int)[2:]).decode()

def int_to_hex(int):
    return hex(int)[2:].upper()

def hex_to_int(hex):
    return int(hex, 16)

class Abonent():
    def __init__(self):
        self.n = None
        self.e = None
        self.d = None

    def print_keys_dec(self):
        print(f"dec n = {self.n}")
        print(f"dec e = {self.e}")
        print(f"dec d = {self.d}")

    def print_keys_hex(self):
        print(f"hex n = {int_to_hex(self.n)}")
        print(f"hex e = {int_to_hex(self.e)}")
        print(f"hex d = {int_to_hex(self.d)}")

    def generate_key_receiver(self):
        self.n, self.e, self.d = generate_keys()

    def generate_key_sender(self, n):
        self.n, self.e, self.d = generate_keys()
        while n < self.n:
            self.n, self.e, self.d = generate_keys()
    
    def encrypt(self, m, e, n):
        return encrypt(m, e, n)
    
    def decrypt(self, c):
        return decrypt(c, self.d, self.n)
    
    def sign(self, m):
        return sign(m, self.d, self.n)
    
    def verify(self, m, s, e, n):
        return verify(m, s, e, n)
    
    def send_key(self, k, e, n):
        return send_key(k, self.d, self.n, e, n)
    
    def receive_key(self, ks, e, n):
        return receive_key(ks, self.d, self.n, e, n)

def check():
    modulus = "8924ADDA6B60D6B731404DEE5E431A38FAC4394EB313614AB6C834A88A2009E5E87D03138F27B28FF9BFFA69CC06D3D2EC2C513375F2725BB978C55463C95EBD"
    exponent = "10001"

    n = 8923656186321824081488135504643688162548557149446412287814673826161489761208234503251945575864814519792032321401499497921783851153183411834517642465402893
    e = 2823530029678610103498835374423876674948499549170405759747701428808961205060874889721846963083436577371845653879481281075390143374156453411628257844977759
    d = 4961441460831825012373226525627678025794513010830758327806336480230027620606576128573641064597210030770586440798368714061641497820932899289200128431851999

    '''n, e, d = generate_keys()
    while n < hex_to_int(modulus):
        n, e, d = generate_keys()'''
    
    print(f"dec n = {n}")
    print(f"dec e = {e}")
    print(f"dec d = {d}")
    
    print(f"hex n = {int_to_hex(n)}")
    print(f"hex e = {int_to_hex(e)}")
    print(f"hex d = {int_to_hex(d)}")

    m = encode("some message")
    
    def part1():
        #генерируем ключи на сервере, шифруем у себя, расшифровуем на сервере
        print("\nCheck part1")
        c = encrypt(m, hex_to_int(exponent), hex_to_int(modulus))
        print(f"hex cipher = {int_to_hex(c)}")

    def part2():
        #генерируем ключи у себя, шифруем на сервере, расшифровуем у себя
        print("\nCheck part2")
        c= "1A82B9887A65073DF4E09FB4D84085C4FECFE185A7965CA7DB6E941E654D1BF33BA10BCF165F6C64493BB6C89675F41A7658349B262A30C2D61CEB4A8F5BDF03"
        dm = decrypt(hex_to_int(c), d, n)
        print(f"decrypted message = {decode(dm)}")

    def part3():
        #генерируем цифровую подпись у себя, проверяем на сервере
        print("\nCheck part3")
        s = sign(m, d, n)
        print(f"hex signature = {int_to_hex(s)}")

    def part4():
        #генерируем цифровую подпись на сервере, проверяем у себя
        print("\nCheck part4")
        s = "2C205280A13C9E4F36356DF777163E41527EA8DF0D270BFFAA62B4C82102DAA10C30D019FC9808AC806F2007242030CD2C2BD92B00C286940E222E8A3907952C"
        print(verify(m, hex_to_int(s), hex_to_int(exponent), hex_to_int(modulus)))

    part1()
    part2()
    part3()
    part4()

def demo():
    sender = Abonent()
    receiver = Abonent()

    receiver.generate_key_receiver()
    sender.generate_key_sender(receiver.n)

    print("sender:")
    sender.print_keys_dec()
    sender.print_keys_hex()

    print("receiver")
    receiver.print_keys_dec()
    receiver.print_keys_hex()

    msg = encode("hello world")

    cipher = sender.encrypt(msg, receiver.e, receiver.n)

    print(decode(receiver.decrypt(cipher)))

    k = encode("hello this is a private message")

    ks = sender.send_key(k, receiver.e, receiver.n)
    res = receiver.receive_key(ks, sender.e, sender.n)

    print(decode(res))