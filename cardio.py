from concrete import fhe
import time

@fhe.compiler({
    "man": "encrypted",
    "age": "encrypted",
    "smoking": "encrypted",
    "diabetic": "encrypted",
    "high_bp": "encrypted",
    "hdl": "encrypted",
    "weight": "encrypted",
    "height": "encrypted",
    "physical_activity": "encrypted",
    "glasses_alcohol": "encrypted",
})
def cardio(man, age, smoking, diabetic, high_bp, hdl, weight, height, physical_activity, glasses_alcohol):
    not_man = 1 - man

    cond1 = man & (age > 50)
    cond2 = not_man & (age > 60)
    cond3 = smoking
    cond4 = diabetic
    cond5 = high_bp
    cond6 = hdl < 40
    cond7 = weight > (height - 90)
    cond8 = physical_activity < 30
    cond9 = man & (glasses_alcohol > 3)
    cond10 = not_man & (glasses_alcohol > 2)

    return cond1 + cond2 + cond3 + cond4 + cond5 + cond6 + cond7 + cond8 + cond9 + cond10

inputset = [(False, 40, False, True, True, 50, 70, 170, 1, 1)]

start = time.time()
cardio_circuit = cardio.compile(inputset)
end = time.time()

print(cardio_circuit.mlir)

print(f"Compile time {end - start}")

cardio_circuit.keygen()

print(f"Program size {len(cardio_circuit.mlir)}")

example = (False, 40, False, True, True, 50, 70, 170, 1, 1)
encrypted = cardio_circuit.encrypt(*example)

start = time.time()

encrypted_result = cardio_circuit.run(encrypted)

end = time.time()

print(f"Execution time {end - start}")

result = cardio_circuit.decrypt(encrypted_result)
print(result)