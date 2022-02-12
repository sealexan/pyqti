#!/usr/bin/env python3

from pyqti.util import load_template

from uuid import uuid4
from pyqti.util import load_template
from pyqti.xmlfile import XMLFile

class Item:
    template_ref = load_template('test_structure_section_ref')

    def __init__(self, title, uuid=None):
        self.title = title
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = uuid4()
        self.filename = f"{self.uuid}.xml"

    def serialize_structure(self):
        print(f'Writing {self.title} to {self.identity()["href"]}')
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

    def __init__(self, title, select=None, uuid=None):
        super().__init__(title, uuid)
        self.children = []
        self.selection = ("" if select is None else
                          f'<selection select="{select}"/>')

    def add(self, child):
        self.children.append(child)

    def serialize_structure(self):
        refs = [c.serialize_structure() for c in self.children]
        return self.template_structure.substitute({
            "section_id": self.uuid,
            "section_title": self.title,
            "refs": "".join(refs),
            "selection": self.selection
        })

    def serialize_manifest(self):
        resources = [c.serialize_manifest() for c in self.children]
        return "".join(resources)

    def files(self):
        res = []
        for c in self.children:
            res.extend(c.files())
        return res


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

class Essay(Item):
    template_file = load_template('essay')
    template_manifest = load_template('imsmanifest_essay')

    def __init__(self, points, title, html, lines=5, uuid=None):
        super().__init__(title, uuid)
        self.data = {
            "id": self.uuid,
            "title": title,
            "task_html": html,
            "lines": lines,
            "points": points
        }


