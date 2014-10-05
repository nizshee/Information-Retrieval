#!/usr/bin/python3

from sys import stdin
import pymorphy2
import os, sys

import support as sp

if len(sys.argv) != 2:
    sys.exit("Arguments!")
file_index = sys.argv[1]


file_dict = {}
index = {}

ind = True
f = open(file_index)
for ln in f:
    if ind:
        ind =  not ind
        docs = ln.strip().split()
        for i in docs:
            (doc, num) = i.split(":")
            file_dict[int(num)] = doc
    else:
        (word, nums) = ln.strip().split(":")
        index[word] = set([int(i) for i in nums.split(",") if i])

f.close()
#print(file_dict)
#print(index)

morph = pymorphy2.MorphAnalyzer()
request = ""
while True:
    request = stdin.readline()
    if request.strip() == "quit":
        break
    ans = sp.parse_request(request)
    if ans:
        (is_AND, ls) = ans
    else:
        print("    incorrect query")
        continue    
    res = sp.get_docs(index, ls, is_AND)
    if not res:
        print("    no documents found")
    elif len(res) <= 2:
        print("    found ", end="", flush=True)
        for i in res:
            print(file_dict[i] + " ", end="", flush=True)
        print()
    else:
        print("    found ", end="", flush=True)
        count = 0
        for i in res:
            count += 1
            if count == 3:
                break
            print(file_dict[i] + " ", end="", flush=True)
        print("and " + str(len(res) - 2) + " more" )
    

