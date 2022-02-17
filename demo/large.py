#!/usr/bin/env python3

import random
from pyqti.qti import Qti
from pyqti.item import Section, Essay, Kprim

geography = Section("Geography")

# 2 points for a Kprim called "Question"
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
    ],
    # optional parameter to set the question text.
    # You can also set Kprim.default_html to change the default.
    html="""<p>Decide if true or false</p>"""

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
    ])

geography.add(item1)
geography.add(item2)
geography.add(item3)

# Section will contain 5 out of all available questions
maths = Section("Maths", select=5)

# Generate 100 Kprim questions
for i in range(100):
    statements, answers = [], []
    # Each question contains 4 math problems
    for i in range(4):
        x, y = random.sample(range(0, 10), 2)
        rest = (x + y) % 2
        target = random.choice([0, 1])
        target_name = "even" if target == 0 else "odd"
        statements.append(f"The sum of {x} and {y} is {target_name}")
        answers.append(True if target == rest else False)
    item = Kprim(4, "Odd or even", statements, answers)
    # Add each question to the section
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

event = Section("Event", select=1)
for e in ["Christmas", "Easter"]:
    item = Essay(10, e,
           f"""<p>Share your favourite {e} recipe</p>""")
    event.add(item)
recipes.add(event)

pasta = Section("Pasta", select=1)
for i, p in enumerate(["Spaghetti", "Penne", "Linguine"], 1):
    item = Essay(10, p,
           f"""<p>Share your favourite {p.lower()} recipe</p>""",
           uuid=f"pasta{i:02d}")
    pasta.add(item)
recipes.add(pasta)


# Sections in the test
sections = [geography, maths, translations, recipes]

# Generate output files.
qti = Qti("Demo test", sections, navigation_mode="nonlinear")
zip_path = f"out/qti-exam.zip"
files_path = f"out/qti-files/"
# the second parameter is optional. If provided, the qti xml files
# will be written into that directory for manual inspection. If omitted,
# a temporary directory will be used and only the zip will remain
qti.save_as(zip_path, files_path)

