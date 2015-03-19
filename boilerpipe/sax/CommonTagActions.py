# -*- coding: utf-8 -*-

import regex
from .TagAction import TagAction
import BoilerpipeHTMLContentHandler

class TA_IGNORABLE_ELEMENT(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.inIgnorableElement += 1
        return True

    def end(self, instance, tag):
        instance.inIgnorableElement -= 1
        return True

    def changesTagLevel(self):
        return True


class TA_ANCHOR_TEXT(TagAction):
        def start(self, instance, tag, attrs):
            """

            :param instance: BoilerpipeHTMLContentHandler
            :param tag:
            :return:
            """
            if instance.inAnchor > 0:
                instance.inAnchor += 1
                print "Warning input contains nested A elements, looks like bug in parser"
                self.end(instance, tag)
            else:
                instance.inAnchor += 1
            if instance.inIgnorableElement == 0:
                instance.addWhitespaceIfNecessary()
                instance.tokenBuffer += BoilerpipeHTMLContentHandler.BoilerpipeHTMLContentHandler().ANCHOR_TEXT_START
                instance.tokenBuffer += ' '
                instance.sbLastWasWhitespace = True
            return False

        def end(self, instance, tag):
            instance.inAnchor -= 1
            if instance.inAnchor == 0:
                if instance.inIgnorableElement == 0:
                    instance.addWhitespaceIfNecessary()
                    instance.tokenBuffer += BoilerpipeHTMLContentHandler.BoilerpipeHTMLContentHandler().ANCHOR_TEXT_END
                    instance.tokenBuffer += ' '
                    instance.sbLastWasWhitespace = True
            return False

        def changesTagLevel(self):
            return True


class TA_BODY(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.flushBlock()
        instance.inBody += 1
        return False

    def end(self, instance, tag):
        instance.flushBlock()
        instance.inBody -= 1
        return False

    def changesTagLevel(self):
        return True


class TA_BODY(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.flushBlock()
        instance.inBody += 1
        return False

    def end(self, instance, tag):
        instance.flushBlock()
        instance.inBody -= 1
        return False

    def changesTagLevel(self):
        return True


class TA_INLINE_WHITESPACE(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.addWhitespaceIfNecessary()
        return False

    def end(self, instance, tag):
        instance.addWhitespaceIfNecessary()
        return False

    def changesTagLevel(self):
        return False


class TA_INLINE(TA_INLINE_WHITESPACE):
    pass

class TA_INLINE_NO_WHITESPACE(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """

        return False

    def end(self, instance, tag):
        return False

    def changesTagLevel(self):
        return False


class TA_BLOCK_LEVEL(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        return True

    def end(self, instance, tag):
        return True

    def changesTagLevel(self):
        return True


class TA_FONT(TagAction):
    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        PAT_FONT_SIZE = regex.compile("([\+\-]?)([0-9])")
        sizeAttr = attrs.get((None, "size"))
        if sizeAttr:
            m = PAT_FONT_SIZE.findall(sizeAttr)
            if len(m) > 0:
                rel = m[0][0]
                val = int(m[0][1])
                size = int()
                if len(rel) == 0:
                    size = val
                else:
                    prevSize = int()
                    if len(instance.fontSizeStack) == 0:
                        prevSize = 3
                    else:
                        prevSize = 3
                        for s in instance.fontSizeStack:
                            if s:
                                prevSize = s
                                break
                    if rel == '+':
                        size = prevSize + val
                    else:
                        size = prevSize - val
                instance.fontSizeStack.insert(0, size)
            else:
                instance.fontSizeStack.insert(0, None)
        else:
            instance.fontSizeStack.insert(0, None)
        return False

    def end(self, instance, tag):
        instance.fontSizeStack.remove(0)
        return False

    def changesTagLevel(self):
        return False


class InlineTagLabelAction(TagAction):
    def __init__(self, action):
        self.action = action

    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.addWhitespaceIfNecessary()
        instance.labelStacks.append(self.action)
        return False

    def end(self, instance, tag):
        instance.addWhitespaceIfNecessary()
        return False

    def changesTagLevel(self):
        return False


class BlockTagLabelAction(TagAction):
    def __init__(self, action):
        self.action = action

    def start(self, instance, tag, attrs):
        """

        :param instance: BoilerpipeHTMLContentHandler
        :param tag:
        :return:
        """
        instance.addLabelAction(self.action)
        return True

    def end(self, instance, tag):
        return True

    def changesTagLevel(self):
        return True


