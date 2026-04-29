# ~/.sigil/src/main.py
# main.py version : 1.0
import sys

from parser import parser
from router import router
# from pprint import pprint

# sigil -t gentrees --ignore .git @ origin keep
# |        |        |               |      |
# |        |        |               +------+-- TAIL (Sigil modifiers)
# |        |        +-- SCRIPT ARGS (python3 gentrees.py [SCR_ARGV])
# +--------+-- HEAD (Target & Action)

# head list cmd : { -t, -l, -h, -v, -s }
# tail list cmd : { keep, origin }

# arguments = " ".join(sys.argv)
arguments = sys.argv
result    = parser(arguments)
router(result)
# pprint(result)

# I HATE THIS GARBAGE
# IT'S SO FUCKING MESSY