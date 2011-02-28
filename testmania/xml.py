# -*- coding: utf-8; -*-

from __future__ import absolute_import

from itertools import izip_longest

import xml.dom.minidom


def assert_xml_equal(actual, expected, msg=None, ignore_whitespace=True):
    actual = xml.dom.minidom.parseString(actual)
    expected = xml.dom.minidom.parseString(expected)

    if ignore_whitespace:
        _strip_whitespace(actual)
        _strip_whitespace(expected)

    try:
        _assert_node_equal(actual.documentElement, expected.documentElement)
    except AssertionError, e:
        if not msg:
            msg = "\nExpected:\n%s\n\nActual:\n%s\n%s" % \
                    (expected.toprettyxml(), actual.toprettyxml(), e)
        raise AssertionError(msg)


def _assert_node_equal(actual, expected, path=[]):
    if actual is None or expected is None or actual.nodeType != expected.nodeType:
        msg = "at %s expected %s, got %s" % \
                (_format_path(path), _format_node(expected), _format_node(actual))
        raise AssertionError(msg)

    node_type = actual.nodeType

    if node_type == xml.dom.Node.TEXT_NODE:
        actual = actual.data.strip()
        expected = expected.data.strip()
        if actual != expected:
            msg = "at %s expected %r node, got %r" % \
                    (_format_path(path), expected, actual)
            raise AssertionError(msg)
    elif node_type == xml.dom.Node.ELEMENT_NODE:
        if actual.tagName != expected.tagName:
            msg = "at %s expected <%s> element, got <%s>" % \
                    (_format_path(path), expected.tagName, actual.tagName)
            raise AssertionError(msg)

        elem_pairs = izip_longest(actual.childNodes, expected.childNodes)

        for i, (actual_e, expected_e) in enumerate(elem_pairs):
            _assert_node_equal(actual_e, expected_e, path + [actual.tagName, '', i])
    else:
        raise NotImplementedError("Comparison of %s nodes is not implemented" % node_type)


def _format_path(path):
    result = []
    for x in path:
        if isinstance(x, int):
            result.append('[%s]' % x)
        else:
            result.append('/' + x)
    return ''.join(result) or '/'


def _format_node(node):
    if node is None:
        return 'nothing'
    if node.nodeType == xml.dom.Node.TEXT_NODE:
        return '"%s"' % node.data.strip()
    if node.nodeType == xml.dom.Node.ELEMENT_NODE:
        return '<%s> element' % node.tagName
    return repr(node)


def _strip_whitespace(node):
    for n in node.childNodes:
        if n.nodeType == xml.dom.Node.TEXT_NODE and not n.data.strip():
            node.removeChild(n)
            n.unlink()
        elif n.nodeType == xml.dom.Node.ELEMENT_NODE:
            _strip_whitespace(n)
