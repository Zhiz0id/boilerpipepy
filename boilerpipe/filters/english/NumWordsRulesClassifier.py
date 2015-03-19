# -*- coding: utf-8 -*-

from ...document.TextBlock import TextBlock
import sys

class NumWordsRulesClassifier:
    def process(self, doc):
        """
        @type param doc: TextDocument
        :return:
        """
        EMPTY_START = TextBlock("", set(), 0, 0, 0, 0, -1)
        EMPTY_END = TextBlock("", set(), 0, 0, 0, 0, sys.maxint)

        textBlocks = doc.textBlocks
        it = iter(doc.textBlocks)
        hasChanges = False

        if len(textBlocks) == 0:
            return False

        prevBlock = EMPTY_START
        currentBlock = it.next()

        nextBlock = next(it, None)
        if nextBlock == None:
            nextBlock = EMPTY_START

        hasChanges = self.classify(prevBlock, currentBlock, nextBlock) or hasChanges

        if nextBlock != EMPTY_START:
            while True:
                prevBlock = currentBlock
                currentBlock = nextBlock
                nextBlock = next(it, None)
                if nextBlock == None:
                    break
                hasChanges = self.classify(prevBlock, currentBlock, nextBlock) or hasChanges

            nextBlock = EMPTY_START
            hasChanges = self.classify(prevBlock, currentBlock, nextBlock) or hasChanges

        return hasChanges


    def classify(self, prevBlock, currBlock, nextBlock):
        isContent = False
        if currBlock.linkDensity <= 0.333333:
            if prevBlock.linkDensity <= 0.555556:
                if currBlock.numWords <= 16:
                    if nextBlock.numWords <= 15:
                        if prevBlock.numWords <= 4:
                            isContent = False
                        else:
                            isContent = True
                    else:
                        isContent = True
                else:
                    isContent = True
            else:
                if currBlock.numWords <= 40:
                    if nextBlock.numWords <= 17:
                        isContent = False
                    else:
                        isContent = True
                else:
                    isContent = True
        else:
            isContent = False
        # print currBlock.text
        # print isContent
        return currBlock.setIsContent(isContent)