class MT19937:
    def __init__(self, seed: bytes):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u = 11
        self.d = 0xFFFFFFFF
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.f = 1812433253
       
        self.MT = [0 for i in range(self.n)]
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = ((1 << self.w) - 1) & (~self.lower_mask)
        self.seed_mt(seed)
   

    def seed_mt(self, seed: bytes):
        self.index = self.n
        self.MT[0] = int.from_bytes(seed, byteorder='big')
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & ((1 << self.w) - 1)
        return
       

    def extract_number(self) -> int:
        if self.index >= self.n:
            if self.index > self.n:
                print("Generator was never seeded")
                return
            self.twist()


        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)


        self.index += 1
        return y & ((1 << self.w) - 1)


    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0
        return

