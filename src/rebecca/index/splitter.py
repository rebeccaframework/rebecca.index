from zope.interface import implementer
from zope.index.text.interfaces import ISplitter
from persistent import Persistent
from igo.Tagger import Tagger

@implementer(ISplitter)
class IgoSplitter(Persistent):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    @property
    def tagger(self):
        if not hasattr(self, '_v_tagger'):
            self._v_tagger = Tagger(self.dictionary)
        return self._v_tagger

    def process(self, terms):
        results = []
        for term in terms:
            results.extend(self.tagger.wakati(term))
        return results

    def processGlob(self, terms):
        results = []
        for term in terms:
            results.extend(self.tagger.wakati(term))
        return results

