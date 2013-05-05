# -*- coding:utf-8 -*-

import pytest

jugem = u"""寿限無、寿限無
五劫の擦り切れ
海砂利水魚の
水行末 雲来末 風来末
食う寝る処に住む処
藪ら柑子の藪柑子
パイポパイポ パイポのシューリンガン
シューリンガンのグーリンダイ
グーリンダイのポンポコピーのポンポコナーの
長久命の長助"""

dakar = u"""議会の方には突然の無礼を許して頂きたい！！
私はエゥーゴのクワトロ＝バジーナ大尉であります。
話の前にもう一つ知っておいてもらいたい事があります。
私はかつてシャア＝アズナブルという名で呼ばれた事がある男だっ！

私は、この場を借りてジオンの遺志を継ぐ者として語りたい！
もちろんジオン公国のシャアとしてではなく．．．、
ジオン＝ズム＝ダイクンの子としてである！
ジオン＝ズム＝ダイクンの遺志は
ザビ家のように欲望に根差したものではない！！
ジオン＝ズム＝ダイクンがジオン公国を創ったのではない！

現在ティターンズが地球連邦軍を我がものにしている事実は、
ザビ家のやり方より悪質であると気付く！！
人が宇宙（そら）にでたのは、地球が人間の重みで沈むのを避ける為だった。
そして宇宙にでた人類は、
その生活圏を拡大した事により人類そのものの力を身に付けたと誤解し、
ザビ家のような勢力をのさばらせてしまった歴史をもつ！！
それは不幸だっ！！

もう、その歴史を繰り返してはならない！！
宇宙にでる事によって、人間はその能力を広げることができると、
なぜ信じられないのか！！
我々は地球を人の手で汚すなと言っている！！
ティターンズは重力に魂を引かれた人々の集まりで
地球を食い潰そうとしているのだ！！

人は長い間、地球というゆりかごの中で戯れてきた。
しかし時は既に人類を地球から巣立たせる時が来たのだ！！
その後に至って、なぜ人類同士が戦い地球を汚染しなければならないのだ！？
地球を自然のゆりかごに戻し、人間は宇宙で自立しなければ、
地球は水の惑星ではなくなるのだ！！
このダカールでさえ、砂漠に飲み込まれようとしている。
それ程、地球は疲れきっている。

今、誰もがこの美しい地球を残したいと考えている！
ならば、自分の欲求を果たす為だけに
地球の寄生虫のようにへばりついて良い訳がない！！
見るがいい！！この暴虐な行為を！！
彼等はかつての地球連邦軍から膨れあがり
逆らう者全てを悪と称しているが．．．、
それこそ悪であり、人類全体を衰退させていると
言い切れる！
私の話はここで終えるが、人類は終わる事なく
歩み続けねばならぬのだ！！
"""

class TestIt(object):
    @pytest.fixture
    def target(self):
        import os
        from rebecca.index.splitter import IgoSplitter
        dictionary = os.environ['TESTING_DICT']
        return IgoSplitter(dictionary)

    def test_it(self, target):
        result = target.process([jugem])
        for m in result:
            print m
        assert result == [
        u"寿",
        u"限",
        u"無",
        u"、",
        u"寿",
        u"限",
        u"無",
        u"五",
        u"劫",
        u"の",
        u"擦り切れ",
        u"海",
        u"砂利",
        u"水魚",
        u"の",
        u"水",
        u"行末",
        u"雲来",
        u"末",
        u"風",
        u"来",
        u"末",
        u"食う",
        u"寝る",
        u"処",
        u"に",
        u"住む",
        u"処",
        u"藪",
        u"ら",
        u"柑子",
        u"の",
        u"藪",
        u"柑子",
        u"パイポパイポ",
        u"パイ",
        u"ポ",
        u"の",
        u"シューリンガン",
        u"シューリンガン",
        u"の",
        u"グーリンダイ",
        u"グーリンダイ",
        u"の",
        u"ポンポコピー",
        u"の",
        u"ポンポコナー",
        u"の",
        u"長久",
        u"命",
        u"の",
        u"長助",
        ]


class TestCatalog(object):
    @pytest.fixture
    def lexicon(self):
        import os
        from rebecca.index.splitter import IgoSplitter
        from zope.index.text.lexicon import CaseNormalizer
        from zope.index.text.lexicon import StopWordRemover
        dictionary = os.environ['TESTING_DICT']
        splitter = IgoSplitter(dictionary)
        from zope.index.text.lexicon import Lexicon
        return Lexicon(splitter,
                       CaseNormalizer(), StopWordRemover())

    @pytest.fixture
    def catalog(self, lexicon):
        from repoze.catalog.indexes.text import CatalogTextIndex
        from repoze.catalog.catalog import Catalog
        def get_text(object, default):
            return getattr(object, "text", default)

        catalog = Catalog()
        catalog['text'] = CatalogTextIndex(get_text, lexicon=lexicon)
        return catalog

    def test_it(self, catalog):
        from repoze.catalog.query import Contains
        class DummyContent(object):
            def __init__(self, text):
                self.text = text

        content = DummyContent(dakar)
        catalog.index_doc(1, content)
        results = catalog.query(Contains('text', u'シャア'))
        assert results[0] == 1
        for f in results[1]:
            print f
        assert False
