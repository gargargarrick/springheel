#!/usr/bin/python3
# -*- coding: utf-8 -*-

##  Copyright 2017-2019 garrick. Some rights reserved.
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.

##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Springheel -- a static site generator for webcomics."""

name = "springheel"
author = "gargargarrick"
__version__ = '3.0.2'

class Site:
    def __init__(self):
        self.comics = []

class Config(object):         
    def __init__(self,*file_names):
      parser = configparser.ConfigParser()
      parser.optionxform = str
      found = parser.read(file_names)
      if not found:
          raise ValueError("No cfg file")
      for name in ["Config"]:
          self.__dict__.update(parser.items(name))
class Strip:
    def __init__(self,imagef,metaf,transf):
        self.imagef = imagef
        self.metaf = metaf
        self.transf = transf
      
class Comic:
    def __init__(self, category):
        self.category = category

    class Page:
        def __init__(self, category, page_number):
            self.category = category
            self.page_number = page_number
    class Chapter:
        def __init__(self,chap_number,chap_title):
            self.chap_number = chap_number
            self.chap_title = chap_title
            self.pages = []

import springheel.genchars
import springheel.generatearchive
import springheel.generatenav
import springheel.genmultipleindex
import springheel.gentrans
import springheel.genrss
import springheel.gentopnav
import springheel.gettemplatenames
import springheel.parsemeta
import springheel.parsetranscript
import springheel.springheelinit
import springheel.genextra

import shutil
import configparser, os, datetime, sys
from operator import itemgetter
from slugify import slugify

def logMsg(message,path):
    logfile = os.path.join(path,"springheel.log")
    now = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    message = "".join(["\n",now," -- ",message])
    with open(logfile,"a+") as lf:
        lf.write(message)

def wrapImage(link,title,image):
    line = """<a href="{link}"><img src="socialbuttons/{image}" alt="{title}" width="24" height="24" /></a>""".format(link=link,image=image,title=title)
    return(line)

def getButtons(site,rss_s):
    twitter_handle =  site.config.twitter_handle
    tumblr_handle =  site.config.tumblr_handle
    patreon_handle =  site.config.patreon_handle

    pump_url =  site.config.pump_url
    diaspora_url =  site.config.diaspora_url
    liberapay_handle= site.config.liberapay_handle

    social_links = []
    
    if site.config.social_icons == "False":
        rss_link = {"url":"feed.xml", "site":"", "title":rss_s, "image":"rss.png"}
        social_links.append(rss_link)

    if twitter_handle != "False":
        twitter_url = "http://twitter.com/"+twitter_handle
        twitter = {"url":twitter_url, "site":"twitter","title":"Twitter","image":"twitter.png"}
        social_links.append(twitter)
    if tumblr_handle != "False":
        tumblr_url = "http://"+tumblr_handle+".tumblr.com"
        tumblr = {"url":tumblr_url,"site":"tumblr","title":"tumblr.","image":"tumblr.png"}
        social_links.append(tumblr)
    if patreon_handle != "False":
        patreon_url = "https://www.patreon.com/"+patreon_handle
        patreon = {"url":patreon_url,"site":"Patreon","title":"Patreon","image":"patreon.png"}
        social_links.append(patreon)
    if liberapay_handle != "False":
        liberapay_url="https://liberapay.com/"+liberapay_handle
        liberapay={"url":liberapay_url,"site":"Liberapay","title":"Liberapay","image":"liberapay.png"}
        social_links.append(liberapay)
    if pump_url != "False":
        ## An additional, identi.ca-specific icon has also been provided.
        ## To use it, simply move or rename the existing pump.png (just in case) and rename identica.png to pump.png.
        pump = {"url":pump_url,"site":"pump","title":"Pump.io","image":"pump.png"}
        social_links.append(pump)
    if diaspora_url != "False":
        diaspora = {"url":diaspora_url,"site":"diaspora","title":"diaspora*","image":"diaspora.png"}
        social_links.append(diaspora)

    social_icons = []
    for i in social_links:
        icon = wrapImage(i["url"],i["title"],i["image"])
        social_icons.append(icon)

    icons = " ".join(social_icons)
    
    return(social_links,icons)

def copyTheme(site_theme_path,new_site_theme_path):

    files = os.listdir(site_theme_path)

    for i in files:
        source_path = os.path.join(site_theme_path,i)
        try:
            shutil.copy(source_path,new_site_theme_path)
        except IsADirectoryError:
            pass

    logmesg = "Copied assets to {new_site_theme_path}".format(new_site_theme_path=new_site_theme_path)
    logMsg(logmesg,".")

def copyButtons(site,old_buttons_path,socialbuttons_path):

    files = os.listdir(old_buttons_path)
    
    logmesg = "Social icons: {icons}".format(icons=site.config.social_icons)
    logMsg(logmesg,".")
    social_links = getButtons(site,"RSS")[0]

    for item in files:
        for d in social_links:
            if item == d["image"]:
                source_path = os.path.join(old_buttons_path,item)
                shutil.copy(source_path,socialbuttons_path)
            elif item == "rss.png":
                source_path = os.path.join(old_buttons_path,item)
                shutil.copy(source_path,socialbuttons_path)

    if site.config.social_icons == "True":
        logmesg = "Copied social buttons to {socialbuttons_path}".format(socialbuttons_path=socialbuttons_path)
    else:
        logmesg = "Copied RSS feed button to {socialbuttons_path}".format(socialbuttons_path=socialbuttons_path)
    logMsg(logmesg,".")

def copyArrows(site,old_arrows_path,new_arrows_path):

    arrows = os.listdir(old_arrows_path)

    tracking = []

    for arrow in arrows:
        if site.config.site_style in str(arrow):
            source_path = os.path.join(old_arrows_path,arrow)
            shutil.copy(source_path,new_arrows_path)
            tracking.append(str(arrow))
            logmesg = "{arrow} found. Adding...".format(arrow=str(arrow))
            logMsg(logmesg,".")
    if tracking == []:
        logmesg = "No navigation arrows found at {old_arrows_path} in the currently-set style.".format(old_arrows_path=old_arrows_path)
        return(False)
    elif len(tracking) < 3:
        trackingj = ", ".join(tracking)
        logmesg = "At least one navigation arrow is missing. The navigation will not display correctly. I was able to find the following arrows: {arrows}".format(arrows=trackingj)
        logMsg(logmesg,".")
    else:
        logmesg = "Copied navigation arrows to {new_arrows_path}".format(new_arrows_path=new_arrows_path)
        logMsg(logmesg,".")

def copyHeader(old_header_path,new_header_path):

    shutil.copy(old_header_path,new_header_path)
    logmesg = "Site header copied."
    logMsg(logmesg,".")

def copyBanner(old_banner_path,new_banner_path,banner):

    shutil.copy(old_banner_path,new_banner_path)
    logmesg = "Banner {banner} copied.".format(banner=banner)
    logMsg(logmesg,".")

def copyMultiThemes(themes,c_path,o_path,assets_path):

    theme_path = os.path.join(c_path,"themes")
    new_theme_path = os.path.join(o_path,assets_path)
    theme_ds = []

    for theme in themes:
        t_path = os.path.join(c_path,"themes",theme)
        files = os.listdir(t_path)
        sheet = os.path.join(t_path,"style.css")
        with open(sheet,"r",encoding="utf-8") as f:
            sheet_contents = f.read()

        theme_ds.append({"theme":theme,"o_path":t_path,"files":files,"sheet":sheet,"sheet_contents":sheet_contents})

    style = []

    for d in theme_ds:
        sc = d["sheet_contents"]      
        style.append(sc)        
        for i in d["files"]:
            source_dir = d["o_path"]
            source_path = os.path.join(source_dir,i)
            try:
                shutil.copy(source_path,new_theme_path)
            except IsADirectoryError:
                pass
            logmesg = "{source_path} copied to {new_theme_path}".format(source_path=source_path,new_theme_path=new_theme_path)
            logMsg(logmesg,".")

    cstyle = "".join(style)
    new_style_path = os.path.join(new_theme_path,"style.css")
    with open(new_style_path,"w+") as fout:
        fout.write(cstyle)
    logmesg = "Concatenated stylesheet written."
    logMsg(logmesg,".")

    return()

def copyMultiArrows(themes,c_path,o_path,assets_path):

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
                logmesg = "{arrow} found. Adding...".format(arrow=str(arrow))
                logMsg(logmesg,".")
        if tracking == []:
            logmesg = "No navigation arrows found at {old_arrows_path} in the currently-set style.".format(old_arrows_path=old_arrows_path)
            logMsg(logmesg,".")
            return(False)
        elif len(tracking) < 3:
            logmesg = "At least one navigation arrow is missing. The navigation will not display correctly. I was able to find the following arrows: {tracking}".format(tracking=", ".join(tracking))
            logMsg(logmesg,".")
        else:
            logmesg = "Copied navigation arrows to {new_arrows_path}".format(new_arrows_path=new_arrows_path)
            logMsg(logmesg,".")

    return()

def getComics():

    original_path = os.getcwd()

    path = os.path.join(original_path,"input")
    os.chdir(path)

    files = os.listdir()
    
    ## Get a list of images that have the proper meta files.

    images = []
    image_extensions = [".png", ".gif", ".jpg", ".jpeg", ".svg", ".webp"]

    for i in files:
        ext = os.path.splitext(i)[1]
        if ext in image_extensions:
            images.append(i)

    comics = []
    for i in images:
        noext = os.path.splitext(i)[0]
        transcr = noext+".transcript"
        meta = noext+".meta"
        if transcr in files and meta in files:
            logmesg = "Metadata and transcript found for {image}.".format(image=i)
            logMsg(logmesg,original_path)
            comic = Strip(imagef=i,transf=transcr,metaf=meta)
            comics.append(comic)
        elif meta in files and transcr not in files:
            logmesg = "Metadata found, but no transcript for {image}. Please create {transcr}".format(image=i,transcr=transcr)
            logMsg(logmesg,original_path) 
            comic = Strip(imagef=i,transf="no_transcript.transcript",metaf=meta)
            comics.append(comic)
        elif transcr in files and meta not in files:
            logmesg = "Transcript found, but no metadata for {image}. I can't build the page without metadata. Please create {meta}".format(image=i,meta=meta)
            logMsg(logmesg,original_path)
            return(False)
        else:
            logmesg = "{image} doesn't seem to be a comic, as it is missing a transcript and metadata.".format(image=i)
            logMsg(logmesg,original_path)

    if comics == []:
        logmesg = "The comics list is empty. Please add some comics and then try to build again."
        logMsg(logmesg,".")
        return(False)

    os.chdir(original_path)

    return(comics)

def getChapters(chapter_file):
    with open(chapter_file,"r",encoding="utf-8") as f:
        chapter_raws = f.readlines()
    chapters = []
    for line in chapter_raws:
        if line != "":
            split_line = line.split(" = ")
            d = {"num":int(split_line[0]), "title":split_line[1]}
            chapters.append(d)
    return(chapters)

def wrapWithTag(s,tag):
    wrapped = "<{tag}>{s}</{tag}>".format(tag=tag,s=s)
    return(wrapped)

def wrapWithComment(s,comment):
    wrapped = "<!--{comment}-->{s}<!--END {comment}-->".format(comment=comment, s=s)
    return(wrapped)

def checkExtremes(l):
    highest = max(l)
    lowest = min(l)
    return(highest,lowest)

def makeFilename(series_slug,page):
    ##pattern: series_slug_page.html
    file_name_components = [series_slug,page]
    file_name = str("_".join(file_name_components)+".html")
    return(file_name)

def build():
    site = Site()
    sep = "\n"
    falses = [False,"False"]
    config = Config("conf.ini")
    site.config = config
    image_rename_pattern = site.config.image_rename_pattern
    ## Initialize log to avoid confusion
    logfile = os.path.join(".","springheel.log")
    with open(logfile,"w+") as lf:
        lf.write("== Springheel Build Log ==")

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheelinit.makeOutput()
    i_path = os.path.join(c_path,"input")

    ## Get some config variables

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheel.springheelinit.makeOutput()

    site_theme_path = os.path.join(c_path,"themes",site.config.site_style)
    new_site_theme_path = os.path.join(o_path,assets_path)

    old_buttons_path = os.path.join(c_path,"socialbuttons")

    old_arrows_path = os.path.join(c_path,"arrows")
    new_arrows_path = os.path.join(o_path,"arrows")

    old_header_path = os.path.join(c_path,"input",site.config.banner_filename)
    new_header_path = o_path
    
    ## Copy assets from the Springheel installation directory

    copyTheme(site_theme_path,new_site_theme_path)
    copyButtons(site,old_buttons_path,socialbuttons_path)
    copyArrows(site,old_arrows_path,new_arrows_path)
    copyHeader(old_header_path,new_header_path)

    html_filenames = []
    ## Get a list of dictionaries that map image files to metadata
    comics_base = getComics()

    ## Get template paths
    base_t,chars_t,archive_t,index_t,extra_t = gettemplatenames.getTemplateNames()

    ## Select the right template for the specific site type we have
    all_page_ints = []
    if site.config.site_type == "single":
        single = True
    else:
        single = False

    if single == True:
        index_t = index_t+".single"
        archive_t = archive_t+".single"
    else:
        index_t = index_t+".multi"
        archive_t = archive_t+".multi"

    ## Get translation strings, too.
    templates_path = springheelinit.getTemplatesPath()[1]
    translated_strings = gentrans.generateTranslations(site.config.language, templates_path)

    #### Get basic info first.
    for i in comics_base:
        file_name = os.path.join(i_path,i.metaf)
        meta,commentary,slugs = parsemeta.parseMetadata(single,file_name,translated_strings)
        ## Page number
        page = meta["page"]
        page_int = int(page)
        i.metadata = meta
        i.commentary = commentary
        i.slugs = slugs
        i.title_slug = slugs[0]
        i.series_slug = slugs[1]
        i.title_line = slugs[2]
        i.category = i.metadata["category"]
        i.page = page
        i.page_int = page_int
        all_page_ints.append(page_int)

    if single == True:
        last_page,first_page = checkExtremes(all_page_ints)
        cat = comics_base[0].category
        cats_raw = [cat]
        cats_w_pages = [{'category':cat, 'first_page': first_page, 'last_page': last_page}]
    else:
        cats_raw = []
        cats_w_pages = []
        for i in comics_base:
            if i.category not in cats_raw:
                cat = i.category
                cats_raw.append(cat)
        for cat in cats_raw:
            cat_pages = []
            for page in comics_base:
                if page.category == cat:
                    cat_pages.append(page.page_int)
            last_page,first_page = checkExtremes(cat_pages)
            cat_w_pages = {"category":cat,"last_page":last_page,
                           "first_page":first_page}
            cats_w_pages.append(cat_w_pages)

    comics = []
    configs = []
    ccomics = []

    for cat in cats_w_pages:
        c = Comic(cat["category"])
        c.last_page = cat["last_page"]
        c.first_page = cat["first_page"]
        ccomics.append(c)

    ## Get other pages.
    characters_page = site.config.characters_page
    extras_page = site.config.extras_page
    store_page = site.config.store_page

    if characters_page == "True":
        characters_page = True
    else:
        characters_page = False

    if extras_page == "True":
        extras_page = True
    else:
        extras_page = False

    if store_page == "False":
        store_page = False

    ## why did I already use "top_nav" smh
    site_nav_raw = gentopnav.genTopNav(characters_page,
                                       extras_page,
                                       store_page,
                                       translated_strings)
    top_site_nav = sep.join(site_nav_raw)

    cpages = []
    themes = [site.config.site_style]
    chapters_list = []
    logmesg = ", ".join(themes)
    logMsg(logmesg,".")

    for i in comics_base:
        file_name = i.imagef
        meta = i.metadata
        commentary = i.commentary
        slugs = i.slugs

        transcript_file = os.path.join(
            i_path,
            i.transf)
        transcript = parsetranscript.makeTranscript(
            transcript_file)
        if transcript == "No transcript file found.":
            no_trans_p = wrapWithTag(translated_strings["no_transcript"],"p")
            transcript = no_trans_p
        conf_file = os.path.join(
            i_path,
            meta["conf"])
        conf = springheel.parseconf.comicCParse(conf_file)

        i.transcript_c = transcript
        i.conf_c = conf
        category=conf["category"]

        try:
            category_theme = conf["category_theme"]
            themes.append(category_theme)
        except KeyError:
            category_theme = False

        match = [item for item in ccomics if item.category == category][0]

        if conf not in configs:
            configs.append(conf)
            match.author = conf["author"]
            match.email = conf["email"]
            match.header = conf["header"]
            match.banner = conf["banner"]
            match.language = conf["language"]
            match.mode = conf["mode"]
            match.status = conf["status"]
            match.chapters = conf["chapters"]
            if match.chapters not in falses:
                match.chapters = True
                match.chapters_file = os.path.join(i_path,conf["chapters"])
            else:
                match.chapters = False
            match.desc = conf["desc"]
            if category_theme:
                match.category_theme = category_theme
        else:
            logmesg = "{category} config already found...".format(category=category)
            logMsg(logmesg,".")

        old_banner_path = os.path.join(c_path,"input",match.banner)
        new_banner_path = o_path
        if os.path.exists(new_banner_path) == False:
            copyBanner(old_banner_path,new_banner_path,match.banner)

        lang = conf["language"]
        page = i.page
        page_int = i.page_int

        author=conf["author"]
        author_email=conf["email"]
        mode = conf["mode"]
        banner = conf["banner"]
        header = conf["header"]
        if characters_page == True:
            chars_file = conf["chars"]

        if match.chapters not in falses:
            chapters_dicts = getChapters(match.chapters_file)
            match.chapters_dicts = chapters_dicts
            for chapter in chapters_dicts:
                ## Check if chapter exists already
                try:
                    chap_check = [item for item in match.chapters_list if item.chap_number == chapter["num"]]
                    if len(chap_check) == 0:
                        chap = match.Chapter(chapter["num"],chapter["title"])
                        chapters_list.append(chap)
                except AttributeError:
                    pass
            match.chapters_list = chapters_list
            logMsg("Chapters:",".")
            for asdf in match.chapters_list:
                logMsg(str(asdf.__dict__),".")
        else:
            logMsg("{match} has a chapter setting of {chapter}.".format(match=match.category,chapter=match.chapters),".")
            match.chapters_list = []

        title = meta["title"]
        series_slug = i.series_slug
        title_slug = i.title_slug
        match.slug = series_slug
        date = datetime.datetime.strptime(meta["date"],"%Y-%m-%d")
        year = date.year
        if "alt" in meta.keys():
            alt_text = meta["alt"]
        else:
            alt_text = False
        
        ## Make hte license
        clicense = conf["license"]
        ### Init publicdomain
        publicdomain = False
        if conf["license_uri"]:
            license_uri = conf["license_uri"]
            if clicense.lower() == "public domain" or "publicdomain" in license_uri:
                publicdomain = True
                ## Creative Commons Public Domain Waiver
                ccpdw = translated_strings["ccpdw"]
                license_s = ccpdw.format(
                    site_url=site.config.base_url,
                    author=author,
                    site_title=category,
                    author_country=site.config.base_url)
            elif "creativecommons.org/licenses/by" in license_uri:
                cc = translated_strings["cc"]
                license_s = cc.format(
                    license_uri=license_uri,
                    clicense=clicense,
                    author=author,
                    category=category,
                    base_url=site.config.base_url)
        else:
            license_s = clicense

        img_path=i.imagef
        if "chapter" in meta.keys():
            chapter = meta["chapter"]
        else:
            chapter = False

        if single == False:
            matching_cat = [item for item in cats_w_pages if item["category"] == meta["category"]][0]
            last_page = matching_cat["last_page"]
            first_page = matching_cat["first_page"]

        if page_int == last_page:
            final = True
        else:
            final = False
        if page_int == first_page:
            first = True
        else:
            first = False

        #this_page = match.Page(category, page)
        #cpages.append(this_page)

        i.author = author
        i.author_email=author_email
        i.mode = mode
        i.banner = banner
        i.header = header
        i.page_int = int(page)

        i.series_slug = series_slug
        i.date = date
        i.date_s = datetime.datetime.strftime(date,"%Y-%m-%d")
        i.year = year
        i.license = license_s
        i.title = title
        i.img = img_path
        if alt_text == False:
            alt_text = i.title
            i.alt_text = alt_text
        else:
            i.alt_text = alt_text
        if chapter != "False":
            i.chapter = chapter

        if category_theme:
            navblock,linkrels = generatenav.navGen(
                site.config.navdirection,
                page_int,
                first_page,
                last_page,
                first,
                final,
                series_slug,
                category_theme,
                translated_strings)
        else:
            navblock,linkrels = generatenav.navGen(
                site.config.navdirection,
                page_int,
                first_page,
                last_page,
                first,
                final,
                series_slug,
                site.config.site_style,
                translated_strings)
        ##linkrels = generatenav.linkrels

        top_nav = wrapWithComment(navblock,"TOP NAVIGATION")
        bottom_nav = wrapWithComment(navblock,"BOTTOM NAVIGATION")

        page_title = "{category} #{page} - {title}".format(category=meta["category"],
            page=meta["page"],
            title=meta["title"])

        ##header_title = wrapWithTag(page_title,"title")
        header_title = page_title
        h1_title = translated_strings["h1_s"].format(category=meta["category"],  page=meta["page"], title=meta["title"])
        i.h1_title = h1_title
        i.header_title = header_title

        stat_s = translated_strings["statline_s"].format(author=meta["author"],
            date=meta["date"])

        stat_line = """<p class="statline">{stat_s}""".format(stat_s=stat_s)

        tags_in_keys = "tags" in meta.keys()
        if tags_in_keys == True:
            tline = " &mdash; {tags_s}: {tags} &mdash; ".format(
                tags_s=translated_strings["tags_s"],
                tags=meta["tags"])
            stat_line = stat_line+tline

        transcript_block = ["<!--TRANSCRIPT--> ", '<div role="region" id="transcript" aria-label="Transcript"><h2>{transcript_s}</h2>'.format(transcript_s =
            translated_strings["transcript_s"])]

        transcript_block.append(transcript)
        transcript_block.append("</div>")
        transcript_block.append("<!--CONCLUDE TRANSCRIPT-->""")

        tb = "\n".join(transcript_block)

        if publicdomain == False:
            copyright_statement = "<p>&copy; {year} {author}. {clicense}</p>".format(
                year=year,
                author=author,
                clicense=license_s)
        else:
            copyright_statement = wrapWithTag(
                license_s,
                "p")

        i.copyright_statement = copyright_statement

        statuses = [translated_strings["inprogress_s"], translated_strings["complete_s"], translated_strings["hiatus_s"], "Status Not Found - Please add one of 'in-progress', 'complete', or 'dead' to this comic's .conf file!"]

        if match.status == "in-progress":
            status = statuses[0]
        elif match.status == "complete":
            status = statuses[1]
        elif match.status == "hiatus":
            status = statuses[2]
        else:
            status = statuses[3]

        match.statuss = wrapWithTag(status, "strong")
        
        ###########################################################################
        # Generate the actual page!
        ###########################################################################
        
        html_filename = makeFilename(
            series_slug,
            page)
        html_filenames.append(html_filename)
        out_file = os.path.join(
            o_path,
            html_filename)
        
        template_name = base_t
        template = os.path.join(
            c_path,
            template_name)

        with open(template) as f:
            base_template = f.read()

        next_page=str(page_int+1)

        statline = stat_line
        if site.config.social_icons == "True":
            icons = getButtons(site,translated_strings["rss_s"])[1]
        else:
            icons = ""

        if category_theme:
            style = category_theme
        else:
            style = site.config.site_style

        renamed_fn = image_rename_pattern.format(
            comic=series_slug,
            page=page,
            titleslug=title_slug,
            date=i.date_s,
            ext=img_path[-3:])
        renamed_path = os.path.join(
            pages_path,
            renamed_fn)
        source_path = os.path.join(
            i_path,
            img_path)
        shutil.copyfile(
            source_path,
            renamed_path)

        new_meta = image_rename_pattern.format(
            comic=series_slug,
            page=page,
            titleslug=title_slug,
            date=i.date_s,
            ext="meta")
        new_meta_path = os.path.join(
            pages_path,
            new_meta)
        old_meta_path = os.path.join(
            i_path,
            i.metaf)
        shutil.copyfile(
            old_meta_path,
            new_meta_path)

        new_transcr = image_rename_pattern.format(
            comic=series_slug,
            page=page,
            titleslug=title_slug,
            date=i.date_s,
            ext="transcript")
        if os.path.basename(transcript_file) != "no_transcript.transcript":
            new_transcr_path = os.path.join(pages_path,new_transcr)
            old_transcr_path = os.path.join(i_path,transcript_file)
            shutil.copyfile(old_transcr_path,new_transcr_path)

        n_string = base_template.format(
            lang=lang,
            site_style=style,
            header_title=header_title,
            linkrels=linkrels,
            banner=banner,
            category=category,
            top_site_nav=top_site_nav,
            h1_title = h1_title,
            alt_text = alt_text,
            top_nav = top_nav,
            next_page=next_page,
            img_path="pages/"+renamed_fn,
            page = page,
            bottom_nav = bottom_nav,
            commentary = commentary,
            statline = statline,
            metadatafile = "pages/"+new_meta,
            tb=tb,
            year=year,
            author=author,
            icons=icons,
            home_s=translated_strings["home_s"],
            archive_s=translated_strings["archive_s"],
            caption_s=translated_strings["caption_s"],
            metadata_s=translated_strings["meta_s"],
            copyright_statement=copyright_statement,
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skip_s=translated_strings["skip_s"],
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"],
            goarchive_s=translated_strings["goarchive_s"])

        logmesg = "Writing {html_fn}...".format(html_fn=html_filename)
        logMsg(logmesg,".")
        with open(out_file,"w+",encoding="utf-8") as fout:
            fout.write(n_string)
        logmesg = "{html_fn} written.".format(html_fn=html_filename)
        logMsg(logmesg,".")
            
        ###########################################################################

        i.clicense = clicense
        i.file_name = renamed_fn
        i.html_filename = html_filename
        i.lang = lang
        i.meta_fn = new_meta
        i.o_meta_fn = i.metaf
        i.o_transcr_fn = i.transf
        i.page_int = page_int
        i.title_slug = title_slug
        i.transcr_fn = new_transcr
        if match.chapters not in falses:
            #meta["chapter"] = chapter
            i.chapter = chapter

        banner_path = os.path.join(o_path,banner)

        if os.path.exists(banner_path) == False:
            old_banner_path = os.path.join(i_path,banner)
            shutil.copy(old_banner_path,banner_path)
            logMsg(logmesg,".")
            logmesg = "Banner {banner} copied.".format(banner=banner)
            logMsg(logmesg,".")
        else:
            pass

    ## If there are multiple series that have separate themes,
    ## time 2 concatenate the stylesheets.

    if category_theme:
        logmesg = "Categories have separate themes. Concatenating stylesheets..."
        logMsg(logmesg,".")
        copyMultiThemes(themes,c_path,o_path,assets_path)
        copyMultiArrows(themes,c_path,o_path,assets_path)

    ## Generate archives
    logmesg = "Generating archives..."
    logMsg(logmesg,".")

    ## Some things are done by page and some things are done by year.

    cpages_by_page = sorted(comics_base, key=lambda x: x.page_int)
    cpages_by_date = sorted(comics_base, key=lambda x: x.date)

    archives_r = []

    ## Get all pages for each series.
    for cat in cats_raw:
        cur_cat = []
        match = [item for item in ccomics if item.category == cat][0]
        for page in cpages_by_page:
            if page.category == cat:
                cur_cat.append(page)
        match.pbp = cur_cat
        
        cur_cat = []
        for page in cpages_by_date:
            if page.category == cat:
                cur_cat.append(page)
        match.pbd = cur_cat

        allp = len(match.pbd)-1

        match.fbp_link = match.pbp[0].html_filename
        match.lbp_link = match.pbp[allp].html_filename

        match.fbd_link = match.pbd[0].html_filename
        match.lbd_link = match.pbd[allp].html_filename
        
    sdate_comics = cpages_by_date
    spage_comics = cpages_by_page

    ex_by_page = []
    ex_by_date = []
    for comic in ccomics:
        logmesg = "Category: "+comic.category
        logMsg(logmesg,".")

        first_bypage = comic.fbp_link
        last_bypage = comic.lbp_link

        logmesg = "First/last by page:" + ", ".join([first_bypage,last_bypage])
        logMsg(logmesg,".")

        d = {"category":category,"first_bypage":first_bypage,
             "last_bypage":last_bypage}
        ex_by_page.append(d)
        
    for comic in ccomics:
        logmesg = "Category: "+comic.category
        logMsg(logmesg,".")

        first_bydate = comic.fbd_link
        last_bydate = comic.lbd_link

        d = {"category":category,"first_bydate":first_bydate,
             "last_bydate":last_bydate}
        ex_by_date.append(d)

    archive_d_secs = []

    logmesg = "Got first and last strips for each series..."
    logMsg(logmesg,".")

    for comic in ccomics:
        logmesg = "Generating archive..."
        logMsg(logmesg,".")
        category = comic.category
        status = comic.statuss
        comic_header = comic.header
        desc = comic.desc
        logmesg = "Currently working on {category}.".format(category=category)
        logMsg(logmesg,".")

        ## Get the comic-specific header.
        old_cheader_path = os.path.join(c_path,"input",comic_header)
        new_cheader_path = o_path

        copyHeader(old_cheader_path,new_cheader_path)
        ## This got reset somewhere? Huh
        match = [item for item in ccomics if item.category == page.category][0]

        archive_links_page = []
        archive_links_date = []
        for i in comic.pbp:
            archive_link = generatearchive.getLinks(i,translated_strings)
            i.archive_link = archive_link
            archive_links_page.append(archive_link)
        for i in comic.pbd:
            archive_link = generatearchive.getLinks(i,translated_strings)
            archive_links_date.append(archive_link)
        archive_sections_date = generatearchive.generateSeriesArchives(
            category,
            status,
            archive_links_page)
        archive_d_secs.append(archive_sections_date)

        if comic.chapters not in falses:
            for page in comic.pbp:
                if hasattr(page,"chapter"):
                    match = [item for item in ccomics if item.category == page.category][0]
                    cho = [item for item in match.chapters_list if item.chap_number == int(page.chapter)][0]
                    cho.pages.append(page)
                else:
                    logmesg = "No chapters found."
                    logMsg(logmesg,".")

        if comic.chapters not in falses:
            chapter_sections = []
            for chapi in match.chapters_list:
                in_this_chapter = []
                for page in chapi.pages:
                    in_this_chapter.append(page.archive_link)
                if single == True:
                    header_level = "2"
                else:
                    header_level = "3"
                archive_list = generatearchive.generateChapArchList(
                    in_this_chapter,
                    chapi.chap_number,
                    chapi.chap_title,
                    translated_strings,
                    header_level)
                chapter_sections.append(archive_list)
            chapter_sections_j = sep.join(chapter_sections)
            if single == False:
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<h2>{category}</h2>',
                                               '<p class="status">{status}</p>',
                                               chapter_sections_j,
                                               "</section>"])
            else:
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<p class="status">{status}</p>',
                                               chapter_sections_j,
                                               "</section>"])
            chapter_archives = chapter_archives_r.format(
                category=comic.category,status=comic.statuss)
            archives_r.append(chapter_archives)
        else:
            archive_sections = sep.join(archive_d_secs)
            archives_r.append(archive_sections)

    archives = sep.join(archives_r)
        
    arch_template_name = archive_t
    arch_template = os.path.join(c_path,arch_template_name)

    link_rel_l = ['<link rel="alternate" type="application/rss+xml" title="{rss_s}" href="feed.xml">'.format(rss_s=translated_strings["rss_s"])]
    link_rel = sep.join(link_rel_l)

    out_file = os.path.join(o_path,"archive.html")

    archive_header_title = "{site_title} - Archive".format(site_title=site.config.site_title)

    with open(arch_template) as f:
        arch_template = f.read()

        arch_string = arch_template.format(
            lang=lang,
            site_style=site.config.site_style,
            site_title=site.config.site_title,
            header_title=archive_header_title,
            linkrels=link_rel,
            banner=site.config.banner_filename,
            category=category,
            status=status,
            top_site_nav=top_site_nav,
            archive_sections=archives,
            year=year,
            author=site.config.site_author,
            copyright_statement=copyright_statement,
            icons=icons,
            home_s=translated_strings["home_s"],
            archive_s=translated_strings["archive_s"],
            stylesheet_name_s=translated_strings["stylesheet_name_s"],
            skip_s=translated_strings["skip_s"],
            page_s=translated_strings["page_s"],
            meta_s=translated_strings["meta_s"],
            generator_s=translated_strings["generator_s"],
            goarchive_s=translated_strings["goarchive_s"])

        logmesg = "Writing {archive}...".format(archive="archive.html")
        logMsg(logmesg,".")
        with open(out_file,"w+",encoding="utf-8") as fout:
            fout.write(arch_string)
        logmesg = "{archive} written.".format(archive="archive.html")
        logMsg(logmesg,".")

    ##Generate feed

    base_url = site.config.base_url

    rssmeta = {
            "author":site.config.site_author,
            "email":site.config.site_author_email,
            "language":site.config.language,
            "link":site.config.base_url,
            "desc":site.config.description,
            "title":site.config.site_title
        }

    rss = genrss.generateFeed(site.config.base_url,rssmeta,comics_base)

    ## Generate main page

    if single == True:
        template = os.path.join(c_path,index_t)

        out_file = os.path.join(o_path,"index.html")

        logmesg = "First/last by page:" + ", ".join([first_bypage,last_bypage])
        logMsg(logmesg,".")

        with open(template) as f:
            index_template = f.read()

            n_string = index_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=site.config.site_title,
                linkrels=link_rel,
                banner=site.config.banner_filename,
                site_title=site.config.site_title,
                category=category,
                top_site_nav=top_site_nav,
                header=header,
                desc=desc,
                status=status,
                latest=last_bypage,
                first=first_bypage,
                archive="archive.html",
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                golatest_s=translated_strings["golatest_s"],
                gofirst_s=translated_strings["gofirst_s"],
                generator_s=translated_strings["generator_s"],
                goarchive_s=translated_strings["goarchive_s"])


            logmesg = "Writing {indexh}...".format(indexh="index.html")
            logMsg(logmesg,".")
            with open(out_file,"w+",encoding="utf-8") as fout:
                fout.write(n_string)
            logmesg = "{indexh} written.".format(indexh="index.html")
            logMsg(logmesg,".")
    else:
        multi_secs = genmultipleindex.genMultipleIndex(
            ccomics,
            characters_page,
            translated_strings)
        secs = sep.join(multi_secs)

        template = os.path.join(c_path,index_t)

        out_file = os.path.join(o_path,"index.html")

        with open(template) as f:
            index_template = f.read()

            n_string = index_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=site.config.site_title,
                linkrels=link_rel,
                banner=site.config.banner_filename,
                site_title=site.config.site_title,
                category=site.config.site_title,
                top_site_nav=top_site_nav,
                multi_secs=secs,
                year=year,
                author=site.config.site_author,
                copyright_statement=copyright_statement,
                icons=icons,
                home_s=translated_strings["home_s"],
                archive_s=translated_strings["archive_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                skip_s=translated_strings["skip_s"],
                page_s=translated_strings["page_s"],
                meta_s=translated_strings["meta_s"],
                generator_s=translated_strings["generator_s"],
                goarchive_s=translated_strings["goarchive_s"])


            logmesg = "Writing {indexh}...".format(indexh="index.html")
            logMsg(logmesg,".")
            with open(out_file,"w+",encoding="utf-8") as fout:
                fout.write(n_string)
            logmesg = "{indexh} written.".format(indexh="index.html")
            logMsg(logmesg,".")

    ## Generate characters page if necessary.
    if characters_page == True:

        character_pages = []

        for conf in configs:
            
            fn = conf["chars"]
            fp = os.path.join(i_path,fn)
            logmesg = "Loading characters file {fn}...".format(fn=fn)
            logMsg(logmesg,".")

            try:
                with open(fp,"r",encoding="utf-8") as f:
                    raw_text = f.read()
            except UnboundLocalError:
                logmesg = "An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist."
                logMsg(logmesg,".")
            except FileNotFoundError:
                logmesg = "The characters page couldn't be built because I couldn't find the characters file at {fp}.".format(fp=fp)
                logMsg(logmesg,".")
            characters_parsed = genchars.parseChars(raw_text)
            character_elements = genchars.genCharsPage(characters_parsed)

            ##Get character images
            for char in characters_parsed:
                if type(char) == list:
                    if char[2][1] != "None":
                        img_source_path = os.path.join(i_path,char[2][1])
                        img_out_path = os.path.join(o_path,char[2][1])
                        shutil.copy(img_source_path,img_out_path)
            
            chars_template_path = os.path.join(c_path,chars_t)

            cat_slug = slugify(conf["category"])

            if single == True:
                out_name = "characters.html"
            else:
                out_name = "".join([cat_slug,"-","characters.html"])
                cpd = {"charpage":out_name,
                       "category":conf["category"]}
                character_pages.append(cpd)

            out_file = os.path.join(o_path,out_name)

            chars_title_line = " - ".join([conf["category"],translated_strings["char_s"]])

            with open(chars_template_path) as f:
                chars_template = f.read()

                n_string = chars_template.format(
                    lang=lang,
                    site_style=site.config.site_style,
                    header_title=chars_title_line,
                    linkrels=link_rel,
                    banner=banner,
                    banner_alt=category,
                    title_line=translated_strings["char_s"],
                    top_site_nav=top_site_nav,
                    chars = character_elements,
                    year=year,
                    author=site.config.site_author,
                    copyright_statement=copyright_statement,
                    icons=icons,
                    home_s=translated_strings["home_s"],
                    archive_s=translated_strings["archive_s"],
                    stylesheet_name_s=translated_strings["stylesheet_name_s"],
                    skip_s=translated_strings["skip_s"],
                    page_s=translated_strings["page_s"],
                    meta_s=translated_strings["meta_s"],
                    generator_s=translated_strings["generator_s"],
                    goarchive_s=translated_strings["goarchive_s"])


                logmesg = "Writing {out_name}...".format(out_name=out_name)
                logMsg(logmesg,".")
                with open(out_file,"w+",encoding="utf-8") as fout:
                    fout.write(n_string)
                logmesg = "{out_name} written.".format(out_name=out_name)
                logMsg(logmesg,".")

        if single == False:
            out_name = "characters.html"
            out_file = os.path.join(o_path,out_name)

            chars_title_line = " - ".join([site.config.site_title,translated_strings["char_s"]])

            charpage_elements = ['<div class="allchars">']

            for chpage in character_pages:
                character_page_line = ['<p><a href="',
                    chpage["charpage"],
                    '">',
                    chpage["category"],
                    "</a></p>"]
                character_page_line = "".join(character_page_line)
                charpage_elements.append(character_page_line)
            charpage_elements.append("</div>")
            charpages = sep.join(charpage_elements)

            with open(chars_template_path) as f:
                chars_template = f.read()

                n_string = chars_template.format(
                    lang=lang,
                    site_style=site.config.site_style,
                    header_title=chars_title_line,
                    linkrels=link_rel,
                    banner=site.config.banner_filename,
                    banner_alt=site.config.site_title,
                    title_line=chars_title_line,
                    top_site_nav=top_site_nav,
                    chars = charpages,
                    year=year,
                    author=site.config.site_author,
                    copyright_statement=copyright_statement,
                    icons=icons,
                    home_s=translated_strings["home_s"],
                    archive_s=translated_strings["archive_s"],
                    stylesheet_name_s=translated_strings["stylesheet_name_s"],
                    skip_s=translated_strings["skip_s"],
                    page_s=translated_strings["page_s"],
                    meta_s=translated_strings["meta_s"],
                    generator_s=translated_strings["generator_s"],
                    goarchive_s=translated_strings["goarchive_s"])


                logmesg = "Writing {out_name}...".format(out_name=out_name)
                logMsg(logmesg,".")
                with open(out_file,"w+",encoding="utf-8") as fout:
                    fout.write(n_string)
                logmesg = "{out_name} written.".format(out_name=out_name)
                logMsg(logmesg,".")
    logmesg = "Springheel compilation complete! ^_^"
    print(logmesg)
    logMsg(logmesg,".")

    ## Generate extras page if necessary.
    if extras_page == True:

        extras_j = os.path.join(i_path,"Extra.json")
        if os.path.exists(extras_j):
            extras = genextra.gen_extra(i_path,o_path,extras_j,translated_strings)
            
            extr_title = " - ".join([category,translated_strings["extra_s"]])

            ex_html_filename = "extras.html"
            out_file = os.path.join(
                o_path,
                ex_html_filename)

            with open(extra_t) as f:
                extra_template = f.read()

            extras_html = extra_template.format(
                lang=lang,
                site_style=site.config.site_style,
                header_title=extr_title,
                h1_title=translated_strings["extra_s"],
                stylesheet_name_s=translated_strings["stylesheet_name_s"],
                home_s=translated_strings["home_s"],
                linkrels=linkrels,
                skip_s=translated_strings["skip_s"],
                banner=banner,
                category=category,
                top_site_nav=top_site_nav,
                extras=extras.content,
                copyright_statement=copyright_statement,
                generator_s=translated_strings["generator_s"],
                icons=icons,
            )

            with open(out_file,"w") as fout:
                fout.write(extras_html)
            logmesg = "Extras page written to {out_file}.".format(out_file=out_file)
            logMsg(logmesg,".")
        else:
            logmesg = "Extra pages are supposed to be generated, but Extras.json wasn't found in input/. Make sure it exists and is valid, then try again."
            logMsg(logmesg,".")
    else:
        logmesg = "Not generating extras page..."
        logMsg(logmesg,".")

## Initialize a Springheel project.
def init():
    lang=springheelinit.getLang()
    springheelinit.copyAssets(lang)

def version():
    print("{name} {version} copyright 2017-2019 {author}. Some rights reserved. See LICENSE.".format(name=springheel.name,author=springheel.author,version=springheel.__version__))
    print("Installed to {dir}.".format(dir=sys.modules['springheel'].__path__[0]))
    print("Run springheel-init to create a new site in the current directory, or springheel-build to regenerate the site.")
        
        






