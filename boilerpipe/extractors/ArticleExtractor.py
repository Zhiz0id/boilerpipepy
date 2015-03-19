# -*- coding: utf-8 -*-

from ..filters.english.NumWordsRulesClassifier import NumWordsRulesClassifier

class ArticleExtractor:
    def process(self, doc):
        return NumWordsRulesClassifier().process(doc)

    def getText(self, doc):
        self.process(doc)
        return doc.getContent()