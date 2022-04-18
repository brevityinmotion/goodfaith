#!/usr/bin/env python3

import argparse
import sys
from sys import stdin
from os import isatty
import pandas as pd

def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description='Check for scope.')
 
    # Adding optional argument
    parser.add_argument("-s", "--scope", help="The location of the JSON scope file.")
    parser.add_argument("-i", "--inputfile", help="The location of the URL input file.")
    parser.add_argument("-o", "--outputfile", help="The location of the URL output file.")
    parser.add_argument("-c", "--config", help="The location of the configuration file.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Outputs runtime details, information, and debugging insight.")
    parser.add_argument('-q', "--quiet", dest='quiet', action='store_true', help='Quiet mode, no console output.')
    # Read arguments from command line
    args = parser.parse_args()
    
    if args.quiet:
        print = nullify

    # Check if there is any bash pipe input
    if not sys.stdin.isatty():
        if args.verbose is True:
            print("There is bash input.")
        for line in sys.stdin:
            sys.stdout.write(line)
    else:
        if args.verbose is True:
            print("There is no bash input.")
        if args.inputfile is not None:
            dfAllURLs = pd.read_csv(args.inputpath, header=None, names=['url'], sep='\n')
            print(dfAllURLs)
    #is_pipe = not isatty(stdin.fileno())

    if args.output:
        print("Displaying Output as: % s" % args.output)

    #outputStatus = boundaryGuard(urlInputPath, urlOutputPath, programScope)
    #print(outputStatus)
    print("successful run")

if __name__ == "__main__":
    main()