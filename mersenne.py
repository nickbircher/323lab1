class MersenneTwister:
    def __init__(self, seed):
        self.n = 624
        self.m = 397
        self.mt = [0] * self.n
        self.index = self.n
        self.lower_mask = (1 << 31) - 1
        self.upper_mask = 1 << 31

        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = (1812433253 * (self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xFFFFFFFF

    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                raise ValueError("Generator was never seeded")
            self.twist()

        y = self.mt[self.index]
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)

        self.index += 1
        return y & 0xFFFFFFFF

    def twist(self):
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) | (self.mt[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= 0x9908B0DF
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0


# # Test the Mersenne Twister with a seed of 12345
# mt = MersenneTwister(12345)

# # Generate 10 random numbers
# output = []
# for _ in range(10):
#     output.append(mt.extract_number())

# print(output)
