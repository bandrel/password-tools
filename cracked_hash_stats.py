# !/usr/bin/python
__author__ = 'rleese'
'''
Processes a cracked password list from hashcat, compares it to the full original hash dump and spits out statstics
about the cracked passwords.

Usage: cracked-hash-stats.py [hashcat cracked passwords file] [full hash list passwords were cracked from]
'''

import sys
import credsfinder
import getopt
import operator
def runstats(hashcatOutput, ntdsDump):
    allHashSet = set()
    crackedHashSet = set()
    popularPasswordsDict = {}

    # Determine the number of unique hashes processed by placing all ntds dump lines in a set
    for dumpline in ntdsDump:
        allHashSet.add(dumpline.split(":")[1].upper())
    uniqueHashesProcessed = len(allHashSet)

    # Make a dictionary of all users with cracked passwords. Username is the key. Value returned is [plaintextPW,hash]
    crackedCreds = credsfinder.gen_dict_user_pass_hash(ntdsDump, hashcatOutput)

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
    # Print the stats. These final blocks could easily be broken in to a separate funtion, and instead have this
    # function return uniqueHashesProcessed, uniqueHashesCracked, usernameHashCombosProcessed,
    # usernameHashCombosCracked, popularPasswordsDict

        # Print the top popular passwords
        loop = 0
        print '\nTop %d popular passwords:\n' % popularPasswordCount
        # Process and sort the passwords in popularPasswords dictionary
        topPasswordKeys = sorted(popularPasswordsDict.keys(), key=popularPasswordsDict.get, reverse=True)
        while loop < popularPasswordCount:
            try:
                print topPasswordKeys[loop].rstrip() + "\t\t\t\t" + str(popularPasswordsDict[topPasswordKeys[loop]])
            except IndexError:
                print "\nInfo: Not enough unique cracked passwords available to fully fill the popular passwords list"
                break
            loop += 1

    print "\n\n%d/%d (%d%%) unique passwords cracked" % \
                                             (uniqueHashesCracked,
                                              uniqueHashesProcessed,
                                              round(float(uniqueHashesCracked) / uniqueHashesProcessed * 100)
                                             )
    print "%d/%d (%d%%) username/password combinations cracked (includes duplicate passwords across multiple users)" % \
                                            (usernameHashCombosCracked,
                                             usernameHashCombosProcessed,
                                             round(float(usernameHashCombosCracked) / usernameHashCombosProcessed * 100)
                                            )
    if ignoreHistory0:
        print "\n%d 'history0' hashes ignored\n\n" % history0hashes

    return


#Set defaults if command arguments are not used
matchPasswordsToUsers = False # Change to True to output a list of usernames matched with passwords
showPopularPasswords = False # Change to True to output a list of most popular passwords
popularPasswordCount = 100 # Number of popular passwords to show
ignoreHistory0 = True # Ignore history0 entry because history0 is current password
showCombinedStats = False # Show stats for both modern and history passwords at the same time
showModernStats = True # Show a separate stats blocks for history passwords and non-history passwords
showHistoryStats = True # Show a separate stats block for history passwords
matchedfile = ""
#System arguments for input and output files
try:
    opts, args = getopt.getopt(sys.argv[1:],"hm:pc:CMH",["help","hashcat=","ntds=","match=","popular","popcount=",
                                                          "combined","modern","history"])
except getopt.GetoptError as err:
    print 'cracked_hash_stats.py -1 <hashcat file> -2 [ntds] \n' \
          ' OR \n' \
          'cracked_hash_stats.py --hashcat <hashcat file> --ntds <ntds file>\n'
    print str(err)
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print 'cracked_hash_stats.py -1 <hashcat file> -2 [ntds] \n' \
              ' OR \n' \
              'cracked_hash_stats.py --hashcat <hashcat file> --ntds <ntds file>\n'
        sys.exit()
    elif opt in ("-p", "--popular"):
        showPopularPasswords = operator.not_(showPopularPasswords)
    elif opt in ("-c", "--popcount"):
        popularPasswordCount = int(arg)
    elif opt in ("-C", "--combined"):
        showCombinedStats = operator.not_(showCombinedStats)
    elif opt in ("-M", "--modern"):
        showModernStats = operator.not_(showModernStats)
    elif opt in ("-H", "--history"):
        showHistoryStats = operator.not_(showHistoryStats)

hashcatOutputArgument = args[0]
ntdsDumpArgument = args[1]


# Initialize global variables defaults
ntdsDumpCombined = []
ntdsDumpModern = []
ntdsDumpHistory = []
history0hashes = 0



# create processed ntds dumps based on the options specified above. These will be input in to runstats()
with open(ntdsDumpArgument, 'r') as ntdsDumpFile:
    for line in ntdsDumpFile.readlines():
        if ignoreHistory0 and line.find('_nthistory0') > -1:
            history0hashes += 1
        else:
            if showCombinedStats:
                ntdsDumpCombined.append(line.rstrip())
            if showModernStats:
                if not line.find('_nthistory') > -1:
                    ntdsDumpModern.append(line.rstrip())
            if showHistoryStats:
                if line.find('_nthistory') > -1:
                    ntdsDumpHistory.append(line.rstrip())

# # File to output matched user names and passwords
#if matchPasswordsToUsers:
#     matchedfile = file("matched.txt", "w")

# Prepare contents of the hashcat output file for multiple uses
with open(hashcatOutputArgument, 'r') as hashcatOutputFile:
    hashcatOutput = hashcatOutputFile.readlines()

# Where the real work begins
if showCombinedStats:
    print "********************************    Combined Password Stats     ********************************"
    runstats(hashcatOutput, ntdsDumpCombined)

if showModernStats:
    print"********************************     Modern Password Stats      ********************************"
    runstats(hashcatOutput, ntdsDumpModern)

if showHistoryStats:
    print"********************************     History Password Stats      ********************************"
    runstats(hashcatOutput, ntdsDumpHistory)
