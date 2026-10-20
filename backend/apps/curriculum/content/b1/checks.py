"""B1 check content: what the review of each Lektion and each Modul test asks
beyond the generated word batches (see apps.curriculum.checks and
content/a1/checks.py for the format).

B1 is stage 4 of the ramp throughout, like A2: gaps and translations are typed
(gaps carry a hint), and every extra format is used. Translations list the
common word-order variants, since typing is graded exactly. All sentences are
original. Each Modul adds its Lektionen here as it is written.
"""

from ..dsl import lektion_check, modul_check

LEVEL = "B1"


def _l(n, gaps, translations):
    return n, lektion_check(LEVEL, n, gaps, translations)


LEKTION_CHECKS = dict(
    [
        _l(
            1,
            [
                ("Ihr seid einfach die [Besten]!", "gut, Superlativ"),
                ("Ein [Erwachsener] muss unterschreiben.", "erwachsen"),
                ("Ich helfe meinem [Nachbarn].", "Nachbar"),
                ("Kennst du den neuen [Kollegen]?", "Kollege"),
                ("Sie hat viel [Mut].", "courage"),
            ],
            [
                ("She is really honest.", "Sie ist wirklich ehrlich."),
                ("I trust my neighbour.", "Ich vertraue meinem Nachbarn."),
                ("He is the bravest of us.", "Er ist der Mutigste von uns."),
                (
                    "I have great respect for her.",
                    "Ich habe großen Respekt vor ihr.",
                ),
            ],
        ),
        _l(
            2,
            [
                ("Insgesamt [gefiel] mir das Praktikum gut.", "gefallen"),
                ("Er [erledigte] seine Aufgaben zuverlässig.", "erledigen"),
                ("Der Azubi [brachte] die Post.", "bringen"),
                ("Niemand [wusste] die Antwort.", "wissen"),
                ("Sie arbeitet in [Teilzeit].", "part-time"),
            ],
            [
                ("He looked after the children.", "Er betreute die Kinder."),
                ("I took over a group.", "Ich übernahm eine Gruppe."),
                (
                    "The working atmosphere was pleasant.",
                    "Das Betriebsklima war angenehm.",
                ),
                ("We didn't know the colleagues yet.", "Wir kannten die Kollegen noch nicht."),
            ],
        ),
        _l(
            3,
            [
                ("Das ist der Mann, [dem] ich geholfen habe.", "relative pronoun"),
                ("Das sind die Kunden, [denen] wir schreiben.", "relative pronoun"),
                ("Das ist die Wohnung, in [der] ich wohne.", "relative pronoun"),
                ("Wir wohnen in einem [Vorort].", "suburb"),
                ("Die [Hälfte] von uns wohnt zur Miete.", "half"),
            ],
            [
                ("Do you rent? (Sie)", "Wohnen Sie zur Miete?"),
                (
                    "That is the house I grew up in.",
                    "Das ist das Haus, in dem ich aufgewachsen bin.",
                ),
                ("The street is very narrow.", "Die Straße ist sehr eng."),
                (
                    "A quarter of the people live alone.",
                    "Ein Viertel der Menschen lebt allein.",
                ),
            ],
        ),
    ]
)


MODUL_CHECKS = {
    1: modul_check(
        LEVEL,
        3,
        dialogue=(
            [
                "A: Wie war dein erster Tag im Praktikum?",
                "B: ___",
                "A: Und die Kollegen?",
                "B: Die sind total nett. Wir duzen uns sogar.",
            ],
            "Insgesamt gefiel er mir sehr gut.",
            "Ich wohne in einem Reihenhaus.",
            "Das ist der Mann, dem ich geholfen habe.",
        ),
        qa=[
            ("Wer ist dein Vorbild?", "Meine Großmutter, weil sie so mutig ist."),
            ("Wo hast du dein Praktikum gemacht?", "In einem Kindergarten."),
            ("Wohnen Sie zur Miete?", "Nein, wir haben eine Eigentumswohnung."),
            ("Wie viel verdienst du netto?", "Das sage ich nicht!"),
            ("Wie ist das Betriebsklima?", "Sehr angenehm."),
        ],
        odd=[
            ("der Ofen", "großzügig", "sparsam", "vernünftig"),
            ("der Vorort", "der Erzieher", "der Praktikant", "der Auszubildende"),
            ("bewundern", "das Reihenhaus", "der Wohnblock", "das Einfamilienhaus"),
            ("einsam", "die Hälfte", "das Drittel", "das Viertel"),
        ],
        reading=(
            """
Jonas hat nach der Schule ein Praktikum bei einem Makler gemacht. Am ersten
Tag war er sehr nervös, aber seine Chefin war geduldig und erklärte ihm alles.
Er begleitete sie zu Besichtigungen und lernte viele Kunden kennen. Eine Kundin
suchte drei Wochen lang eine Wohnung in bester Lage, und am Ende fanden sie eine
Dachwohnung mit Terrasse. Heute macht Jonas eine Ausbildung als Immobilienkaufmann.
""",
            [
                ("Jonas war am ersten Tag ganz ruhig.", False),
                ("Die Chefin hat ihm viel erklärt.", True),
                ("Die Kundin hat keine Wohnung gefunden.", False),
                ("Jonas macht jetzt eine Ausbildung.", True),
            ],
        ),
        form=[
            ("Ich habe mit dem ___ gesprochen. (Kunde)", "Kunden"),
            ("Ein ___ muss das unterschreiben. (erwachsen)", "Erwachsener"),
            ("Sie ___ die Antwort nicht. (wissen, Präteritum)", "wusste"),
            ("Das ist die Frau, ___ ich danke. (relative pronoun)", "der"),
            ("Die Kinder, mit ___ ich spiele, sind fünf. (relative pronoun)", "denen"),
        ],
        mistake=[
            ("Ich kenne den *Student* aus Polen.", "Ich kenne den Studenten aus Polen."),
            ("Er *bringte* mir einen Kaffee.", "Er brachte mir einen Kaffee."),
            (
                "Das ist der Mann, *den* ich geholfen habe.",
                "Das ist der Mann, dem ich geholfen habe.",
            ),
            ("Das ist die Wohnung, in *die* ich wohne.", "Das ist die Wohnung, in der ich wohne."),
        ],
        dictation=[
            "Ihr seid einfach die Besten!",
            "Er erledigte seine Aufgaben zuverlässig.",
            "Mein Beruf ist meine Leidenschaft.",
            "Die Hälfte von uns wohnt zur Miete.",
        ],
    ),
}
