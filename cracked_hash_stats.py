__author__ = 'rleese'
# !/usr/bin/python
'''
Processes a cracked password list from hashcat, compares it to the full original hash dump and spits out statstics
about the cracked passwords.

Usage: cracked-hash-stats.py [hashcat cracked passwords file] [full hash list passwords were cracked from]
'''

import sys
import re
import credsfinder

# Change to True to output a list of usernames matched with passwords
matchPasswordsToUsers = False
# Change to True to output a list of most popular passwords
showPopularPasswords = True
# Ignore the latest history entry for every use because it's always the same as the user's current password
ignoreHistory0 = True
# Show stats for both modern and history passwords at the same time
showCombinedStats = True
# Show a separate stats blocks for history passwords and non-history passwords
showModernStats = True
# Show a separate stats block for history passwords
showHistoryStats = True

hashcatOutputArgument = sys.argv[1]
ntdsDumpArgument = sys.argv[2]

ntdsDumpCombined = []
ntdsDumpModern = []
ntdsDumpHistory = []

uniqueHashesProcessedCombined = 0
uniqueHashesCrackedCombined = 0
usernameHashCombosProcessedCombined = 0
usernameHashCombosCrackedCombined = 0

uniqueHashesProcessedModern = 0
uniqueHashesCrackedModern = 0
usernameHashCombosProcessedModern = 0
usernameHashCombosCrackedModern = 0

uniqueHashesProcessedHistory = 0
uniqueHashesCrackedHistory = 0
usernameHashCombosProcessedHistory = 0
usernameHashCombosCrackedHistory = 0



#create processed ntds dumps based on the options specified above
with open(ntdsDumpArgument, 'r') as ntdsDumpFile:
    for line in ntdsDumpFile.readlines():
        if ignoreHistory0 and line.find('_history0'):
            break
        else:
            ntdsDumpCombined.append(line.rstrip())

        if showModernStats:
            if not line.find('_history'):
                ntdsDumpModern.append(line.rstrip())

        if showHistoryStats:
            if line.find('history'):
                ntdsDumpHistory.append(line.rstrip())


def runstats(ntdsDump):
    uniqueHashesCracked = 0
    uniqueHashesProcessed = 0

    usernameHashCombosCracked = 0
    usernameHashCombosProcessed = 0


    # Determine the number of unique hashes processed by placing all ntds dump lines in a set
    allHashSet = set()
    for dumpline in ntdsDump:
        usernameHashCombosProcessed += 1
        allHashSet.add(dumpline.split(":")[1].upper())
    uniqueHashesProcessed = len(allHashSet)

    credsfinder.gen_dict_user_pass_hash(,ntdsDump)
        #
        #








    # Output file from hashcat in the default [hash]:[cleartext password] format
    hashcatCrackedOuput = file(sys.argv[1], "r")

    # File to output matched user names and passwords
    if matchPasswordsToUsers:
        matchedfile = file("matched.txt", "w")

    if showPopularPasswords:
        popularPasswordsDict = {}
        # max number of popular passwords to display in the results
        popularCount = 25





    # Go through every cracked password, count the total number of usernames that have thier hashes cracked
    # as well as the number of UNIQUE hashes cracked.
    for line in hashcatCrackedOuput.readlines():
        hash = line.split(":")[0]
        cleartextPW = line.split(":")[1]
        # convert all hashes to upper to avoid case sensitivity issues when running find operations.
        hash = hash.upper()
        # Original dump file that has passwords in hashcat [username]:[hash] format
        # hashDumpfile = file(sys.argv[2], "r")
        for dumpline in ntdsDump:
            if dumpline.upper().find(hash) >= 0:
                usernameHashCombosCracked += 1
                if matchPasswordsToUsers:
                    matchedfile.write(cleartextPW + "  " + dumpline.split(":")[0] + "\n")
                if showPopularPasswords:
                    if popularPasswordsDict.has_key(cleartextPW):
                        popularPasswordsDict[cleartextPW] = popularPasswordsDict[cleartextPW] + 1
                    else:
                        popularPasswordsDict[cleartextPW] = 1
        uniqueHashesCracked += 1

    # Print the top popular passwords
    if showPopularPasswords:
        loop = 0
        print 'Top %d popular passwords' % popularCount
        topPasswordKeys = sorted(popularPasswordsDict.keys(), key=popularPasswordsDict.get, reverse=True)
        while loop < popularCount:
            print topPasswordKeys[loop].rstrip() + "    " + str(popularPasswordsDict[topPasswordKeys[loop]])
            loop += 1

    # Count number of hash dump file lines processed as well as the number of unique hashes that are in the dump file
    # May be able to combine this loop with the one above (or not since it needs run only once) ^^^
    # hashDumpfile = file(sys.argv[2], "r")
    for dumpline in ntdsDump:
        usernameHashCombosProcessed += 1
        else:
            usernameHashCombosProcessed += 1
        allHashSet.add(dumpline.split(":")[1].upper())
    uniqueHashesProcessed = len(allHashSet)

    # cleanup
    if matchPasswordsToUsers:
        matchedfile.close()
    hashcatCrackedOuput.close()

    print "\n\n%d/%d (%d%%) unique passwords cracked" % (uniqueHashesCracked,uniqueHashesProcessed,round(float(uniqueHashesCracked) / uniqueHashesProcessed * 100))
    print "%d/%d (%d%%) username/password combinations cracked (includes duplicate passwords across multiple users)" % (usernameHashCombosCracked,usernameHashCombosProcessed,round(float(usernameHashCombosCracked) / usernameHashCombosProcessed * 100))
    if ignoreHistory0:
        print "'*_nthistory0' entries ignored"
