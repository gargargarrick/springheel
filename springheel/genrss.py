#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - RSS Feed Generation
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

from feedgen.feed import FeedGenerator
import datetime, os
from datetime import timezone

def generateFeed(base_url,rssmeta,comics):
    from feedgen.feed import FeedGenerator
    fg = FeedGenerator()
    fg.id(base_url)
    fg.title(rssmeta["title"])
    fg.author( {'name':rssmeta["author"],'email':rssmeta["email"]} )
    fg.link( href=rssmeta["link"], rel='self' )
    fg.language(rssmeta["language"])
    fg.description(rssmeta["desc"])

    for i in comics:
        fe = fg.add_entry()
        full_url = str(base_url+i.html_filename)
        link = {"href":full_url, "rel":"alternate", "type":"image",
                "hreflang":i.lang, "title":i.title}
        fe.id(full_url)
        fe.link(link)
        authord = {"name":i.author, "email":i.author_email}
        fe.author(authord)
        ## Feedgen throws a fit if it doesn't get a timezone. This'll
        ## fix its little red wagon.
        utc = timezone.utc
        adate = i.date.replace(tzinfo=utc)
        fe.published(adate)
        fe.title(i.title)
        page = str(i.page_int)
        fe.description(str(i.category+" #"+page))

    rssfeed  = fg.rss_str(pretty=True)

    o_path = os.path.join(".","output","feed.xml")

    fg.rss_file(o_path)
    return(rssfeed)
