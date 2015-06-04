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
    for line in user_hash_list:
        username,phash = line.rstrip().split(":")
        userhash[username] = phash
    for line in hash_pass_list:
        phash,password = line.rstrip().split(":",1)
        hashpass[phash] = password
    for user in userhash.keys():
        passwordquery = hashpass[userhash[user]]
        hashquery = userhash[user]
        userpasshash[user] = [passwordquery,hashquery]
    return userpasshash

def query_dic(userquery,dic):
    password = dic[userquery][0]
    phash = dic[userquery][1]
    return password,phash