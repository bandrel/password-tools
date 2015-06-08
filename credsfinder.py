#!/usr/bin/env python
__author__ = 'jbollin'
import re

"""Function to generate a dictionary that contains usernames as the keys with password and hash.
Requires the input of lists containing username:hash and a hash:crackedpasswords file"""

def gen_dict_user_pass_hash(user_hash_list, hash_pass_list):
    # initialize variables
    userhash = {}       # Dictionary using username as the key and hash as the content.
    hashpass = {}       # Dictionary using hash as the key and password as the content.
    userpasshash = {}   # Dictionary using username as the key and password and hash as the content.
    uncracked = set()
    for item in user_hash_list:                     # Iteration of each username password hash in list
        username,phash = item.rstrip().split(":")   # Splits the username and password hash into two variables
        userhash[username] = phash                  # Stores the password hash into the userhash dictionary using the
                                                    # user as the key.
    for item in hash_pass_list:                     # Iteration of each password hash and plaintext password in list
        phash,password = item.rstrip().split(":",1) # Splits the username and password hash into two variables using a
                                                    # colon as the delimiter.  In the event that there is a a colon in
                                                    # the plaintext password then the line will be split at the first
                                                    # colon
        hashpass[phash] = password                  # Stores the plaintext password into the hashpass dictionary
                                                    # using the hash as the key.

    # Combine the userhash and userpass dictionaries in to a single userpasshash dictionary.
    for user in userhash.keys():                    #iterates through each unique user
        try:                                        #Check to see if there is a cracked password for the user
            hashquery = userhash[user]              # looks up the hash associated with the user
            passwordquery = hashpass[hashquery]     # Looks up hash assoicated with user then looks up password
                                                    # associated with password
            userpasshash[user] = [passwordquery,hashquery]  # creates a dictionary with using the username as the key
                                                            # with the password/hash combination as the content.
        except KeyError:
            # User doesn't have a cracked password
            uncracked.add(user)  #add username to uncracked userlist
            pass
    return userpasshash,uncracked

def query_dic(userquery,dic):
    password = dic[userquery][0]
    phash = dic[userquery][1]
    return password,phash