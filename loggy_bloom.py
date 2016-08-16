#Initial code from https://gist.github.com/mburst/4700640

from bitarray import bitarray
import mmh3
import math

def is_pow2(num):
    assert(num >=0 )
    return num != 0 and ((num & (num - 1)) == 0)

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
    def __init__(self, size, hash_count):
        assert(is_pow2(size))
        self.size = size
        self.hash_count = hash_count
        self.bit_arrays = []
        while size > 1:
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
        #iterate from the deepest array to second one
        for level in range(len(self.bit_arrays)-1, 0, -1):
            assert(level-1 >= 0)
            for loc in range(len(self.bit_arrays[level])):
                newbit = self.bit_arrays[level-1][loc*2] or \
                         self.bit_arrays[level-1][loc*2 +1]
                self.bit_arrays[level][loc] = newbit

        self.bit_arrays[0].setall(0)

    def num_levels(self):
        return len(self.bit_arrays)