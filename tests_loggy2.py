import loggy_bloom as lb



def basic():
    str1 = "Hello"
    bf = lb.LoggyBloomFilter2(23, 4)
    print(bf)
    assert(bf.lookup(str1) == -1)
    bf.add(str1)
    
    for i in range(200):
        assert(bf.lookup(str1) == i)
        bf.shift()
        print(bf)
        continue
        
    
basic()