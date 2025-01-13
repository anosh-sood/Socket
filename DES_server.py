import socket
import sys

IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

FP_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]

def permute(block, table):
    return ''.join([block[i - 1] for i in table])

def string_to_bits(s):
    return ''.join(format(ord(c), '08b') for c in s)

def bits_to_string(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def decrypt(ciphertext, key):
    ct_bits = string_to_bits(ciphertext)
    permuted_ct = permute(ct_bits, IP_TABLE)
    # Placeholder for rounds of DES, using just a simple reversal
    plaintext_bits = permuted_ct[::-1]
    final_pt = permute(plaintext_bits, FP_TABLE)
    return bits_to_string(final_pt)

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 4455
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    while True:
        client, address = server.accept()
        print(f"Connection established - {address[0]}:{address[1]}")
        encrypted_message = client.recv(1024).decode()
        key = "hardkey"
        decrypted_message = decrypt(encrypted_message, key)
        print("Decrypted message:", decrypted_message)

        response = encrypt(decrypted_message, key)
        client.sendall(response.encode())
        client.close()