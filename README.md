# loggy-bloom
Testing out an idea for a bloom filter variant

Requires python3, bitarray, and mmh3

Basic idea - have a cascade of bloom filters. For example of size 2^n, 2^(n-1), all the way down to 2^0. In regular operation, set() sets bits in the topmost 2^n-sized filter. At some point, shift() is called. This results in the 2-bit filter feeding OR'd bits to the 1-bit filter, the 4-bit filter feeding OR'd bits to the 2-bit filter, and so on. The 2^n bit filter would have all blank bits. This type of data structure offers two neat things. One is being able to have "fuzzy memory" where after a shift(), the error rate on all stored data goes up, but frees up space to remember new things. This means that the oldest-seen data has the highest error rate, and the freshest data has the lowest error rate. The second is being able to roughly estimate when an object was seen (false positives but no false negatives for a given period between two shift()'s).

The other way of implementing this cascade is to have the cascade only feed 2 bits from the topmost filter each shift(). This makes it harder to calculate hash indeces, but allows a "probabilistic" forgetfullness where each time period has a gradual increase in error rate, as opposed to factors of 2.