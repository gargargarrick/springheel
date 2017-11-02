#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - File Scanner
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
import springheel.parsemeta

def getComics():
    ##Demo values.
    series = "Mimi and Eunice"

    original_path = os.getcwd()

    path = os.path.join(original_path,"input")
    os.chdir(path)

    files = os.listdir()

    images = []

    for i in files:
        if i[-4:] == ".png" or i[-4:] == ".gif" or i[-4:] == ".jpg":
            images.append(i)

    comics = []
    for i in images:
        transcr = i[:-3]+"transcript"
        meta = i[:-3]+"meta"
        if transcr in files and meta in files:
            print("Metadata and transcript found for %s." % (i))
            comics.append({"image":i,"transcript":transcr,"meta":meta})
        elif meta in files and transcr not in files:
            print("Metadata found, but no transcript for %s. Please create %s" % (i,transcr))
            comics.append({"image":i,"transcript":"no_transcript.transcript","meta":meta})
        elif transcr in files and meta not in files:
            print("Transcript found, but no metadata for %s. I can't build the page without metadata. Please create %s" % (i,meta))
            return(False)
        else:
            print("%s doesn't seem to be a comic, as it is missing a transcript and metadata." % (i))

    if comics == []:
        print("The comics list is empty. Please add some comics and then try to build again.")
        return(False)

    os.chdir(original_path)

    return(comics)
