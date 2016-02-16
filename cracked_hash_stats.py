#!/usr/bin/python
"""
cracked_hash_stats.py processes a cracked password list from hashcat, compares
it to the full, original hash dump, and returns statstics for the cracked
passwords.

Usage: cracked_hash_stats.py [Options] {<hashcat file> <ntds file>}
If no options are specified, [-p -c 15 -M] will be used.
Run "cracked_hash_stats.py -h" for more command information.


The hashcat input file should have lines in the format of [hash]:[username]
The ntds input file should have lines in the format of [username]:[hash]
"""

import sys
import credsfinder
import getopt
import pack.statsgen
import collections
from decimal import *


def runstats(mode, hcoutput, ntdsdump):
    if not ntdsdump:
        print 'There are no ' + mode + ' passwords\n'
        return
    print '\n********************************\n' \
          '   ' + mode + ' Password Stats\n' \
          '********************************'
    allhashset = set()
    crackedhashset = set()
    popularpwsdict = collections.defaultdict(int)
    crackedpws = []
    # Determine the number of unique hashes processed by placing all ntds dump lines in a set.
    for dumpline in ntdsdump:
        try:
            if dumpline.split(':')[1].lower() in allhashset:
                sharedHashSet.add(dumpline.split(':')[1].lower())
            allhashset.add(dumpline.split(':')[1].lower())
        except IndexError:
            print 'Warning: line containing "' + dumpline + '" not processed'
    uniquepwsran = len(allhashset)

    # Make a dictionary of all users with cracked passwords. Username is the key.
    # Key values are returned as [plaintextPW,hash].
    crackedcreds, uncracked = credsfinder.gen_dict(ntdsdump, hcoutput)

    # Determine the number of unique hashes cracked by placing all hashes from the crackedcreds dict in to a set.
    for userCreds in crackedcreds.values():
        crackedhashset.add(userCreds[1])
        # Track cracked PWs (including duplicates) for running PACK stats.
        crackedpws.append(userCreds[0])
        # Make a dict showing how many times each cracked password has been used.
        cleartextpw = userCreds[0]
        popularpwsdict[cleartextpw] += 1

    uniquepwscracked = len(crackedhashset)
    userpwcombossran = len(ntdsdump)  # Determine the number of username/hash combos processed.
    userpwcomboscracked = len(crackedcreds)  # Determine the number of username/hash combos cracked.
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

    print '%d "history0" hashes ignored' % history0hashes
    if ignoreBlankPWUsers:
        print '%d users with hashes of blank passwords ignored\n' % blankPWUsers

    print 'Top %d popular passwords:' % popularPasswordCount
    print '\n                               Password | Usage Count'
    print '                              ------------------------'
    # Process and sort the passwords in popularPasswords dictionary.
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

    # Run the PACK-0.0.4 statsgen to give stats about password length/complexity/character sets/etc.
    statsgen = pack.statsgen.StatsGen()
    statsgen.generate_stats(crackedpws)
    statsgen.print_stats(uniquepwscracked)
    print '\nTotal number of user/password ' \
          'combinations not cracked: %d' % len(uncracked)
    print ''
    if outputUncracked:
        with open(mode + '-' + uncrackedOutputfile, 'w') as outputfile:
            for user in uncracked:
                outputfile.write(user + '\n')
            print 'Uncracked usernames output to ' + str(uncrackedOutputfile)
    print '\n\n*************************************************************' \
          '***********************************\n\n'
    if writeOutShared:
        with open(mode+'-'+sharedOutputFile, 'w') as f:
            for sharedHash in sharedHashSet:
                for currentline in ntdsdump:
                    if sharedHash.lower() == currentline.split(':')[1].lower():
                        f.write(currentline.split(':')[0] + '\t' + sharedHash.lower() + '\n')
    # Write out usernames & passwords of users that match the "interestingNames" contents.
    if writeOutInteresting:
        with open(mode + '-' + interestingOutputFile, 'w') as f:
            for iname in interestingNames:
                for name in crackedcreds.keys():
                    if iname in name:
                        f.write(name + '\t' + crackedcreds[name][0] + '\n')
    if writeOutCracked is True:
        outputcracked(mode, hcoutput, ntdsdump)
    return


def outputcracked(mode, hcoutput, ntdsdump):
    dic, uncracked = credsfinder.gen_dict(ntdsdump, hcoutput)
    with open(mode + '-' + crackedOutputfile, 'w') as output_file:
        for username, password_hash in dic.iteritems():
            if 'history0' in username:
                output_line = str(username) + '\t' + str(password_hash[0]) + '\n'
                output_file.write(output_line)
    return


def helpmsg():
    print '\ncracked_hash_stats.py processes a cracked password list from hashcat, compares\n' \
          'it to the full, original hash dump, and returns statstics for the cracked\n' \
          'passwords.\n' \
          '\n' \
          'Usage: cracked_hash_stats.py [Options] {<hashcat file> <ntds file>}\n' \
          'If no options are specified, [-p -c 15 -M] will be used\n' \
          '\n' \
          'The hashcat file should have lines in the format of [hash]:[username]\n' \
          'The ntds file should have lines in the format of [username]:[hash]\n' \
          '\n' \
          'Options:\n' \
          '\n' \
          '    Modes:\n' \
          '        -M or --modern: Print statistics for current passwords.\n' \
          '        -H or --history: Print statistics for history passwords\n' \
          '        -C or --combined: Print combined statistics of current and history users\n ' \
          '\n' \
          '    File Output:\n'\
          '        -U or --cracked-users <file>: Write cracked usernames to a file.\n'\
          '        -u or --uncracked <file>: Write uncracked usernames to a file.\n' \
          '        -s or --shared <file>: Write a file with users who do not have a unique\n' \
          '            password hash.\n' \
          '        -i or --interesting <file>: Write a file of cracked usernames that\n' \
          '            could be more valuable than average i.e. admin, root, svc, sql, etc\n' \
          '\n' \
          '    Other:\n' \
          '        -c or --popcount <count>: Set number of popular passwords output.\n' \
          '        -b or --blank: Include users with hashes of blank passwords in the statistics\n' \
          '            processing.\n' \
          '        -h or --help:  Show this help screen.\n'
    return

popularPasswordCount = 15
showModernStats = None  # Show a stats block for current passwords
showHistoryStats = None  # Show a stats block for history passwords
showCombinedStats = None  # Show stats of both modern and history passwords combined
ignoreBlankPWUsers = True  # Ignore users whose hash == blank password
getcontext().rounding = ROUND_HALF_UP  # Configure proper rounding for the decimal module

outputUncracked = False  # Output a list of usernames with uncracked passwords
writeOutCracked = False  # Output a list of cracked usernames and passwords
crackedOutputfile = 'cracked_usernames.txt'
writeOutShared = False  # Output a list of users who have a shared hash
sharedOutputFile = 'users_with_shared_hashes.txt'
sharedHashSet = set()
writeOutInteresting = False  # Output a list of users that meet the interesing criteria
interestingOutputFile = 'interesting_cracked_users.txt'
interestingNames = ('admin', 'svc', 'service', 'root', 'apc', 'altiris', 'sql', 'manage', 'cisco')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hm:c:CMHu:bU:s:i:',
                               ['help', 'popcount=', 'combined', 'modern', 'history',
                                'uncracked=', 'blank', 'shared=', 'cracked-users=', 'interesting='])
except getopt.GetoptError as err:
    helpmsg()
    print str(err)
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        helpmsg()
        sys.exit()
    elif opt in ('-c', '--popcount'):
        popularPasswordCount = int(arg)
    elif opt in ('-C', '--combined'):
        showCombinedStats = True
    elif opt in ('-M', '--modern'):
        showModernStats = True
    elif opt in ('-H', '--history'):
        showHistoryStats = True
    elif opt in ('-u', '--uncracked'):
        outputUncracked = True
        uncrackedOutputfile = arg
    elif opt in ('-b', '--blank'):
        ignoreBlankPWUsers = False
    elif opt in ('-U', '--cracked-users'):
        writeOutCracked = True
        crackedOutputfile = arg
    elif opt in ('-s', '--shared'):
        writeOutShared = True
        sharedOutputFile = arg
    elif opt in ('-i', '--interesting'):
        writeOutInteresting = True
        interestingOutputFile = arg
try:
    hashcatOutputArgument = args[0]
    ntdsDumpArgument = args[1]
except IndexError:
    helpmsg()
    sys.exit(2)

# Intialize global variables
ntdsDumpCombined = []
ntdsDumpModern = []
ntdsDumpHistory = []
history0hashes = 0
blankPWUsers = 0

# Run modern stats if no mode is specified.
if not(showModernStats or showCombinedStats or showHistoryStats):
    showModernStats = True

# Create processed ntds dumps based on the options specified above. These will be given to runstats()
with open(ntdsDumpArgument, 'r') as ntdsDumpFile:
    for line in ntdsDumpFile.readlines():
        if line.find('_nthistory0') > -1:
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


# Prepare contents of the hashcat output file for multiple uses.
with open(hashcatOutputArgument, 'r') as hashcatOutputFile:
    hashcatOutput = hashcatOutputFile.readlines()

if showCombinedStats:
    runstats('Combined', hashcatOutput, ntdsDumpCombined)
if showModernStats:
    runstats('Modern', hashcatOutput, ntdsDumpModern)
if showHistoryStats:
    runstats('History', hashcatOutput, ntdsDumpHistory)
