# -*- coding: utf-8; -*-

from testmania.pep8 import assert_equal, assert_raises, assert_raises_regexp, assert_in
from testmania.xml import assert_xml_equal


class TestXmlAssert(object):
    def test_trivial(self):
        xml = "<root></root>"
        assert_xml_equal(xml, xml)

    def test_trivial_inequal(self):
        with assert_raises_regexp(AssertionError, "at / expected <bar> element, got <foo>"):
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

    def test_ignore_whitespace(self):
        xml1 = """
        <root>
            <foo>
                Hello
            </foo>
            <bar>
                <baz>
                    <qux/>
                </baz>
            </bar>
        </root>
        """.strip()

        xml2 = """
        <root>
          <foo>Hello</foo>
          <bar>
            <baz><qux/></baz>
          </bar>
        </root>
        """.strip()

        assert_xml_equal(xml1, xml2)

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

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in("at /root expected <bar> element, got nothing", str(e.exception))

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

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in("at /root expected nothing, got <bar> element", str(e.exception))

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

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in('at /root/foo expected "Privet", got "Hello"', str(e.exception))

    def test_ignore_extra_elements(self):
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

        assert_xml_equal(xml1, xml2, ignore_extra_elements=True)
        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml2, xml1, ignore_extra_elements=True)

    def test_ignore_element_order(self):
        xml1 = """
        <root>
            <foo/>
            <bar/>
        </root>
        """.strip()

        xml2 = """
        <root>
            <bar/>
            <foo/>
        </root>
        """.strip()

        assert_xml_equal(xml1, xml2, ignore_element_order=True)
        assert_xml_equal(xml2, xml1, ignore_element_order=True)

    def test_ignore_list_order(self):
        xml1 = """
        <root>
            <foo>
                <bar/>
            </foo>
            <foo>
                <qux/>
            </foo>
        </root>
        """.strip()

        xml2 = """
        <root>
            <foo>
                <qux/>
            </foo>
            <foo>
                <bar/>
            </foo>
        </root>
        """.strip()

        assert_xml_equal(xml1, xml2, ignore_list_order=True)
        assert_xml_equal(xml2, xml1, ignore_list_order=True)

    def test_attributes_equal(self):
        xml1 = '<root foo="bar" baz="qux" />'
        xml2 = '<root baz="qux" foo="bar" />'
        assert_xml_equal(xml1, xml2)
        assert_xml_equal(xml2, xml1)

    def test_attributes_inequal(self):
        xml1 = '<root foo="bar"/>'
        xml2 = '<root foo="qux"/>'

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in('at /root@foo expected "qux", got "bar"', str(e.exception))

    def test_attr_missed(self):
        xml1 = '<root />'
        xml2 = '<root foo="" />'

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in('at /root@foo expected "", got nothing', str(e.exception))

    def test_extra_attr(self):
        xml1 = '<root foo="bar" />'
        xml2 = '<root />'

        with assert_raises(AssertionError) as e:
            assert_xml_equal(xml1, xml2)

        assert_in('at /root@foo expected nothing, got "bar"', str(e.exception))

    def test_extra_attr_ok(self):
        xml1 = '<root foo="bar" />'
        xml2 = '<root />'

        assert_xml_equal(xml1, xml2, ignore_extra_attrs=True)
