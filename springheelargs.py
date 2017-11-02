#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Argument Parsing
########
##  Copyright 2017 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU Lesser General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys, os

def getArgs():

    args = sys.argv

    hlp = ["Springheel copyright 2017 garrick. Some rights reserved.", "Released under the GNU General Public License <http://www.gnu.org/licenses/>.",
           "Commands:", "  springheel init", "    Create a new Springheel site in the current directory.",
           "  springheel update", "    Update the Springheel site found in the current directory.",
           "  springheel help", "    Display this message."]
    helps = os.linesep.join(hlp)

    if len(args) <= 1:
        print("Error: please provide some parameters.")
        print(helps)
    elif args[1] == "init":
        ## run initialization routine
        pass
    elif args[1] == "update":
        ## run update routine
        pass
    elif args[1] == "help":
        print(helps)
