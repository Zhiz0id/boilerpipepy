# -*- coding: utf-8 -*-
import regex

class UnicodeTokenizer:
    # \b Matches a word boundary where a word character is [a-zA-Z0-9_].
    PAT_WORD_BOUNDARY = regex.compile(ur'\b')
    #[\u2063] without '*' at end, didn't know if it is ok
    PAT_NOT_WORD_BOUNDARY = regex.compile(ur"[⁣\u2063]([\"'\.,\!\@\-\:\;\$\?\(\)/])[⁣\u2063]")
    IDK = regex.compile(ur"[ \u2063]+")

    def tokenize(self, text):
        text2 = self.PAT_WORD_BOUNDARY.sub(u"\u2063", text)
        text3 = self.PAT_NOT_WORD_BOUNDARY.sub(u"\u2063", text2)
        text4 = self.IDK.sub(" ", text3)

        return text4.strip().split()
