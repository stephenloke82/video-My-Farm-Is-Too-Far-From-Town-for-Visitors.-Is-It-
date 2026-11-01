"""Compare beats.py word for word against the script as pasted."""
import os, re
from beats import BEATS

here = os.path.dirname(os.path.abspath(__file__))
words = lambda s: re.findall(r"[\w'’,.-]+", s.replace("...", " ").replace('"', " "))
a = words(open(os.path.join(here, "script.txt"), encoding="utf8").read())
b = words(" ".join(text for _, text, _ in BEATS))
print("script words:", len(a), "beat words:", len(b))
for i, (x, y) in enumerate(zip(a, b)):
    if x != y:
        print("FIRST DIFFERENCE at word", i, a[i - 3:i + 3], "vs", b[i - 3:i + 3])
        break
else:
    print("MATCH" if len(a) == len(b) else "LENGTH DIFFERS")
