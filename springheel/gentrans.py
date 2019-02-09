#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Translation generator
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

## You may ask why I don't use the existing i18n methods, like gettext.
## Well, the short answer is that I'm too stupid to!
## The long answer is that I generally didn't think the existing libraries
## were a good fit for Springheel's specific setup.

import os, json

def generateTranslations(lang,translation_path):

    print("Getting translation for {lang}...".format(lang=lang))

    strings_path = os.path.join(translation_path,"strings.json")
    with open(strings_path,"r",encoding="utf-8") as f:
        json_data = json.load(f)

    strings = {}
    string_names = ["archive_by_date_s", "home_s", "char_s", "caption_s", "transcript_s", "archive_s", "tags_s","extra_s", "store_s", "chapter_s", "first_s", "prev_s", "next_s", "last_s", "firsts_s", "prevs_s", "nexts_s", "lasts_s", "golatest_s", "gofirst_s", "goarchive_s", "complete_s", "inprogress_s", "hiatus_s", "statline_s", "ccpdw", "cc", "no_comment", "no_transcript", "rss_s", "h1_s", "stylesheet_name_s", "skip_s","page_s","meta_s","generator_s","archive_l_s"]
    for i in string_names:
        try:
            translated_value = json_data[i][lang]
            strings[i] = translated_value
        except KeyError:
            default_value = json_data[i]["en"]
            strings[i] = default_value
    return(strings)
        
        

        
