# Springheel
A static site generator for webcomics (in alpha)

![](springheel-logo.svg)

![](jackie.svg)

Springheel is a static site generator for webcomics.

Whether it's static site generators or Wordpress plugins, most existing software is geared towards blogs, not comics. Adapting them to work with comics is kludgey and fragile, and unecessarily exposes you to security problems. But why force a square peg into a round hole when round pegs are easy enough to make? With that in mind I created Springheel. (The name comes from Spring-heel Jack, for the "English monster" naming scheme that many static generators keep to.)

Springheel is built with Python 3.5, [Feedgenerator](https://github.com/lkiesow/python-feedgen), and [arrow](https://github.com/crsmithdev/arrow/).

Keep in mind that I'm self-taught \([obligatory xkcd](http://www.xkcd.com/1513/)\) and maybe don't look too closely at the actual code.

## Features

* Easy to use. Updating is a matter of putting a couple of files in a folder and running a single Python script.
* Lots of customization. Use your site as a hub for multiple comics or just one; select one of many (mobile-accessible!) default themes or roll your own; fiddle with almost any aspect of the finished site you can think of. Not to mention that the generated HTML is clean and easy to modify. It's all up to you!
* Small and secure. Keep hosting costs down, and never worry about updating Wordpress again (and again and again...) because of yet another gaping security flaw.
* Accessible. Generated sites are marked up with WAI-ARIA landmarks, include alt text and skip links, and make it easy to drop in textual transcripts. The default themes are large and easy to read, and their color schemes comply with WCAG AAA. Even link rel navigation is generated by default.
* Everything a comic (not a blog) needs. Make a characters page is so quick, you'll never have an out-of-date one again! Sections for creator commentaries, extra galleries, and guest comics are included by default too. Archives can be divided by chapter (if you have them) and/or date.
* Freely licensed -- Springheel is GPLv3+ software that anyone can fork and contribute to. (Releasing Springheeled comics under a Free Culture license is encouraged but not required.)
* Cute mascot!

## Installing

Springheel requires at least **Python 3.**

If you want to build from the git source, you'll need the following dependencies:

* [Feedgenerator](https://github.com/lkiesow/python-feedgen)
* [arrow](https://github.com/crsmithdev/arrow/)
* [awesome-slugify](https://github.com/dimka665/awesome-slugify)

Then navigate to the springheel directory, and run `setup.py install` (you may need to run this with `su -c` depending on the type of Python install you have).

**Important**: If you're on Windows and get an error about Visual C++ while installing dependencies (lxml especially), do not panic! Just use PyPi to install that specific library directly, then try to install springheel again.
