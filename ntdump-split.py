__author__ = 'jbollin'
import sys
import re

username_and_lmhash = []
username_and_ntlmhash = []
inputfile = sys.argv[1]
lmoutput = str(sys.argv[1]+'.lm')
ntlmoutput = str(sys.argv[1]+'.ntlm')

with open(inputfile) as input:
    for line in input:
        if re.search(r'^SAM.Account.type',line) is None:
            sline = line.strip(':::\n')
            username, userid, lmhash, ntlmhash = sline.split(':')
            username_and_lmhash.append(str(username + ':' + lmhash))
            username_and_ntlmhash.append(str(username + ':' + ntlmhash))

with open(lmoutput,mode='w') as file:
    for line in username_and_lmhash:
        file.write(str(line + '\n'))

with open(ntlmoutput,mode='w') as file:
    for line in username_and_ntlmhash:
        file.write(str(line + '\n'))






