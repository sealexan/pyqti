#!/usr/bin/env python3

from pyqti.item import Item, Section, Essay, Kprim
from pyqti.util import read_resource

def expected(name):
    return read_resource("tests.templates", name)

def instantiate_item(uuid=None):
    return Item("item_title", uuid)

def instantiate_section(select=None, uuid=None):
    return Section("item_title", select, uuid)

def instantiate_kprim(html=None, uuid=None):
    return Kprim(13, "item_title",
        [ "This statement is true"
        , "This statement is false"
        , "This statement is false"
        , "This statement is true"
        ],
        [ True, False, False, True ],
        html, uuid)

def instantiate_essay(lines=None, uuid=None):
    return Essay(13, "item_title", "<p>Hi</p>", lines, uuid)

def make_content():
    s1 = instantiate_section(uuid="s1")
    s2 = instantiate_section(uuid="s2")
    k1 = instantiate_kprim(uuid="k1")
    k2 = instantiate_kprim(uuid="k2")
    e1 = instantiate_essay(uuid="e1")
    s1.add(k1, e1)
    s2.add(k2)
    return [s1, s2]

