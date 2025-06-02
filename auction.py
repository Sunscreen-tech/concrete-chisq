from concrete import fhe
import time
import numpy as np

@fhe.compiler({
    "bids": "encrypted",
})
def auction(bids):
    bid = bids[0]
    idx = 0

    for i in range(1, len(bids)):
        gt = bids[i] > bid
        
        # Ideally, we'd do the below, but that fails to compile
        # bid = fhe.if_then_else(gt, curBid, bid)
        # idx = fhe.if_then_else(gt, i, idx)
        bid = (bids[i] - bid) * gt + bid
        idx = (i - idx) * gt + idx
    
    return (bid, idx)
    

num_bids = 32

bit_padding = np.array([32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768, 32768][0:num_bids])
bids = np.array([1, 1024, 17, 555, 384, 97, 138, 682, 1, 1024, 17, 555, 384, 97, 138, 682, 1, 1024, 17, 555, 384, 97, 138, 682, 1, 1024, 17, 555, 384, 97, 138, 682][0:num_bids])
inputset = [bit_padding, bids]

start = time.time()
auction_circuit = auction.compile(inputset)
end = time.time()

print(auction_circuit.mlir)

print(f"Compile time {end - start}")

auction_circuit.keygen()

print(f"Program size {len(auction_circuit.mlir)}")

bids_enc = fhe.array(bids)

start = time.time()

result = auction_circuit.encrypt_run_decrypt(bids)

end = time.time()

print(f"Execution time {end - start}")
print(result)