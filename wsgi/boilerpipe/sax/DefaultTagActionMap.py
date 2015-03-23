# -*- coding: utf-8 -*-

from .CommonTagActions import *


class DefaultTagActionMap:
    def __init__(self):
        self.tagActions = {
            "STYLE": TA_IGNORABLE_ELEMENT,
            "SCRIPT": TA_IGNORABLE_ELEMENT,
            "OPTION": TA_IGNORABLE_ELEMENT,
            "OBJECT": TA_IGNORABLE_ELEMENT,
            "EMBED": TA_IGNORABLE_ELEMENT,
            "APPLET": TA_IGNORABLE_ELEMENT,
            "LINK": TA_IGNORABLE_ELEMENT,

            "A": TA_ANCHOR_TEXT,
            "BODY": TA_BODY,

            "STRIKE": TA_INLINE_NO_WHITESPACE,
            "U": TA_INLINE_NO_WHITESPACE,
            "B": TA_INLINE_NO_WHITESPACE,
            "I": TA_INLINE_NO_WHITESPACE,
            "EM": TA_INLINE_NO_WHITESPACE,
            "STRONG": TA_INLINE_NO_WHITESPACE,
            "SPAN": TA_INLINE_NO_WHITESPACE,

            "SUP": TA_INLINE_NO_WHITESPACE,

            "CODE": TA_INLINE_NO_WHITESPACE,
            "TT": TA_INLINE_NO_WHITESPACE,
            "SUB": TA_INLINE_NO_WHITESPACE,
            "VAR": TA_INLINE_NO_WHITESPACE,

            "ABBR": TA_INLINE_WHITESPACE,
            "ACRONYM": TA_INLINE_WHITESPACE,
            "FONT": TA_INLINE_NO_WHITESPACE,

            "NOSCRIPT": TA_IGNORABLE_ELEMENT
        }