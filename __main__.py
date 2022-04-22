#!/usr/bin/env python3

import argparse
import sys
import os
import json
from sys import stdin
from os import isatty
from pathlib import Path
import pandas as pd

from core.scope import *

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
    parser.add_argument('-g', "--graph", dest='graph', action='store_true', help='Experimental - Generate a graph as output. Could take a couple minutes for generation.')
    # Read arguments from command line
    args = parser.parse_args()
    
    def showBanner():
        print('''
 _                 _                    _                             _               _     
| |               | |            o     | |                        |  | |       o     | |    
| |     __,   __  | |              _|_ | |       __,  __   __   __|  | |  __,    _|_ | |    
|/ \   /  |  /    |/_)   |  |  |_|  |  |/ \     /  | /  \_/  \_/  |  |/  /  |  |  |  |/ \   
|   |_/\_/|_/\___/| \_/   \/ \/  |_/|_/|   |_/  \_/|/\__/ \__/ \_/|_/|__/\_/|_/|_/|_/|   |_/
                                                  /|                 |\                     
                                                  \|                 |/                     
    ''')
    
    # Check whether console output should be disabled.
    if args.quiet:
        quietMode = True
    else:
        quietMode = False
        
    if not (quietMode):
        showBanner()

    # Check if scope is provided
    if args.scope is None:
        if not (quietMode):
            print("Scope input file is required.")
        quit()
    else:
        scopeFile = Path(args.scope)
        #if not os.path.exists(scopeFile):
        if not scopeFile.exists():
            if not (quietMode):
                print("Scope file does not exist.")
            quit()
        else:
            if not (quietMode):
                print("Loading program scope file.")
            try:
                programScope = loadScope(scopeFile)
            except:
                if not (quietMode):
                    print('Failed to load project scope.')
                quit()

    # Validate output directory
    if args.outputdir:
        outputDir = args.outputdir
        if not os.path.exists(outputDir): # Check if directory exists
            try:
                os.mkdir(outputDir) # create a new directory
            except:
                if (quietMode):
                    print('Failed to create output directory.')

    # Check if there is any bash pipe input
    if not sys.stdin.isatty():
        try:
            dfAllURLs = pd.read_csv(sys.stdin, header=None, names=['url'], sep='\n')
        except:
            if not (quietMode):
                print('Failed to load standard input.')
        #for line in sys.stdin:
        #    sys.stdout.write(line)
    else:
        if args.inputfile is not None:
            inputFile = Path(args.inputfile)
            if not inputFile.exists():
                print("Input file does not exist.")
                quit()
            else:
                try:
                    dfAllURLs = pd.read_csv(inputFile, header=None, names=['url'], sep='\n')
                except:
                    if not (quietMode):
                        print('Input file failed to load.')
    
    dfUpdatedURLs = boundaryGuard(dfAllURLs, outputDir, programScope, quietMode)
    if not (quietMode):
        print('Scope processing completed.')
    
    # Need to run graph after data analysis
    if args.graph is True:
        try:
            if not (quietMode):
                print('Generating graph. This could take a couple minutes.')
            graphStatus = generateGraph(outputDir,dfUpdatedURLs,programScope)
            if not (quietMode):
                print(graphStatus)
        except:
            if not (quietMode):
                print('Graph failed to generate.')

if __name__ == "__main__":
    main()