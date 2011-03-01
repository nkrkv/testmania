# -*- coding: utf-8; -*-

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from nose.tools import assert_equal
from testmania.xml import assert_xml_equal


class TestXmlAssert(TestCase):
    def test_trivial(self):
        xml = "<root></root>"
        assert_xml_equal(xml, xml)

    def test_trivial_inequal(self):
        with self.assertRaisesRegexp(AssertionError, "at / expected <bar> element, got <foo>"):
            assert_xml_equal("<foo></foo>", "<bar></bar>")

    def test_nested(self):
        xml = """
        <root>
            <nested-one>
                <double-nested-one/>
            </nested-one>
            <nested-two/>
        </root>
        """.strip()
        assert_xml_equal(xml, xml)

    def test_extra_element(self):
        xml1 = """
        <root>
            <foo/>
        </root>
        """.strip()

        xml2 = """
        <root>
            <foo/>
            <bar/>
        </root>
        """.strip()

        with self.assertRaises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        self.assertIn("at /root expected <bar> element, got nothing", str(e.exception))

    def test_lack_of_element(self):
        xml1 = """
        <root>
            <foo/>
            <bar/>
        </root>
        """.strip()

        xml2 = """
        <root>
            <foo/>
        </root>
        """.strip()

        with self.assertRaises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        self.assertIn("at /root expected nothing, got <bar> element", str(e.exception))

    def test_text(self):
        xml1 = """
        <root>
            <foo>
                Hello
            </foo>
        </root>
        """.strip()

        xml2 = """
        <root>
            <foo>Hello</foo>
        </root>
        """.strip()

        assert_xml_equal(xml1, xml2)

    def test_text_inequal(self):
        xml1 = """
        <root>
            <foo>Hello</foo>
        </root>
        """.strip()

        xml2 = """
        <root>
            <foo>Privet</foo>
        </root>
        """.strip()

        with self.assertRaises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        self.assertIn("at /root/foo expected u'Privet', got u'Hello'", str(e.exception))
