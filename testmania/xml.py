# -*- coding: utf-8; -*-

from __future__ import absolute_import

from itertools import izip_longest

import xml.dom.minidom


def assert_xml_equal(actual, expected, msg=None, 
                     ignore_whitespace=True, 
                     ignore_extra_elements=False,
                     ignore_element_order=False):

    actual = xml.dom.minidom.parseString(actual)
    expected = xml.dom.minidom.parseString(expected)

    if ignore_whitespace:
        _strip_whitespace(actual)
        _strip_whitespace(expected)

    settings = Settings()
    settings.ignore_extra_elements = ignore_extra_elements
    settings.ignore_element_order = ignore_element_order
    twiroot = Twinode(actual.documentElement, expected.documentElement, settings)

    try:
        twiroot.assert_equal()
    except AssertionError, e:
        if not msg:
            msg = "\nExpected:\n%s\n\nActual:\n%s\n%s" % \
                    (expected.toprettyxml(), actual.toprettyxml(), e)
        raise AssertionError(msg)


def _strip_whitespace(node):
    for n in node.childNodes:
        if n.nodeType == xml.dom.Node.TEXT_NODE and not n.data.strip():
            node.removeChild(n)
            n.unlink()
        elif n.nodeType == xml.dom.Node.ELEMENT_NODE:
            _strip_whitespace(n)


class Settings(object):
    pass


class Twinode(object):
    def __init__(self, actual, expected, settings, parent=None):
        self.actual = actual
        self.expected = expected
        self.settings = settings
        self.parent = parent

    def assert_equal(self):
        if self.actual is None or self.expected is None:
            self._raise()

        if self.actual.nodeType != self.expected.nodeType:
            self._raise()

        node_type = self.actual.nodeType
        if node_type == xml.dom.Node.TEXT_NODE:
            self.assert_equal_text()
        elif node_type == xml.dom.Node.ELEMENT_NODE:
            self.assert_equal_elements()
        else:
            raise NotImplementedError("Comparison of %s nodes is not implemented" % node_type)

        self.arrange_children()
        for twinode in self.children:
            twinode.assert_equal()

    def assert_equal_text(self):
        actual_str = self.actual.data.strip()
        expected_str = self.expected.data.strip()
        if actual_str != expected_str:
            self._raise()

    def assert_equal_elements(self):
        if self.actual.tagName != self.expected.tagName:
            self._raise()

    def _raise(self):
        msg = "at %s expected %s, got %s" % \
                (self.path(), self.format_node(self.expected), self.format_node(self.actual))
        raise AssertionError(msg)

    def path(self, root_symbol='/'):
        if not self.parent:
            return root_symbol
        return '%s/%s' % (self.parent.path(root_symbol=''), 
                          (self.actual or self.expected).parentNode.tagName)

    def format_node(self, node):
        if node is None:
            return 'nothing'
        if node.nodeType == xml.dom.Node.TEXT_NODE:
            return '"%s"' % node.data.strip()
        if node.nodeType == xml.dom.Node.ELEMENT_NODE:
            return '<%s> element' % node.tagName
        return repr(node)

    def arrange_children(self):
        actual_children = self.actual.childNodes
        expected_children = self.expected.childNodes

        expected_child_tags = [
            n.tagName for n in self.expected.childNodes
            if n.nodeType == xml.dom.Node.ELEMENT_NODE]

        if self.settings.ignore_extra_elements:
            actual_children = [c for c in actual_children 
                               if c.nodeType != xml.dom.Node.ELEMENT_NODE or 
                               c.tagName in expected_child_tags]

        if self.settings.ignore_element_order:
            key = lambda node: node.tagName if node.nodeType == xml.dom.Node.ELEMENT_NODE else '!text'
            actual_children = sorted(actual_children, key=key)
            expected_children = sorted(expected_children, key=key)

        self.children = map(self.create_child, izip_longest(actual_children, expected_children))

    def create_child(self, pair):
        actual, expected = pair
        return Twinode(actual, expected, settings=self.settings, parent=self)

    def are_equal(self, node1, node2):
        try:
            self.create_child((node1, node2)).assert_equal()
        except AssertionError:
            return False
        else:
            return True
