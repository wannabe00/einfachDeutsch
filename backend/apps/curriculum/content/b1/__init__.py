"""B1: Menschen B1.1 (Lektionen 1-12) and B1.2 (Lektionen 13-24), the last level.

One module file per three Lektionen, like the book's Module. The books supply
the structure, topics, word lists and exercise types; every sentence here is
written for this app. Word lists only hold words that are new at B1: the A1 and
A2 words are already learned, and the exercises use them freely.
"""

from . import m1, m2, m3, m4

B1_LEVEL = "B1"
B1_UNITS = [*m1.UNITS, *m2.UNITS, *m3.UNITS, *m4.UNITS]
