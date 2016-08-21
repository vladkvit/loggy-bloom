from bitarray import bitarray
import mmh3
import math

def is_pow2(num):
    assert(num >=0 )
    return num != 0 and ((num & (num - 1)) == 0)

#Initial BloomFilter code from https://gist.github.com/mburst/4700640
class BloomFilter:
    
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
        
    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1
            
    def lookup(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                return "Nope"
        return "Probably"

#this thing keeps multiple Bloom Filters of sizes
# N, N/2, N/4, ..., 1
#The shifts are similar to generating a mipmap (shift entire level at a time)
#Read the readme for more info
class LoggyBloomFilter1:
    def __init__(self, size, hash_count, keepLastBit = True):
        assert(is_pow2(size))
        self.size = size
        self.hash_count = hash_count
        self.bit_arrays = []
        self.keep_last_bit = keepLastBit
        while size >= 1:
            ba = bitarray(size)
            ba.setall(0)
            self.bit_arrays.append(ba)
            size //= 2
        
    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_arrays[0][result] = 1
        
    #returns -1 if not found
    #otherwise, returns the most recent / largest level at which 
    #object was found
    def lookup(self, string, maxlevel = math.inf):
        indeces = []
        for seed in range(self.hash_count):
            index = mmh3.hash(string, seed) % self.size
            indeces.append(index)

        for level, arr in enumerate(self.bit_arrays):
            if level > maxlevel:
                break
            for index in indeces:
                if arr[index//(2**level)] == 0:
                    continue
                return level
        return -1
    
    def shift(self):
        oldbit = self.bit_arrays[-1][0] #needed for keep_last_bit so info isn't erased

        #iterate from the deepest array to second one
        for level in range(len(self.bit_arrays)-1, 0, -1):
            assert(level-1 >= 0)

            for loc in range(len(self.bit_arrays[level])):
                newbit = self.bit_arrays[level-1][loc*2] or \
                         self.bit_arrays[level-1][loc*2 +1]
                self.bit_arrays[level][loc] = newbit

        self.bit_arrays[0].setall(0)

        if self.keep_last_bit:
            self.bit_arrays[-1][0] = self.bit_arrays[-1][0] or oldbit

    def num_levels(self):
        return len(self.bit_arrays)

    def __str__(self):
        ret = "["
        for idx, arr in enumerate(self.bit_arrays):
            for bit in arr:
                if bit:
                    ret += '*'
                else:
                    ret += '.'
            if idx != len(self.bit_arrays)-1:
               ret += '|'
        ret += ']'
        return ret

def shift_by_two(arr):
    return

class LoggyBloomFilter2:
    def __init__(self, size, hash_count):
        self.sizes = [size, size, size]
        self.hash_count = hash_count
        self.bit_arrays = []

        #if interpreted as integer, overflows represents 
        # numshifts % (2 ** len(sizes))
        self.overflows = bitarray(len(self.sizes)) 
        self.overflows.setall(0)
        for size in self.sizes:
            ba = bitarray(size+1)
            ba.setall(0)
            self.bit_arrays.append(ba)
        
    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.sizes[0]
            self.bit_arrays[0][result] = 1
        
    #returns -1 if not found
    #otherwise, returns the most recent / largest level at which 
    #object was found
    def lookup(self, string, maxlevel = math.inf):
        indeces = []
        for seed in range(self.hash_count):
            index = mmh3.hash(string, seed) % self.sizes[0]
            indeces.append(index)

        #TODO
        return

    def shift_bank(self, bank_idx, bit):
        return_bits = None
        if self.overflows[bank_idx] == 1:
            return_bits = self.bit_arrays[bank_idx][-2:]

        self.overflows[bank_idx] = not self.overflows[bank_idx]
        self.bit_arrays[bank_idx][1:] = self.bit_arrays[bank_idx][:-1]
        self.bit_arrays[bank_idx][0] = bit

        return return_bits

    def shift(self):
        cur_bank = 0
        new_bit = 0
        while cur_bank < len(self.bit_arrays):
            bits = self.shift_bank(cur_bank, new_bit)
            if bits == None:
                break
            
            new_bit = bits[0] or bits[1]
            cur_bank += 1
        return

    def num_levels(self):
        counter = 0
        #count only shifts where bits don't "disappear" past the buffers.
        for i in range(1, len(self.sizes)):
            counter += (self.sizes[i]+1) * 2**i

        return counter

    def __str__(self):
        ret = "["
        for idx, arr in enumerate(self.bit_arrays):
            for i, bit in enumerate(arr):
                if i == len(arr)-1 and self.overflows[idx] == 0:
                    continue
                if bit:
                    ret += '*'
                else:
                    ret += '.'
            if idx != len(self.bit_arrays)-1:
               ret += '|'
        ret += ']'
        return ret