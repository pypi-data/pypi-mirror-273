import time
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

class TimeBasedToken:
    def __init__(self, primary_toke, secondary_token):
        self.__enckey = None
        self.primary = primary_toke
        self.special = secondary_token
        self.__iv = None
        self.regenerate()
        self.__geniv()


    def regenerate(self):
        # Berechne den gerundeten Unix-Zeitstempel
        timestamp = int(time.time() // 10 * 10)

        # Kombiniere Token und Zeitstempel und erstelle einen SHA-256 Hash
        combined = f"{self.special}{timestamp}".encode()
        hash_result = hashlib.sha256(combined).hexdigest()

        # Erstelle eine Bitmap aus den ersten 8 Zeichen des Hashes
        bitmap = bin(int(hash_result[:8], 16))[2:].zfill(32)
        print(bitmap)

        # Erstelle eine "zufällige" Reihenfolge aus den nächsten 8 Zeichen
        order_seed = int(hash_result[8:16], 16)
        order = sorted(range(32), key=lambda x: (order_seed >> (x % 8)) & 1)
        print(order)

        # Extrahiere und sortiere Zeichen basierend auf der Bitmap und der Reihenfolge
        extracted_chars = ''.join([self.special[i] for i, bit in enumerate(bitmap) if bit == '1'])
        sorted_chars = ''.join([extracted_chars[i] for i in order if i < len(extracted_chars)])

        # Kombiniere den self.primary mit den sortierten Zeichen und erstelle einen finalen Hash
        final_combined = f"{self.primary}{sorted_chars}".encode()
        final_hash = hashlib.sha256(final_combined).hexdigest()
        self.__enckey = final_hash
        return str(final_hash)
    
    def __geniv(self):
        # Kombiniere die Token
        combined_tokens = self.primary + self.special

        # Erstelle einen SHA-256 Hash des kombinierten Strings
        hash_obj = SHA256.new(combined_tokens.encode())

        # Extrahiere die ersten 16 Bytes des Hashes für den IV
        iv = hash_obj.digest()[:16]

        self.__iv = iv
    
    def encrypt(self, plaintext):
        # Konvertiere den Hex-Schlüssel in Bytes
        key_bytes = bytes.fromhex(self.__enckey)
        
        # Initialisiere den AES Cipher im CBC Modus
        cipher = AES.new(key_bytes, AES.MODE_CBC, self.__iv)
        
        # Verschlüssle den Klartext mit Padding
        encrypted_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        
        # Kombiniere IV und verschlüsselten Text, kodiere beides in Base64 für einfache Handhabung
        encrypted_data = base64.b64encode(self.__iv + encrypted_bytes).decode()
        
        return encrypted_data

    def decrypt(self, encrypted_data):
        # Konvertiere den Hex-Schlüssel in Bytes
        key_bytes = bytes.fromhex(self.__enckey)
        
        # Dekodiere die Daten aus Base64
        encrypted_bytes = base64.b64decode(encrypted_data)
        

        encrypted_text = encrypted_bytes[AES.block_size:]
        
        # Initialisiere den AES Cipher im CBC Modus
        cipher = AES.new(key_bytes, AES.MODE_CBC, self.__iv)
        
        # Entschlüssle den Text und entferne das Padding
        decrypted_bytes = unpad(cipher.decrypt(encrypted_text), AES.block_size)
        
        return decrypted_bytes.decode()
    
    def __str__(self):
        return self.key



# Example
# primary = "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
# special = "7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f"
# import timeit
# def main():
#     final_token = TimeBasedToken(primary, special)
# 
#     print(final_token.regenerate())
#     enc = final_token.encrypt("in Python umsetzen könnte:")
#     print(enc)
#     dec = final_token.decrypt(enc)
#     print(dec)
# 
# if __name__ == "__main__":
#     print(timeit.timeit(main, number=1))