__author__ = 'rleese'
# !/usr/bin/python

# Processes a cracked password list from hashcat, compares it to the full original hash dump and spits out statstics
# about the cracked passwords.

# Usage: cracked-hash-stats.py [hashcat cracked passwords file] [full hash list passwords were cracked from]

import sys

# Change to True to output a list of usernames matched with passwords
matchPasswordsToUsers = False
# Change to True to output a list of most popular passwords
showPopularPasswords = True

# Output file from hashcat in the default [hash]:[cleartext password] format
hashcatCrackedOuput = file(sys.argv[1], "r")

# File to output matched user names and passwords
if matchPasswordsToUsers:
    matchedfile = file("matched.txt", "w")

if showPopularPasswords:
    popularPasswordsDict = {}
    # max number of popular passwords to display in the results
    popularCount = 25

uniqueHashesCracked = 0
totalHashesCracked = 0
totalHashesProcessed = 0

#a set used to calculate the number of unique hashes in the hashcatCrackedOuput
allHashSet = set()

# Go through every cracked password, count the total number of usernames that have thier hashes cracked
# as well as the number of UNIQUE hashes cracked.
for line in hashcatCrackedOuput.readlines():
    hash = line.split(":")[0]
    cleartextPW = line.split(":")[1]
    # convert all hashes to upper to avoid case sensitivity issues when running find operations.
    hash = hash.upper()
    # Original dump file that has passwords in hashcat [username]:[hash] format
    hashDumpfile = file(sys.argv[2], "r")
    for dumpline in hashDumpfile.readlines():
        if dumpline.upper().find(hash) >= 0:
            totalHashesCracked += 1
            if matchPasswordsToUsers:
                matchedfile.write(cleartextPW + "  " + dumpline.split(":")[0] + "\n")
            if showPopularPasswords:
                if popularPasswordsDict.has_key(cleartextPW):
                    popularPasswordsDict[cleartextPW] = popularPasswordsDict[cleartextPW] + 1
                else:
                    popularPasswordsDict[cleartextPW] = 1

    hashDumpfile.close()
    uniqueHashesCracked += 1

if showPopularPasswords:
    loop = 0
    print 'Top %d popular passwords' % popularCount
    topPasswordKeys = sorted(popularPasswordsDict.keys(), key=popularPasswordsDict.get, reverse=True)
    while loop < popularCount:
        print topPasswordKeys[loop].rstrip() + "    " + str(popularPasswordsDict[topPasswordKeys[loop]])
        loop += 1

#count number of lines processed
hashDumpfile = file(sys.argv[2], "r")
for dumpline in hashDumpfile.readlines():
    totalHashesProcessed += 1
    allHashSet.add(dumpline.split(":")[1].upper())
uniqueHashesProcessed = len(allHashSet)

#cleanup
if matchPasswordsToUsers:
    matchedfile.close()
hashcatCrackedOuput.close()

print "\n\n%d/%d (%d%%) unique passwords cracked" % (uniqueHashesCracked,uniqueHashesProcessed,round(float(uniqueHashesCracked) / uniqueHashesProcessed * 100))
print "%d/%d (%d%%) username/password combinations cracked (includes duplicate passwords across multiple users)" % (totalHashesCracked,totalHashesProcessed,round(float(totalHashesCracked) / totalHashesProcessed * 100))
