#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Comic Archive Page Generation
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

import springheel.parseconf, os

def getLinks(i,translated_strings):
    ## Oh no u don't
    #link_format = """<li><a href="{html_filename}">#{page}: {title} ({date})</a></li>"""
    archive_l = translated_strings["archive_l_s"].format(title=i.title,page=i.page)
    link_format = "<li><a href='{html_filename}'>{archive_l}</a></li>"
    archive_link = link_format.format(html_filename=i.html_filename,
                                      archive_l=archive_l)
    return(archive_link)

def generateArchives(archive,translated_strings):
    sep = "\n"
    link_list = sep.join(archive)
    archive_by_date_s = translated_strings["archive_by_date_s"]
    sect = """<section class="archive">
<h2>{archive_by_date_s}</h2>
<p class="status">{status}</p>
<ol class="datearch">
{link_list}
</ol>
</section>"""

    arch_section = sect.format(link_list=link_list,
                               status=status,
                               archive_by_date_s=archive_by_date_s)
    return(arch_section)

def generateChapArchList(archive,chapter,chapter_title,translated_strings,l):
    sep = "\n"
    link_list = sep.join(archive)

    chapter_s = translated_strings["chapter_s"].format(chapter=chapter,chapter_title=chapter_title)
    
    sect = """<h{l}>{chapter_s}</h{l}>
<ol class="chapterarch">
{link_list}
</ol>"""

    arch_list = sect.format(chapter_s=chapter_s,
                            link_list=link_list,
                            l=l)
    return(arch_list)

def generateSeriesArchives(category,status,archive):
    sep = "\n"
    link_list = sep.join(archive)
    sect = """<section class="archive">
<h2>{category}</h2>
<p class="status">{status}</p>
<ol class="datearch">
{link_list}
</ol>
</section>"""

    arch_section = sect.format(category=category,
                               status=status,
                               link_list=link_list)
    return(arch_section)

def generateArchPage(c_path,comics,archive,site_style):

    if single:
        template_name = "archive-template.html"
    else:
        template_name = "archive-template.multiple.html"
    template = os.path.join(c_path,template_name)

    with open(template) as f:
        archive_template = f.read()

        n_string = archive_template.format(lang=comics["lang"],
                                           site_style=site_style,
                                           header_title=header_title,
                                           linkrels=linkrels,
                                           banner=banner,
                                           category=category,
                                           status=status,
                                           archive_sections=archive_sections,
                                           year=year,
                                           author=author,
                                           clicense=clisense,
                                           icons=icons)
    return(n_string)

