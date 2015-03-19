#!/usr/bin/env python
# -*- coding: utf-8 -*-

from boilerpipe.sax.BoilerpipeHTMLContentHandler import BoilerpipeHTMLContentHandler
import urllib2
from boilerpipe.extractors.ArticleExtractor import ArticleExtractor
from StringIO import StringIO
from lxml import etree, sax
import sys
import codecs
from textwrap import TextWrapper

def main():
    response = urllib2.urlopen(sys.argv[1])
    encoding = response.headers.getparam('charset')
    html = response.read().decode(encoding)

    f = StringIO(html)
    parser = etree.HTMLParser()

    #create SAX tree
    tree = etree.parse(f, parser)

    handler = BoilerpipeHTMLContentHandler()
    sax.saxify(tree, handler)

    a = ArticleExtractor()

    #parses our data and creates TextDocument with TextBlocks
    doc = handler.toTextDocument()

    tw = TextWrapper()
    tw.width = 80
    tw.initial_indent = '\n\n'
    parsed_url = urllib2.urlparse.urlparse(sys.argv[1])
    filename = parsed_url.netloc + "-" + "".join(
        [c for c in parsed_url.path if c.isalpha() or c.isdigit() or c == ' ']
        ).rstrip() + '.txt'
    output = []
    for line in a.getText(doc).splitlines():
        output.append(tw.fill(line))

    with codecs.open(filename, 'w', encoding='utf8') as f:
        for line in output:
            f.write(line)
    print "Article saved. Lines: %s. Filename: %s" % (len(output), filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        print "Please run with url as a parameter"
