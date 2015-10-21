#!/usr/bin/python
__author__ = 'rleese'
#Dedupe lines of a single file and returns the lines via stdout
import sys

f = file(sys.argv[1],'r')
lineset = set()
for line in f.readlines():
    lineset.add(line.rstrip())
for line in lineset:
    print line
f.close()
