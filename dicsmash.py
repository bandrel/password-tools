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

def split_to_size(file,size):
    global tempfiles
    tempfile = str(str(size)+'.dictemp')
    tempfiles.append(tempfile)
    with open(tempfile,'a') as f:
        current_working_list = []
        with open(file) as origionaldic:
            for line in origionaldic:
                if len(line.strip('\r\n')) == size:
                    current_working_list.append(line.strip('\r\n'))
        for line in current_working_list:
            f.write(line+'\n')

def dedupe_and_merge(outname):
    with open(outname,'w') as outfile:
        for file in tempfiles:
            working_set = set()
            with open(file) as current_working_file:
                for line in current_working_file:
                    working_set.add(line)
            for line in working_set:
                outfile.write(line)

def cleanup_temp():
    for tfile in tempfiles:
        os.remove(tfile)

if __name__ == '__main__':
    for file in filetype:
        for size in xrange(1,maxlength):
            split_to_size(file,size)
    dedupe_and_merge(outputfile)
    cleanup_temp()
