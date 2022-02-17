#!/usr/bin/env python3

import random
from pyqti.qti import Qti
from pyqti.item import Section, Essay, Kprim

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

pasta = Section("Recipes")
# Generate three essay questions
for i, p in enumerate(["Spaghetti", "Penne", "Linguine"], 1):
   item = Essay(10, p,
          f"""<p>Share your favourite {p.lower()} recipe</p>""",
          uuid=f"pasta{i:02d}")
   # Add each question to the section
   pasta.add(item)

sections = [pasta, maths]
qti = Qti("Demo exam", sections, navigation_mode="nonlinear")
zip_path = f"my-exam.zip"
qti.save_as(zip_path)

