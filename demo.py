#!/usr/bin/env python3

import random
from pyqti import Qti, Section, Essay, Kprim


# Basic, handcrafted questions one by one, select 2 out of 3
geography = Section("Geography", select=2)

item1 = Kprim(2, "Question",
    [ "Berlin is the capital of France"
    , "France is a country in Europe"
    , "Greenland is an independent nation"
    , "Italy is larger than Russia"
    ],
    [ False
    , True
    , False
    , False
    ]
)

item2 = Kprim(2, "Question",
    [ "Berlin is the capital of Germany"
    , "France is landlocked"
    , "Greenland is part of Denmark"
    , "Antarctica is a country"
    ],
    [ True
    , False
    , True
    , False
    ]
)

item3 = Kprim(2, "Question",
    [ "Paris is the capital of France"
    , "Panama is a country in Europe"
    , "Liechtenstein is an independent nation"
    , "Italy is larger than Albania"
    ],
    [ True
    , False
    , True
    , True
    ],
    # optional parameter to set the question text.
    # You can also set Kprim.default_html to change the default.
    """<p>Decide if true or false</p>"""
)

geography.add(item1)
geography.add(item2)
geography.add(item3)

# Generated questions, select 5 out of 50
maths = Section("Maths", select=5)

for i in range(50):
    statements = []
    answers = []
    for i in range(4):
        x = random.randrange(10)
        y = random.randrange(10)
        rest = (x + y) % 2
        target = random.choice([0, 1])
        target_name = "even" if target == 0 else "odd"
        statements.append(f"The sum of {x} and {y} is {target_name}")
        answers.append(True if target == rest else False)
    item = Kprim(4, "Math problem", statements, answers)
    maths.add(item)

# Essay questions
# without the select parameter, all items will be included.
translations = Section("Translation")

item1 = Essay(10, "German",
"""<p>Translate the following sentence into German:</p>
<blockquote><p>An apple a day keeps the doctor away</p></blockquote>""")
translations.add(item1)

item2 = Essay(10, "Italian",
"""<p>Translate the following sentence into Italian:</p>
<blockquote><p>She sells sea shells by the sea shore shop</p></blockquote>""")
translations.add(item2)

item3 = Essay(10, "Russian",
"""<p>Translate the following sentence into Russian:</p>
<blockquote><p>I don't speak any Russian.</p></blockquote>""",
    # optional parameter setting the answer field size
    lines=50)
translations.add(item3)

# Sections can be nested
recipes = Section("Cooking")

pasta = Section("Pasta", select=1)
for p in ["Spaghetti", "Penne", "Linguine"]:
    item = Essay(10, p,
           f"""<p>Share your favourite {p.lower()} recipe</p>""")
    pasta.add(item)
recipes.add(pasta)

event = Section("Event", select=1)
for p in ["Christmas", "Easter"]:
    item = Essay(10, p,
           f"""<p>Share your favourite {p} recipe</p>""")
    event.add(item)
recipes.add(event)

# Sections in the test
sections = [geography, maths, translations, recipes]

# Generate output files.
qti = Qti("Basic knowledge test", sections, navigation_mode="nonlinear")
zip_path = f"out/qti-exam.zip"
files_path = f"out/qti-files/"
# the second parameter is optional. If provided, the qti xml files
# will be written into that directory for manual inspection. If omitted,
# a temporary directory will be used and only the zip will remain
qti.save_as(zip_path, files_path)

