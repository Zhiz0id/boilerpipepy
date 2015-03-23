#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Yura Beznos'


import web
from boilerpipe.sax.BoilerpipeHTMLContentHandler import BoilerpipeHTMLContentHandler
import urllib2
from boilerpipe.extractors.ArticleExtractor import ArticleExtractor
from StringIO import StringIO
from lxml import etree, sax
import sys
import codecs
import os
from textwrap import TextWrapper

urls = (
    '/', 'index',
)

# Redirect to index
class index:
    def GET(self):
        print locals()
        print globals()
        web.header('Content-Type', 'text/html')
        path = u''
        article = u''
        if 'path' in web.input():
            path = web.input()['path']
            ugly = False
            if os.sys.platform[0:3] == 'win':
                ugly = True

            response = urllib2.urlopen(path)
            encoding = response.headers.getparam('charset')
            html = response.read().decode(encoding)

            f = StringIO(html)
            parser = etree.HTMLParser()

            #create SAX tree
            tree = etree.parse(f, parser)

            handler = BoilerpipeHTMLContentHandler()
            handler.recycle()
            sax.saxify(tree, handler)

            a = ArticleExtractor()


            #parses our data and creates TextDocument with TextBlocks
            doc = handler.toTextDocument()

            tw = TextWrapper()
            tw.width = 80
            tw.initial_indent = os.linesep + os.linesep
            parsed_url = urllib2.urlparse.urlparse(path)
            filename = parsed_url.netloc + "-" + "".join(
                [c for c in parsed_url.path if c.isalpha() or c.isdigit() or c == ' ']
            ).rstrip() + '.txt'
            output = []
            for line in a.getText(doc).splitlines():
                output.append(tw.fill(line))
            i = 0
            article = ''
            for line in output:
                if ugly:
                    line.replace('\n', os.linesep)
                article += line



        print article
        index = u"""<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>
            BoilerpipePy example aith ArticleExtractor(simple filter)
        </title>
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/united/bootstrap.min.css">
    </head>
    <body>
        <div class="row">
            <div class="col-md-5 col-md-offset-3 col-sd-12">
                <form action="/" class="text-center">
                  <fieldset>
                    <legend>BoilerpipePy example</legend>
                    <legend>(you get main article from URL without no needed ads/menu/trash)</legend>
                    <input type="text" name="path" class="form-control" placeholder="Enter full URL like http://domain.domain/path/…">
                    <button type="submit" class="btn">Submit</button>
                  </fieldset>
                  </form>
                  <pre class="text-left">
                  %(path)s

                %(article)s
                </pre>
                <address>
                  <strong>BoilerpipePy</strong><br>
                  This site is show room of BoilerpipePy library:
                  <a href="https://github.com/Zhiz0id/boilerpipepy">github.com -> boilerpipepy</a>
                </address>

                <address>
                  <strong>Author</strong><br>
                  Yura Beznos
                </address>
            </div>
        </div>
    </body>
</html>        
        """ % locals()
        return index


app = web.application(urls, globals())
application = app.wsgifunc()
# if __name__ == "__main__":
#    app = web.application(urls, globals())
#    app.run()
