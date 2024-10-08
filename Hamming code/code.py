import numpy as np

# Text to binary
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

# Calculate redundant bits needed for error correction
def calc_redundant_bits(m):
    r = 0
    while (2**r < m + r + 1):
        r += 1
    return r

# Insert redundant bits into the data
def pos_redundant_bits(data, r):
    j = 0
    k = 0
    m = len(data)
    res = ''
    positions = []  # List to keep track of redundant bit positions

    # Powers of 2
    for i in range(1, m + r + 1):
        if i == 2**j:
            res = res + '0'
            positions.append(i)  # Record the position of redundant bit
            j += 1
        else:
            res = res + data[k]
            k += 1

    return res, positions

# Parity bits
def calc_parity_bits(arr, r):
    n = len(arr)
    arr = list(arr)
    for i in range(r):
        parity = 0
        position = 2**i
        for j in range(1, n+1):
            if j & position:
                parity ^= int(arr[j-1])
        arr[position-1] = str(parity)
    return ''.join(arr)

# Detect and correct errors
def detect_and_correct(data, r):
    n = len(data)
    res = 0
    binary_res = ''

    # Parity bits
    for i in range(r):
        parity = 0
        position = 2**i
        for j in range(1, n+1):
            if j & position:
                parity ^= int(data[j-1])
        if parity != 0:
            res += position
            binary_res = format(position, '0' + str(r) + 'b') + binary_res

    if res != 0:
        # Print error details
        binary_pos = format(res, '0' + str(n) + 'b')
        print(f"Error detected at position: {res} (Binary: {binary_pos}, Value: {data[res - 1]})")
        data = list(data)
        # Error correction
        if res <= n:
            original_value = data[res - 1]
            data[res - 1] = '0' if data[res - 1] == '1' else '1'
            new_value = data[res - 1]
            print(f"Error corrected at position: {res} (Binary: {binary_pos}, Original Value: {original_value}, New Value: {new_value})")
        else:
            print("Error position out of range. No correction performed.")
        corrected_data = ''.join(data)
        return corrected_data
    else:
        print("No error detected.")
        return data

# Remove redundant bits
def remove_redundant_bits(data, r):
    j = 0
    original_data = ''
    for i in range(1, len(data) + 1):
        if i == 2**j:
            j += 1
        else:
            original_data += data[i-1]
    return original_data

# Introduce an error in the data
def introduce_error(data, position):
    if position < 1 or position > len(data):
        print("Error position is out of range.")
        return data
   
    data = list(data)
    original_value = data[position - 1]
    data[position - 1] = '0' if data[position - 1] == '1' else '1'
    new_value = data[position - 1]
   
    # Print the updated data with the error introduced
    bin_length = len(data)
    bin_position = format(position, '0' + str(bin_length) + 'b')
   
    print(f"Introduced error at position: {position} (Binary: {bin_position}, Original Value: {original_value}, New Value: {new_value})")
    print(f"Data with introduced error: {''.join(data)}")
    return ''.join(data)

# Sender program
def sender(text):
    binary_data = text_to_binary(text)
    print(f"Input string: {text}")
    print(f"Binary data: {binary_data}")

    m = len(binary_data)
    r = calc_redundant_bits(m)
    print(f"Redundant bits needed: {r}")

    arr, redundant_positions = pos_redundant_bits(binary_data, r)
    arr = calc_parity_bits(arr, r)
    print(f"Binary data with redundant bits: {arr}")

    # Print positions of redundant bits with binary values
    print("Positions of redundant bits:")
    for pos in redundant_positions:
        print(f"Position: {pos} (Binary: {format(pos, '0' + str(r) + 'b')}, Value: {arr[pos - 1]})")

    return arr

# Receiver program
def receiver(data):
    r = calc_redundant_bits(len(data))
    corrected_data = detect_and_correct(data, r)
   
    # Remove redundant bits
    original_data = remove_redundant_bits(corrected_data, r)

    # Print corrected data with redundant bits
    print(f"Corrected binary data with redundant bits: {corrected_data}")
   
    # Decode to text
    ascii_output = binary_to_text(original_data)
    print(f"Decoded text: {ascii_output}")

# Main program
if __name__ == "__main__":
    input_text = "KAVIARASU"
   
    # Sender side
    channel_data = sender(input_text)
   
    # Introduce an error
    corrupted_data = introduce_error(channel_data, 2)
   
    # Receiver side
    receiver(corrupted_data)