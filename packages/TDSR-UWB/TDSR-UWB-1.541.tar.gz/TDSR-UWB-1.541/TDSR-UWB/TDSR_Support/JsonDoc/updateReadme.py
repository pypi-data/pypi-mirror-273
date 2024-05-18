#!/usr/bin/env python3

import os
import collections
import datetime
from datetime import date
import socket
import json
import sys

import re

import time
import argparse

def ProcessFile ( fileName):
    with open(fileName+".template.md", "r") as f:
        contents = f.readlines()

    for line in range(len(contents)):
        if (contents[line].find("<$#insert_here=") != -1):
            print(contents[line])
            match = re.search('.*?\"(.*)\".*',contents[line])
            print(match.group(1))
            with open(match.group(1), "r") as ff:
                jsonData = json.load(ff)
                contents[line]= json.dumps(jsonData, indent=4)+'\n'
            print(contents[line])


    with open(fileName+".md", "w") as f:
        contents = "".join(contents)
        f.write(contents)

if __name__ == "__main__":
  
    print(sys.argv[1:])
    parser = argparse.ArgumentParser('Get readme md Parameters')
    parser.add_argument('-f', '--fileName', type=str, help='file name prefix', required=True)
    
    
    args = parser.parse_args()
    ProcessFile(args.fileName)