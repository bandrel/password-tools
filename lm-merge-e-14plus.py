#!/usr/bin/env python
__author__ = 'jbollin'
import sys
username = ""
file = sys.argv[1]
passl = []
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

with open(file,mode="r") as infile:
    lines = infile.read().splitlines()
    for line in lines:
        try:
            a = line.split(":")
            if username != a[0]:
                username = a[0]
                firsthalf = a[2]
            else:
                secondhalf = a[2]
                password = str(firsthalf).strip('\n') + str(secondhalf).strip('\n')
                passl.append(password)
                username = ""
        except IndexError:
            pass
dudupe = f7(passl)
for password in dudupe:
    if len(str(password)) > 13:
        print password



