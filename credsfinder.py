#!/usr/bin/env python
__author__ = 'jbollin'
import re

"""Function to generate a dictionary that contains usernames as the keys with password and hash.
Requires the input of file containing username:hash and a hash:crackedpasswords file"""

def gen_dict_user_pass_hash(user_hash_file, hash_pass_file):
    # initialize variables
    userhash = {}       # Dictionary using username as the key and hash as the content.
    hashpass = {}       # Dictionary using hash as the key and password as the content.
    userpasshash = {}   # Dictionary using username as the key and password and hash as the content.
    with open(user_hash_file, mode="rb") as f:
        for line in f:
            username,phash = line.rstrip().split(":")
            userhash[username] = phash
    with open(hash_pass_file, mode="rb") as f:
        for line in f:
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