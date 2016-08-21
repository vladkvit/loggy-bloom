import loggy_bloom as lb



def basic():
    str1 = "Hello"
    bf = lb.LoggyBloomFilter2(23, 4)
    print(bf)
    #assert(bf.lookup(str1) == -1)
    bf.add(str1)
    #assert(bf.lookup(str1) == 0)
    print(bf)
    bf.shift()
    #assert(bf.lookup(str1) == 1)
    print(bf)
    bf.shift()
    #assert(bf.lookup(str1) == 2)
    print(bf)
    bf.shift()
    # assert(bf.lookup(str1) == 3)
    print(bf)
    bf.lookup("Hello")
    for _ in range(200):
        bf.shift()
        print(bf)
        
    
basic()