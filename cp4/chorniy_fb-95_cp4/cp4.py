import random 
LOW = pow(2, 255) + 1
HIGH = pow(2, 256) - 1

gcd = lambda a, b: a if b == 0 else not a % b and b or gcd(b , a % b)
encode = lambda msg: int(msg.encode('utf-8').hex(), 16)
decode = lambda msg: bytes.fromhex(hex(msg)[2:]).decode('ASCII')
encrypt = lambda msg, e, n: gorner(msg, e, n)
decrypt = lambda msg, d, n: gorner(msg, d, n)
sign = lambda msg, d, n: gorner(msg, d, n)
verify = lambda msg, sign, e, n: True if msg == gorner(sign, e, n) else False

def gorner(x, y, p):
    res = 1
    while y > 0:
        if y & 1: res = (res * x) % p
        y >>= 1
        x = (x ** 2) % p
    return res

def milrab(num, r = 100):
    m = num - 1
    while not m & 1: m >>= 1
    a = random.randrange(2, num - 1)
    res = gorner(a, m, num)
    if res == 1 or res == num - 1: return True
    else:
        for i in range(r):
            res = gorner(res, 2, num)
            if res == num - 1: return True
    return False

def getran():
    num = random.randrange(LOW, HIGH)
    if not num & 1: num += 1
    for i in range(num, HIGH, 2):
        if not milrab(i): continue
        else: return i

def genkey():
    pair = (getran(), getran())
    while pair[0] == pair[1]: pair[1] = getran()
    n = pair[0] * pair[1]
    phi = (pair[0] - 1) * (pair[1] - 1)
    e = random.randrange(2, phi)
    while(gcd(e, phi) != 1): e = random.randrange(2, phi)
    d = pow(e, -1, phi)
    openkey = (n, e)
    return (openkey, d)

class abonent():

    def __init__(self):
        self.n = 0
        self.e = 0
        self.d = 0

    def GenerateKeyPairSender(self, n):
        key = genkey()
        self.n = key[0][0]
        self.e = key[0][1]
        self.d = key[1]
        while n < self.n:
            key = genkey()
            self.n = key[0][0]
            self.e = key[0][1]
            self.d = key[1]
        print(f'Alice n = {hex(self.n)[2:]}')
        print(f'Alice e = {hex(self.e)[2:]}')
        print(f'Alice d = {hex(self.d)[2:]}')

    def GenerateKeyPairReceiver(self):
        key = genkey()
        self.n = key[0][0]
        self.e = key[0][1]
        self.d = key[1]
        print(f'Bob n = {hex(self.n)[2:]}')
        print(f'Bob e = {hex(self.e)[2:]}')
        print(f'Bob d = {hex(self.d)[2:]}')

    Encrypt = lambda self, msg, e, n: encrypt(encode(msg), e, n) if isinstance(msg, str) else encrypt(msg, e, n)
    Decrypt = lambda self, msg: decrypt(msg, self.d, self.n)
    Sign = lambda self, msg: sign(encode(msg), self.d, self.n) if  isinstance(msg, str) else sign(msg, self.d, self.n)
    Verify = lambda self, msg, signature, e, n: verify(encode(msg), signature, e, n)
    SendKey = lambda self, msg, e, n: (self.Encrypt(msg, e, n), self.Encrypt(self.Sign(msg), e, n))
    ReceiveKey = lambda self, packet, e, n: 'authentication failed' if not self.Verify(decode(self.Decrypt(packet[0])), self.Decrypt(packet[1]), e, n) else decode(self.Decrypt(packet[0]))

Alice = abonent()
Bob = abonent()

msg = 'hello, my name is tolya its pleasure for me to meet you'

Bob.GenerateKeyPairReceiver()
Alice.GenerateKeyPairSender(Bob.n)

packet = Alice.SendKey(msg, Bob.e, Bob.n)
output = Bob.ReceiveKey(packet, Alice.e, Alice.n)

print(output)

# def testserver():
#     Alice = abonent()
#     servermod = int('0xA53346F4729270537DF889F6CBD514B8AD5E7101F7D13DFFE77CE2636014A713D64E4764F952407115714BBD4A187EDFA91F7063EB381ACEE99BE642BD8F6DAF', 16)
#     serversign = int('0x830CCAFC347763CDC6AE2BBD08D1E449FA829B6930F62916A79D4B352F2A2EEA37F45B2F01439FDDC26377DD3DD2FC9149F5394781676CFC69CC207516C8CE3B', 16)
#     e = 0x10001
#     msg = 0x24082001
#     Alice.GenerateKeyPairSender(servermod)
#     packet = Alice.SendKey(msg, e, servermod)
#     print(f'encrypted message is {hex(encrypt(msg, e, servermod))[2:]}')
#     print(f'verify is ok {verify(msg, serversign, e, servermod)}')
#     print(f'message is {hex(packet[0])[2:]}')
#     print(f'signature is {hex(packet[1])[2:]}')

# testserver()