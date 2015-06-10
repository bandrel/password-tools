__author__ = 'jbollin'
import sys
import credsfinder
import re

userlist = []

history = re.compile(r"_(nt|lm)history")
dic = credsfinder.gen_dict(sys.argv[1],sys.argv[2])

with open(sys.argv[3], mode="rb") as f:
    for line in f:
        userlist.append(line.rstrip())

for user in userlist:
    if re.search(history,user) is not None:
        password,phash = credsfinder.query_dic(user,dic)
        print user, password, phash

for user in userlist:
    if re.search(history,user) is None:
        password,phash = credsfinder.query_dic(user,dic)
        print user, password, phash
