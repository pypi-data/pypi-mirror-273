import time
import hashlib

def generate_final_token(primary_token, special_token):
    # Berechne den gerundeten Unix-Zeitstempel
    timestamp = int(time.time() // 100 * 100)
    
    # Kombiniere Token und Zeitstempel und erstelle einen SHA-256 Hash
    combined = f"{special_token}{timestamp}".encode()
    hash_result = hashlib.sha256(combined).hexdigest()
    
    # Erstelle eine Bitmap aus den ersten 8 Zeichen des Hashes
    bitmap = bin(int(hash_result[:8], 16))[2:].zfill(32)
    print(bitmap)
    
    # Erstelle eine "zufällige" Reihenfolge aus den nächsten 8 Zeichen
    order_seed = int(hash_result[8:16], 16)
    order = sorted(range(32), key=lambda x: (order_seed >> (x % 8)) & 1)
    print(order)
    
    # Extrahiere und sortiere Zeichen basierend auf der Bitmap und der Reihenfolge
    extracted_chars = ''.join([special_token[i] for i, bit in enumerate(bitmap) if bit == '1'])
    sorted_chars = ''.join([extracted_chars[i] for i in order if i < len(extracted_chars)])
    
    # Kombiniere den primary_token mit den sortierten Zeichen und erstelle einen finalen Hash
    final_combined = f"{primary_token}{sorted_chars}".encode()
    final_hash = hashlib.sha256(final_combined).hexdigest()
    
    return final_hash



# Beispielverwendung
#primary_token = "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"
#special_token = "7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f"
#final_token = generate_final_token(primary_token, special_token)
#print(final_token)