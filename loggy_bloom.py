#Initial code from https://gist.github.com/mburst/4700640

from bitarray import bitarray
import mmh3

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

bf = BloomFilter(500000, 7)
huge = []

#alternative: https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt
lines = open("words.txt").read().splitlines()
for line in lines:
    bf.add(line)
    huge.append(line)

import datetime

start = datetime.datetime.now()
bf.lookup("google")
finish = datetime.datetime.now()
print((finish-start).microseconds)

start = datetime.datetime.now()
for word in huge:
    if word == "google":
        break
finish = datetime.datetime.now()
print((finish-start).microseconds)


print(bf.lookup("Max"))
print(bf.lookup("mice"))
print(bf.lookup("3"))


start = datetime.datetime.now()
bf.lookup("apple")
finish = datetime.datetime.now()
print((finish-start).microseconds)


start = datetime.datetime.now()
for word in huge:
    if word == "apple":
        break
finish = datetime.datetime.now()
print((finish-start).microseconds)