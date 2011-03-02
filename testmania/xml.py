# -*- coding: utf-8; -*-

from __future__ import absolute_import

import itertools
import xml.dom.minidom


def assert_xml_equal(actual, expected, msg=None, 
                     ignore_whitespace=True, 
                     ignore_extra_elements=False,
                     ignore_element_order=False,
                     ignore_list_order=False,
                     ignore_extra_attrs=False):
    """Test that two XMLs are equivalent.

    Provides detailed message if they don't match.

    `actual` and `expected` should be strings with xmls to test.

    :param ignore_whitespace: whether insignificant whitespace should be ignored
    :param ignore_extra_elements: whether `actual` is allowed to have extra elements
        with tag names not present in `expected` on same level. Set to `True` if you're
        just testing presence of necessary elements.
    :param ignore_element_order: controls whether order of elements with distinct
        tag names is important on a level.
    :param ignore_list_order: controls whether order of elements with same
        tag names is important on a level. Set to `True` if recurring elements
        represent sets, not lists in your XML.
    :param ignore_extra_attrs: whether `actual` is allowed to have element attributes
        that aren't present in `expected`.
    """

    actual = xml.dom.minidom.parseString(actual)
    expected = xml.dom.minidom.parseString(expected)

    if ignore_whitespace:
        _strip_whitespace(actual)
        _strip_whitespace(expected)

    settings = Settings()
    settings.ignore_extra_elements = ignore_extra_elements
    settings.ignore_element_order = ignore_element_order
    settings.ignore_list_order = ignore_list_order
    settings.ignore_extra_attrs = ignore_extra_attrs
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

        for key, value in self.actual.attributes.items():
            try:
                if self.expected.attributes[key].value != value:
                    self._raise_attr(key)
            except KeyError:
                if not self.settings.ignore_extra_attrs:
                    self._raise_attr(key)

        for key in self.expected.attributes.keys():
            if not self.actual.hasAttribute(key):
                self._raise_attr(key)

    def _raise(self):
        msg = "at %s expected %s, got %s" % \
                (self.path(), self.format_node(self.expected), self.format_node(self.actual))
        raise AssertionError(msg)

    def _raise_attr(self, attr):
        msg = "at %s expected %s, got %s" % \
                (self.path_to_attr(attr), self.format_attr(self.expected, attr), self.format_attr(self.actual, attr))
        raise AssertionError(msg)

    def path(self, root_symbol='/'):
        if not self.parent:
            return root_symbol
        return '%s/%s' % (self.parent.path(root_symbol=''), 
                          (self.actual or self.expected).parentNode.tagName)

    def path_to_attr(self, attr):
        return '%s/%s@%s' % (self.path(root_symbol=''), self.actual.tagName, attr)

    def format_node(self, node):
        if node is None:
            return 'nothing'
        if node.nodeType == xml.dom.Node.TEXT_NODE:
            return '"%s"' % node.data.strip()
        if node.nodeType == xml.dom.Node.ELEMENT_NODE:
            return '<%s> element' % node.tagName
        return repr(node)
    
    def format_attr(self, node, attr):
        try:
            return '"%s"' % node.attributes[attr].value
        except KeyError:
            return 'nothing'

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

        tag_key = lambda node: node.tagName if node.nodeType == xml.dom.Node.ELEMENT_NODE else '!text'

        if self.settings.ignore_element_order:
            actual_children = sorted(actual_children, key=tag_key)
            expected_children = sorted(expected_children, key=tag_key)

        if self.settings.ignore_list_order:
            actual_children_groups = itertools.groupby(actual_children, key=tag_key)
            expected_children_groups = itertools.groupby(expected_children, key=tag_key)
            group_pairs = itertools.izip_longest(actual_children_groups, expected_children_groups)
            actual_children = []
            expected_children = []
            for (actual_tag, actual_nodes), (expected_tag, expected_nodes) in group_pairs:
                if actual_tag != expected_tag or actual_tag == '!text':
                    actual_children.extend(actual_nodes)
                    expected_children.extend(expected_nodes)
                    continue
                # we've got two element lists: actual_nodes and expected_nodes
                # check all combinations and add those that match at the beginning
                matches = filter(self.are_equal, itertools.product(actual_nodes, expected_nodes))
                actual_matched = [n for n, _ in matches]
                expected_matched = [n for _, n in matches]
                actual_not_matched = [n for n in actual_nodes if n not in actual_matched]
                expected_not_matched = [n for n in expected_nodes if n not in expected_matched]
                actual_children.extend(actual_matched + actual_not_matched)
                expected_children.extend(expected_matched + expected_not_matched)

        self.children = map(self.create_child, itertools.izip_longest(actual_children, expected_children))

    def create_child(self, pair):
        actual, expected = pair
        return Twinode(actual, expected, settings=self.settings, parent=self)

    def are_equal(self, pair):
        try:
            self.create_child(pair).assert_equal()
        except AssertionError:
            return False
        else:
            return True
