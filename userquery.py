__author__ = 'jbollin'
import sys
import credsfinder
import re

userlist = []

with open(sys.argv[1], mode="rb") as f1:
    with open(sys.argv[2], mode="rb") as f2:
        history = re.compile(r"_(nt|lm)history")
        dic, uncracked = credsfinder.gen_dict(f1,f2)

with open(sys.argv[3], mode="rb") as f:
    for line in f:
        userlist.append(line.rstrip())

for user in userlist:
    if re.search(history,user) is not None:
        password,phash = credsfinder.userquery(user,dic)
        print user, password, phash

