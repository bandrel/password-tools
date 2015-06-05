__author__ = 'rleese'
# !/usr/bin/python
'''
Processes a cracked password list from hashcat, compares it to the full original hash dump and spits out statstics
about the cracked passwords.

Usage: cracked-hash-stats.py [hashcat cracked passwords file] [full hash list passwords were cracked from]
'''

import sys
import credsfinder

def runstats(hashcatOutput, ntdsDump):

    # Determine the number of unique hashes processed by placing all ntds dump lines in a set
    allHashSet = set()
    for dumpline in ntdsDump:
        allHashSet.add(dumpline.split(":")[1].upper())
    uniqueHashesProcessed = len(allHashSet)

    # Make a dictionary of all users with cracked passwords. Username is the key. Value returned is [plaintextPW,hash]
    crackedCreds = credsfinder.gen_dict_user_pass_hash(hashcatOutput, ntdsDump)

    # Determine the number of unique hashes cracked by placing all hashes from the cracked Creds dictionary in to a set.
    for userCreds in crackedCreds.values():
        crackedHashSet.add(userCreds[1])
        # Make a dictionary showing how many times each cracked password has been used
        if showPopularPasswords:
            clearTextPW = userCreds[0]
            if popularPasswordsDict.has_key(userCreds[0]):
                popularPasswordsDict[clearTextPW] = popularPasswordsDict[clearTextPW] + 1
            else:
                popularPasswordsDict[clearTextPW] = 1

    uniqueHashesCracked = len(crackedHashSet)

    # Determine the number of username/hash combos processed
    usernameHashCombosProcessed = len(ntdsDump)

    # Determine the number of username/hash combos cracked
    usernameHashCombosCracked = len(crackedCreds)

    if showPopularPasswords:
        for password in
        if popularPasswordsDict.has_key(clearTextPW):
            popularPasswordsDict[clearTextPW] = popularPasswordsDict[clearTextPW] + 1
        else:
            popularPasswordsDict[clearTextPW] = 1

    # Print the stats. These final blocks could easily be broken in to a separate funtion, and instead have this
    # function return uniqueHashesProcessed, uniqueHashesCracked, usernameHashCombosProcessed,
    # usernameHashCombosCracked, popularPasswordsDict

    # Print the top popular passwords
        loop = 0
        print 'Top %d popular passwords' % popularPasswordCount
        topPasswordKeys = sorted(popularPasswordsDict.keys(), key=popularPasswordsDict.get, reverse=True)
        while loop < popularPasswordCount:
            print topPasswordKeys[loop].rstrip() + "    " + str(popularPasswordsDict[topPasswordKeys[loop]])
            loop += 1

    print "\n\n%d/%d (%d%%) unique passwords cracked" % (uniqueHashesCracked,uniqueHashesProcessed,round(float(uniqueHashesCracked) / uniqueHashesProcessed * 100))
    print "%d/%d (%d%%) username/password combinations cracked (includes duplicate passwords across multiple users)" % (usernameHashCombosCracked,usernameHashCombosProcessed,round(float(usernameHashCombosCracked) / usernameHashCombosProcessed * 100))
    if ignoreHistory0:
        print "%d 'history0' hashes ignored" % history0hashes


    return uniqueHashesProcessed, uniqueHashesCracked, usernameHashCombosProcessed, usernameHashCombosCracked, popularPasswordsDict

# Change to True to output a list of usernames matched with passwords
matchPasswordsToUsers = False
# Change to True to output a list of most popular passwords
showPopularPasswords = True
# Number of popular passwords to show
popularPasswordCount = 100
# Ignore the latest history entry for every use because it's always the same as the user's current password
ignoreHistory0 = True
# Show stats for both modern and history passwords at the same time
showCombinedStats = True
# Show a separate stats blocks for history passwords and non-history passwords
showModernStats = True
# Show a separate stats block for history passwords
showHistoryStats = True

# Prepare variables
hashcatOutputArgument = sys.argv[1]
ntdsDumpArgument = sys.argv[2]

popularPasswordsDict = {}

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

history0hashes = 0


#create processed ntds dumps based on the options specified above. These will be input in to runstats()
with open(ntdsDumpArgument, 'r') as ntdsDumpFile:
    for line in ntdsDumpFile.readlines():
        if ignoreHistory0 and line.find('_history0'):
            history0hashes += 1
            break
        else:
            if showCombinedStats:
                ntdsDumpCombined.append(line.rstrip())
            if showModernStats:
                if not line.find('_history'):
                    ntdsDumpModern.append(line.rstrip())
            if showHistoryStats:
                if line.find('history'):
                    ntdsDumpHistory.append(line.rstrip())

# # File to output matched user names and passwords
# if matchPasswordsToUsers:
#     matchedfile = file("matched.txt", "w")

# Prepare contents of the hashcat output file for multiple uses
with open(hashcatOutputArgument, 'r') as hashcatOutputFile:
    hashcatOutput = hashcatOutputFile.readlines()

# Where the real work begins
if showCombinedStats:
    print "********************************" \
          "    Combined Password Stats     " \
          "********************************"
    runstats(hashcatOutput, ntdsDumpCombined)

if showModernStats:
    print"********************************" \
         "     Modern Password Stats      " \
         "********************************"
    runstats(hashcatOutput, ntdsDumpModern)

if showHistoryStats:
    print"********************************" \
         "     History Password Stats     " \
         "********************************"
    runstats(hashcatOutput, ntdsDumpHistory)






