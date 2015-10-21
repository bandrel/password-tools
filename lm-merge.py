#!/usr/bin/env python
__author__ = 'jbollin'
import sys
username = ""
file = sys.argv[1]
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
                userpass = username + ":" + password
                print userpass
                username = ""
        except IndexError:
            pass










