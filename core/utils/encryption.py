from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib
import sys

from mnemonic import Mnemonic

def generate_key_pair():
    """
    returns a tuple of private key and public key
    """
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    # Serialize keys if you want to store them
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def sign_data(private_key, data):
    private_key = serialization.load_pem_private_key(private_key, password=None)
    signature = private_key.sign(
        data.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature(public_key, signature, data):
    public_key = serialization.load_pem_public_key(public_key)
    try:
        public_key.verify(
            signature,
            data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False

def _extract_private_key_bytes(private_key_pem):
    """
    Extracts the 32-byte private key from the PEM-encoded private key.
    """
    # Load the PEM private key
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    
    # Extract the private key as a number (this will be 32 bytes in the case of SECP256K1)
    private_key_bytes = private_key.private_numbers().private_value.to_bytes(32, byteorder='big')
    
    return private_key_bytes

def _get_private_key_from_bytes(private_key_bytes):
    """
    Returns a PEM-encoded private key from the 32-byte private key.
    """
    # Load the private key from the bytes
    private_key = ec.derive_private_key(int.from_bytes(private_key_bytes, byteorder='big'), ec.SECP256K1())
    
    # Serialize the private key
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    return private_key_pem

def key_to_mnemonic(key):
    bytes = _extract_private_key_bytes(key)
    return Mnemonic("english").to_mnemonic(bytes)

def mnemonic_to_private_key(mnemonic):
    bytes =  Mnemonic("english").to_entropy(mnemonic)
    return _get_private_key_from_bytes(bytes)

def _test_mnemonic():
    private, _ = generate_key_pair()
    print(private)
    mnemonic = key_to_mnemonic(private)
    print(mnemonic)
    key2 = mnemonic_to_private_key(mnemonic)
    print(key2)
    print(private == key2)

def _test_signature():
    private, public = generate_key_pair()
    data = "Hello, World!"
    signature = sign_data(private, data)
    print("Signature:", signature)
    assert verify_signature(public, signature, data)
    print("Signature verified successfully.")

if __name__ == "__main__":
    # _test_mnemonic()
    # Uncomment the following line to test signature generation and verification
    _test_signature()