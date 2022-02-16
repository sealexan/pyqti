#!/usr/bin/env python3

from unittest import TestCase
from uuid import UUID
from pyqti.item import Item, Section, Essay, Kprim
from pyqti.util import read_resource
from pyqti.xmlfile import XMLFile
from string import whitespace

class TestItems(TestCase):

    def expected(self, name):
        return read_resource("tests.templates", name)

    def instantiate_item(self, uuid=None):
        return Item("item_title", uuid)

    def instantiate_section(self, select=None, uuid=None):
        return Section("item_title", select, uuid)

    def instantiate_kprim(self, html=None, uuid=None):
        return Kprim(13, "item_title",
            [ "This statement is true"
            , "This statement is false"
            , "This statement is false"
            , "This statement is true"
            ],
            [ True, False, False, True ],
            html, uuid)

    def instantiate_essay(self, lines=None, uuid=None):
        return Essay(13, "item_title", "<p>Hi</p>", lines, uuid)

    def test_item_title(self):
        i = self.instantiate_item()
        self.assertEqual(i.title, "item_title")

    def test_item_uuid4(self):
        i = self.instantiate_item()
        self.assertEqual(UUID(i.uuid).version, 4)

    def test_item_uuid_manually(self):
        i = self.instantiate_item("my-id")
        self.assertEqual(i.uuid, "my-id")

    def test_item_identity(self):
        i = self.instantiate_item("my-id")
        actual = i.identity()
        expected = {
            "id": "my-id",
            "href": "my-id.xml",
            "title": "item_title"
        }
        self.assertDictEqual(actual, expected)

    def test_section_title(self):
        i = self.instantiate_section()
        self.assertEqual(i.title, "item_title")

    def test_section_no_selection(self):
        i = self.instantiate_section()
        self.assertEqual(i.selection, "")

    def test_section_selection(self):
        i = self.instantiate_section(select=12)
        self.assertEqual(i.selection,
            '<selection select="12"/>')

    def test_section_add(self):
        i = self.instantiate_section()
        c1 = self.instantiate_item()
        i.add(c1)
        c2 = self.instantiate_item()
        i.add(c2)
        self.assertIn(c1, i.children)
        self.assertIn(c2, i.children)

    def test_section_files(self):
        i = self.instantiate_section(select=13, uuid="my-id")
        c1 = self.instantiate_essay(uuid="my-essay1")
        i.add(c1)
        c2 = self.instantiate_essay(uuid="my-essay2")
        i.add(c2)
        expected = self.expected("manifest_section.xml")
        expected_filenames = {"my-essay1.xml", "my-essay2.xml"}
        actual_filenames = set()
        for elem in i.files():
            self.assertTrue(isinstance(elem, XMLFile))
            actual_filenames.add(elem.filename)
        self.assertSetEqual(expected_filenames, actual_filenames)

    def test_kprim_output_manifest(self):
        i = self.instantiate_kprim(uuid="my-id")
        actual = i.output_manifest()
        expected = self.expected("manifest_kprim.xml")
        self.assertEqual(actual, expected)

    def test_kprim_output_file(self):
        i = self.instantiate_kprim(uuid="my-id")
        actual = i.output_file()
        expected = self.expected("kprim.xml")
        self.assertEqual(actual, expected)

    def test_essay_output_manifest(self):
        i = self.instantiate_essay(uuid="my-id")
        actual = i.output_manifest()
        expected = self.expected("manifest_essay.xml")
        self.assertEqual(actual, expected)

    def test_essay_output_file(self):
        i = self.instantiate_essay(uuid="my-id")
        actual = i.output_file()
        expected = self.expected("essay.xml")
        self.assertEqual(actual, expected)

    def test_item_output_structure_section_ref(self):
        i = self.instantiate_item("my-id")
        actual = i.output_structure()
        expected = self.expected("structure_section_ref.xml")
        self.assertEqual(actual, expected)

    def test_section_output_manifest(self):
        i = self.instantiate_section(select=13, uuid="my-id")
        c1 = self.instantiate_essay(uuid="my-essay")
        i.add(c1)
        actual = i.output_manifest()
        expected = self.expected("manifest_section.xml")
        self.assertEqual(actual, expected)

    def test_section_output_structure(self):
        i = self.instantiate_section(select=13, uuid="my-id")
        actual = i.output_structure()
        expected = self.expected("structure_section.xml")
        self.assertEqual(actual, expected)

