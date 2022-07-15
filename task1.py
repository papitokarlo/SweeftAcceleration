""" 
    You are given words. Some words may repeat. For each word, output its number of
    occurrences. The output order should correspond with the input order of appearance of the
    word. See the sample input/output for clarification.
"""

import collections;

n = int(input("Enter input range :"))
d = collections.OrderedDict()

for i in range(n):
    word = input("Input words: ")
    if word in d:
        d[word] +=1
    else:
        d[word] = 1

print(len(d));

for j,v in d.items():
    print(v,end = " ");