import loggy_bloom as lb
import math



def basic():
    str1 = "Hello"
    bf_len = 23
    num_buckets = 3
    bf = lb.LoggyBloomFilter2(bf_len, 4, 3)
    print(bf)
    assert(bf.lookup(str1) == -1)
    bf.add(str1)
    
    print("---")

    for i in range(200):
        print(bf)
        #suppose the first bucket has size k.
        #then the next one stores 2 OR'd bits, and "virtually" is k*2 bits
        #then, each bucket is k*(2^n) virtual bits
        #f[n] represents the "virtual index" of the first bit in a bucket
        #f[n] := f[n-1] + k*(2^(n-1))
        #if f[0] = 0, solving recurrence gives:
        #f[n] = k(2^n-1)
        #solving for N, the bucket, gives:
        #n = log2((k + f[n]) / k)
        last_index = i + bf_len - 1
        bucket = math.log2( ( bf_len + last_index) / bf_len)
        #print( bucket, last_index)
        if( bucket < num_buckets ):
            worst_case_shift = 2 ** bucket
            assert(bf.lookup(str1) <= (i + worst_case_shift))
            assert(bf.lookup(str1) >= (i - worst_case_shift))
        
        bf.shift()
        
        continue
        
    
basic()