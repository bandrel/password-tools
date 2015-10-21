__author__ = 'rleese'
#returns lines that are of the specified length

''' usage: length_select [password list] [length]

need to add the ability to choose a range of lengths'''

import sys
pwfilepath = sys.argv[1]
length = int(sys.argv[2])
pwfile = open(pwfilepath, 'r')

for line in pwfile.readlines():
    if len(line.rstrip()) == length:
        print line.rstrip()
pwfile.close()

