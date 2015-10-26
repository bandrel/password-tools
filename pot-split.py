#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import glob

with open(sys.argv[1]) as potfile:
    for line in potfile:
        a = line.split(':')
        print a[1].rstrip('\n')
