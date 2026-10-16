"""A1 Hören sets, shaped like the Start Deutsch 1 listening paper: one set per
Modul. Teil 1: 6 short dialogues, a/b/c, heard twice. Teil 2: 4 announcements,
richtig/falsch, heard once. Teil 3: 5 phone messages, a/b/c, heard twice.

All scripts are original and use the words taught up to the Modul's last
Lektion. The audio is generated once with `manage.py make_hoeren_audio`.
Moduls 1-2 for now; more follow the same pattern.
"""

from ..dsl import clip, hoeren_mc, hoeren_rf, hoeren_teil

# The Moduls testers see in production; the rest stay local (DEBUG shows all).
LIVE = {1}

DIALOGUES = "Listen to the dialogue. Choose a, b or c. (You hear it twice.)"
ANNOUNCEMENTS = "Listen to the announcement. Richtig oder falsch? (You hear it once.)"
MESSAGES = "Listen to the message. Choose a, b or c. (You hear it twice.)"


def _set(dialogues, announcements, messages) -> list:
    return [
        hoeren_teil(1, DIALOGUES, *[hoeren_mc(clip(*s), *q) for s, q in dialogues]),
        hoeren_teil(
            2,
            ANNOUNCEMENTS,
            *[hoeren_rf(clip(("Ansage", s), plays=1), *q) for s, q in announcements],
        ),
        hoeren_teil(3, MESSAGES, *[hoeren_mc(clip((who, s)), *q) for who, s, q in messages]),
    ]


HOEREN = {
    # Modul 1 (Lektionen 1-3): names, countries, jobs, numbers, family, languages.
    1: _set(
        [
            (
                [
                    ("Frau", "Guten Tag! Wie ist Ihr Name, bitte?"),
                    ("Mann", "Mein Name ist Schneider."),
                    ("Frau", "Wie schreibt man das?"),
                    ("Mann", "S – C – H – N – E – I – D – E – R."),
                ],
                ("Wie heißt der Mann?", "Schneider", "Schreiner", "Schröder"),
            ),
            (
                [
                    ("Mann", "Woher kommst du, Lucia?"),
                    ("Frau", "Ich komme aus Spanien, aus Madrid. Und du?"),
                    ("Mann", "Ich komme aus Italien."),
                ],
                ("Woher kommt Lucia?", "Aus Spanien.", "Aus Italien.", "Aus Brasilien."),
            ),
            (
                [
                    ("Frau", "Was sind Sie von Beruf?"),
                    ("Mann", "Ich bin Lehrer. Und meine Frau ist Ärztin."),
                ],
                ("Was ist der Mann von Beruf?", "Lehrer", "Arzt", "Kellner"),
            ),
            (
                [
                    ("Mann", "Wie alt ist deine Tochter?"),
                    ("Frau", "Sie ist zwölf. Und mein Sohn ist acht."),
                ],
                ("Wie alt ist die Tochter?", "12 Jahre", "8 Jahre", "20 Jahre"),
            ),
            (
                [
                    ("Frau", "Wie ist deine Telefonnummer?"),
                    (
                        "Mann",
                        "Null – eins – sieben – null, fünfundvierzig, dreiundsechzig, neunundzwanzig.",
                    ),
                ],
                ("Wie ist die Telefonnummer?", "0170 45 63 29", "0170 54 63 29", "0170 45 36 29"),
            ),
            (
                [
                    ("Mann", "Sprechen Sie Englisch?"),
                    (
                        "Frau",
                        "Ja. Und ich spreche auch ein bisschen Französisch. Aber kein Russisch.",
                    ),
                ],
                (
                    "Welche Sprachen spricht die Frau?",
                    "Englisch und Französisch",
                    "Englisch und Russisch",
                    "Französisch und Russisch",
                ),
            ),
        ],
        [
            (
                "Liebe Studenten, der Deutschkurs ist heute nicht in Zimmer zwölf. "
                "Er ist in Zimmer zwanzig.",
                ("Der Kurs ist heute in Zimmer 20.", True),
            ),
            (
                "Achtung, bitte! Frau Weber, bitte kommen Sie zur Information. "
                "Frau Weber, bitte zur Information.",
                ("Frau Weber soll zum Telefon kommen.", False),
            ),
            (
                "Guten Tag im Hotel Europa! Wir sprechen Deutsch, Englisch und Italienisch.",
                ("Im Hotel sprechen sie Spanisch.", False),
            ),
            (
                "Liebe Eltern, die Lehrerin von Klasse drei ist Frau Yilmaz. Ihre "
                "Telefonnummer ist null – drei – null, vierundfünfzig, zweiundachtzig.",
                ("Frau Yilmaz ist Lehrerin.", True),
            ),
        ],
        [
            (
                "Frau",
                "Hallo Tom, hier ist Anna. Meine Freundin Sofia ist da, sie kommt aus "
                "Brasilien. Sie spricht ein bisschen Deutsch. Bis bald!",
                ("Woher kommt Sofia?", "Aus Brasilien.", "Aus Spanien.", "Aus Georgien."),
            ),
            (
                "Mann",
                "Guten Tag, Frau Klein. Hier ist Peter Novak von der Firma Hoffmann. "
                "Meine Telefonnummer ist null – sechs – neun, achtunddreißig, "
                "einundfünfzig. Danke und auf Wiederhören!",
                (
                    "Wie ist die Nummer von Herrn Novak?",
                    "069 38 51",
                    "069 83 51",
                    "069 38 15",
                ),
            ),
            (
                "Frau",
                "Hallo Papa, hier ist Lena. Oma und Opa sind heute bei uns. Kommst du auch? Tschüs!",
                ("Wer ist heute bei Lena?", "Oma und Opa", "Mama und Papa", "Ihr Bruder"),
            ),
            (
                "Mann",
                "Hallo Maria, hier ist Jonas. Mein Kollege Ben sucht eine Lehrerin für "
                "Spanisch. Du bist doch Spanischlehrerin! Bis bald.",
                ("Was sucht Ben?", "Eine Spanischlehrerin", "Einen Job", "Eine Kollegin"),
            ),
            (
                "Frau",
                "Guten Tag, hier ist die Sprachschule Lingua. Ihr Englischkurs ist in "
                "Zimmer fünfzehn, nicht in Zimmer fünf. Auf Wiederhören!",
                ("In welchem Zimmer ist der Kurs?", "Zimmer 15", "Zimmer 5", "Zimmer 50"),
            ),
        ],
    ),
    # Modul 2 (Lektionen 4-6): furniture and prices, things and colours, the office.
    2: _set(
        [
            (
                [
                    ("Frau", "Entschuldigung, was kostet der Tisch?"),
                    ("Mann", "Der Tisch kostet zweihundertneunzig Euro."),
                    ("Frau", "Oh, das ist zu teuer!"),
                ],
                ("Was kostet der Tisch?", "290 Euro", "219 Euro", "209 Euro"),
            ),
            (
                [
                    ("Mann", "Wie findest du die Lampe?"),
                    (
                        "Frau",
                        "Die rote? Die finde ich schön. Aber die schwarze Lampe ist hässlich.",
                    ),
                ],
                ("Welche Lampe findet die Frau schön?", "Die rote", "Die schwarze", "Die weiße"),
            ),
            (
                [
                    ("Frau", "Hast du einen Kugelschreiber für mich?"),
                    ("Mann", "Nein, aber hier ist ein Bleistift."),
                    ("Frau", "Danke!"),
                ],
                (
                    "Was bekommt die Frau?",
                    "Einen Bleistift",
                    "Einen Kugelschreiber",
                    "Ein Notizbuch",
                ),
            ),
            (
                [
                    ("Mann", "Ist das deine Tasche?"),
                    ("Frau", "Nein, meine Tasche ist braun. Die Tasche hier ist schwarz."),
                ],
                ("Welche Farbe hat die Tasche von der Frau?", "Braun", "Schwarz", "Grau"),
            ),
            (
                [
                    ("Frau", "Herr Lang, wo ist der Drucker?"),
                    ("Mann", "Der Drucker ist im Büro von Frau Schmidt. Das ist Büro elf."),
                ],
                ("Wo ist der Drucker?", "In Büro 11", "In Büro 7", "Im Büro von Herrn Lang"),
            ),
            (
                [
                    ("Mann", "Brauchen Sie einen Schreibtisch?"),
                    ("Frau", "Nein, einen Schreibtisch habe ich. Ich brauche einen Stuhl."),
                ],
                ("Was braucht die Frau?", "Einen Stuhl", "Einen Schreibtisch", "Einen Schrank"),
            ),
        ],
        [
            (
                "Liebe Kunden, heute im Sonderangebot: Sofas für nur "
                "dreihundertneunundneunzig Euro!",
                ("Die Sofas kosten heute 399 Euro.", True),
            ),
            (
                "Liebe Kunden, im Möbelhaus Krause kosten alle Stühle heute nur "
                "neunundzwanzig Euro.",
                ("Die Stühle kosten heute 39 Euro.", False),
            ),
            (
                "Liebe Kolleginnen und Kollegen, wir haben neue Computer. Haben Sie "
                "Fragen? Bitte fragen Sie Herrn Becker in Büro zwölf.",
                ("Herr Becker ist in Büro 12.", True),
            ),
            (
                "Achtung, bitte: Hier ist eine Tasche. Sie ist blau und klein. "
                "Bitte kommen Sie zur Information.",
                ("Die Tasche ist schwarz.", False),
            ),
        ],
        [
            (
                "Mann",
                "Hallo Sabine, hier ist Tim. Ich habe einen Tisch, aber ich brauche "
                "noch zwei Stühle. Hast du Stühle für mich? Bis bald!",
                ("Was braucht Tim?", "Zwei Stühle", "Einen Tisch", "Ein Bett"),
            ),
            (
                "Frau",
                "Guten Tag, Herr Weber, hier ist Möbel Krause. Ihr Sofa ist da. Es kostet "
                "vierhundertneunundneunzig Euro. Auf Wiederhören!",
                ("Was kostet das Sofa?", "499 Euro", "449 Euro", "994 Euro"),
            ),
            (
                "Mann",
                "Hallo, hier ist Paul aus dem Büro. Frau Schmidt hat eine Frage zur "
                "Rechnung. Bitte schreiben Sie ihr eine E-Mail. Danke!",
                (
                    "Was sollen Sie machen?",
                    "Frau Schmidt eine E-Mail schreiben",
                    "Frau Schmidt anrufen",
                    "Ins Büro kommen",
                ),
            ),
            (
                "Frau",
                "Hallo Jan, hier ist Mia. Ich habe deinen Schlüssel! Er ist bei mir im Büro. Tschüs!",
                ("Was hat Mia?", "Jans Schlüssel", "Jans Brille", "Jans Handy"),
            ),
            (
                "Mann",
                "Guten Tag, hier ist die Firma Meyer. Wir brauchen von Ihnen noch das "
                "Formular. Bitte schreiben Sie uns eine E-Mail. Auf Wiederhören!",
                ("Was braucht die Firma Meyer?", "Das Formular", "Eine Rechnung", "Einen Termin"),
            ),
        ],
    ),
}
