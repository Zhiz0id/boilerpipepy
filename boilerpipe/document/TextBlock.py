# -*- coding: utf-8 -*-


class TextBlock:

    def __init__(self,
                 text,
                 containedTextElements,
                 numWords,
                 numWordsInAnchorText,
                 numWordsInWrappedLines,
                 numWrappedLines,
                 offsetBlocks):
        self.isContent = False
        self.text = text
        self.labels = set()

        self.offsetBlocksStart = offsetBlocks
        self.offsetBlocksEnd = offsetBlocks

        self.numWords = numWords
        self.numWordsInAnchorText = numWordsInAnchorText
        self.numWordsInWrappedLines = numWordsInWrappedLines
        self.numWrappedLines = numWrappedLines

        self.textDensity = int()
        self.linkDensity = int()

        # TODO: check if used at all(looks like it is not)
        #self.containedTextElements = {
        #    'words': [],
        #    'wordsInUse': 0,
        #    'sizeIsSticky': False}
        self.containedTextElements = containedTextElements
        self.numFullTextWords = int()
        self.tagLevel = int()


        self.initDensities()

    def __str__(self):
        return "[" + self.offsetBlocksStart + "-" + self.offsetBlocksEnd + ";tl=" + self.tagLevel + "; nw=" + \
               self.numWords + ";nwl=" + self.numWrappedLines + ";ld=" + self.linkDensity + "]\t" + \
               "CONTENT" if self.isContent else "boilerplate" + "," + str(self.labels) + "\n" + self.text

    def setIsContent(self, isContent):
        if isContent != self.isContent:
            self.isContent = isContent
            return True
        else:
            return False

    def mergeNext(self, other):
        self.text += '\n'
        self.text += other.text

        self.numWords += other.numWords
        self.numWordsInAnchorText += other.numWordsInAnchorText

        self.numWordsInWrappedLines += other.numWordsInWrappedLines
        self.numWrappedLines += other.numWrappedLines

        self.offsetBlocksStart = min(self.offsetBlocksStart, other.offsetBlocksStart)
        self.offsetBlocksEnd = max(self.offsetBlocksStart, other.offsetBlocksStart)

        self.initDensities()

        self.isContent |= other.isContent

        self.numFullTextWords += other.numFullTextWords

        if len(other.labels) > 0:
            if len(self.labels) == 0:
                self.labels = other.labels
            else:
                self.labels = self.labels.union(other.labels)
        self.tagLevel = min(self.tagLevel, other.tagLevel)

    def initDensities(self):
        if self.numWordsInWrappedLines == 0:
            self.numWordsInWrappedLines = self.numWords
            self.numWrappedLines = 1

        self.textDensity = self.numWordsInWrappedLines / float(self.numWrappedLines)
        if self.numWords != 0:
            self.linkDensity = self.numWordsInAnchorText / float(self.numWords)

    def addLabel(self, label):
        self.labels.add(label)

    def addLabels(self, labels):
        if len(labels) == 0:
            return
        self.labels = self.labels.union(labels)

    def hasLabel(self, label):
        return label in self.labels


