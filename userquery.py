__author__ = 'jbollin'
import sys
import credsfinder
import re
"""Script that takes three CLI arguments.  NTDS output file, Hashcat output file, and a list of usernames that
you would like to find what their passwords are. The user list is line separated and case sensitive.  The output
generated is the username password and hash of each of the users"""
userlist = []
__file__ , hashcatoutput, ntdsdump, userquery = sys.argv

with open(ntdsdump, mode="rb") as ntdsDumpFile:
    with open(hashcatoutput, mode="rb") as hashcatfile:
        history = re.compile(r"_(nt|lm)history")
        dic, uncracked = credsfinder.gen_dict(ntdsDumpFile,hashcatfile)

with open(userquery, mode="rb") as userqueryfile:
    for line in userqueryfile:
        userlist.append(line.rstrip())

for user in userlist:
    if re.search(history,user) is None:
        password,phash = credsfinder.userquery(user,dic)
        if password:
            print user, password, phash

