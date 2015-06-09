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
import pack.statsgen

def runstats(hashcatOutput, ntdsDump):
    allHashSet = set()
    crackedHashSet = set()
    popularPasswordsDict = {}
    uncracked = []
    crackedPWs = []
    # Determine the number of unique hashes processed by placing all ntds dump lines in a set
    for dumpline in ntdsDump:
        allHashSet.add(dumpline.split(":")[1].upper())
    uniqueHashesProcessed = len(allHashSet)

    # Make a dictionary of all users with cracked passwords. Username is the key. Value returned is [plaintextPW,hash]
    crackedCreds, uncracked = credsfinder.gen_dict_user_pass_hash(ntdsDump, hashcatOutput)

    # Determine the number of unique hashes cracked by placing all hashes from the cracked Creds dictionary in to a set.
    for userCreds in crackedCreds.values():
        crackedHashSet.add(userCreds[1])
        # Make a dictionary showing how many times each cracked password has been used
        crackedPWs.append(userCreds[0])
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

    print "%d/%d (%d%%) unique passwords cracked" % \
          (uniqueHashesCracked,
           uniqueHashesProcessed,
           round(float(uniqueHashesCracked) / uniqueHashesProcessed * 100)
          )
    print "%d/%d (%d%%) username/password combinations cracked (includes duplicate passwords across multiple users)\n" % \
          (usernameHashCombosCracked,
           usernameHashCombosProcessed,
           round(float(usernameHashCombosCracked) / usernameHashCombosProcessed * 100)
          )
    if ignoreHistory0:
        print "%d 'history0' hashes ignored\n" % history0hashes

    if showPopularPasswords:
        # Print the stats. These final blocks could easily be broken in to a separate funtion, and instead have this
        # function return uniqueHashesProcessed, uniqueHashesCracked, usernameHashCombosProcessed,
        # usernameHashCombosCracked, popularPasswordsDict

        # Print the top popular passwords
        loop = 0
        print 'Top %d popular passwords:' % popularPasswordCount
        print '\n                     Password | Usage Count'
        print '                    ------------------------'
        # Process and sort the passwords in popularPasswords dictionary
        topPasswordKeys = sorted(popularPasswordsDict.keys(), key=popularPasswordsDict.get, reverse=True)
        while loop < popularPasswordCount:
            try:
                print "%30s: %d" % (topPasswordKeys[loop].rstrip(), popularPasswordsDict[topPasswordKeys[loop]])
            except IndexError:
                print "\nInfo: Not enough unique cracked passwords available to fully fill the popular passwords list\n\n"
                break
            loop += 1


    #run the PACK-0.0.4 statsgen to give stats about password length/complexity/character sets/etc
    statsgen = pack.statsgen.StatsGen()
    statsgen.generate_stats(crackedPWs)
    statsgen.print_stats()
    print "\nTotal number of user/password combinations not cracked: %d" % len(uncracked)
    print ''
    if showUncracked:
        for user in uncracked:
            print user
    print '\n\n************************************************************************************************\n\n'
    return


def helpmsg():
    print "Usage: cracked_hash_stats.py [Options] {<hashcat file> <ntds file>}\n" \
          " Note:  If no options are specified [-p -c 100 -M -H] will be used"\
          "  -h or --help:  This help screen\n" \
          "  -p or --popular: Prints a list of most popular passwords.\n" \
          "                   Defaults to top 100.  Use -c to change count.\n" \
          "  -c or --popcount: Changes the default number of popular passwords\n" \
          "                    output when using the -p option\n" \
          "  -M or --modern: Prints the statistics for current passwords. \n" \
          "  -H or --history: Prints the statistics for history passwords\n" \
          "  -C or --combined: Shows statistics for both current and historical passwords\n"\
          "  -u or --uncracked: Prints statistics for usernames with uncracked passwords\n"
    return

# Set defaults if command arguments are not used
showPopularPasswords = True  # Show a list of most popular passwords
popularPasswordCount = 15  # Number of popular passwords to show
ignoreHistory0 = True  # Ignore history0 entries because history0 is current password
showCombinedStats = False  # Show stats for both modern and history passwords at the same time
showModernStats = False  # Show a separate stats blocks for history passwords and non-history passwords
showHistoryStats = False  # Show a separate stats block for history passwords
showUncracked = False  # Show a separate stats block for usernames with uncracked passwords

if len(sys.argv) < 4:# if no options are specified use default options
    showModernStats = True  # Show a separate stats blocks for history passwords and non-history passwords
    showHistoryStats = True  # Show a separate stats block for history passwords

try:
    opts, args = getopt.getopt(sys.argv[1:], "hm:pc:CMHu",
                               ["help", "popular", "popcount=", "combined", "modern", "history","uncracked="])
except getopt.GetoptError as err:
    helpmsg()
    print str(err)
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        helpmsg()
        sys.exit()
    elif opt in ("-p", "--popular"):
        showPopularPasswords = True
    elif opt in ("-c", "--popcount"):
        popularPasswordCount = int(arg)
    elif opt in ("-C", "--combined"):
        showCombinedStats = True
    elif opt in ("-M", "--modern"):
        showModernStats = True
    elif opt in ("-H", "--history"):
        showHistoryStats = True
    elif opt in ("-u", "--uncracked"):
        showUncracked = True
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


# Prepare contents of the hashcat output file for multiple uses
with open(hashcatOutputArgument, 'r') as hashcatOutputFile:
    hashcatOutput = hashcatOutputFile.readlines()

# Where the real work begins
if showCombinedStats:
    print "********************************    Combined Password Stats     *****************************************"
    runstats(hashcatOutput, ntdsDumpCombined)

if showModernStats:
    print "********************************     Modern Password Stats      *****************************************"
    runstats(hashcatOutput, ntdsDumpModern)

if showHistoryStats:
    print "********************************     History Password Stats      ****************************************"
    runstats(hashcatOutput, ntdsDumpHistory)
