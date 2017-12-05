#!/usr/bin/python3
# -*- coding: utf-8 -*-
########
##  Springheel - Sitewide Configuration
########
##  This file is released into the public domain.

[BasicPrefs]

## The base domain of your site. This is used for generating RSS feeds and
## other items that need a full URL.
## This MUST end with a slash.

base_url = http://sample-springheel-comic.notarealtld/

## The person or people who authored this site.
## This is used for copyright statements and RSS feeds.
site_author = Springheel D. Jack

## Your email address.  This is used for generating RSS feeds.
site_author_email = notarealemail@notarealsite.notarealtld

## The site language. ISO-formatted 2-letter code.
## If you want to e.g. have comics in multiple languages, I'd recommend just
## generating multiple sites and putting them
## in different directories: root/eng, root/deu, and so forth.
language = en

## A short description of your site.
description = My awesome Springheel comic!

## The overall title of your site.
## If site_type is single, this'll probably be the name of the comic.
site_title = Springheel Comics

## The country from which you are publishing, or are under the legal jurisdiction of.
## This is mostly relevant if you have waived copyright to your work.
country = United States

[SiteLayout]
## What type of site will this be? Choices are:
## "single" - one series only. Most comics fall under this category so it
## is the default.
## "multi" - multiple series. Site is a kind of hub for various works. Some
## examples would be the works of David Willis or MS Paint Adventures.
## If "multi", the site menu will have an "other comics" link.
site_type = multi

## Is the comic divided into chapters?
chapters = False

## Generate cast pages?
## If True, set a .chars file in your series .conf files, and a Characters
## page will be generated based on that.
## (Only series with valid .chars files will get Characters pages, so don't
## worry about setting them if e.g. you have one series that doesn't have
## recurring characters; you can just leave the .chars file off and nothing
## will go wrong.)
## If site_type is multi and this is True, characters.html will go to a page
## that links to the other characters pages. If it is single, characters.html
## will be the characters page itself.
characters_page = True

## If you have a merchandise storefront on another site, you can include
## the URL here and it will appear in the site navigation.
## If you don't have a shop or don't want it to appear there, just leave
## this as False.
store_page = False

## Setting this to True will create an Extras page, which you can use for
## extra art, wallpapers, guest comics, and so forth.
## I mean, eventually. It does nothing for now.
extras_page = False

## What license is the comic available under?
## Some choices might be "Released into the public domain", the HTML snippet
## from the Creative Commons license chooser, or "all rights reserved".
license = All rights reserved.

## The metaphorical direction used for navigation arrows.
## In languages that read left-to-right, like English, "back" arrows point
## to the left and "forward" arrows point to the right.
## Obviously, this must be reversed for languages that read right-to-left,
## such as Hebrew or Japanese.
## The default direction is "ltr"; set to "rtl" for right-to-left
## directionality.
navdirection = ltr


[SiteStyles]

## Should image files be renamed?
## This works on the output files only; the originals stay as they are.
## This should probably be true, because most people really don't choose
## useful filenames. Dates (without any other info), vague titles, and random
## gibberish seem to be most common.
## I implemented this feature because I've personally spent WAY too much
## time sifting through poorly-designed webcomic sites, desperately trying to
## find the original URL of a given strip.
## Ideally, the filename should give users all the information they need to
## work out where a comic came from.
rename_images = True

## Image renaming pattern.
## This isn't really implemented yet.
## For chaptered works, you might want to add {chapter}} and {page} to
## insert those respective numbers.
## Also available are {titleslug} (slugified strip title), {author}, {height},
## and {width}.
image_rename_pattern = {comic}_{page}_{titleslug}_{date}.{ext}

## Page/strip filename format. To make sure that the page-scan doesn't pick up
## other images, the pattern you use for pages or strip files is listed here.
## By default, all files beginning with "page" are considered pages. The
## scanner checks if the first 4 characters are "page".
page_name_trigger = page

## Site style.
## Defaults are: "plain", "dark", "beach", "book", "brandy", "cherry", "city",
## "cute", "cyber", "fantasy", "garden", "gothic", "haunted", "magiccircle",
## "note", "prayers", "starship", "steam", "twothousand", "seasonal"
site_style = plain

## The filename for the site header banner (the image that appears at the) top
## of non-comic pages, like the archive).
banner_filename = Please_Set_a_Site_Header_in_conf.py.png

[SocialMedia]

## All social media icons are optional. If you don't want to include a given
## link, just set the value to False and it won't appear.
## Set "social_icons" to False to disable all social media icons.
social_icons = False

## Twitter handle. Applied in the form of http://twitter.com/MyAwesomeSpringheeledComic
twitter_handle = MyAwesomeSpringheeledComic

## Tumblr blog. Applied in the form of http://my-awesome-springheeled-comic.tumblr.com
tumblr_handle = my-awesome-springheeled-comic

## Patreon handle. Applied in the form of https://www.patreon.com/awesomespringheeledcomic
patreon_handle = awesomespringheeledcomic

## Liberapay handle. Applied in the form of https://liberapay.com/awesomespringheeledcomic
liberapay_handle=awesomespringheeledcomic

## Pump microblog. This requires a full URL.
pump_url = https://identi.ca/awesomespringheeledauthor

##Diaspora* stream. This requires a full URL.
diaspora_url = https://joindiaspora.com/people/awesomespringheeledauthor




