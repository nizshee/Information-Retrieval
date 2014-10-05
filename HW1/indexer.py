#!/usr/bin/python3

import pymorphy2
import os, sys

import support as sp

if len(sys.argv) != 3:
    sys.exit("Arguments!")
dict_db = sys.argv[1]
file_index = sys.argv[2]

morph = pymorphy2.MorphAnalyzer()

file_count = 0
file_dict = {}

index = {}
for root, dirs, files in os.walk(dict_db):
    for fl in files:
        file_count += 1
        file_dict[file_count] = fl
        print(fl)
        f = open(root + "/" + fl)
        for ln in f:
            ls = ln.strip().split()
            for string in ls:
                word = sp.to_word(string)
                if not sp.is_russian(word):
                    continue

                st = set()
                for form in morph.parse(word):
                    st.add(form.normal_form)

                for i in st:
                    if i not in index:
                        index[i] = set()
                    index[i].add(file_count)
        f.close()

f = open(file_index,'w')

for i in file_dict:
    f.write(file_dict[i] + ":" + str(i) + " ")
f.write("\n")

for i in index:
    f.write(i + ":")
    for j in index[i]:
        f.write(str(j) + ",")
    f.write("\n")

f.close()