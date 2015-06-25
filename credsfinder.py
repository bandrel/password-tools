#!/usr/bin/env python
__author__ = 'jbollin'



def gen_dict(user_hash_list, hash_pass_list):
    """Function to generate a dictionary that contains usernames as the keys
    with password and hash.  Requires the input of lists containing
    username:hash and a hash:crackedpasswords"""
    # initialize local variables
    userhash = {}
    hashpass = {}
    userpasshash = {}
    uncracked = []
    for item in user_hash_list:
        # Splits the username and password hash into two variables
        username, phash = item.rstrip().split(":")
        # Stores the password hash into the userhash dict
        userhash[username] = phash
    for item in hash_pass_list:
        # Splits the username and password hash into two variables using a
        # colon as the delimiter.  In the event that there is a a colon in
        # the plaintext password then the line will be split at the first
        # colon.
        phash, password = item.rstrip().split(":",1)
        # Stores the plaintext password into the hashpass dict
        hashpass[phash] = password

    # Combine the userhash and userpass dictionaries in to a single
    # userpasshash dictionary.
    for user in userhash.keys():
        # Check to see if there is a cracked password for the user.  If
        # password is not found then KeyError will occur
        try:
            #defines hash lookup per user
            hashquery = userhash[user]
            #defines password lookup per hash.
            passwordquery = hashpass[hashquery]

            # Creates a dictionary with using the username as the key with
            # the password/hash combination as the content.
            userpasshash[user] = [passwordquery,hashquery]
        except KeyError:
            # User doesn't have a cracked password.  Add username to uncracked
            # list and continue
            uncracked.append(user)
            pass
    return userpasshash, uncracked

""" Function accepts a username in the form of a string and a dictionary generated by gen_dict().  The function
iterates through each key of the dictionary until it finds the value associated with the string.  The password and
hash of the matching username are returned"""

def userquery(uquery,dic):
    try:
        password = dic[uquery][0]
        phash = dic[uquery][1]
    except KeyError:
        return None, None
    return password,phash

""" Function accepts a password in the form of a string and a dictionary generated by gen_dict().  The function
iterates through each key of the dictionary until it finds the value associated with the string.  The usernames
assoicated with the password are returned but the hash is not."""

def passquery(pquery,dic):
    usernames = set()
    for user, values in dic.iteritems():
        if values[0] == pquery:      # Check to see if the password stored in the dictionary matches the queried pass
            usernames.add(user)         # If the password matches then add the username to the username set
    return usernames

""" Function accepts a hash in the form of a string and a dictionary generated by gen_dict().  The function iterates
through each key of the dictionary until it finds the value associated with the string.  The key of the dictionary
item is then returned along with the password that matches the hash"""


def hashquery(hquery,dic):
    usernames = set()
    password = ""
    for user, values in dic.iteritems():
        if values[1] == hquery:      # Check to see if the hash stored in the dictionary matches the queried hash
            usernames.add(user)         # If the password matches then add the username to the username set
            password = values[0]     # Also sets the password that is listed in the dictionary.
    return usernames, password

