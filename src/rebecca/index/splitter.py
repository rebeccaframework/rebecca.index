from zope.interface import implementer
from zope.index.text.interfaces import ISplitter
from igo.Tagger import Tagger

@implementer(ISplitter)
class IgoSplitter(object):
    def __init__(self, dictionary):
        self._tagger = Tagger(dictionary)

    def process(self, terms):
        results = []
        for term in terms:
            results.extend(self._tagger.wakati(term))
        return results

    def processGlob(self, terms):
        results = []
        for term in terms:
            results.extend(self._tagger.wakati(term))
        return results

