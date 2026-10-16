"""Every level's path content in one place, for the seed command and the tests.

Kept out of `content/__init__.py` so importing the content helpers (dsl) doesn't
load every level's content files.
"""

from .a1 import A1_LEVEL, A1_UNITS
from .a1 import checks as a1_checks
from .a1 import lesen as a1_lesen
from .a1 import schreiben as a1_schreiben
from .a2 import A2_LEVEL, A2_UNITS
from .a2 import checks as a2_checks
from .a2 import lesen as a2_lesen
from .a2 import schreiben as a2_schreiben

# {level: {"units", "lektion_checks", "modul_checks", "lesen", "schreiben"}}, lowest level first.
LEVELS = {
    A1_LEVEL: {
        "units": A1_UNITS,
        "lektion_checks": a1_checks.LEKTION_CHECKS,
        "modul_checks": a1_checks.MODUL_CHECKS,
        "lesen": a1_lesen.LESEN,
        "schreiben": a1_schreiben.SCHREIBEN,
    },
    A2_LEVEL: {
        "units": A2_UNITS,
        "lektion_checks": a2_checks.LEKTION_CHECKS,
        "modul_checks": a2_checks.MODUL_CHECKS,
        "lesen": a2_lesen.LESEN,
        "schreiben": a2_schreiben.SCHREIBEN,
    },
}

ALL_UNITS = [(level, u) for level, spec in LEVELS.items() for u in spec["units"]]
