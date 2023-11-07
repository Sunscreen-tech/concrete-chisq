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

@fhe.compiler({"n_0": "encrypted", "n_1": "encrypted", "n_2": "encrypted"})
def chi_sq_a_sq(n_0, n_1, n_2):
  a = 4 * n_0 * n_2 - n_1 * n_1
  return a * a

@fhe.compiler({"n_0": "encrypted", "n_1": "encrypted", "n_2": "encrypted"})
def chi_sq_b_1_sq(n_0, n_1, n_2):
  b_1 = 2 * n_0 + n_1
  return 2 * b_1 * b_1

@fhe.compiler({"n_0": "encrypted", "n_1": "encrypted", "n_2": "encrypted"})
def chi_sq_b_2(n_0, n_1, n_2):
  return(2 * n_0 + n_1) * (2 * n_2 + n_1)

@fhe.compiler({"n_0": "encrypted", "n_1": "encrypted", "n_2": "encrypted"})
def chi_sq_b_3(n_0, n_1, n_2):
  return 2 * (2 * n_2 + n_1) * (2 * n_2 + n_1)

configuration = fhe.Configuration(p_error=0.0000001, dataflow_parallelize=True)

inputset = []

#for i in range(10):
# for j in range(10):
#   for k in range(10):
#     inputset.append((i, j, k))

inputset = [(2, 7, 9)]

print(f"Compiling...")

start = time.time()

circuit_a_sq = chi_sq_a_sq.compile(inputset)
circuit_b_1_sq = chi_sq_b_1_sq.compile(inputset)
circuit_b_2 = chi_sq_b_2.compile(inputset)
circuit_b_3 = chi_sq_b_3.compile(inputset)

end = time.time()

print(f"Compile time {end - start}")

#circuit_chi_sq = chi_sq.compile(inputset)

print(f"Generating keys...")
start = time.time()
print("a_sq")
circuit_a_sq.keygen()
print("b_1_sq")
circuit_b_1_sq.keygen()
print("b_2")
circuit_b_2.keygen()
print("b_3")
circuit_b_3.keygen()

end = time.time()

print(f"Keygen time {end - start}")
print(f"Keygen done!")

examples = [(2, 7, 9)]
for example in examples:
	start = time.time()
	encrypted_example_1 = circuit_a_sq.encrypt(*example)
	encrypted_example_2 = circuit_b_1_sq.encrypt(*example)
	encrypted_example_3 = circuit_b_2.encrypt(*example)
	encrypted_example_4 = circuit_b_3.encrypt(*example)
	end = time.time()

	print(f"Encryption time {end - start}")

	start = time.time()
	encrypted_result_1 = circuit_a_sq.run(encrypted_example_1)
	encrypted_result_2 = circuit_b_1_sq.run(encrypted_example_2)
	encrypted_result_3 = circuit_b_2.run(encrypted_example_3)
	encrypted_result_4 = circuit_b_3.run(encrypted_example_4)
	end = time.time()
	
	print(f"Execution time {end - start}")

	start = time.time()
	result = circuit_a_sq.decrypt(encrypted_result_1)
	print(f"a_sq = {result}")
	result = circuit_b_1_sq.decrypt(encrypted_result_2)
	print(f"b_1_sq = {result}")
	result = circuit_b_2.decrypt(encrypted_result_3)
	print(f"b_2 = {result}")
	result = circuit_b_3.decrypt(encrypted_result_4)
	print(f"b_3 = {result}")
	end = time.time()
	print(f"Decryption time {end - start}")

