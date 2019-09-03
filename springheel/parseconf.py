#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########
##  Springheel - Configuration Parser
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

import configparser, os

def parseConf(config_file):

    config = configparser.ConfigParser()
    config.read(config_file,encoding="utf-8")
    config.sections()

    config_od = config._sections

    reg_dicts=[]
    for sec in config_od:
        rdict = dict(config_od[sec])
        reg_dicts.append(rdict)

    reg_range=len(reg_dicts)
    merged_conf=dict([(k,v) for k,v in reg_dicts[0].items()]+[(k,v) for k,v in reg_dicts[1].items()]+[(k,v) for k,v in reg_dicts[2].items()]+[(k,v) for k,v in reg_dicts[3].items()])

    return(merged_conf)

##    base_url = config.get("BasicPrefs","base_url")
##    site_author = config.get("BasicPrefs","site_author")
##    site_author_email = config.get("BasicPrefs","site_author_email")
##    lang = config.get("BasicPrefs","language")
##    desc = config.get("BasicPrefs","description")
##    site_title = config.get("BasicPrefs","site_title")
##    country = config.get("BasicPrefs","country")
##
##    site_type = config.get("SiteLayout","site_type")
##    chapters = config.get("SiteLayout","chapters")
##    navdirection = config.get("SiteLayout", "navdirection")
##    characters_page = config.get("SiteLayout","characters_page")
##    store_page = config.get("SiteLayout","store_page")
##    extras_page = config.get("SiteLayout","extras_page")
##    comic_license = config.get("SiteLayout","license")
##
##    rename_images = config.getboolean("SiteStyles","rename_images")
##    image_rename_pattern = config.get("SiteStyles","image_rename_pattern")
##    page_name_trigger = config.get("SiteStyles","page_name_trigger")
##    site_style = config.get("SiteStyles","site_style")
##    banner_filename = config.get("SiteStyles","banner_filename")
##
##    social_icons = config.getboolean("SocialMedia","social_icons")
##    twitter_handle = config.get("SocialMedia","twitter_handle")
##    tumblr_handle = config.get("SocialMedia","tumblr_handle")
##    patreon_handle = config.get("SocialMedia","patreon_handle")
##    pump_url = config.get("SocialMedia","pump_url")
##    diaspora_url = config.get("SocialMedia","diaspora_url")
##    liberapay_handle=config.get("SocialMedia","liberapay_handle")
    

def comicCParse(conf):
    cc = configparser.ConfigParser()
    cc.read(conf,encoding="utf-8")
    cc.sections()

    category = cc.get("ComicConfig","category")
    author = cc.get("ComicConfig","author")
    email = cc.get("ComicConfig","email")
    header = cc.get("ComicConfig","header")
    banner = cc.get("ComicConfig","banner")
    language = cc.get("ComicConfig","language")
    mode = cc.get("ComicConfig","mode")
    status = cc.get("ComicConfig","status")
    chapters = cc.get("ComicConfig","chapters")
    desc = cc.get("ComicConfig","desc")
    chars = cc.get("ComicConfig","chars")
    clicense = cc.get("ComicConfig","license")

    comic_config = {"category":category, "author":author,
                    "email":email, "header":header, "banner":banner,
                    "language":language, "mode":mode, "status":status,
                    "chapters":chapters, "desc":desc,"license":clicense,
                    "chars":chars}
    try:
        clicense_uri = cc.get("ComicConfig","license_uri")
        comic_config["license_uri"] = clicense_uri
    except configparser.NoOptionError:
        pass

    try:
        category_theme = cc.get("ComicConfig","category_theme")
        comic_config["category_theme"] = category_theme
    except configparser.NoOptionError:
        pass

    return(comic_config)
