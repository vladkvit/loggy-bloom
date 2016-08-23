import loggy_bloom as lb

bf = lb.BloomFilter(500000, 7)
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

assert(bf.lookup("Max") == "Probably")
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