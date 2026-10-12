"""A1: Menschen A1.1 (Lektionen 1-12) and A1.2 (Lektionen 13-24).

One module file per three Lektionen, like the book's Module. The books supply
the structure, topics, word lists and exercise types; every sentence here is
written for this app.
"""

from . import m1, m2, m3, m4, m5, m6, m7, m8

A1_LEVEL = "A1"
A1_UNITS = [*m1.UNITS, *m2.UNITS, *m3.UNITS, *m4.UNITS, *m5.UNITS, *m6.UNITS, *m7.UNITS, *m8.UNITS]
