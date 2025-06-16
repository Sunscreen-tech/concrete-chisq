from concrete import fhe
import time

@fhe.compiler({"n_0": "encrypted", "n_1": "encrypted", "n_2": "encrypted"})
def chi_sq(n_0, n_1, n_2):
  a = 4 * n_0 * n_2 - n_1 * n_1
  a_sq = a * a

  b_1 = 2 * n_0 + n_1
  b_1_sq = 2 * b_1 * b_1

  b_2 = (2 * n_0 + n_1) * (2 * n_2 + n_1)
  b_3 = 2 * (2 * n_2 + n_1) * (2 * n_2 + n_1)

  return (a_sq, b_1_sq, b_2, b_3)

configuration = fhe.Configuration(p_error=0.0000001, dataflow_parallelize=True)

inputset = [(2, 7, 9), (8, 0, 7)]

print(f"Compiling...")

start = time.time()

circuit_chi_sq = chi_sq.compile(inputset)
end = time.time()

print(circuit_chi_sq.mlir)
with open("foo", "w") as f:
	f.write(circuit_chi_sq.mlir)

print(f"Compile time {end - start}")

print(f"MLIR size {len(circuit_chi_sq.mlir)}")

print(f"Generating keys...")
start = time.time()
circuit_chi_sq.keygen()
end = time.time()

print(f"Keygen time {end - start}")
print(f"Keygen done!")

examples = [(2, 7, 9)]
for example in examples:
	start = time.time()
	encrypted = circuit_chi_sq.encrypt(*example)
	end = time.time()

	print(f"Encryption time {end - start}")

	start = time.time()
	encrypted_result = circuit_chi_sq.run(encrypted)
	end = time.time()
	
	print(f"Execution time {end - start}")

	start = time.time()
	result = circuit_chi_sq.decrypt(encrypted_result)
	print(f"{result}")
	end = time.time()
	print(f"Decryption time {end - start}")

