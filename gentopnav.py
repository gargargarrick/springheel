#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Generate site navigation
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

def genTopNav(characters_page,extras_page,store_page,translated_strings):
    home_s = translated_strings["home_s"]
    char_s = translated_strings["char_s"]
    archive_s = translated_strings["archive_s"]
    extra_s = translated_strings["extra_s"]
    store_s = translated_strings["store_s"]

    d = [{"s":home_s,"u":"index.html"},{"s":archive_s,"u":"archive.html"}]
    if characters_page == True:
        d.append({"s":char_s,"u":"characters.html"})
    if extras_page == True:
        d.append({"s":extra_s,"u":"extras.html"})
    if store_page:
        d.append({"s":store_s,"u":store_page})

    elements = ["<ul>"]

    for pair in d:
        line = '<li><a href="{u}">{s}</a></li>'.format(u=pair["u"],s=pair["s"])
        elements.append(line)
    elements.append("</ul>")
    return(elements)

    
