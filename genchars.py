#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate characters page
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

sep = os.linesep

def parseChars(charfile):
    ##fn = input("File name? > ")

    l = []
    divider = "---"+sep
    sectioned = charfile.split(divider)[:-1]
    for i in sectioned:
        s_text = i.split(sep)[:-1]
        l.append(s_text)

    raw_page_m = l[0]
    category = raw_page_m[0].split("category: ")[1]
    lang = raw_page_m[1].split("lang: ")[1]

    print("This seems to be a file for the category %s in %s language." % (category,lang))

    cl = [category,lang]

    characters = l[1:]

    for char in characters:
        d = {}
        for item in char:
            attr,val = item.split(": ")
            d[attr] = val
        cl.append(d)

    return(cl)

def genCharsPage(chars_list):

    chars = []
    for item in chars_list:
        char_elements = ['<div class="char">']
        if type(item) == dict:
            title = "<h2>{name}</h2>".format(name=item["name"])
            char_elements.append(title)
            if item["img"] != 'None':
                img = '<img src="{img}" alt="" />'.format(img=item["img"])
                char_elements.append(img)
            char_elements.append("<dl>")
            keys = list(item.keys())
            dls = []
            for key in keys:
                if key == "name" or key == "img" or key == "desc":
                    pass
                else:
                    line = "<dt>{attr}</dt>{sep}<dd>{val}</dd>".format(
                                                                       attr=key,
                                                                       val=item[key],
                                                                       sep=sep)
                    dls.append(line)
            dl = sep.join(dls)
            char_elements.append(dl)
            char_elements.append("</dl>")
            desc = "<p>{desc}</p>".format(desc=item["desc"])
            char_elements.append(desc)
            char_elements.append("</div>")
            char_fin = sep.join(char_elements)
            chars.append(char_fin)
    characters = sep.join(chars)
    return(characters)
