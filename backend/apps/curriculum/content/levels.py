"""Every level's path content in one place, for the seed command and the tests.

Kept out of `content/__init__.py` so importing the content helpers (dsl) doesn't
load every level's content files.
"""

from .a0 import A0_LEVEL, A0_UNITS
from .a1 import A1_LEVEL, A1_UNITS
from .a1 import checks as a1_checks
from .a1 import hoeren as a1_hoeren
from .a1 import lesen as a1_lesen
from .a1 import schreiben as a1_schreiben
from .a2 import A2_LEVEL, A2_UNITS
from .a2 import checks as a2_checks
from .a2 import hoeren as a2_hoeren
from .a2 import lesen as a2_lesen
from .a2 import schreiben as a2_schreiben
from .b1 import B1_LEVEL, B1_UNITS
from .b1 import checks as b1_checks
from .b1 import hoeren as b1_hoeren
from .b1 import lesen as b1_lesen
from .b1 import schreiben as b1_schreiben

# {level: {"units", "lektion_checks", "modul_checks", "lesen", "schreiben", "hoeren"}}, lowest level first.
LEVELS = {
    A1_LEVEL: {
        "units": A1_UNITS,
        "lektion_checks": a1_checks.LEKTION_CHECKS,
        "modul_checks": a1_checks.MODUL_CHECKS,
        "lesen": a1_lesen.LESEN,
        "schreiben": a1_schreiben.SCHREIBEN,
        "hoeren": a1_hoeren.HOEREN,
        "hoeren_live": a1_hoeren.LIVE,
        "hoeren_next": a1_hoeren.NEXT,
    },
    A2_LEVEL: {
        "units": A2_UNITS,
        "lektion_checks": a2_checks.LEKTION_CHECKS,
        "modul_checks": a2_checks.MODUL_CHECKS,
        "lesen": a2_lesen.LESEN,
        "schreiben": a2_schreiben.SCHREIBEN,
        "hoeren": a2_hoeren.HOEREN,
        "hoeren_live": a2_hoeren.LIVE,
    },
    B1_LEVEL: {
        "units": B1_UNITS,
        "lektion_checks": b1_checks.LEKTION_CHECKS,
        "modul_checks": b1_checks.MODUL_CHECKS,
        "lesen": b1_lesen.LESEN,
        "schreiben": b1_schreiben.SCHREIBEN,
        "hoeren": b1_hoeren.HOEREN,
        "hoeren_live": b1_hoeren.LIVE,
    },
}

# The Grundlagen starter units: seeded like a level, but nobody is at A0, so no
# checks, skill sets or exam (see accounts.levels.STARTER_LEVEL).
STARTER = {"units": A0_UNITS, "lektion_checks": {}, "modul_checks": {}}
SEED_LEVELS = {A0_LEVEL: STARTER, **LEVELS}

ALL_UNITS = [(level, u) for level, spec in SEED_LEVELS.items() for u in spec["units"]]
