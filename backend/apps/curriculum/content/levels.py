"""Every level's path content in one place, for the seed command and the tests.

Kept out of `content/__init__.py` so importing the content helpers (dsl) doesn't
load every level's content files.
"""

from .a1 import A1_LEVEL, A1_UNITS
from .a1 import checks as a1_checks
from .a2 import A2_LEVEL, A2_UNITS
from .a2 import checks as a2_checks

# {level: {"units", "lektion_checks", "modul_checks"}}, lowest level first.
LEVELS = {
    A1_LEVEL: {
        "units": A1_UNITS,
        "lektion_checks": a1_checks.LEKTION_CHECKS,
        "modul_checks": a1_checks.MODUL_CHECKS,
    },
    A2_LEVEL: {
        "units": A2_UNITS,
        "lektion_checks": a2_checks.LEKTION_CHECKS,
        "modul_checks": a2_checks.MODUL_CHECKS,
    },
}

ALL_UNITS = [(level, u) for level, spec in LEVELS.items() for u in spec["units"]]
