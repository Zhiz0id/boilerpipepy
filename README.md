# BoilerpipePy
## Boilerplate Removal and Fulltext Extraction from HTML pages

## Summary
The boilerpipe library provides algorithms to detect and remove the surplus "clutter" (boilerplate, templates) around
the main textual content of a web page.

This project is native python port of [Boilerpipe](https://code.google.com/p/boilerpipe/) Java library by Christian Kohlschütter


## Algorithm
The algorithms used by the library are based on (and extending) some concepts of the paper
"[Boilerplate Detection using Shallow Text Features](http://www.l3s.de/~kohlschuetter/boilerplate/)" by Christian
Kohlschütter et al.


## Components

  * an HTML parser that transforms HTML into an internal text-only document model supporting "blocks" of text.
    * Python version uses fast [lxml](http://lxml.de/) parsers
  * several Filter components analyze and tag these text blocks
  * extractors consisting of one or more Filters. Such "pipelines" take the parsed document object and distill the main textual content from it
    * one extractor in python version atm
  * an HTML highlighter to visually inspect the extracted main content within a copy of the input page.
    * not supported atm

## How to use
  * Simple run ./url2article.py with url as a parameter
    * It will save article-name.txt with extracted text data
  * Tested with cnn.com, gazeta.ru , lenta.ru, roem.ru
    * Parsed examples in doc directory
  * on windows you can view files with browser(utf8 turned on) or nice text editor, Notepad is ugly

## You can test this library online
  * [http://boilerpipepy-youra.rhcloud.com/](http://boilerpipepy-youra.rhcloud.com/)

## TODO
  * Unit tests
  * More filters
  * More extractors
  * Different data extraction support:
    * images
    * video
    * links

## Version
  * 0.001 - 23.03.2014