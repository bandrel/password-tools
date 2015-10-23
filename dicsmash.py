#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import glob
import os

maxlength = (int(sys.argv[2])+1)
minlength = (int(sys.argv[2])+1)
filetype = glob.glob(str('*.'+sys.argv[1]))
outputfile = sys.argv[3]
tempfiles = []

def split_to_size(file):
    global tempfiles
    with open(file) as origionaldic:
        for line in origionaldic:
            current_length = len(line.rstrip())
            tempfile = str(str(current_length)+'.dictemp')
            tempfiles.append(tempfile)
            with open(tempfile, 'a') as a:
                 a.write(line)

def dedupe_and_merge(outname):
    working_list = []
    with open(outname,'w') as outfile:
        for file in tempfiles:
            with open(file) as current_working_file:
                for line in current_working_file:
                    working_list.append(line)
        working_set = set(working_list)
        for line in working_set:
            outfile.write(line)

def cleanup_temp():
    tempfiles = glob.glob('*.dictemp')
    for tfile in tempfiles:
        os.remove(tfile)

if __name__ == '__main__':
    for file in filetype:
        split_to_size(file)
    dedupe_and_merge(outputfile)
    cleanup_temp()
