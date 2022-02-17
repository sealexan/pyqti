#!/usr/bin/env python3

from unittest import TestCase
from pyqti.qti import Qti
from tests import util

class TestQti(TestCase):

    def test_qti_init(self):
        q = Qti("qti_title", [])
        self.assertEqual(q.title, "qti_title")

    def test_qti_sections(self):
        sections = util.make_content()
        q = Qti("qti_title", sections)
        for s in sections:
            self.assertIn(s, q.sections)

    def test_qti_output_structure(self):
        q = Qti("qti_title", util.make_content())
        structure = q.output_structure()
        expected = util.expected("structure.xml")
        self.assertEqual(structure, expected)

    def test_qti_output_manifest(self):
        q = Qti("qti_title", util.make_content())
        manifest = q.output_manifest()
        print(manifest)
        expected = util.expected("imsmanifest.xml")
        self.assertEqual(manifest, expected)

