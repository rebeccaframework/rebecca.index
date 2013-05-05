# -*- coding: utf-8 -*-

import pytest

settings = {
    "zodbconn.uri": "memory://",
}


def test_ft():
    import webtest
    import ftapp
    app = ftapp.main({}, **settings)
    app = webtest.TestApp(app)
    res = app.post('/add_document',
                   params=[('name', 'testing'),
                           ('text', 'もももすももももものうち')])
    assert res.json['uri'] == 'http://localhost/testing/'

    res = app.get(res.json['uri'])
    assert res.json == {'text': u'もももすももももものうち'}

    res = app.get('/search',
                  params=[('word', 'もも')])
    assert res.json == {u'count': 1, u'results': [{u'path': u'/testing/'}]}
