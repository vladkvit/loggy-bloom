import loggy_bloom as lb
import math



def basic():
    str1 = "Hello"
    bf_len = 23
    bf = lb.LoggyBloomFilter2(bf_len, 4)
    print(bf)
    assert(bf.lookup(str1) == -1)
    bf.add(str1)
    
    for i in range(200):
        #suppose the first bucket can take k shifts before its contents are completely new
        #then the next one is k*2 shifts
        #then, each bucket is k*(2^n) shifts
        #then, the total number of shifts to exceed bucket N from beginning is:
        #f[n] := f[n-1] + k*(2^n)
        #if we hash something, do N shifts, and look at the deepest bucket
        #solving for the index gives:
        #n = log2((k + f[n]) / k) - 1
        #bucket = math.log2( (bf_len + i) / i
        #worst_case_shift = 2 ** deepest_bucket
        #assert(bf.lookup(str1) <= (i + worst_case_shift))
        #assert(bf.lookup(str1) >= (i - worst_case_shift))
        bf.shift()
        print(bf)
        continue
        
    
basic()