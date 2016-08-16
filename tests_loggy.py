import loggy_bloom as lb

def largedicttest():
    bf = lb.LoggyBloomFilter1(2**19, 7)
    huge = []
    lines = open("words.txt").read().splitlines()
    for line in lines:
        bf.add(line)
        huge.append(line)


def basic():
    str1 = "Hello"
    bf = lb.LoggyBloomFilter1(512, 4)
    assert(bf.lookup(str1) == -1)
    bf.add(str1)
    assert(bf.lookup(str1) == 0)
    bf.shift()
    assert(bf.lookup(str1) == 1)

basic()