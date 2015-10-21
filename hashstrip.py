#!/usr/bin/python
__author__ = 'rleese'
#returns just plain text password from lines that are [hash]:plaintext
import sys
f = file(sys.argv[1],'r')
for line in f.readlines():
    print line.split(':', 1)[1].rstrip()
f.close()
