#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import glob

pots = glob.glob('*.pot')
everything = set()
with open(sys.argv[1],'w') as b:
    for pot in pots:
        with open(pot) as file:
            for line in file:
                a = line.split(':')
                if len(a[0]) > 16:
                    everything.add(line)

    for line in everything:
        b.write(line)



