"""A2: Menschen A2.1 (Lektionen 1-12) and A2.2 (Lektionen 13-24).

One module file per three Lektionen, like the book's Module. The books supply
the structure, topics, word lists and exercise types; every sentence here is
written for this app. Word lists only hold words that are new at A2: the A1
words are already learned, and the exercises use them freely.

A2.1 order follows the books (the Kursbuch study guide lists 7-12 out of
order): 7 Sport, 8 Gesundheit, 9 Arbeitsleben, 10 Restaurant, 11 Ich freue mich
so, 12 Ernährung.
"""

from . import m1, m2, m3, m4, m5, m6, m7, m8

A2_LEVEL = "A2"
A2_UNITS = [*m1.UNITS, *m2.UNITS, *m3.UNITS, *m4.UNITS, *m5.UNITS, *m6.UNITS, *m7.UNITS, *m8.UNITS]
