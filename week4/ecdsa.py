import hashlib, hmac, secrets
from ecpy.curves import Curve, Point
from random import randint

# Available curves with their properties
AVAILABLE_CURVES = {
    '1': {
        'name': 'secp256k1',
        'description': 'Bitcoin/Ethereum curve (256-bit)',
        'hash_size': 32
    },
    '2': {
        'name': 'secp256r1',
        'description': 'NIST P-256 (256-bit)',
        'hash_size': 32
    },
    '3': {
        'name': 'secp384r1',
        'description': 'NIST P-384 (384-bit)',
        'hash_size': 48
    },
    '4': {
        'name': 'secp521r1',
        'description': 'NIST P-521 (521-bit)',
        'hash_size': 66
    },
    '5': {
        'name': 'brainpoolP256r1',
        'description': 'Brainpool P-256 (256-bit)',
        'hash_size': 32
    }
}

def select_curve():
    # Interactive curve selection
    print("\nAvailable Elliptic Curves:")
    print("-" * 40)
    for key, curve_info in AVAILABLE_CURVES.items():
        print(f"{key}. {curve_info['name']} - {curve_info['description']}")
    
    while True:
        choice = input("\nSelect a curve (1-5): ").strip()
        if choice in AVAILABLE_CURVES:
            curve_name = AVAILABLE_CURVES[choice]['name']
            hash_size = AVAILABLE_CURVES[choice]['hash_size']
            try:
                curve = Curve.get_curve(curve_name)
                print(f"\nSelected: {curve_name}")
                print(f"Curve order: {curve.order}")
                print(f"Field size: {curve.field}")
                return curve, hash_size
            except Exception as e:
                print(f"Error loading curve {curve_name}: {e}")
                continue
        else:
            print("Invalid choice. Please select 1-5.")

def rfc6979_k(priv: int, z: int, n: int, hash_size: int) -> int:
    # Deterministic nonce per RFC 6979 (HMAC-SHA256), adapted for different curve sizes
    # Calculate the byte length needed for the curve order
    byte_len = (n.bit_length() + 7) // 8
    
    x = priv.to_bytes(byte_len, 'big')
    z = (z % n).to_bytes(byte_len, 'big')
    k = b'\x00' * 32  # HMAC key is always 32 bytes for SHA-256
    v = b'\x01' * 32  # HMAC value is always 32 bytes for SHA-256
    
    k = hmac.new(k, v + b'\x00' + x + z, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b'\x01' + x + z, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    
    while True:
        v = hmac.new(k, v, hashlib.sha256).digest()
        # For curves larger than 256 bits, we may need multiple rounds
        candidate_bytes = v
        rounds_needed = (byte_len + 31) // 32  # How many 32-byte chunks we need
        
        for _ in range(rounds_needed - 1):
            v = hmac.new(k, v, hashlib.sha256).digest()
            candidate_bytes += v
        
        # Take only the bytes we need
        candidate_bytes = candidate_bytes[:byte_len]
        cand = int.from_bytes(candidate_bytes, 'big')
        
        if 1 <= cand < n:
            return cand
        k = hmac.new(k, v + b'\x00', hashlib.sha256).digest()
        v = hmac.new(k, v, hashlib.sha256).digest()

def generate_private_key(curve_order):
    # Generate a random private key
    return randint(1, curve_order-1)

def generate_public_key(private_key, curve_generator):
    # Generate public key from private key
    return private_key * curve_generator

def generate_keypair(curve_generator, curve_order):
    # Generate a complete key pair
    private_key = generate_private_key(curve_order)
    public_key = generate_public_key(private_key, curve_generator)
    return private_key, public_key

def hash_message(message, hash_size):
    # Hash message with appropriate algorithm based on curve size
    if hash_size <= 32:
        # Use SHA-256 for smaller curves
        return hashlib.sha256(message.encode()).digest()
    elif hash_size <= 48:
        # Use SHA-384 for medium curves
        return hashlib.sha384(message.encode()).digest()
    else:
        # Use SHA-512 for larger curves
        return hashlib.sha512(message.encode()).digest()

def sign(message, private_key, curve_generator, curve_order, hash_size):
    # Sign a message using ECDSA
    h = hash_message(message, hash_size)
    k = rfc6979_k(private_key, int.from_bytes(h, 'big'), curve_order, hash_size)
    R = k * curve_generator
    r = R.x % curve_order  # Ensure r is within the curve order
    s = (pow(k, -1, curve_order) * (int.from_bytes(h, 'big') + private_key * r)) % curve_order
    return (r, s) 

def verify(message, signature, public_key, curve_generator, curve_order, hash_size):
    # Verify an ECDSA signature
    h = hash_message(message, hash_size)
    s1 = pow(signature[1], -1, curve_order)
    R = (s1 * int.from_bytes(h, 'big') * curve_generator + (s1 * signature[0]) * public_key)
    r = R.x % curve_order  # Ensure r is within the curve order
    return r == signature[0]

def main():
    # Main function to demonstrate multi-curve ECDSA
    print("Multi-Curve ECDSA Demonstration")
    print("=" * 35)
    
    # Let user select curve
    curve, hash_size = select_curve()
    G = curve.generator  # base point
    n = curve.order      # group order (prime)
    
    print(f"\nGenerating key pair...")
    (d, Q) = generate_keypair(G, n)
    print(f"Private key: {hex(d)}")
    print(f"Public key: ({hex(Q.x)}, {hex(Q.y)})")
    
    # Test message
    msg = input("\nEnter message to sign (or press Enter for 'hello'): ").strip()
    if not msg:
        msg = "hello"
    
    print(f"\nSigning message: '{msg}'")
    sig = sign(msg, d, G, n, hash_size)
    ok = verify(msg, sig, Q, G, n, hash_size)
    
    print(f"\nOriginal signature: (r={hex(sig[0])}, s={hex(sig[1])})")
    print(f"Verification result: {ok}")
    
    # Test with tampered signature
    print(f"\nTesting with tampered signature...")
    tampered_sig = (sig[0]-1, sig[1])  # simulate tampering
    print(f"Tampered signature: (r={hex(tampered_sig[0])}, s={hex(tampered_sig[1])})")
    ok_tampered = verify(msg, tampered_sig, Q, G, n, hash_size)
    print(f"Verification result: {ok_tampered}")
    
    print(f"\nDemo completed successfully!")

if __name__ == "__main__":
    main()