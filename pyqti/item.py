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
        self.item_type = type(self).__name__.lower()
        self.data = {}

    def identity(self):
        return {"id": self.uuid, "href": self.filename, "title": self.title}

    def output_structure(self):
        print(f'Output "{self.title}" to {self.identity()["href"]}')
        return self.template_ref.substitute(self.identity())

    def output_manifest(self):
        template_manifest = load_template(f'manifest_{self.item_type}')
        return template_manifest.substitute({**self.data, **self.identity()})

    def output_file(self):
        template_file = load_template(self.item_type)
        return template_file.substitute({**self.data, **self.identity()})

    def files(self, prefix=""):
        return [XMLFile(self.filename, self.output_file())]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)

class Section(Item):
    template_structure = load_template('structure_section')

    def __init__(self, title, select=None, uuid=None):
        super().__init__(title, uuid)
        self.children = []
        self.selection = ("" if select is None else
                          f'<selection select="{select}"/>')
        self.data = {
            "id": self.uuid,
            "title": title,
            "select": select
        }

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
    def __init__(self, points, title, html, lines=5, uuid=None):
        super().__init__(title, uuid)
        self.data = {
            "id": self.uuid,
            "title": title,
            "task_html": html,
            "lines": lines,
            "points": points
        }


