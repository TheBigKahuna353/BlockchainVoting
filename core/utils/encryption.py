from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from mnemonic import Mnemonic

# ------------------------
# Key Pair Generation
# ------------------------

def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    # Get 32-byte private key as hex
    private_int = private_key.private_numbers().private_value
    private_hex = private_int.to_bytes(32, byteorder='big').hex()

    # Get public key in uncompressed form (0x04 + X + Y)
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    public_hex = public_bytes.hex()

    return private_hex, public_hex

# ------------------------
# Sign / Verify
# ------------------------

def sign_data(private_hex: str, data: str) -> str:
    # Convert back to private key object
    private_int = int(private_hex, 16)
    private_key = ec.derive_private_key(private_int, ec.SECP256K1())

    signature = private_key.sign(
        data.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    return signature.hex()

def verify_signature(public_hex: str, signature_hex: str, data: str) -> bool:
    try:
        public_bytes = bytes.fromhex(public_hex)
        signature_bytes = bytes.fromhex(signature_hex)

        public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256K1(), public_bytes)

        public_key.verify(
            signature_bytes,
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False

# ------------------------
# Mnemonic Support
# ------------------------

def key_to_mnemonic(private_hex: str) -> str:
    private_bytes = bytes.fromhex(private_hex)
    return Mnemonic("english").to_mnemonic(private_bytes)

def mnemonic_to_private_key(mnemonic: str) -> str:
    private_bytes = Mnemonic("english").to_entropy(mnemonic)
    return private_bytes.hex()

# ------------------------
# Test Example
# ------------------------

def _test():
    priv, pub = generate_key_pair()
    print("Private:", priv)
    print("Public :", pub)

    msg = "vote:Alice"
    sig = sign_data(priv, msg)
    print("Signature:", sig)

    ok = verify_signature(pub, sig, msg)
    print("Signature valid?", ok)

if __name__ == "__main__":
    _test()
