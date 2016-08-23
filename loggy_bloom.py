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

    def __hash_indeces__(self, string):
        indeces = []
        for seed in range(self.hash_count):
            indeces.append(mmh3.hash(string, seed) % self.size)
        return indeces
        
    def add(self, string):
        for idx in self.__hash_indeces__(string):
            self.bit_array[idx] = 1
            
    def lookup(self, string):
        for idx in self.__hash_indeces__(string):
            if self.bit_array[idx] == 0:
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
    
    def __hash_indeces__(self, string):
        indeces = []
        for seed in range(self.hash_count):
            indeces.append(mmh3.hash(string, seed) % self.size)
        return indeces
                
    def add(self, string):
        for idx in self.__hash_indeces__(string):
            self.bit_arrays[0][idx] = 1
        
    #returns -1 if not found
    #otherwise, returns the most recent / largest level at which 
    #object was found
    def lookup(self, string, maxlevel = math.inf):
        indeces = self.__hash_indeces__(string)

        for level, arr in enumerate(self.bit_arrays):
            if level > maxlevel:
                break

            found = True
            for index in indeces:
                if arr[index//(2**level)] == 0:
                    found = False
                    break

            if found:
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


class Accessor:
    def __init__(self, idx, bank):
        self.idx = idx
        self.bank = bank
    def __str__(self):
        return str(self.idx) + ", " + str(self.bank)

class LoggyBloomFilter2:


    def __init__(self, size, hash_count, num_buckets):
        self.sizes = [size for _ in range(num_buckets)]
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

    def __hash_indeces__(self, string):
        indeces = []
        for seed in range(self.hash_count):
            indeces.append(mmh3.hash(string, seed) % self.sizes[0])
        return indeces

    def add(self, string):
        for idx in self.__hash_indeces__(string):
            self.bit_arrays[0][idx] = 1
        
    #returns -1 if not found
    #otherwise, returns the most recent / largest level at which 
    #object was found
    def lookup(self, string, maxlevel = math.inf):
        indeces = []

        idxs = self.__hash_indeces__(string)
        for index in idxs:
            tup = Accessor(index, 0)
            indeces.append(tup)

        shift_lvl = 0

        numlevels = self.num_levels()
        while shift_lvl < maxlevel and shift_lvl < numlevels:
            #check
            found = True
            for tup in indeces:
                assert(tup.bank < len(self.bit_arrays))
                if self.bit_arrays[tup.bank][tup.idx // (2**tup.bank)] == 0:
                    found = False
                    break

            if found:
                return shift_lvl

            #increment
            for tup in indeces:
                tup.idx += 1
                assert(tup.bank < len(self.sizes))
                assert(tup.bank < len(self.overflows))
                if tup.idx >= self.sizes[tup.bank] * (2**tup.bank) + self.overflows[tup.bank]:
                    tup.idx = 0
                    tup.bank += 1

            shift_lvl += 1

        return -1

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
            counter += (self.sizes[i]) * 2**i

        return counter

    def __str__(self):
        ret = "["
        for idx, arr in enumerate(self.bit_arrays):
            for i, bit in enumerate(arr):
                if i == len(arr)-1 and self.overflows[idx] == 0:
                    ret += ' '
                elif bit:
                    ret += '*'
                else:
                    ret += '.'
            if idx != len(self.bit_arrays)-1:
               ret += '|'
        ret += ']'
        return ret