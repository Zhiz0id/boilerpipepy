# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler

from ..document.TextBlock import TextBlock
from ..document.TextDocument import TextDocument
from ..util import UnicodeTokenizer
from DefaultTagActionMap import DefaultTagActionMap
import regex


class BoilerpipeHTMLContentHandler(ContentHandler):
    """
    Main handler for SAX events

    Handles SAX events like start/end tag and data
    """
    START_TAG = 0
    END_TAG = 1
    CHARACTERS = 2
    WHITESPACE = 3

    tagActions = DefaultTagActionMap().tagActions
    title = ''
    ANCHOR_TEXT_START = u"$\ue00a<"
    ANCHOR_TEXT_END = u">\ue00a$"

    tokenBuffer = ''
    textBuffer = ''

    inBody = 0
    inAnchor = 0
    inIgnorableElement = 0

    tagLevel = 0
    blockTagLevel = -1

    sbLastWasWhitespace = False
    textElementIdx = 0

    textBlocks = []

    lastStartTag = None
    lastEndTag = None
    lastEvent = None

    offsetBlocks = 0

    currentContainedTextElements = set()

    flush = False
    inAnchorText = False

    labelStacks = []
    fontSizeStack = []

    def __init__(self):
        pass

    def recycle(self):
        self.tokenBuffer = ''
        self.textBuffer = ''

        self.inBody = 0
        self.inAnchor = 0
        self.inIgnorableElement = 0
        self.sbLastWasWhitespace = False
        self.textElementIdx = 0

        self.textBlocks = []

        self.lastStartTag = None
        self.lastEndTag = None
        self.lastEvent = None

        self.offsetBlocks = 0
        self.currentContainedTextElements = []

        self.flush = False
        self.inAnchorText = False

    def startElementNS(self, name, tag, attrs):
        """
        Handles start element event
        """
        self.labelStacks.append(None)

        tag = tag.upper()
        if tag.upper() in self.tagActions:
            ta = self.tagActions[tag]()
            if ta.changesTagLevel():
                self.tagLevel += 1
            self.flush = ta.start(self, tag, attrs)
        else:
            self.tagLevel += 1
            self.flush = True

        self.lastEvent = self.START_TAG
        self.lastStartTag = tag

    def endElementNS(self, name, tag):
        """
        Handles end element SAX event
        """
        tag = tag.upper()
        ta = False
        if tag in self.tagActions:
            ta = self.tagActions[tag]()
            self.flush = ta.end(self, tag) | self.flush
        else:
            self.flush = True

        if not ta or ta and ta.changesTagLevel():
            self.tagLevel -= 1

        if self.flush:
            self.flushBlock()

        self.lastEvent = self.END_TAG
        self.lastEndTag = tag

        if len(self.labelStacks) > 0:
            self.labelStacks.pop()

    def characters(self, data):
        """
        Handles data event (between tags data)
        """
        length = len(data)
        self.textElementIdx += 1

        if self.flush:
            self.flushBlock()
            self.flush = False

        if self.inIgnorableElement != 0:
            return

        startWhitespace = False
        endWhitespace = False

        if length == 0:
            return

        _idx = 0
        for c in data:
            if c.isspace():
                data = data[:_idx] + ' ' + data[_idx+1:]
            _idx += 1

        for c in data:
            if c == ' ':
                startWhitespace = True
                length -= 1
            else:
                break

        if length > 0:
            for c in data[::-1]:
                if c == " ":
                    endWhitespace = True
                    length -= 1
                else:
                    break

        if length == 0:
            if startWhitespace or endWhitespace:
                if not self.sbLastWasWhitespace:
                    self.textBuffer += " "
                    self.tokenBuffer += " "
                self.sbLastWasWhitespace = True
            else:
                self.sbLastWasWhitespace = False

            self.lastEvent = self.WHITESPACE
            return

        if startWhitespace:
            if not self.sbLastWasWhitespace:
                self.textBuffer += " "
                self.tokenBuffer += " "

        if self.blockTagLevel == -1:
            self.blockTagLevel = self.tagLevel

        self.textBuffer += data #TODO: maybe we need fix it by length
        self.tokenBuffer += data

        if endWhitespace:
            self.textBuffer += " "
            self.tokenBuffer += " "
        self.sbLastWasWhitespace = endWhitespace
        self.lastEvent = self.CHARACTERS

        self.currentContainedTextElements = set(self.textBlocks) #TODO: set idx ?


    def flushBlock(self):
        """
        Creates TextBlock if needed (flush variable)
        """
        if self.inBody == 0:
            if "TITLE" == str.upper(self.lastStartTag) and self.inBody == 0:
                if len(self.tokenBuffer) > 0:
                    self.title = self.tokenBuffer
            self.textBuffer = ''
            self.tokenBuffer = ''
            return

        length = len(self.tokenBuffer)
        if length == 0:
            return
        elif length == 1:
            if self.sbLastWasWhitespace:
                self.textBuffer == ''
                self.tokenBuffer == ''
                return

        tokens = UnicodeTokenizer.UnicodeTokenizer().tokenize(self.tokenBuffer)

        numWords = 0
        numLinkedWords = 0
        numWrappedLines = 0
        currentLineLength = -1
        maxLineLength = 80
        numTokens = 0
        numWordsCurrentLine = 0

        for token in tokens:
            if self.ANCHOR_TEXT_START == token:
                self.inAnchorText = True
            elif self.ANCHOR_TEXT_END == token:
                self.inAnchorText = False
            elif self.isWord(token):
                numTokens += 1
                numWords += 1
                numWordsCurrentLine += 1
                if self.inAnchorText:
                    numLinkedWords += 1

                tokenLength = len(token)
                currentLineLength = tokenLength
                numWordsCurrentLine = 1
            else:
                numTokens += 1

        if numTokens == 0:
            return

        numWordsInWrappedLines = int()
        if numWrappedLines == 0:
            numWordsInWrappedLines = numWords
            numWrappedLines = 1
        else:
            numWordsInWrappedLines = numWords - numWordsCurrentLine

        tb = TextBlock(self.textBuffer.lstrip().rstrip(),
                       self.currentContainedTextElements,
                       numWords,
                       numLinkedWords,
                       numWordsInWrappedLines,
                       numWrappedLines,
                       self.offsetBlocks)

        self.currentContainedTextElements = set()

        self.offsetBlocks += 1

        self.textBuffer = ''
        self.tokenBuffer = ''

        tb.tagLevel = self.blockTagLevel

        self.addTextBlock(tb)
        self.blockTagLevel = -1


    def addTextBlock(self, tb):
        for l in self.fontSizeStack:
            if l:
                tb.label.append("font-" + l)
                break

        for labelStack in self.labelStacks:
            if labelStack:
                for labels in labelStack:
                    if labels:
                        tb.labels = tb.labels.union(labels)

        self.textBlocks.append(tb)




    PAT_VALID_WORD_CHARACTER = regex.compile(ur'[\p{L}\p{Nd}\p{Nl}\p{No}]')

    def isWord(self, token):
        """
        Checks if token is word(by regex)
        """
        return len(self.PAT_VALID_WORD_CHARACTER.findall(token)) > 0


    def toTextDocument(self):
        self.flushBlock()

        return TextDocument(self.title, self.textBlocks)

    def addWhitespaceIfNecessary(self):
        if not self.sbLastWasWhitespace:
            self.tokenBuffer += ' '
            self.textBuffer += ' '
            self.sbLastWasWhitespace = True



