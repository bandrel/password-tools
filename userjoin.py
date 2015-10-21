#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import re
uname = sys.argv[1]
hashfile1 = sys.argv[2]
hashfile2 = sys.argv[3]
userhash = {}
hashpass = {}
with open(hashfile1, mode="rb") as f:
    for line in f:
        username = re.sub(':.*', "", line).rstrip()
        phash = re.sub('.*:', "", line).rstrip()
        userhash[username] = phash
with open(hashfile2, mode="rb") as f:
    for line in f:
        phash = re.sub(':.*', "", line).rstrip()
        password = re.sub('.*:', "", line).rstrip()
        hashpass[phash] = password

try:
    print uname, hashpass[userhash[str(uname)]]
except KeyError:
    print "username not found"
    quit()


