#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Copy Theme Files
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

import os, shutil, springheel.parseconf, springheel.springheelinit, springheel.process_icons

def copyTheme(site_style):

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    site_theme_path = os.path.join(c_path,"themes",site_style)
    new_site_theme_path = os.path.join(o_path,assets_path)

    files = os.listdir(site_theme_path)

    for i in files:
        source_path = os.path.join(site_theme_path,i)
        try:
            shutil.copy(source_path,new_site_theme_path)
        except IsADirectoryError:
            pass

    print("Copied assets to %s" % (new_site_theme_path))

    return(new_site_theme_path)

def copyButtons(sitewide_conf):
    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    old_buttons_path = os.path.join(c_path,"socialbuttons")

    files = os.listdir(old_buttons_path)
    
    print("Social icons: %s" % sitewide_conf["social_icons"])

    if sitewide_conf["social_icons"] == "True":
        social_links = springheel.process_icons.getButtons(sitewide_conf)[0]
        print(social_links)

        for item in files:
            for d in social_links:
                if item == d["image"]:
                    source_path = os.path.join(old_buttons_path,item)
                    shutil.copy(source_path,socialbuttons_path)
                elif item == "rss.png":
                    source_path = os.path.join(old_buttons_path,item)
                    shutil.copy(source_path,socialbuttons_path)

        print("Copied social buttons to %s" % (socialbuttons_path))
    else:
        social_links = springheel.process_icons.getButtons(sitewide_conf)[0]
        print(social_links)

        for item in files:
            for d in social_links:
                if item == d["image"]:
                    pass
                elif item == "rss.png":
                    source_path = os.path.join(old_buttons_path,item)
                    shutil.copy(source_path,socialbuttons_path)

        print("Copied RSS feed button to %s" % (socialbuttons_path))
        

    return(socialbuttons_path)

def copyArrows(site_style):

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    old_arrows_path = os.path.join(c_path,"arrows")
    new_arrows_path = os.path.join(o_path,"arrows")

    arrows = os.listdir(old_arrows_path)

    tracking = []

    for arrow in arrows:
        if site_style in str(arrow):
            source_path = os.path.join(old_arrows_path,arrow)
            shutil.copy(source_path,new_arrows_path)
            tracking.append(str(arrow))
            print("%s found. Adding..." % (str(arrow)))
    if tracking == []:
        print("No navigation arrows found at %s in the currently-set style." % (old_arrows_path))
        return(False)
    elif len(tracking) < 3:
        print("At least one navigation arrow is missing. The navigation will not display correctly. I was able to find the following arrows: %s" % (", ".join(tracking)))
    else:
        print("Copied navigation arrows to %s" % (new_arrows_path))

    return(new_arrows_path)

def copyHeader(header):
    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    old_header_path = os.path.join(c_path,"input",header)
    new_header_path = o_path

    shutil.copy(old_header_path,new_header_path)
    print("Site header copied.")

    return(new_header_path)

def copyBanner(banner):
    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    old_banner_path = os.path.join(c_path,"input",banner)
    new_banner_path = o_path

    shutil.copy(old_banner_path,new_banner_path)
    print("Banner %s copied." % (banner))

    return(new_banner_path)

def copyMultiThemes(themes):
    
    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    theme_path = os.path.join(c_path,"themes")
    new_theme_path = os.path.join(o_path,assets_path)
    theme_ds = []

    for theme in themes:
        print(theme)
        t_path = os.path.join(c_path,"themes",theme)
        files = os.listdir(t_path)
        sheet = os.path.join(t_path,"style.css")
        with open(sheet,"r") as f:
            sheet_contents = f.read()

        theme_ds.append({"theme":theme,"o_path":t_path,"files":files,"sheet":sheet,"sheet_contents":sheet_contents})

    style = []

    for d in theme_ds:
        sc = d["sheet_contents"]      
        style.append(sc)        
        for i in d["files"]:
            source_path = d["o_path"]
            try:
                shutil.copy(source_path,new_theme_path)
            except IsADirectoryError:
                pass
            print("Assets copied to %s" % (new_theme_path))

    cstyle = "".join(style)
    new_style_path = os.path.join(new_theme_path,"style.css")
    with open(new_style_path,"w+") as fout:
        fout.write(cstyle)
    print("Concatenated stylesheet written.")

    return()

def copyMultiArrows(themes):

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheelinit.makeOutput()

    for theme in themes:

        old_arrows_path = os.path.join(c_path,"arrows")
        new_arrows_path = os.path.join(o_path,"arrows")

        arrows = os.listdir(old_arrows_path)

        tracking = []

        for arrow in arrows:
            if theme in str(arrow):
                source_path = os.path.join(old_arrows_path,arrow)
                shutil.copy(source_path,new_arrows_path)
                tracking.append(str(arrow))
                print("%s found. Adding..." % (str(arrow)))
        if tracking == []:
            print("No navigation arrows found at %s in the currently-set style." % (old_arrows_path))
            return(False)
        elif len(tracking) < 3:
            print("At least one navigation arrow is missing. The navigation will not display correctly. I was able to find the following arrows: %s" % (", ".join(tracking)))
        else:
            print("Copied navigation arrows to %s" % (new_arrows_path))

    return()












