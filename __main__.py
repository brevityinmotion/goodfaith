#!/usr/bin/env python3

import argparse
import sys
import os
import json
from sys import stdin
from os import isatty
import pandas as pd

from goodfaith.core.scope import *

#def quietmode(*args, **kwargs):
#    """
#    a function that does nothing
#    """
#    pass

#def loadScope(programScope):
#    programScope = dict(json.loads(programScope))
#    return programScope

def loadScope(scopeFile):
    programData = open(scopeFile)
        #programScope = dict(json.loads(programScope))
    programScope = json.load(programData)
    return programScope

def main():
    # Initialize parser
    parser = argparse.ArgumentParser(description='Check for scope.')
 
    # Adding optional argument
    parser.add_argument("-s", "--scope", help="The location of the JSON scope file.")
    parser.add_argument("-i", "--inputfile", dest='inputfile', help="The location of the URL input file.")
    parser.add_argument("-o", "--outputdir", dest='outputdir', help="The location of the output directory.")
    parser.add_argument("-c", "--config", help="The location of the configuration file.")
    parser.add_argument("-v", "--verbose", dest='quiet', action='store_false', help="Outputs runtime details, information, and debugging insight.")
    parser.add_argument('-q', "--quiet", dest='quiet', action='store_true', help='Quiet mode, no console output.')
    # Read arguments from command line
    args = parser.parse_args()
    
 #   if args.quiet is True:
 #       print = quietmode
 
#    if args.inputfile:
#        inputFile = args.inputfile
#        if not os.path.exists(inputFile):
#            print("Input file does not exist.")

    if args.outputdir:
        outputDir = args.outputdir
        if not os.path.exists(outputDir): # Check if directory exists
            os.mkdir(outputDir) # create a new directory

    if args.scope is None:
        print("Scope input file is required.")
        quit()
    else:
        print("There is no bash input.")
        scopeFile = args.scope
        if not os.path.exists(scopeFile):
            print("Scope file does not exist.")
            quit()
        else:
            print("Loading program scope file.")
            programScope = loadScope(scopeFile)
            print(programScope)

    # Check if there is any bash pipe input
    if not sys.stdin.isatty():
        if args.verbose is True:
            print("There is bash input.")
        for line in sys.stdin:
            sys.stdout.write(line)
    else:
        if args.quiet is False:
            print("There is no bash input.")
        if args.inputfile is not None:
            inputFile = args.inputfile
            if not os.path.exists(inputFile):
                print("Input file does not exist.")
                quit()
            #print("Create dataframe here")
            #dfAllURLs = pd.read_csv(inputFile, header=None, names=['url'], sep='\n')
            #print(dfAllURLs[:10])
    #is_pipe = not isatty(stdin.fileno())

#    if args.outputdir:
#        print("Displaying Output as: % s" % args.output)
    

    outputStatus = boundaryGuard(inputFile, outputDir, programScope)
    print(outputStatus)
    print("successful run")

if __name__ == "__main__":
    main()