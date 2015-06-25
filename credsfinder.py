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
        userhash[username] = phash.lower()
    for item in hash_pass_list:
        # Splits the username and password hash into two variables using a
        # colon as the delimiter.  In the event that there is a a colon in
        # the plaintext password then the line will be split at the first
        # colon.
        phash, password = item.rstrip().split(":",1)
        # Stores the plaintext password into the hashpass dict
        hashpass[phash.lower()] = password

    # Combine the userhash and userpass dictionaries in to a single
    # userpasshash dictionary.
    for user in userhash.keys():
        # Check to see if there is a cracked password for the user.  If
        # password is not found then KeyError will occur
        try:
            # Defines hash lookup per user.
            hashquery = userhash[user]
            # Defines password lookup per hash.
            passwordquery = hashpass[hashquery]

            # Creates a dictionary with using the username as the key with
            # the password/hash combination as the content.
            userpasshash[user] = [passwordquery,hashquery]
        except KeyError:
            # User doesn't have a cracked password.  Add username to uncracked
            # list and continue
            uncracked.append(user)
            pass
    return userpasshash,uncracked

def query_dic(userquery,dic):
    password = dic[userquery][0]
    phash = dic[userquery][1]
    return password,phash
