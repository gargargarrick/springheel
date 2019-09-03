# Springheel Changelog

## 5.0.0 "Azumane"
+ Added proper tagging system.
+ Added option for zero-padding page numbers.
+ Cleared out some unused stuff from archive and navigation generation + the default conf.ini
+ Fixed some issues with image renaming.
+ Fixed error where chaptered works sometimes appeared twice on archive pages.
+ Started naming versions ~~after hot anime dudes~~

## 4.1.0
+ Springheel now generates XML site maps of comic sites.
+ Cleaned up logging a bit.

## 4.0.0
+ Added new themes "revolution", "fairy", "sysadmin", and "might".
+ Separated traits from descriptions on character pages.
+ Fixed major error where a multi-comic site wouldn't generate if some comics had a characters file and some didn't.
+ Fixed bug where slugs were not URL-safe.
+ Fixed bug where the archive page's main heading wasn't getting translated.
+ Fixed bug where extras pages used a comic's title and banner, instead of the sitewide ones.
+ Slight improvements to "seasonal" and "showtime" themes.

## 3.0.3
+ Fixed a very stupid copy+paste error that caused public domain comics to be described as published from a U.R.L. (instead of their respective country).

## 3.0.2
+ Did a better job fixing the character bug from the previous version.
+ Fixed an error where non-transcribed comics wouldn't generate on Windows.
+ Fiddled with the markdown in HOWTO.md because it was displaying strangely in some programs.

## 3.0.1
+ Fixed a bug where archives weren't generating correctly for non-chaptered comics.
+ Fixed a bug where the ordering of character attributes changed randomly every time the page was regenerated.
+ Updated some information in the default conf.ini file.

## 3.0.0
+ Added extras page functionality
+ Added new theme "showtime"
+ Corrected <title> elements for character pages
+ Improved logging

## 2.0.0
+ Condensed template files into one
+ Improved accessibility
+ Updated translations

## 1.0.2
+ Fixed a bug where archives couldn't be generated for multi-comic sites.

## 1.0.1
+ Fixed the parts of the readme that said arrow was a dependency (it isn't).
+ Fixed a bug where .sass-cache was getting installed as if it were a theme.

## 1.0.0

+ Streamlined config files.
+ Tidied up all stylesheets and templates.
+ Added some more translation strings.
+ Refactored a whole lot of code and made it neater.
+ Fixed miscellaneous bugs.
+ Added new themes "rock" and "western".
+ Added better arrows for some themes.