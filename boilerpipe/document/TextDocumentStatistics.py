# -*- coding: utf-8 -*-


class TextDocumentStatistics:
    def __init__(self, doc, contentOnly):
        for tb in doc.textBlocks:
            if contentOnly and not tb.isContent:
                continue

        self.numWords += tb.numWords
        self.numBlocks += 1

    def avgNumWords(self):
        return self.numWords / float(self.numBlocks)
