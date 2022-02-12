#!/usr/bin/env python3

import os
from string import Template
from pathlib import Path
from uuid import uuid4
from tempfile import TemporaryDirectory
import zipfile

def load_template(name):
    with open(f"qti_templates/{name}.xml", 'r') as f:
        return Template(f.read())

class Qti:
    template_manifest = load_template('imsmanifest')
    template_structure = load_template('test_structure')

    def __init__(self, title, sections):
        self.title = title
        self.sections = sections

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

    def _create_structure(self):
        structure = self.template_structure.substitute({
            "sections": "".join([s.serialize_structure() for s in self.sections]),
            "exam_title": self.title
        })
        manifest = self.template_manifest.substitute({
            "resources": "".join([s.serialize_manifest() for s in self.sections])
        })
        return structure, manifest

class XMLFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

class Item:
    template_ref = load_template('test_structure_section_ref')

    def __init__(self, title, uuid=None):
        self.title = title
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = uuid4()
        self.filename = f"{self.uuid}.xml"

    def serialize_structure(self):
        return self.template_ref.substitute(self.identity())

    def identity(self):
        return {"id": self.uuid, "href": self.filename, "title": self.title}

    def serialize_manifest(self):
        return self.template_manifest.substitute({**self.data, **self.identity()})

    def files(self, prefix=""):
        res = XMLFile(self.filename,
          self.template_file.substitute({**self.data, **self.identity()}))
        return [res]

    def naming(self, strategy, prefix=""):
        self.filename, self.prefix = strategy(self.uuid, prefix)
        for s in self.sections:
            s.naming(strategy, prefix)

class Section(Item):
    template_structure = load_template('test_structure_section')

    def __init__(self, title, select=1, uuid=None):
        super().__init__(title, uuid)
        self.children = []
        self.select = select

    def add(self, child):
        self.children.append(child)

    def serialize_structure(self):
        refs = [c.serialize_structure() for c in self.children]
        return self.template_structure.substitute({
            "section_id": self.uuid,
            "section_title": self.title,
            "refs": "".join(refs),
            "select_count": self.select
        })

    def serialize_manifest(self):
        resources = [c.serialize_manifest() for c in self.children]
        return "".join(resources)

    def files(self):
        res = []
        for c in self.children:
            res.extend(c.files())
        return res


class Essay(Item):
    template_file = load_template('essay')
    template_manifest = load_template('imsmanifest_essay')

    def __init__(self, points, title, html, lines=20, uuid=None):
        super().__init__(title, uuid)
        self.data = {
            "id": self.uuid,
            "title": title,
            "task_html": html,
            "lines": lines,
            "points": points
        }

class Kprim(Item):
    template_file = load_template('kprim')
    template_manifest = load_template('imsmanifest_kprim')

    default_html = """<p>Decide for each of the following statements whether it is true or false.</p>"""

    def __init__(self, points, title, statements, answers, html=default_html, uuid=None):
        super().__init__(title, uuid)
        self.data = {
            "id": self.uuid,
            "title": title,
            "task_html": html,
            "points": points
        }
        for i, s in enumerate(statements, 1):
            self.data[f"statement_{i}"] = s
        for i, answer in enumerate(answers, 1):
            self.data[f"statement_{i}_correct"] = "correct" if answer else "wrong"

