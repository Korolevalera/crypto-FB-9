import random

MAX = 1 << 256
MIN = 1 << 255


def gorner(X, e, n):
    e = bin(e)
    Y = 1
    for i in e[2:]:
        Y = (pow(Y, 2)) % n
        if int(i) == 1:
            Y = (X * Y) % n
    return Y


def extended_euclidean_algorithm(a: int, b: int) -> list:  # cp_3
    original_b = b
    u, uu, v, vv = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        u, uu = uu, u - q * uu
        v, vv = vv, v - q * vv
    return [a, u % original_b]  # a - gcd, u - a^-1


def miller_rabin(n, k=100):
    for i in range(k):
        a = random.randrange(2, n - 1)
        exp = n - 1
        s = 0
        while not exp & 1:
            exp >>= 1
            s += 1

        if gorner(a, exp, n) == 1:
            return True

        for _ in range(s - 1):
            if gorner(a, exp, n) == n - 1:
                return True

            exp <<= 1  # d*2**r == d << 1
        return False
    return True


def gen_primes():
    primes = []
    for _ in range(4):
        while True:
            a = (random.randrange(MIN, MAX) << 1) + 1
            if miller_rabin(a):
                primes.append(a)
                break
    return primes


def GenerateKeyPairs(p, q):
    n = p * q
    euler = (p - 1) * (q - 1)
    e = random.randint(2, euler - 1)
    while not extended_euclidean_algorithm(e, euler)[0] == 1:
        e = random.randint(2, euler - 1)
    d = extended_euclidean_algorithm(e, euler)[1]
    return [e, n, d, p, q]


class User:
    def __init__(self, e, n, d, p, q):
        self.msg = random.randint(0, n - 1)
        self.e = e
        self.n = n
        self._d = d
        self._p = p
        self._q = q
        self.signature = self._Sign()
        self.e1 = None
        self.n1 = None
        self.encrypted_msg = None
        self.received_message = []
        self.decrypted_received_message = None

    def SendKey(self):
        return [self.e, self.n]

    def ReceiveKey(self, e, n):
        self.e1 = e
        self.n1 = n

    def _Sign(self):
        return gorner(self.msg, self._d, self.n)

    def Verify(self):
        return self.decrypted_received_message == gorner(gorner(self.received_message[1], self._d, self.n), self.e1,
                                                         self.n1)

    def Encrypt(self):
        self.encrypted_msg = gorner(self.msg, self.e1, self.n1)

    def Decrypt(self):
        self.decrypted_received_message = gorner(self.received_message[0], self._d, self.n)

    def send_message(self):
        return [self.encrypted_msg, gorner(self.signature, self.e1, self.n1)]

    def receive_message(self, message: list):
        self.received_message = message


p, q, p1, q1 = gen_primes()
while not p * q <= p1 * q1:
    # print(p, q, p1, q1)
    p, q, p1, q1 = gen_primes()

A = User(*GenerateKeyPairs(p, q))
B = User(*GenerateKeyPairs(p1, q1))
print(f"A`s message: {A.msg}")

A.ReceiveKey(*B.SendKey())
B.ReceiveKey(*A.SendKey())
A.Encrypt()
B.Encrypt()
B.receive_message(A.send_message())
B.Decrypt()
if B.Verify():
    print(f"B successfully received and verified message from A. Message: {B.decrypted_received_message}")
