#!/usr/bin/env python
__author__ = 'jbollin'
import sys
import glob
import getopt
import os

def smash_pots(directory,mode,outputfile):
    everything = set()
    with open(outputfile,'w') as b:
        os.chdir(directory)
        pots = glob.glob('*.pot')
        for pot in pots:
            with open(pot) as file:
                for line in file:
                    a = line.split(':')
                    if mode == 'LM':
                        if len(a[0]) == 16:
                            everything.add(line)
                    elif mode == 'NTLM':
                        if len(a[0]) > 16:
                            everything.add(line)
                    else:
                        everything.add(line)
        for line in everything:
            b.write(line)
def helpmsg():
    print 'Usage: potsmash.py [Options] ' \
          '  -h or --help:  This help screen\n' \
          '  -o or --output: secifies the output file name\n' \
          '  -d or --directory: uses the directory specified.\n' \
          '                   Defaults to current directory.\n' \
          '  -n or --ntlm: specifies output to only be ntlm\n' \
          '  -l or --lm: specifies output to only be ntlm\n'

if __name__ == '__main__':
    mode = 'ALL'
    outputfile = ''
    directory = os.curdir
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd:lno:',['help', 'directory=', 'lm', 'ntlm', 'output='])
    except getopt.GetoptError as err:
        helpmsg()
        print str(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            helpmsg()
            sys.exit()
        elif opt in ('-d', '--directory'):
            directory = arg
        elif opt in ('-l', '--lm'):
            mode = 'LM'
        elif opt in ('-n', '--ntlm'):
            mode = 'NTLM'
        elif opt in ('-o', '--output'):
            outputfile = arg
    if outputfile == '':
        print '[!] you must specify an output file name'
        sys.exit(2)
    smash_pots(directory,mode,outputfile)



