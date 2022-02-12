#!/usr/bin/env python3

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile

from pyqti.util import load_template
from pyqti.xmlfile import XMLFile

class Qti:
    template_manifest = load_template('imsmanifest')
    template_structure = load_template('test_structure')

    def __init__(self, title, sections, navigation_mode="linear"):
        self.title = title
        self.sections = sections
        self.navigation_mode = navigation_mode

    def save_as(self, zip_path, files_path=None):
        structure, manifest = self._create_structure()
        manifest = XMLFile("imsmanifest.xml", manifest)
        structure = XMLFile("structure.xml", structure)
        files = []
        for s in self.sections:
            files.extend(s.files())
        files.extend([structure, manifest])
        if files_path is not None:
            Path(files_path).mkdir(parents=True, exist_ok=True)
            self._save_as(files, zip_path, files_path)
        else:
            with TemporaryDirectory() as tmpdir:
                self._save_as(files, zip_path, tmpdir)

    def _save_as(self, files, zip_path, files_path):
            # create xml files
            for f in files:
                with open(os.path.join(files_path, f.filename), "w") as outfile:
                    outfile.write(f.content)
            # save zip file
            zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(files_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
            print(f"Resulting zip file written to {zip_path}")

    def _create_structure(self):
        structure = self.template_structure.substitute({
            "sections": "".join([s.serialize_structure() for s in self.sections]),
            "exam_title": self.title,
            "navigation_mode": self.navigation_mode
        })
        manifest = self.template_manifest.substitute({
            "resources": "".join([s.serialize_manifest() for s in self.sections])
        })
        return structure, manifest

