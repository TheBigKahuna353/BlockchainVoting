from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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