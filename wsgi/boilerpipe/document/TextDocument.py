# -*- coding: utf-8 -*-


class TextDocument:
    def __init__(self, title="", textBlocks=[]):
        self.textBlocks = textBlocks
        self.title = title

    def __str__(self):
        """
        :return: debug information
        """
        sb = ""
        for block in self.textBlocks:
            sb += unicode(block)
            sb += '\n'
        return sb

    def getContent(self):
        return self.getText(True, False)

    def getText(self, includeContent, includeNonContent):
        """
        :param includeContent: bool
        :param includeNonContent: bool
        :return: text in all blocks
        """
        sb = ""
        for block in self.textBlocks:
            if block.isContent:
                if not includeContent:
                    continue
            else:
                if not includeNonContent:
                    continue
            sb += block.text
            sb += '\n'
        return sb