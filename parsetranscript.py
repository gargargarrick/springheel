#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Transcript Parsing
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

import os

##Retrieve the transcript file.
def readText(file_name):
    try:
        f = open(file_name, "r")
        try:
            textToRead = f.read()
        finally:
            f.close()
    except IOError:
        pass
    return textToRead

##TODO: functionify

def makeTranscript(file_name):
    raw_transcript = readText(file_name)

    sep = os.linesep

    ##separate the individual lines
    sep_transcript = raw_transcript.split(sep)

    ##For navigation within the list. A bit kludgey.
    transcript_length = len(sep_transcript)-1
    curr_loc = 0

    ##Initializing a variable to hold the HTML transcript.
    first_pass = []

    for i in sep_transcript:
        ##Actions are offset by parentheses.
        if i[0:1] == "(":
            action_list = ["""<p class="action">""",i,"</p>"]
            action_string = "".join(action_list)
            first_pass.append(action_string)
        ##Actual dialogues are indented by 2 spaces. They're part of the same line as names.
        elif i[0:2] == "  ":
            line_stripped = i[2:]
            #line_list = ["""<span class="linedia">""",line_stripped,"</span></p>"]
            line_list = ["""<span class="linedia">""",line_stripped,"</span></p>"]
            line_string = "".join(line_list)
            first_pass.append(line_string)
        ##Blank lines are just there for ease of formatting and can be ignored for the final product.
        elif i == "":
            pass
        ##Anything else is probably a character name.
        else:
            charname_list = ["""<p class="line"><span class="charname">""",i,"</span>: "]
            charname_string = "".join(charname_list)
            first_pass.append(charname_string)
        curr_loc += 1

    sep = os.linesep
    second_pass = sep.join(first_pass)
    return(second_pass)
