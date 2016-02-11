#!/usr/bin/python
__author__ = 'rleese'
'''Processes a cracked password list from hashcat, compares it to the
full original hash dump and spits out statstics about the cracked
passwords.
Usage: cracked-hash-stats.py [hashcat cracked passwords file] [full
hash list passwords were cracked from]
'''

import sys
import credsfinder
import getopt
import pack.statsgen
import collections
from decimal import *


def runstats(hcoutput, ntdsdump):
    allhashset = set()
    crackedhashset = set()
    popularpwsdict = collections.defaultdict(int)
    crackedpws = []
    # Determine the number of unique hashes processed by placing all ntds dump
    # lines in a set.
    for dumpline in ntdsdump:
        try:
            allhashset.add(dumpline.split(':')[1].lower())
        except IndexError:
            print "Warning: line containing '" + dumpline + "' not processed"
    uniquepwsran = len(allhashset)

    # Make a dictionary of all users with cracked passwords. Username is the
    # key. Key values are returned as [plaintextPW,hash].
    crackedcreds, uncracked = credsfinder.gen_dict(ntdsdump, hcoutput)

    # Determine the number of unique hashes cracked by placing all hashes from
    # the cracked Creds dictionary in to a set.
    for userCreds in crackedcreds.values():
        crackedhashset.add(userCreds[1])
        # Track cracked passwords (including duplicates) for running PACK
        # stats.
        crackedpws.append(userCreds[0])
        # Make a dictionary showing how many times each cracked password has
        # been used.
        if showPopularPasswords:
            cleartextpw = userCreds[0]
            popularpwsdict[cleartextpw] += 1

    uniquepwscracked = len(crackedhashset)
    # Determine the number of username/hash combos processed.
    userpwcombossran = len(ntdsdump)
    # Determine the number of username/hash combos cracked.
    userpwcomboscracked = len(crackedcreds)
    try:
        uniquepercentcracked = Decimal(str(float(uniquepwscracked) / uniquepwsran))
    except ZeroDivisionError:
        uniquepercentcracked = 0
    print '{}/{} ({:.2%}) unique passwords cracked'.format(
        uniquepwscracked, uniquepwsran, uniquepercentcracked)
    try:
        percentcracked = Decimal(str(float(userpwcomboscracked) / userpwcombossran))
    except ZeroDivisionError:
        percentcracked = 0
    print '{}/{} ({:.2%}) username/password combinations cracked ' \
          '(includes duplicate passwords across multiple users)\n'.format(
              userpwcomboscracked, userpwcombossran, percentcracked)

    if ignoreHistory0:
        print '%d "history0" hashes ignored' % history0hashes
    if ignoreBlankPWUsers:
        print '%d users with hashes of blank passwords ignored\n' % blankPWUsers
    if showPopularPasswords:
        # Print the stats. These final blocks could easily be broken in to a
        # separate funtion, and instead have this function return uniquepwsran,
        # uniquepwscracked, userpwcombossran, userpwcomboscracked,
        # popularpwsdict.

        # Print the top popular passwords.
        print 'Top %d popular passwords:' % popularPasswordCount
        print '\n                               Password | Usage Count'
        print '                              ------------------------'
        # Process and sort the passwords in popularPasswords dictionary
        toppwkeys = sorted(
            popularpwsdict.keys(), key=popularpwsdict.get, reverse=True)
        for count in xrange(popularPasswordCount):
            try:
                print '%40s: %d' % (
                    toppwkeys[count].rstrip(),
                    popularpwsdict[toppwkeys[count]])
            except IndexError:
                print '\nInfo: Not enough unique cracked passwords ' \
                      'available to fully fill the popular passwords list\n\n'
                break

    # Run the PACK-0.0.4 statsgen to give stats about
    # password length/complexity/character sets/etc.
    statsgen = pack.statsgen.StatsGen()
    statsgen.generate_stats(crackedpws)
    statsgen.print_stats()
    print '\nTotal number of user/password ' \
          'combinations not cracked: %d' % len(uncracked)
    print ''
    if showUncracked:
        for user in uncracked:
            print user
    print '\n\n*************************************************************' \
          '***********************************\n\n'
    return


def helpmsg():
    print 'Usage: cracked_hash_stats.py [Options] ' \
          '{<hashcat file> <ntds file>}\n' \
          ' Note:  If no options are specified [-p -c 15 -M -H] will be ' \
          'used\n' \
          '  -h or --help:  This help screen\n' \
          '  -p or --popular: Prints a list of most popular passwords.\n' \
          '                   Defaults to top 100.  Use -c to change ' \
          'count.\n' \
          '  -c or --popcount: Changes the default number of popular\n' \
          '                    passwords output when using the -p option\n' \
          '  -M or --modern: Prints the statistics for current passwords. \n' \
          '  -H or --history: Prints the statistics for history passwords\n' \
          '  -C or --combined: Shows statistics for both current and ' \
          'historical passwords\n'\
          '  -u or --uncracked: Prints usernames with uncracked passwords\n' \
          '  -b or --blank: Includes users with hashes of blank passwords\n'
    return


# Set defaults if command arguments are not used
showPopularPasswords = True  # List top x most popular passwords
popularPasswordCount = 15
ignoreHistory0 = True  # Ignore history0 entries *_history0 hashes
showModernStats = True  # Show a stats block for current passwords
showHistoryStats = False  # Show a stats block for history passwords
showCombinedStats = False  # Combine stats of both modern and history passwords
showUncracked = False  # Print usernames with uncracked passwords
ignoreBlankPWUsers = True  # Ignore users whose hash == blank password
getcontext().rounding = ROUND_HALF_UP  # Configure proper rounding for decimal module

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hm:pc:CMHub',
                               ['help', 'popular', 'popcount=', 'combined',
                                'modern', 'history', 'uncracked=', 'blank'])
except getopt.GetoptError as err:
    helpmsg()
    print str(err)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        helpmsg()
        sys.exit()
    elif opt in ('-p', '--popular'):
        showPopularPasswords = True
    elif opt in ('-c', '--popcount'):
        popularPasswordCount = int(arg)
    elif opt in ('-C', '--combined'):
        showCombinedStats = True
    elif opt in ('-M', '--modern'):
        showModernStats = True
    elif opt in ('-H', '--history'):
        showHistoryStats = True
    elif opt in ('-u', '--uncracked'):
        showUncracked = True
    elif opt in ('-b', '--blank'):
        ignoreBlankPWUsers = False
try:
    hashcatOutputArgument = args[0]
    ntdsDumpArgument = args[1]
except IndexError:
    helpmsg()
    sys.exit(2)
# Initialize global variables defaults
ntdsDumpCombined = []
ntdsDumpModern = []
ntdsDumpHistory = []
history0hashes = 0
blankPWUsers = 0

# Create processed ntds dumps based on the options specified above. These
# will be input in to runstats() .
with open(ntdsDumpArgument, 'r') as ntdsDumpFile:
    for line in ntdsDumpFile.readlines():
        if ignoreHistory0 and line.find('_nthistory0') > -1:
            history0hashes += 1
        else:
            if ignoreBlankPWUsers:
                if line.find('31d6cfe0d16ae931b73c59d7e0c089c0') > -1:
                    blankPWUsers += 1
                    continue
            if showCombinedStats:
                ntdsDumpCombined.append(line.rstrip())
            if showModernStats:
                if not line.find('_nthistory') > -1:
                    ntdsDumpModern.append(line.rstrip())
            if showHistoryStats:
                if line.find('_nthistory') > -1:
                    ntdsDumpHistory.append(line.rstrip())


# Prepare contents of the hashcat output file for multiple uses
with open(hashcatOutputArgument, 'r') as hashcatOutputFile:
    hashcatOutput = hashcatOutputFile.readlines()

# Where the real work begins
if showCombinedStats:
    print '********************************\n' \
          '    Combined Password Stats\n' \
          '********************************'
    runstats(hashcatOutput, ntdsDumpCombined)

if showModernStats:
    print '********************************\n' \
          '     Modern Password Stats\n' \
          '********************************'
    runstats(hashcatOutput, ntdsDumpModern)

if showHistoryStats:
    print '********************************\n' \
          '     History Password Stats\n' \
          '********************************'
    runstats(hashcatOutput, ntdsDumpHistory)
