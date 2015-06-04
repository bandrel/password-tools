#!/usr/bin/env python
__author__ = 'jbollin'
import re

def gen_dict_user_pass_hash(user_hash_file, hash_pass_file):
    userhash = {}
    hashpass = {}
    userpasshash = {}

    with open(user_hash_file, mode="rb") as f:
        for line in f:
            username = re.sub(':.*', "", line).rstrip()
            phash = re.sub('.*:', "", line).rstrip()
            userhash[username] = phash

    with open(hash_pass_file, mode="rb") as f:
        for line in f:
            phash = re.sub(':.*', "", line).rstrip()
            password = re.sub('.*:', "", line).rstrip()
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