__author__ = 'jbollin'
import sys
import credsfinder
"""Script that takes three CLI arguments.  NTDS output file, Hashcat output file, and a list of passwords that
you would like to find which users have a password in the list.  The password list is line separated and case
sensitive.  The output generated is the username/password pair since you can user multiple passwords in the password
query file"""

passlist = []
__file__ , ntdsdump, hashcatoutput, passwordquery = sys.argv
with open(ntdsdump, mode="rb") as ntdsDumpFile:
    with open(hashcatoutput, mode="rb") as hashcatfile:
        dic, uncracked = credsfinder.gen_dict(ntdsDumpFile,hashcatfile)

with open(passwordquery, mode="rb") as passwordqueryfile:
    for line in passwordqueryfile:
        passlist.append(line.rstrip())

for password in passlist:
    users = credsfinder.passquery(password,dic)
    for user in users:
        print user, password


