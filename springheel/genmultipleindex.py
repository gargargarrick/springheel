#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate index pages for multiple series
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
from slugify import slugify

sep = "\n"

def genMultipleIndex(comics,characters_page,translated_strings):
    print(characters_page)
    elements = []
    dopen = "<div class='intro'>"
    dclose = "</div>"

    golatest_s = translated_strings["golatest_s"]
    gofirst_s = translated_strings["gofirst_s"]

    if characters_page == True:
        character_s = translated_strings["char_s"]

    ltemplate = ["<h2>{category}</h2>",'<img src="{header}" alt="{category}" />',
                    '<p class="author">by {author}</p>','<p class="desc">{desc} (<span class="status">{status}</span>)</p>',
                    '<p>{golatest} | {gofirst}</p>']

    maintemplate = sep.join(ltemplate)

    for i in comics:
        golatest=['<a href="',i.lbp_link,'">',golatest_s,"</a>"]
        golatest = "".join(golatest)
        gofirst=['<a href="',i.fbp_link,'">',gofirst_s,"</a>"]
        gofirst = "".join(gofirst)
        elements.append(dopen)
        div = maintemplate.format(header=i.header,
                            category=i.category,
                            author=i.author,
                            desc=i.desc,
                            status=i.statuss,
                            golatest=golatest,
                            gofirst=gofirst
        )
        elements.append(div)
        if characters_page == True:
            cat_slug = slugify(i.category)
            characters_link = "".join([cat_slug,"-","characters.html"])
            char_line = '<p><a href="{characters_link}">{character_s}</a></p>'.format(characters_link=characters_link,
                                                                                      character_s=character_s)
            elements.append(char_line)
        elements.append(dclose)
    return(elements)
