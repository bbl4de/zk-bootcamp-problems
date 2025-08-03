import hashlib, hmac, secrets
from ecpy.curves import Curve, Point
from random import randint

# curve domain params (secp256k1) 
curve = Curve.get_curve('secp256k1')
G = curve.generator            # base point
n = curve.order                # group order (prime)
# helper for k:
def rfc6979_k(priv: int, z: int, n: int) -> int:
    # Deterministic nonce per RFC 6979 (HMAC-SHA256), specialized for 256-bit n.
    x = priv.to_bytes(32, 'big')
    z = (z % n).to_bytes(32, 'big')
    k = b'\x00' * 32
    v = b'\x01' * 32
    k = hmac.new(k, v + b'\x00' + x + z, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b'\x01' + x + z, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    while True:
        v = hmac.new(k, v, hashlib.sha256).digest()
        cand = int.from_bytes(v, 'big')
        if 1 <= cand < n:
            return cand
        k = hmac.new(k, v + b'\x00', hashlib.sha256).digest()
        v = hmac.new(k, v, hashlib.sha256).digest()


def generate_private_key(curve_order):
    rand = randint(1, curve_order-1)
    return rand

def generate_public_key(private_key, curve_generator):
    return private_key * curve_generator

def generate_keypair(curve_generator, curve_order):
    private_key = generate_private_key(curve_order)
    public_key = generate_public_key(private_key, curve_generator)
    return private_key, public_key

def hash(message):
    return hashlib.sha256(message.encode()).digest()

# This has to be called with curve_generator being a GF point from galois
def sign(message, private_key, curve_generator, curve_order):
    h = hash(message)
    k = rfc6979_k(private_key, int.from_bytes(h, 'big'), curve_order)
    R = k * curve_generator
    r = R.x 
    s = (pow(k, -1, curve_order) * (int.from_bytes(h, 'big') + private_key * r)) % curve_order
    return (r, s) 

def verify(message, signature, public_key, curve_generator, curve_order):
    h = hash(message)
    s1 = pow(signature[1], -1, curve_order)
    R = (s1 * int.from_bytes(h, 'big') * curve_generator + (s1 * signature[0]) * public_key)
    r = R.x
    return r == signature[0]

(d, Q) = generate_keypair(G, n)
msg = "hello"
sig = sign(msg, d, G, n)
ok = verify(msg, sig, Q, G, n)
print("Untampered signature:", sig)
print("Verification:", ok)  
print(sig)
sig = (sig[0]-1, sig[1])  # simulate tampering with signature
print("Tampered signature:", sig)
# verify with tampered signature
ok = verify(msg, sig, Q, G, n)
print("Verification:", ok)  
