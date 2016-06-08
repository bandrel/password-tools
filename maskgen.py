#!/usr/bin/python
__author__ = 'jbollin'
'''Processes a cracked password list and returns a list of masks used in the passwords.  The file is sorted by
frequency of use.
'''

import sys
import string
import operator
import getopt
from tabulate import tabulate

def calc_mask(password):
    mask = ''
    for x in password:
        if x in string.digits:
            mask += '?d'
        elif x in string.uppercase:
            mask += '?u'
        elif x in string.lowercase:
            mask += '?l'
        else:
            mask += '?s'
    return mask
def helpmsg():
    print 'Usage: maskgen.py <dictionary> [options]   \n' \
          ' Note:  If no options are specified [-p -c 15 -M -H] will be used\n' \
          '  -h or --help:  This help screen\n' \
          '  -n or --results:  Limits the number of results.  Defaults to display all results\n'
    return

num_results = 999999
include_totals = False

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hn:t', ['help', 'results=', 'totals'])
except getopt.GetoptError as err:
    helpmsg()
    print str(err)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        helpmsg()
        sys.exit()
    elif opt in ('-n', '--results'):
        num_results = int(arg)
    elif opt in ('-t', '--totals'):
        include_totals = True

uniquemasks = {}
try:
    dictionary = args[0]
except:
    helpmsg()
    sys.exit(2)
with open(dictionary, mode="rb") as passwords:
    for password in passwords:
        mask = calc_mask(password.rstrip())
        try:
            uniquemasks[mask] += 1
        except KeyError:
            uniquemasks[mask] = 1
items = sorted(uniquemasks.items(), key=operator.itemgetter(1), reverse=True)[0:num_results]

if include_totals:
    print tabulate(items, headers=["Masks","Total number of instances"],tablefmt="simple")
else:
    print('Masks')
    print('--------------------')
    for item in items:
        print item[0]











