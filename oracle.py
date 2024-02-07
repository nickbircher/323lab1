import random
import time
import base64
from mersenne import MersenneTwister
from Crypto.Util.number import long_to_bytes

def oracle():
    time.sleep(random.randint(5, 60))  # Wait between 5 and 60 seconds
    seed = int(time.time())  # Get current UNIX timestamp
    print(seed)
    mt = MersenneTwister(seed)  # Seed the Mersenne Twister
    time.sleep(random.randint(5, 60))  # Wait another 5 to 60 seconds
    output = mt.extract_number()  # Get the first 32 bit output
    return base64.b64encode(long_to_bytes(output))  # Return as base64 encoded value

def brute_force_seed(output):
    current_time = int(time.time())
    for possible_seed in range(current_time, current_time - 120, -1):  # Go back 120 seconds
        mt = MersenneTwister(possible_seed)
        if base64.b64encode(long_to_bytes(mt.extract_number())) == output:
            return possible_seed  # Return the seed if a match is found
    return None  # Return None if no match is found

output = oracle()
print(output)  # Print the output
print(brute_force_seed(output))  # Print the seed