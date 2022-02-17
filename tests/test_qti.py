#!/usr/bin/env python3

import os
from pathlib import Path
from unittest import TestCase
from tempfile import TemporaryDirectory
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
        expected = util.expected("imsmanifest.xml")
        self.assertEqual(manifest, expected)

    def test_qti_save_as_with_files(self):
        q = Qti("qti_title", util.make_content())
        with TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "test.zip")
            files_path = os.path.join(tmpdir, "test-files")
            q.save_as(zip_path, files_path)
            from pathlib import Path
            with self.subTest("zip roughly the rigth size"):
                size = os.path.getsize(zip_path)
                self.assertGreater(size, 4000)
            with self.subTest("number of files"):
                number_of_files = len(os.listdir(files_path))
                self.assertEqual(number_of_files, 5)
            with self.subTest("files roughly the right size"):
                size = sum(p.stat().st_size
                           for p in Path(files_path).rglob('*'))
                self.assertGreater(size, 15000)

    def test_qti_save_as_without_files(self):
        q = Qti("qti_title", util.make_content())
        with TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "test.zip")
            q.save_as(zip_path)
            size = os.path.getsize(zip_path)
            self.assertGreater(size, 4000)

