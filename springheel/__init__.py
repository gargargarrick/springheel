#!/usr/bin/python3
# -*- coding: utf-8 -*-

##  Copyright 2017 garrick. Some rights reserved.
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

__version__ = '0.1'

class Comic:
    def __init__(self, category):
        self.category = category

    class Page:
        def __init__(self, category, page_number):
            self.category = category
            self.page_number = page_number


import springheel.copytheme
import springheel.genchars
import springheel.generatearchive
import springheel.generatenav
import springheel.genmultipleindex
import springheel.gentrans
import springheel.genrss
import springheel.gentopnav
import springheel.getfiles
import springheel.gettemplatenames
import springheel.parseconf
import springheel.parsemeta
import springheel.parsetranscript
import springheel.process_icons
import springheel.springheelinit

import os
import shutil

from operator import itemgetter
from slugify import slugify


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
    sep = "\n"
    sitewide_conf = parseconf.parseConf("conf.py")
    image_rename_pattern = str(sitewide_conf["image_rename_pattern"])

    c_path,o_path,pages_path,assets_path,arrows_path,socialbuttons_path = springheelinit.makeOutput()
    i_path = os.path.join(c_path,"input")

    ## Get configuration variables
    site_title = sitewide_conf["site_title"]
    site_author = sitewide_conf["site_author"]
    site_author_email = sitewide_conf["site_author_email"]
    site_banner = sitewide_conf["banner_filename"]
    site_lang = sitewide_conf["language"]
    site_desc = sitewide_conf["description"]
    site_license = sitewide_conf["license"]
    site_style = sitewide_conf["site_style"]
    site_type = sitewide_conf["site_type"]
    base_url = sitewide_conf["base_url"]
    country = sitewide_conf["country"]
    navdirection = sitewide_conf["navdirection"]

    theme_path = copytheme.copyTheme(site_style)
    buttons_path = copytheme.copyButtons(sitewide_conf)
    arrows_path = copytheme.copyArrows(site_style)
    header_path = copytheme.copyHeader(site_banner)

    html_filenames = []
    comics_base = getfiles.getComics()

    base_t,chars_t,archive_t,index_t = gettemplatenames.getTemplateNames(site_lang)

    ## Figure out wtf I was doing here
    all_page_ints = []
    if site_type == "single":
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

    templates_path = springheelinit.getTemplatesPath(site_lang)[1]
    translated_strings = gentrans.generateTranslations(site_lang, templates_path)

    #### Get basic info first.

    for i in comics_base:
        file_name = os.path.join(i_path,i["meta"])
        meta,commentary,slugs = parsemeta.parseMetadata(single,file_name)
        page = meta["page"]
        page_int = int(page)
        i["metadata"] = meta
        i["commentary"] = commentary
        i["slugs"] = slugs
        i["page"] = page
        i["page_int"] = page_int
        all_page_ints.append(page_int)

    if single == True:
        last_page,first_page = checkExtremes(all_page_ints)
        cat = comics_base[0]["metadata"]["category"]
        cats_raw = [cat]
        cats_w_pages = [{'category':cat, 'first_page': first_page, 'last_page': last_page}]
    else:
        cats_raw = []
        cats_w_pages = []
        for i in comics_base:
            if i["metadata"]["category"] not in cats_raw:
                cat = i["metadata"]["category"] 
                cats_raw.append(cat)
        for cat in cats_raw:
            cat_pages = []
            for page in comics_base:
                if page["metadata"]["category"] == cat:
                    cat_pages.append(page["page_int"])
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
    characters_page = sitewide_conf["characters_page"]
    extras_page = sitewide_conf["extras_page"]
    store_page = sitewide_conf["store_page"]

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
    themes = [site_style]

    for i in comics_base:
        file_name = i["meta"]
        meta = i["metadata"]
        commentary = i["commentary"]
        slugs = i["slugs"]

        transcript_file = os.path.join(
            i_path,
            i["transcript"])
        transcript = parsetranscript.makeTranscript(
            transcript_file)
        if transcript == "No transcript file found.":
            transcript = translated_strings["no_transcript"]
        conf_file = os.path.join(
            i_path,
            meta["conf"])
        conf = springheel.parseconf.comicCParse(conf_file)

        i["transcript_c"] = transcript
        i["conf_c"] = conf
        category=conf["category"]

        try:
            category_theme = conf["category_theme"]
            themes.append(category_theme)
        except KeyError:
            category_theme = False

        match = [item for item in ccomics if item.category == category][0]

        if conf not in configs:
            configs.append(conf)
            ##print("Configs: ",configs)
            match.author = conf["author"]
            match.email = conf["email"]
            match.header = conf["header"]
            match.banner = conf["banner"]
            match.language = conf["language"]
            match.mode = conf["mode"]
            match.status = conf["status"]
            match.chapters = conf["chapters"]
            if match.chapters != "False":
                match.chapters = True
                match.chapters_file = os.path.join(i_path,conf["chapters"])
            else:
                match.chapters = False
            match.desc = conf["desc"]
            if category_theme:
                match.category_theme = category_theme
        else:
            print("%s config already found..." % (category))

        springheel.copytheme.copyBanner(match.banner)
        springheel.copytheme.copyBanner(match.header)

        lang = conf["language"]
        page = i["page"]
        page_int = i["page_int"]

        author=conf["author"]
        author_email=conf["email"]
        mode = conf["mode"]
        banner = conf["banner"]
        header = conf["header"]
        if characters_page == True:
            chars_file = conf["chars"]

        if match.chapters != False:
            match.chapters_list = springheel.parseconf.getChapters(match.chapters_file)

        title = meta["title"]
        series_slug = slugs[1]
        title_slug = slugs[0]
        match.slug = series_slug
        date = meta["date"]
        year = date[0:4]
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
                    site_url=base_url,
                    author=author,
                    site_title = category,
                    author_country = country)
            elif "creativecommons.org/licenses/by" in license_uri:
                cc = translated_strings["cc"]
                license_s = cc.format(
                    license_uri = license_uri,
                    clicense=clicense,
                    author=author,
                    category=category,
                    base_url=base_url)
        else:
            license_s = clicense

        img_path=i["image"]
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

        this_page = match.Page(category, page)
        cpages.append(this_page)

        this_page.author = author
        this_page.author_email=author_email
        this_page.mode = mode
        this_page.banner = banner
        this_page.header = header
        this_page.page_int = int(page)

        this_page.series_slug = series_slug
        this_page.date = date
        this_page.year = year
        this_page.license = license_s
        this_page.title = title
        this_page.img = img_path
        if alt_text == False:
            alt_text = this_page.title
            this_page.alt_text = alt_text
        else:
            this_page.alt_text = alt_text
            print(this_page.alt_text)
        if chapter != "False":
            this_page.chapter = chapter


        if category_theme:
            navblock,linkrels = generatenav.navGen(
                navdirection,
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
                navdirection,
                page_int,
                first_page,
                last_page,
                first,
                final,
                series_slug,
                site_style,
                translated_strings)
        ##linkrels = generatenav.linkrels

        top_nav = wrapWithComment(navblock,"TOP NAVIGATION")
        bottom_nav = wrapWithComment(navblock,"BOTTOM NAVIGATION")

        page_title = "{category} #{page} - {title}".format(category=meta["category"],
                                                           page=meta["page"],title=meta["title"])

        ##header_title = wrapWithTag(page_title,"title")
        header_title = page_title
        h1_title = "{category} #{page} &ldquo;{title}&rdquo;".format(category=meta["category"],
                                                                     page=meta["page"],title=meta["title"])
        this_page.h1_title = h1_title
        this_page.header_title = header_title

        stat_s = translated_strings["statline_s"].format(author=meta["author"],
                                                     date=meta["date"])

        stat_line = """<p class="statline">{stat_s}""".format(stat_s=stat_s)

        tags_in_keys = "tags" in meta.keys()
        if tags_in_keys == True:
            tline = " &mdash; {tags_s}: {tags} &mdash; ".format(tags_s=translated_strings["tags_s"],
                                                                tags=meta["tags"])
            stat_line = stat_line+tline

        transcript_block = ["<!--TRANSCRIPT--> ", '<div role="region" id="transcript" aria-label="Transcript"><h2>{transcript_s}</h2>'.format(transcript_s = translated_strings["transcript_s"])]

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

        this_page.copyright_statement = copyright_statement

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
        if sitewide_conf["social_icons"] == "True":
            icons = springheel.process_icons.getButtons(sitewide_conf)[1]
        else:
            icons = ""


        if category_theme:
            style = category_theme
        else:
            style = site_style

        renamed_fn = image_rename_pattern.format(
            comic=series_slug,
            page=page,
            titleslug=title_slug,
            date=date,
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
            date=date,
            ext="meta")
        new_meta_path = os.path.join(
            pages_path,
            new_meta)
        old_meta_path = os.path.join(
            i_path,
            file_name)
        shutil.copyfile(
            old_meta_path,
            new_meta_path)

        new_transcr = image_rename_pattern.format(
            comic=series_slug,
            page=page,
            titleslug=title_slug,
            date=date,
            ext="transcript")
        if transcript_file[-24:] != "no_transcript.transcript":
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
            copyright_statement=copyright_statement)

        print("Writing %s..." % (html_filename))
        with open(out_file,"w+") as fout:
            fout.write(n_string)
        print("%s written." % (html_filename))
            
        ###########################################################################

        this_page.clicense = clicense
        this_page.file_name = renamed_fn
        this_page.html_filename = html_filename
        this_page.lang = lang
        this_page.meta_fn = new_meta
        this_page.o_meta_fn = i["meta"]
        this_page.o_transcr_fn = i["transcript"]
        this_page.page_int = page_int
        this_page.title_slug = title_slug
        this_page.transcr_fn = new_transcr
        #if match.chapters != "False":
            #meta["chapter"] = chapter
            #this_page.chapter = chapter

        banner_path = os.path.join(o_path,banner)

        if os.path.exists(banner_path) == False:
            old_banner_path = os.path.join(i_path,banner)
            shutil.copy(old_banner_path,banner_path)
            print("Banner %s copied." % (banner))
        else:
            pass

    ## If there are multiple series that have separate themes,
    ## time 2 concatenate the stylesheets.

    if category_theme:
        print("Categories have separate themes. Concatenating stylesheets...")
        copytheme.copyMultiThemes(themes)
        copytheme.copyMultiArrows(themes)

    ## Generate archives
    print("Generating archives...")

    ## Some things are done by page and some things are done by year.

    cpages_by_page = sorted(cpages, key=lambda x: x.page_int)
    cpages_by_date = sorted(cpages, key=lambda x: x.date)

    archives_r = []

    if single == False:
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
            print("Category: "+comic.category)

            first_bypage = comic.fbp_link
            last_bypage = comic.lbp_link

            print("--First/last by page:--")
            print(", ".join([first_bypage,last_bypage]))

            d = {"category":category,"first_bypage":first_bypage,
                 "last_bypage":last_bypage}
            ex_by_page.append(d)
            
        for comic in ccomics:
            print("Category: "+comic.category)

            first_bydate = comic.fbd_link
            last_bydate = comic.lbd_link

            print(", ".join([first_bydate,last_bydate]))

            d = {"category":category,"first_bydate":first_bydate,
                 "last_bydate":last_bydate}
            ex_by_date.append(d)

        archive_d_secs = []

        print("Got first and last strips for each series...")

    ## Clean up this godforsaken mess

        for comic in ccomics:
            print("Generating archive...")
            category = comic.category
            status = comic.statuss
            print("Currently working on %s" % (category))
            archive_links_page = []
            archive_links_date = []
            for i in comic.pbp:
                archive_link = generatearchive.getLinks(i)
                i.archive_link = archive_link
                print(archive_link)
                archive_links_page.append(archive_link)
            for i in comic.pbd:
                archive_link = generatearchive.getLinks(i)
                archive_links_date.append(archive_link)
            archive_sections_date = generatearchive.generateSeriesArchives(
                category,
                status,
                archive_links_page)
            archive_d_secs.append(archive_sections_date)

            if comic.chapters == True:
                chapters = []
                pages_w_chap = []
                for page in comic.pbp:
                    if hasattr(page,"chapter"):
                        chap = page.chapter
                        chapters.append(chap)
                        li = page.archive_link
                        pages_w_chap.append((li,chap))
                    else:
                        print("No chapters found.")

                chapters = list(set(chapters))

            if comic.chapters == True:
                chapter_sections = []
                for chapi in chapters:
                    chapn = int(chapi)
                    chapter_title = [item for item in comic.chapters_list if item["num"] == chapn]
                    chapter_title = chapter_title[0]["title"]
                    in_this_chapter = []
                    for page in comic.pbp:
                        if hasattr(page,"chapter"):
                            chap = page.chapter
                            if chap == chapi:
                                in_this_chapter.append(page.archive_link)
                    archive_list = generatearchive.generateChapArchList(
                        in_this_chapter,
                        chapi,
                        chapter_title,
                        translated_strings)
                    chapter_sections.append(archive_list)
                chapter_sections_j = sep.join(chapter_sections)
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<h2>{category}</h2>',
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

    ## No seriously, do it
            
    else:
        for cat in cats_raw:
            cur_cat = []
            match = [item for item in ccomics if item.category == cat][0]
            for page in cpages_by_page:
                if page.category == cat:
                    cur_cat.append(page)
            match.pbp = cur_cat
            
            cur_cat = []
            for page in cpages_by_page:
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
            print("Category: "+comic.category)

            first_bypage = comic.fbp_link
            last_bypage = comic.lbp_link

            print(", ".join([first_bypage,last_bypage]))

            d = {"category":category,"first_bypage":first_bypage,
                 "last_bypage":last_bypage}
            ex_by_page.append(d)
            
        for comic in ccomics:
            print("Category: "+comic.category)

            first_bydate = comic.fbd_link
            last_bydate = comic.lbd_link

            print(", ".join([first_bydate,last_bydate]))

            d = {"category":category,"first_bydate":first_bydate,
                 "last_bydate":last_bydate}
            ex_by_date.append(d)

        archive_d_secs = []

        print("Got first and last strips for each series...")
        
        for comic in ccomics:
            print("Generating archive...")
            category = comic.category
            archive_links_page = []
            archive_links_date = []
            for i in comic.pbp:
                archive_link = generatearchive.getLinks(i)
                i.archive_link = archive_link
                print(archive_link)
                archive_links_page.append(archive_link)
            for i in comic.pbd:
                archive_link = generatearchive.getLinks(i)
                archive_links_date.append(archive_link)
            archive_sections_date = generatearchive.generateSeriesArchives(category,
                                                                           status,
                                                                           archive_links_page)
            archive_d_secs.append(archive_sections_date)

            if comic.chapters == True:
                chapters = []
                pages_w_chap = []
                for page in comic.pbp:
                    if hasattr(page,"chapter"):
                        chap = page.chapter
                        chapters.append(chap)
                        li = page.archive_link
                        pages_w_chap.append((li,chap))
                    else:
                        print("No chapters found.")

                chapters = list(set(chapters))

            if comic.chapters == True:
                chapter_sections = []
                for chapi in chapters:
                    chapn = int(chapi)
                    chapter_title = [item for item in comic.chapters_list if item["num"] == chapn]
                    chapter_title = chapter_title[0]["title"]
                    in_this_chapter = []
                    for page in comic.pbp:
                        if hasattr(page,"chapter"):
                            chap = page.chapter
                            if chap == chapi:
                                in_this_chapter.append(page.archive_link)
                    archive_list = generatearchive.generateChapArchList(in_this_chapter,
                                                                        chapi,
                                                                        chapter_title,
                                                                        translated_strings)
                    chapter_sections.append(archive_list)
                chapter_sections_j = sep.join(chapter_sections)
                chapter_archives_r = sep.join(['<section class="archive">',
                                               '<h2>{category}</h2>',
                                               '<p class="status">{status}</p>',
                                               chapter_sections_j,"</section>"])
                chapter_archives = chapter_archives_r.format(category=comic.category,
                                                             status=comic.statuss)
                archives_r.append(chapter_archives)
            else:
                archive_sections = sep.join(archive_d_secs)
                archives_r.append(archive_sections)

        archives = sep.join(archives_r)
        print(archives)
        
    arch_template_name = archive_t
    arch_template = os.path.join(c_path,arch_template_name)

    link_rel_l = ["""<link rel="home" href="index.html" title="{home_s}">""".format(home_s=translated_strings["home_s"]),
                """<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">"""]
    link_rel = sep.join(link_rel_l)

    out_file = os.path.join(o_path,"archive.html")

    archive_header_title = "{site_title} - Archive".format(site_title=site_title)

    with open(arch_template) as f:
        arch_template = f.read()

        arch_string = arch_template.format(
            lang=lang,
            site_style=site_style,
            site_title=site_title,
            header_title=archive_header_title,
            linkrels=link_rel,
            banner=site_banner,
            category=category,
            status=status,
            top_site_nav=top_site_nav,
            archive_sections=archives,
            year=year,
            author=site_author,
            clicense=site_license,
            icons=icons)

        print("Writing %s..." % ("archive.html"))
        with open(out_file,"w+") as fout:
            fout.write(arch_string)
        print("%s written." % ("archive.html"))

    ##Generate feed

    base_url = sitewide_conf["base_url"]

    rssmeta = {
            "author":site_author,
            "email":site_author_email,
            "language":site_lang,
            "link": base_url,
            "desc":site_desc,
            "title":site_title
        }

    rss = genrss.generateFeed(base_url,rssmeta,cpages)

    ## Generate main page

    if single == True:
        template = os.path.join(c_path,index_t)

        out_file = os.path.join(o_path,"index.html")

        print("--First/last:--")
        print("{first_bypage}, {last_bypage}".format(first_bypage=first_bypage,last_bypage=last_bypage))

        with open(template) as f:
            index_template = f.read()

            n_string = index_template.format(
                                             lang=lang,
                                             site_style=site_style,
                                             header_title=site_title,
                                             linkrels=link_rel,
                                             banner=site_banner,
                                             site_title=site_title,
                                             category=category,
                                             top_site_nav=top_site_nav,
                                             latest=last_bypage,
                                             first=first_bypage,
                                             archive="archive.html",
                                             year=year,
                                             author=site_author,
                                             clicense=clicense,
                                             icons=icons)


            print("Writing %s..." % ("index.html"))
            with open(out_file,"w+") as fout:
                fout.write(n_string)
            print("%s written." % ("index.html"))
    else:
    ##    for i in configs:
    ##        for ex in ex_by_date:
    ##            if ex["category"] == i["category"]:
    ##                i["first_bydate"] = ex["first_bydate"]
    ##                i["last_bydate"] = ex["last_bydate"]
    ##        if "first_bydate" not in i.keys() and "last_bydate" not in i.keys():
    ##            print("Error getting the values for %s's first-latest links on the index page." % (i["category"]))
    ##    multi_secs = genmultipleindex.genMultipleIndex(configs,characters_page)
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
                                             site_style=site_style,
                                             header_title=site_title,
                                             linkrels=link_rel,
                                             banner=site_banner,
                                             site_title=site_title,
                                             category=site_title,
                                             top_site_nav=top_site_nav,
                                             multi_secs=secs,
                                             year=year,
                                             author=site_author,
                                             clicense=site_license,
                                             icons=icons)


            print("Writing %s..." % ("index.html"))
            with open(out_file,"w+") as fout:
                fout.write(n_string)
            print("%s written." % ("index.html"))

    ## Generate characters page if necessary.
    if characters_page == True:

        character_pages = []

        for conf in configs:
            
            fn = conf["chars"]
            fp = os.path.join(i_path,fn)
            print("Loading characters file %s..." % (fn))

            try:
                with open(fp,"r",encoding="utf-8") as f:
                    raw_text = f.read()
            except UnboundLocalError:
                print("""An Unbound Local Error has occurred."""\
                      """I'm probably looking for a page that doesn't exist.""")
            except FileNotFoundError:
                print("""The characters page couldn't be built because I couldn't"""\
                      """find the characters file at %s.""" % (fp))
            characters_parsed = genchars.parseChars(raw_text)
            character_elements = genchars.genCharsPage(characters_parsed)

            ##Get character images
            for char in characters_parsed:
                if type(char) == dict:
                    if char["img"] != "None":
                        img_source_path = os.path.join(i_path,char["img"])
                        img_out_path = os.path.join(o_path,char["img"])
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

            chars_title_line = "{category} - {char_s}".format(category=conf["category"],
                                                              char_s=translated_strings["char_s"])

            with open(chars_template_path) as f:
                chars_template = f.read()

                n_string = chars_template.format(
                    lang=lang,
                    site_style=site_style,
                    header_title=site_title,
                    linkrels=link_rel,
                    banner=banner,
                    banner_alt=category,
                    title_line=chars_title_line,
                    top_site_nav=top_site_nav,
                    chars = character_elements,
                    year=year,
                    author=site_author,
                    clicense=site_license,
                    icons=icons)


                print("Writing %s..." % (out_name))
                with open(out_file,"w+") as fout:
                    fout.write(n_string)
                print("%s written." % (out_name))

        if single == False:
            out_name = "characters.html"
            out_file = os.path.join(o_path,out_name)

            chars_title_line = "{site_title} - {char_s}".format(site_title=site_title,
                                                              char_s=translated_strings["char_s"])

            charpage_elements = ['<div class="allchars">']

            for i in character_pages:
                character_page_line = ['<p><a href="',i["charpage"],'">',
                                       i["category"],"</a></p>"]
                character_page_line = "".join(character_page_line)
                charpage_elements.append(character_page_line)
            charpage_elements.append("</div>")
            charpages = sep.join(charpage_elements)

            with open(chars_template_path) as f:
                chars_template = f.read()

                n_string = chars_template.format(
                    lang=lang,
                    site_style=site_style,
                    header_title=site_title,
                    linkrels=link_rel,
                    banner=site_banner,
                    banner_alt=site_title,
                    title_line=chars_title_line,
                    top_site_nav=top_site_nav,
                    chars = charpages,
                    year=year,
                    author=site_author,
                    clicense=site_license,
                    icons=icons)


                print("Writing %s..." % (out_name))
                with open(out_file,"w+") as fout:
                    fout.write(n_string)
                print("%s written." % (out_name))

## Initialize a Springheel project.
def init():
    lang=springheelinit.getLang()
    springheelinit.copyAssets(lang)
        
        






