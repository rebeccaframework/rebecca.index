# -*- coding:utf-8 -*-

from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from persistent import Persistent
from persistent.mapping import PersistentMapping
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.document import DocumentMap
from rebecca.index.splitter import IgoSplitter
from zope.index.text.lexicon import CaseNormalizer
from zope.index.text.lexicon import StopWordRemover
from zope.index.text.lexicon import Lexicon
from repoze.catalog.query import Contains

def add_document(request):
    name = request.params['name']
    text = request.params['text']
    doc = Document(name, text)
    request.context[doc.name] = doc
    doc.__parent__ = request.context
    doc.__name__ = name
    

    root = request.root
    catalog = root.catalog
    document_map = root.document_map
    docid = document_map.new_docid()
    path = request.resource_path(doc)
    document_map.add(path, docid)
    catalog.index_doc(docid, doc)

    return dict(uri=request.resource_url(doc))


def document_view(request):

    return dict(text=request.context.text)

def search(request):
    word = request.params['word']
    root = request.root
    catalog = root.catalog
    document_map = root.document_map
    count, results = catalog.query(Contains('text', word))
    return dict(count=count,
                results=[dict(path=document_map.address_for_docid(docid))
                         for docid in results])


class FtApp(PersistentMapping):
    __parent__ = __name__ = None
    def __init__(self, catalog):
        super(FtApp, self).__init__()
        self.catalog = catalog
        self.document_map = DocumentMap()

class Document(Persistent):
    def __init__(self, name, text):
        self.name = name
        self.text = text

def appmaker(root):
    if 'app_root' not in root:
        import os
        dictionary = os.environ['TESTING_DICT']
        splitter = IgoSplitter(dictionary)
        lexicon = Lexicon(splitter,
                       CaseNormalizer(), StopWordRemover())
        catalog = Catalog(lexicon)
        catalog['text'] = CatalogTextIndex("text", lexicon=lexicon)

        app_root = FtApp(catalog)
        root['app_root'] = app_root
        import transaction
        transaction.commit()
    return root['app_root']

def root_factory(request):
    db = get_connection(request)
    return appmaker(db.root())

def main(global_conf, **settings):
    config = Configurator(settings=settings,
                          root_factory=root_factory)
    config.include('pyramid_zodbconn')
    config.include('pyramid_tm')
    config.add_view(add_document, name="add_document", renderer="json")
    config.add_view(search, name="search", renderer="json")
    config.add_view(document_view, context=Document, renderer="json")
    return config.make_wsgi_app()
