#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import glob
import os
import getopt
import datetime

def split_to_size(file):    #read file line by line and copy the password into a file that corresponds to the length
    if verbose_mode == True:
        print '[+] Splitting %s' % file
    with open(file) as origionaldic:
        for line in origionaldic:
            current_length = len(line.rstrip())
            tempfile = str(str(current_length)+'.dictemp')
            with open(tempfile, 'a') as a:
                 a.write(line)

def dedupe_and_merge(outname):  #reads each tempfile in and then adds the contents to a set.
    #Then the system outputs the set to a file and combines all of the sets to one file.
    import gc
    global tempfiles

    tempfiles = glob.glob('*.dictemp')
    tempfiles.sort()
    with open(outname,'w') as outfile:
        for file in tempfiles:
            if verbose_mode == True:
                print '[*] Processing %s' % file
                print_elapsed()
            working_set = set()
            with open(file) as current_working_file:
                for line in current_working_file:
                    working_set.add(line)
            for item in working_set:
                outfile.write(item)
            gc.collect()

def cleanup_temp():         #delets the dictemp files
    if verbose_mode == True:
        print '[+] Cleaning up tempfiles'
    for tfile in tempfiles:
        os.remove(tfile)


def helpmsg():
    print 'Usage: dicsmash.py [Options] ' \
          '  -h or --help:  This help screen\n' \
          '  -d or --directory: uses the directory specified.\n' \
          '                   Defaults to current directory.\n' \
          '  -e or --extension: specifies the extension of the input dictionaries\n' \
          '  -o or --output: Specifies the output file name of the new dictionary\n' \
          '  -v or --verbose: Creates verbose output\n'
def print_elapsed():
    global elapsed_time
    elapsed_time = datetime.datetime.now() - start_time
    if verbose_mode == True:
        print '[+] %s since start' % elapsed_time
tempfiles = []
directory = os.curdir
extension = 'dic'
working_dir = os.curdir
verbose_mode = False
start_time = datetime.datetime.now()
elapsed_time = datetime.datetime.now() - start_time
if __name__ == '__main__':
    #Program defaults

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd:e:o:v',['help', 'directory=', 'extension=', 'output=','verbose'])
    except getopt.GetoptError as err:
        helpmsg()
        print str(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            helpmsg()
            sys.exit()
        elif opt in ('-d', '--directory'):
            working_dir = arg
        elif opt in ('-e', '--extension'):
            extension = arg
        elif opt in ('-o', '--output'):
            outputfile = arg
        elif opt in ('-v', '--verbose'):
            verbose_mode = True


    try:
        os.chdir(working_dir)
    except:
        print '%s is not a valid directory' % working_dir
        sys.exit(2)
    try:
        filetype = glob.glob(str('*.'+extension))
    except:
        print '[!] There are no files with the extension %s in %a' % extension, working_dir
        sys.exit(2)


    for file in filetype:
        split_to_size(file)
        print_elapsed()
    dedupe_and_merge(outputfile)
    cleanup_temp()
    elapsed_time = datetime.datetime.now() - start_time
    print_elapsed()
    finished_time = datetime.datetime.now()
    print '[*] Finished after %s seconds' % elapsed_time

