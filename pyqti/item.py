#!/usr/bin/env python3

from uuid import uuid4
from pyqti.util import load_template
from pyqti.xmlfile import XMLFile

class Item:
    template_ref = load_template('structure_section_ref')

    def __init__(self, title, uuid=None):
        self.title = title
        self.uuid = uuid
        if self.uuid is None:
            self.uuid = str(uuid4())
        self.filename = f"{self.uuid}.xml"

    def identity(self):
        return {"id": self.uuid, "href": self.filename, "title": self.title}

    def output_structure(self):
        # TODO: this doesn't belong here, needs better logging
        print(f'Writing {self.title} to {self.identity()["href"]}')
        return self.template_ref.substitute(self.identity())

    def output_manifest(self):
        # self.template_manifest is set in subclasses
        return self.template_manifest.substitute({**self.data, **self.identity()})

    def output_file(self):
        # self.template_file is set in subclasses
        return self.template_file.substitute({**self.data, **self.identity()})

    def files(self, prefix=""):
        return [XMLFile(self.filename, self.output_file())]

class Section(Item):
    template_structure = load_template('structure_section')

    def __init__(self, title, select=None, uuid=None):
        super().__init__(title, uuid)
        self.children = []
        self.selection = ("" if select is None else
                          f'<selection select="{select}"/>')

    def add(self, *children):
        self.children.extend(children)

    def output_structure(self):
        refs = [c.output_structure() for c in self.children]
        return self.template_structure.substitute({
            "section_id": self.uuid,
            "section_title": self.title,
            "refs": "".join(refs),
            "selection": self.selection
        })

    def output_manifest(self):
        resources = [c.output_manifest() for c in self.children]
        return "".join(resources)

    def files(self):
        res = []
        for c in self.children:
            res.extend(c.files())
        return res

class Kprim(Item):
    template_file = load_template('kprim')
    template_manifest = load_template('manifest_kprim')

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
    template_manifest = load_template('manifest_essay')

    def __init__(self, points, title, html, lines=5, uuid=None):
        super().__init__(title, uuid)
        self.data = {
            "id": self.uuid,
            "title": title,
            "task_html": html,
            "lines": lines,
            "points": points
        }


