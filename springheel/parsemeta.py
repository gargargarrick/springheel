#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Metadata Parsing
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

## This script returns a dictionary of metadata (title, author, etc.), the commentary, the navigation boxes, and link rel navigation.

from slugify import slugify
import springheel.parseconf
##import arrow

##Retrieve the metadata file.
def readText(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            textToRead = f.readlines()
    except IOError:
        print("An I/O error has occurred.")
        return(False)
    except UnboundLocalError:
        print("An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist.")
        return(False)
    return textToRead

##Separate the metadata from formatting info, and from the commentary.
def getMetaCom(meta_raw,translated_strings):
    meta_nl = []
    comments = []
    for i in meta_raw:
        if i == "---\n" or i == "---":
            pass
        else:
            if i[0:2] == "  ":
                meta_nl.append(i[2:-1])
            else:
                comments.append(i[:-1])
    if comments == []:
        comments = [translated_strings["no_comment"]]
    return(meta_nl,comments)

##Separate the metadata from the commentary.
def splitMC(file_name,translated_strings):
    meta_raw = readText(file_name)
    mc = getMetaCom(meta_raw,translated_strings)
    m = mc[0]
    c = mc[1]
    return(mc)

##Convert the plain metadata into a dict.
def dictizeMeta(m):
    meta = []
    for i in m:
        s = i.split(": ")
        d = {s[0]:s[1]}
        meta.append(d)
    result = {}
    for d in meta:
        result.update(d)

    meta = result

    return(meta)

def parseMetadata(single,file_name,translated_strings):

    ##We now have a formatted list of metadata items, and of the commentary lines.
    mc = splitMC(file_name,translated_strings)
    m = mc[0]
    c = mc[1]

    ##The metadata list has become a dictionary.
    meta = dictizeMeta(m)

    ##Title slug and line are created.

    series_slug = slugify(meta["category"])
    title_slug = slugify(meta["title"])
    title_line = [meta["category"], " #", meta["page"], ": ", meta["title"]]
    title_line = "".join(title_line)

    slugs = [title_slug,series_slug,title_line]

    commentary = []
    for line in c:
        comm = ["<p>",line,"</p>"]
        comm = "".join(comm)
        commentary.append(comm)
    commentary = "".join(commentary)
    return(meta,commentary,slugs)


