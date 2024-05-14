from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# RSA Schlüsselpaar generieren
def gen_keypair():
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pub_key = priv_key.public_key()
    return (priv_key, pub_key)

# Nachricht mit dem öffentlichen Schlüssel verschlüsseln
def encrypt(nachricht, pub_key):
    return pub_key.encrypt(
        nachricht.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Nachricht mit dem privaten Schlüssel entschlüsseln
def decrypt(message, priv_key):
    decrypted = priv_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Example
# priv_key, pub_key = generiere_rsa_schluesselpaar()
# message = verschluesseln("Geheime Nachricht", pub_key)
# print(f"Verschlüsselt: {message}")
# 
# decrypted = decrypt(message, priv_key)
# print(f"Entschlüsselt: {decrypted}")