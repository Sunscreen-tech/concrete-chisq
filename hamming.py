from concrete import fhe
import time
import numpy as np

@fhe.compiler({
    "x": "encrypted",
    "y": "encrypted",
})
def hamming(x, y):
    count = 0

    for i in range(0, len(x)):
        for j in range(0, 8):
            count += ((x[i] ^ y[i]) >> j) & 1

    return count
    
x = np.array([0xFE, 0xED, 0xF0, 0x0D, 0xCA, 0xFE, 0xBA, 0xBE][0:8])
y = np.array([0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0][0:8])

inputset = [(x, y)]

start = time.time()
auction_circuit = hamming.compile(inputset)
end = time.time()

print(auction_circuit.mlir)

print(f"Compile time {end - start}")

auction_circuit.keygen()

print(f"Program size {len(auction_circuit.mlir)}")

start = time.time()

result = auction_circuit.encrypt_run_decrypt(x, y)

end = time.time()

print(f"Execution time {end - start}")
print(result)
