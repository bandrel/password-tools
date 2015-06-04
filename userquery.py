__author__ = 'jbollin'
import sys
import credfinder
import re

userlist = []
dic = userjoin.gen_dict_user_pass_hash(sys.argv[1],sys.argv[2])

with open(sys.argv[3], mode="rb") as f:
    for line in f:
        userlist.append(line.rstrip())

for user in userlist:
    if "_history" in user:
        password,phash = userjoin.query_dic(user,dic)
        print user, password, phash
