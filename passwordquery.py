__author__ = 'jbollin'
import sys
import credsfinder

passlist = []

with open(sys.argv[1], mode="rb") as f1:
    with open(sys.argv[2], mode="rb") as f2:
        dic, uncracked = credsfinder.gen_dict(f1,f2)

with open(sys.argv[3], mode="rb") as f:
    for line in f:
        passlist.append(line.rstrip())

for password in passlist:
    users = credsfinder.passquery(password,dic)
    for user in users:
        print user, password


