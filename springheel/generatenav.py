#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Navigation Block Generation
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

import springheel.parseconf, springheel.parsemeta

##Check for navigation math errors.
def checkNavMath(page_int,first_page,last_page):
    if page_int == False or first_page == False or last_page == False:
        print("One or more needed values not set. Make sure there is a page value in {file_name} and the first and last page values are set, then try again.".format(file_name=file_name))
    elif page_int <= 0:
        print("{page_int} is not a valid page number. Please check the page number set in {file_name} and try again.".format(page_int=str(page_int),file_name=file_name))
    elif first_page < 0:
        print("The first page is set to a number less than zero. Please change it and try again.")
    elif last_page < first_page:
        print("The newest page is set to a number lower than the first page. Please change it and try again.")
    else:
        return(True)
    return(False)

## Generate navigation boxes and link rel navigation.
def navGen(navdirection,page_int,first_page,last_page,first,final,series_slug,site_style,translated_strings):

    strips = range(1,(last_page+1))
    if page_int not in strips:
        print("""Building failed!\n\nNavigation could not be built because {page_int} is an invalid page number. The .meta value "page" may have been set to something incorrect, or the scan may have failed to detect a comic. Please double-check.""".format(page_int=page_int))

    if page_int == last_page:
        final = True
    elif page_int == 1:
        first = True
    first_page = str(first_page)
    last_page = str(last_page)

    first_s = translated_strings["first_s"]
    prev_s = translated_strings["prev_s"]
    next_s = translated_strings["next_s"]
    last_s = translated_strings["last_s"]
    home_s = translated_strings["home_s"]
    last_page = str(last_page)

    firsts_s = translated_strings["firsts_s"]
    prevs_s = translated_strings["prevs_s"]
    nexts_s = translated_strings["nexts_s"]
    lasts_s = translated_strings["lasts_s"]

    navl = [' <ul class="cominavbox">']
    linkl = ['<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">']

    image_template = """<li><a href="{series_slug}_{page}.html"><img src="arrows/{site_style}_{relation}.png" alt="{image_long_string}" /><br/>{image_short_string}</a></li>"""
    linkrel_template = """<link rel="{relation}" href="{series_slug}_{page}.html" title="{page_string}">"""


    if  navdirection == "rtl":
        if not final:
            next_page = str(page_int+1)
            ns = image_template.format(series_slug=series_slug,
                                       page=last_page,
                                       site_style=site_style,
                                       relation="first",
                                       image_long_string=last_s,
                                       image_short_string=lasts_s)
            navl.append(ns)
            ns = image_template.format(series_slug=series_slug,
                                       page=next_page,
                                       site_style=site_style,
                                       relation="prev",
                                       image_long_string=next_s,
                                       image_short_string=nexts_s)
            navl.append(ns)

            ls = linkrel_template.format(relation="last",
                                         series_slug=series_slug,
                                         page=last_page,
                                         page_string=last_s)
            linkl.append(ls)
            ls = linkrel_template.format(relation="next",
                                         series_slug=series_slug,
                                         page=next_page,
                                         page_string=next_s)
            linkl.append(ls)
        if not first:
            prev_page = str(page_int-1)
            ns = image_template.format(series_slug=series_slug,
                                       page=prev_page,
                                       site_style=site_style,
                                       relation="next",
                                       image_long_string=prev_s,
                                       image_short_string=prevs_s)
            navl.append(ns)
            ns = image_template.format(series_slug=series_slug,
                                       page=first_page,
                                       site_style=site_style,
                                       relation="last",
                                       image_long_string=first_s,
                                       image_short_string=firsts_s)
            navl.append(ns)

            ls = linkrel_template.format(relation="prev",
                                         series_slug=series_slug,
                                         page=prev_page,
                                         page_string=prev_s)
            linkl.append(ls)
            ls = linkrel_template.format(relation="first",
                                         series_slug=series_slug,
                                         page=first_page,
                                         page_string=first_s)
            linkl.append(ls)
    else:
        if not first:
            ns = image_template.format(series_slug=series_slug,
                                       page=first_page,
                                       site_style=site_style,
                                       relation="first",
                                       image_long_string=first_s,
                                       image_short_string=firsts_s)
            navl.append(ns)
            prev_page = str(page_int-1)
            ns = image_template.format(series_slug=series_slug,
                                       page=prev_page,
                                       site_style=site_style,
                                       relation="prev",
                                       image_long_string=prev_s,
                                       image_short_string=prevs_s)
            navl.append(ns)

            ls = linkrel_template.format(relation="first",
                                         series_slug=series_slug,
                                         page=first_page,
                                         page_string=first_s)
            linkl.append(ls)
            ls = linkrel_template.format(relation="prev",
                                         series_slug=series_slug,
                                         page=prev_page,
                                         page_string=prev_s)
            linkl.append(ls)
        if not final:
            next_page = str(page_int+1)
            ns = image_template.format(series_slug=series_slug,
                                       page=next_page,
                                       site_style=site_style,
                                       relation="next",
                                       image_long_string=next_s,
                                       image_short_string=nexts_s)
            navl.append(ns)
            ns = image_template.format(series_slug=series_slug,
                                       page=last_page,
                                       site_style=site_style,
                                       relation="last",
                                       image_long_string=last_s,
                                       image_short_string=lasts_s)
            navl.append(ns)

            ls = linkrel_template.format(relation="next",
                                         series_slug=series_slug,
                                         page=next_page,
                                         page_string=next_s)
            linkl.append(ls)
            ls = linkrel_template.format(relation="last",
                                         series_slug=series_slug,
                                         page=last_page,
                                         page_string=last_s)
            linkl.append(ls)

    navl.append(" </ul>")
    nav = """\n""".join(navl)

    linkrels = """\n""".join(linkl)

    return(nav,linkrels)

    ##site_style =  sitewide_conf["site_style"]

def bigGenerator(page_int,first_page,last_page,first,final,series_slug,site_style):

    ##Page navigation.

    valid_math = checkNavMath(page_int,first_page,last_page)

    if valid_math == True:
        navs = navGen(page_int,first_page,last_page,first,final,series_slug,site_style)
        nav_boxes = navs[0]
        linkrels = navs[1]
    else:
        print("The navigation for {file_name} could not be generated. Check the above messages for errors.".format(file_name=file_name))
        return(False)

    return(nav_boxes,linkrels)
