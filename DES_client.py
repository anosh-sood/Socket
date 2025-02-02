import socket

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

def pad_to_64_bits(bits):
    return bits.ljust(64, '0')

def encrypt(plaintext_bits, key):
    plaintext_bits = pad_to_64_bits(plaintext_bits)
    permuted_pt = permute(plaintext_bits, IP_TABLE)
    ciphertext_bits = permuted_pt[::-1]
    final_ct = permute(ciphertext_bits, FP_TABLE)
    return final_ct

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 6000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip, port))

    binary_input = input("Enter 64-bit binary string: ")
    key = "hardkey"
    encrypted_message = encrypt(binary_input, key)
    print("Encrypted Binary Message: ", encrypted_message)

    server.sendall(encrypted_message.encode())
    response = server.recv(1024)
    print("Received from server:", response.decode())
