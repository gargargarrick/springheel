#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Project Initialization
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

import sys, os, shutil
from distutils.dir_util import copy_tree

def initDir(output_path,dir_name):
    dir_path = os.path.join(output_path,dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, mode=0o755)
        os.chmod(dir_path, mode=0o755)
    return(dir_path)

def makeOutput():
    if not os.path.exists("output"):
        os.mkdir("output", mode=0o755)
        os.chmod("output", mode=0o755)
    c_path = os.path.abspath(".")
    output_path = os.path.abspath("output")

    pages_path = initDir(output_path,"pages")
    assets_path = initDir(output_path,"assets")
    arrows_path = initDir(output_path,"arrows")
    socialbuttons_path = initDir(output_path,"socialbuttons")
    templates_path = initDir(c_path, "templates")
    input_path = initDir(c_path, "input")

    return(c_path,output_path,pages_path,assets_path,arrows_path,socialbuttons_path)

def getTemplatesPath():
    ## Get the usr directory of Springheel.
    try:
        raw_springheel_path = sys.modules['springheel'].__path__[0]
        print("Springheel directory found at {path}...".format(path=raw_springheel_path))
    except KeyError:
        print("Could not initialize because the Springheel directory was not found, somehow. I have no idea how you are running this at all. File an issue with the full details, but I may take some time to get back to you.")
        return False
    ## From there, find the path where templates are stored.
    templates_path = os.path.join(raw_springheel_path,"templates")
    return(raw_springheel_path,templates_path)

def copyAssets(lang):
    raw_springheel_path,templates_path = getTemplatesPath()
    strings_path = os.path.join(templates_path, "strings.json")
    ## It's divided up by language.
    #my_lang_templates = os.path.join(templates_path,lang)
    my_lang_templates = templates_path
    print("Getting {lang} templates from {my_lang_templates}...".format(lang=lang,my_lang_templates=my_lang_templates))
    if os.path.exists(my_lang_templates) == False and lang != "en":
        lang="en"
        print("Templates for [{lang}] language were not found, using default language [English] templates...".format(lang=lang))
        my_lang_templates = os.path.join(templates_path,lang)
    elif os.path.exists(my_lang_templates) == False and lang == "en":
        print("The Springheel module was found, but template files in the default language, English, do not exist. What did you do?")
        return False
    current_dir = os.getcwd()

    templates_o = os.path.join(current_dir,"templates")
    
    print("Copying templates to {templates_output}...".format(templates_output=templates_o))
    copy_tree(my_lang_templates,templates_o)

    ## Now get the stuff that's the same in any language.

    print("Copying strings file...")
    new_strings_path = os.path.join(current_dir,"templates","strings.json")
    shutil.copy(strings_path,new_strings_path)
    print("Strings file copied from {old} to {new}.".format(old=strings_path,new=new_strings_path))

    ## input
    input_path = initDir(current_dir,"input")

    ## conf.ini
    o_conf = os.path.join(raw_springheel_path,"conf.ini")
    n_conf = os.path.join(current_dir,"conf.ini")
    if os.path.exists(n_conf) == False:
        try:
            confpy_path = shutil.copy(o_conf,n_conf)
        except FileNotFoundError:
            print("Couldn't find conf.ini in the Springheel install directory. Did you delete it somehow?")
    else:
        print("conf.ini already exists in output directory; not overwriting.")

    ##arrows
    base_arrows_path = os.path.join(raw_springheel_path,"arrows")
    arrows_path = initDir(current_dir,"arrows")
    
    ##themes
    base_themes_path = os.path.join(raw_springheel_path,"themes")
    themes_path = initDir(current_dir,"themes")

    #social buttons
    base_socialbuttons_path = os.path.join(raw_springheel_path,"socialbuttons")
    socialbuttons_path = initDir(current_dir,"socialbuttons")

    copy_tree(base_arrows_path,arrows_path)
    copy_tree(base_themes_path,themes_path)
    copy_tree(base_socialbuttons_path,socialbuttons_path)

    ## I have reasons! Now we shall see!
    return(templates_path)

def getLang():
    lang = input("Language? > ")
    return(lang)

##lang = getLang()
##copyAssets(lang)

