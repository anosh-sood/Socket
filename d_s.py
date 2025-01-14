import socket

IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

INVERSE_IP = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

EXPANSION_TABLE = [32, 1, 2, 3, 4, 5, 4, 5,
                   6, 7, 8, 9, 8, 9, 10, 11,
                   12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21,
                   22, 23, 24, 25, 24, 25, 26, 27,
                   28, 29, 28, 29, 30, 31, 32, 1]

P_BOX = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 15, 11, 1],
     [13, 6, 2, 8, 5, 12, 1, 15, 10, 9, 0, 14, 11, 3, 7, 4],
     [10, 9, 12, 6, 15, 4, 8, 7, 1, 3, 5, 11, 13, 2, 0, 14]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 15, 12, 4],
     [9, 14, 15, 5, 1, 2, 8, 12, 7, 13, 0, 11, 3, 10, 6, 4],
     [2, 5, 8, 12, 7, 9, 6, 3, 15, 10, 14, 11, 1, 13, 0, 4],
     [15, 9, 10, 8, 0, 7, 4, 13, 6, 3, 1, 14, 5, 2, 11, 12]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 8, 15, 10, 3, 9, 6, 0],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 1, 11, 3, 7, 10, 2, 8, 12, 4, 13, 0, 6]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 15, 2, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 10, 9, 0, 12, 11, 7, 4, 13, 15, 1, 3, 5, 14, 8, 2]],
    [[13, 7, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 4, 12, 15],
     [2, 12, 3, 8, 15, 4, 10, 1, 14, 7, 13, 11, 5, 0, 9, 6],
     [4, 2, 1, 10, 13, 7, 11, 15, 14, 9, 8, 12, 0, 3, 5, 6],
     [15, 0, 8, 12, 9, 10, 5, 6, 2, 7, 13, 3, 11, 14, 1, 4]],
    [[10, 15, 4, 9, 14, 2, 7, 13, 8, 1, 11, 5, 3, 12, 0, 6],
     [13, 1, 7, 14, 10, 9, 4, 12, 5, 8, 15, 3, 2, 0, 6, 11],
     [3, 15, 0, 5, 12, 14, 10, 7, 4, 9, 8, 13, 2, 6, 1, 11],
     [7, 13, 14, 12, 11, 3, 8, 4, 2, 10, 9, 5, 6, 1, 15, 0]]
]


KEY_PERM_1 = [57, 49, 41, 33, 25, 17, 9,
              1, 58, 50, 42, 34, 26, 18,
              10, 2, 59, 51, 43, 35, 27,
              19, 11, 3, 60, 52, 44, 36,
              63, 55, 47, 39, 31, 23, 15,
              7, 62, 54, 46, 38, 30, 22,
              14, 6, 61, 53, 45, 37, 29,
              21, 13, 5, 28, 20, 12, 4]

KEY_PERM_2 = [14, 17, 11, 24, 1, 5, 3, 28,
              15, 6, 21, 10, 23, 19, 12, 4,
              26, 8, 16, 7, 27, 20, 13, 2,
              41, 52, 31, 37, 47, 55, 30, 40,
              51, 45, 33, 48, 44, 49, 39, 56,
              34, 53, 46, 42, 50, 36, 29, 32]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

MASTER_KEY = "1111000011001100101010101111010101010110011001111000111100001111"


def main():
    server_host = 'localhost'
    server_port = 12345
    start_server(server_host, server_port)

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)
        print(f"Server listening on {host}:{port}")
        while True:
            client_socket, client_address = server.accept()
            print(f"Connection from {client_address}")
            handle_client(client_socket)

def handle_client(client_socket):
    encrypted_data = client_socket.recv(1024).decode()
    print(f"Received encrypted data: {encrypted_data}")
    decrypted_data = des_decrypt(encrypted_data, MASTER_KEY)
    print(f"Decrypted data: {decrypted_data}")
    client_socket.sendall(decrypted_data.encode())
    client_socket.close()

def des_decrypt(input_block, master_key):
    round_keys = create_round_keys(master_key)
    initial_permutation = transform_bits(input_block, IP_TABLE)
    left, right = initial_permutation[:32], initial_permutation[32:]
    for key in reversed(round_keys):
        new_right = bitwise_xor(left, feistel_function(right, key))
        left, right = right, new_right
    final_data = right + left
    return transform_bits(final_data, INVERSE_IP)

def create_round_keys(master_key):
    permuted_key = transform_bits(master_key, KEY_PERM_1)
    left_half, right_half = permuted_key[:28], permuted_key[28:]
    keys = []
    for shift in SHIFTS:
        left_half = rotate_left(left_half, shift)
        right_half = rotate_left(right_half, shift)
        keys.append(transform_bits(left_half + right_half, KEY_PERM_2))
    return keys

def feistel_function(half_block, key):
    expanded_block = transform_bits(half_block, EXPANSION_TABLE)
    xored_block = bitwise_xor(expanded_block, key)
    substituted_block = apply_sboxes(xored_block)
    return transform_bits(substituted_block, P_BOX)

def apply_sboxes(data):
    result = ''
    for idx in range(8):
        segment = data[idx * 6:(idx + 1) * 6]
        row = int(segment[0] + segment[5], 2)
        col = int(segment[1:5], 2)
        result += format(S_BOXES[idx][row][col], '04b')
    return result

def transform_bits(data, table):
    return ''.join(data[pos - 1] for pos in table)

def rotate_left(data, rotations):
    return data[rotations:] + data[:rotations]

def bitwise_xor(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))

if __name__ == "__main__":
    main()