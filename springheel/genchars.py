#!/usr/bin/env python3
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

sep = "\n"

def parseChars(charfile):
    ##fn = input("File name? > ")

    l = []
    divider = "---"+sep
    sectioned = charfile.split(divider)
    for i in sectioned:
        s_text = i.split(sep)[:-1]
        l.append(s_text)

    raw_page_m = l[0]
    category = raw_page_m[0].split("category: ", 1)[1]
    lang = raw_page_m[1].split("lang: ")[1]

    cl = [category,lang]

    characters = l[1:]

    for char in characters:
        ## Make sure it isn't just a newline
        if char != []:
            d = {}
            char_attrs =[]
            for item in char:
                attr,val = item.split(": ", 1)
                tup = (attr,val)
                char_attrs.append(tup)
            cl.append(char_attrs)

    return(cl)

def genCharsPage(chars_list):

    chars = []
    for item in chars_list:
        char_elements = ['<div class="char">']
        if type(item) == list:
            title = "<h2>{name}</h2>".format(name=item[0][1])
            char_elements.append(title)
            if item[2][1] != 'None':
                img = '<img src="{img}" alt="" />'.format(img=item[2][1])
                char_elements.append(img)
            ## We only need to worry about the DL element if there are custom attributes.
            if len(item) > 3:
                dls = []
                char_elements.append("<dl class='chartraits'>")
                for key in item:
                    if key[0] == "name" or key[0] == "img" or key[0] == "desc":
                        pass
                    else:
                        line = "<dt>{attr}</dt>{sep}<dd>{val}</dd>".format(
                            attr=key[0],
                            val=key[1],
                            sep=sep)
                        dls.append(line)
                dl = sep.join(dls)
                char_elements.append(dl)
                char_elements.append("</dl>")
            char_elements.append('<div class="chartext">')
            desc = "<p>{desc}</p>".format(desc=item[1][1])
            char_elements.append(desc)
            char_elements.append("</div>")
            char_elements.append("</div>")
            char_fin = sep.join(char_elements)
            chars.append(char_fin)
    characters = sep.join(chars)
    return(characters)
