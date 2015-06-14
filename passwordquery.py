__author__ = 'jbollin'
import sys
import credsfinder

passlist = []
__file__ , ntdsdump, hashcatoutput, passwordquery = sys.argv
with open(ntdsdump, mode="rb") as ntdsDumpFile:
    with open(hashcatoutput, mode="rb") as hashcatfile:
        dic, uncracked = credsfinder.gen_dict(ntdsDumpFile,hashcatfile)

with open(sys.argv[3], mode="rb") as passwordquery:
    for line in passwordquery:
        passlist.append(line.rstrip())

for password in passlist:
    users = credsfinder.passquery(password,dic)
    for user in users:
        print user, password


