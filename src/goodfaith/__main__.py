#!/usr/bin/env python3

import argparse
import sys
import traceback
import os
import json
from sys import stdin
from os import isatty
from pathlib import Path
import pandas as pd
import goodfaith.core.scope
import goodfaith.core.graph

# Initialize parser
parser = argparse.ArgumentParser(
    prog='goodfaith',
    description='Check for scope.',
    epilog='hack with goodfaith')
 
# Adding optional argument
parser.add_argument("-s", "--scope", help="Required argument - A JSON formatted scope file is required in order to process the urls. This argument requires the path and filename.")
parser.add_argument("-i", "--inputfile", dest='inputfile', help="Optional argument - The location and filename of the URL input file.")
parser.add_argument("-o", "--outputdir", dest='outputdir', help="Optional argument - The location of the output directory. If the folder does not already exist, it will be created. If no output directory is provided, no output files will be generated and the only output will be printed to the console via stdout.")
parser.add_argument("-c", "--config", help="The parameters will be supported in the future via a config file to limit argument inputs.")
parser.add_argument("-v", "--verbose", dest='quiet', action='store_false', help="Optional argument - Output additional details to the console (statistics, errors, and progress). This mode should not be used if passing the stdout to another tool and is best utilized for troubleshooting.")
parser.add_argument('-q', "--quiet", dest='quiet', action='store_true', help='Optional argument - Only output the URLs to the console/stdout to support bash piping. This mode already defaults to true if verbose is not set although can be explicitly defined.')
parser.add_argument('-g', "--graph", dest='graph', action='store_true', help='Experimental optional argument - Output the information into a html graph file to the output directory. This functionality is implemented but needs to be tuned and enhanced. Future intent would be to provide an interactive file to explore and visualize patterns, scope status, and program correlations. It is also currently slow to generate.')
parser.add_argument('-b', "--bulk", dest='bulk', help = "Optional argument - Generate a bulk scope file from a supported Bug Bounty platform. Valid platform values: bugcrowd, hackerone, intigriti, yeswehack, federacy, hackenproof")
parser.add_argument('-d', "--debug", dest='debug', action='store_false', help='Optional argument - Output debug error information.')
# Read arguments from command line
args = parser.parse_args()

def quitProgram():
    sys.exit()
    
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

def main():
    
    if args.debug is True:
        debugMode = True
    else:
        debugMode = False
    
    # Check whether console output should be disabled.
    if args.quiet is True:
        quietMode = True
    else:
        quietMode = False
        
    if quietMode is False:
        showBanner()


    # OUTPUT PROCESS
    if args.outputdir:
        # Remove it and then re-add it just to ensure consistency
        outputDir = args.outputdir.rstrip('/')
        outputDir = outputDir + '/'
        if not os.path.exists(outputDir): # Check if directory exists
            try:
                os.mkdir(outputDir) # create a new directory
            except:
                if quietMode is False:
                    print('Failed to create output directory.')
                    if debugMode is True:
                        print(traceback.format_exc())
                        
    else:
        outputDir = 'NoOutput'
    
    # SCOPE LOAD
    if args.scope:
        try:
            scopeFile = Path(args.scope)
            #if not os.path.exists(scopeFile):
            if not scopeFile.exists():
                if quietMode is False:
                    print("Scope file does not exist.")
                quitProgram()
            else:
                if quietMode is False:
                    print("Loading program scope file.")
                try:
                    programScope = goodfaith.core.scope.loadScope(scopeFile)
                except:
                    if quietMode is False:
                        print('Failed to load project scope.')
                        if debugMode is True:
                            print(traceback.format_exc())
                    sys.exit()
        except:
            if quietMode is False:
                print('Scope file failed.')
        
    # BASH INPUT PROCESS
    if not sys.stdin.isatty():
        try:
            dfAllURLs = pd.read_csv(sys.stdin, header=None, names=['url'], engine='python')
        except:
            if quietMode is False:
                print('Failed to load standard input.')
                if debugMode is True:
                    print(traceback.format_exc())
    else:
        if args.inputfile is not None:
            inputFile = Path(args.inputfile)
            if not inputFile.exists():
                print("Input file does not exist.")
                quitProgram()
            else:
                try:
                    dfAllURLs = pd.read_csv(inputFile, header=None, names=['url'], engine='python')
                except:
                    if not (quietMode):
                        print('Input file failed to load.')
                        if debugMode is True:
                            print(traceback.format_exc())
                    sys.exit()
    # PROCESS URLS
    if args.scope:
        if (scopeFile is not None):
            try:
                dfUpdatedURLs = goodfaith.core.scope.boundaryGuard(dfAllURLs, outputDir, programScope, quietMode, debugMode)
                if quietMode is False:
                    print('Scope processing completed.')
            except:
                if quietMode is False:
                    print('URL processing failed.')
                    if debugMode is True:
                        print(traceback.format_exc())
    
    # BULK PROCESS
    if args.bulk:
        platformList = ['bugcrowd', 'hackerone', 'intigriti', 'yeswehack', 'federacy', 'hackenproof']
        if (args.bulk in platformList):
            platformName = args.bulk
        else:
            if quietMode is False:
                print('Invalid platform name.')
            quitProgram()
        try:
            if (outputDir != 'NoOutput'):
                platformScope, programStats = goodfaith.core.scope.bulkLoad(platformName)
                filePath = outputDir + platformName + '_programs.json'
                with open(filePath, 'w', encoding='utf-8') as f:
                    json.dump(platformScope, f, ensure_ascii=False, indent=4)
                if quietMode is False:
                    print('There were ' + str(programStats) + ' programs bulk processed.')
            else:
                if quietMode is False:
                    print('Output directory missing or invalid.')
        except:
            if quietMode is False:
                print('Error loading, processing, or writing bulk file.')
                if debugMode is True:
                    print(traceback.format_exc())
            sys.exit()
        
    # GRAPH PROCESS
    if args.graph is True:
        try:
            if quietMode is False:
                print('Generating graph. This could take a couple minutes.')
            graphStatus = goodfaith.core.graph.generateGraph(outputDir,dfUpdatedURLs,programScope)
            if quietMode is False:
                print(graphStatus)
        except:
            if quietMode is False:
                print('Graph failed to generate.')
                if debugMode is True:
                    print(traceback.format_exc())

if __name__ == "__main__":
    main()