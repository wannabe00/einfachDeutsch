"""Grundlagen: two optional starter units before A1, for learners starting
from zero (letters, sounds, numbers, first words, how German works).

They hold no word list: A1 Lektion 1 onwards teaches these words properly, and
a word may only be taught once. Listening tasks use the browser's own speech
(`hear`, `dictate`), so there are no audio files to store.
"""

from .dsl import dictate, fill, grammar, group, hear, lesson, match, mc, rule, tr, unit

A0_LEVEL = "A0"

# ============================================================================
# Unit 1: Buchstaben, Laute, Zahlen bis 20
# ============================================================================

U1_RULES = [
    rule(
        "Das Alphabet",
        "other",
        """
German uses the same 26 letters as English, plus **ä, ö, ü** and **ß**.
The letter *names* are different. Say them out loud:

| | | | |
|---|---|---|---|
| A *ah* | B *beh* | C *tseh* | D *deh* |
| E *eh* | F *eff* | G *geh* | H *hah* |
| I *ee* | J *yott* | K *kah* | L *ell* |
| M *emm* | N *enn* | O *oh* | P *peh* |
| Q *koo* | R *err* | S *ess* | T *teh* |
| U *oo* | V *fow* | W *veh* | X *iks* |
| Y *üpsilon* | Z *tsett* | | |

Watch out: **E** sounds like English "A", **I** like English "E", **J** is *yott*,
**V** is *fow* and **W** is *veh*. To spell a name, say the letters one by one:
*M-A-X*.
""",
        ["Wie schreibt man das?", "M-A-X, Max.", "Buchstabieren Sie bitte!"],
    ),
    rule(
        "Umlaute und ß",
        "other",
        """
Three vowels can wear two dots, the **Umlaut**. It changes the sound:

- **ä** sounds like the *e* in "bed": *Käse* (cheese)
- **ö**: say *e* with round lips: *schön* (beautiful)
- **ü**: say *ee* with round lips: *müde* (tired)

**ß** (*Eszett*) is a sharp **s**: *heißen, Straße*.

No German keyboard? Write **ae, oe, ue** and **ss**: *Kaese, schoen, muede, Strasse*.
""",
        ["Der Käse ist gut.", "Ich bin müde.", "Ich heiße Lena."],
    ),
    rule(
        "Laute: ei, ie, ch, sch",
        "other",
        """
A few letter pairs always sound the same. Learn them once and you can read
almost any German word.

| write | say | example |
|---|---|---|
| **ei** | like English *eye* | *mein, drei* |
| **ie** | like English *ee* | *Bier, vier* |
| **eu / äu** | like *oy* in "boy" | *neun, Häuser* |
| **sch** | like *sh* | *Schule* |
| **ch** | a soft hiss after e/i (*ich*), throaty after a/o/u (*acht*) | *ich, acht* |
| **w** | like English *v* | *Wasser* |
| **v** | usually like *f* | *Vater* |
| **z** | like *ts* | *zehn* |
| **j** | like English *y* | *ja* |

A tip for **ei** and **ie**: say the *second* letter. *ei* says "I", *ie* says "E".
""",
        ["Mein Vater trinkt Wasser.", "Ich bin in der Schule.", "Eins, zwei, drei."],
    ),
    rule(
        "Zahlen 0 bis 20",
        "other",
        """
| | | | |
|---|---|---|---|
| 0 null | 1 eins | 2 zwei | 3 drei |
| 4 vier | 5 fünf | 6 sechs | 7 sieben |
| 8 acht | 9 neun | 10 zehn | 11 elf |
| 12 zwölf | 13 dreizehn | 14 vierzehn | 15 fünfzehn |
| 16 sechzehn | 17 siebzehn | 18 achtzehn | 19 neunzehn |
| 20 zwanzig | | | |

13 to 19 are the small number + **zehn**: *drei + zehn = dreizehn*.
Two short forms: **sech**zehn (not sechszehn) and **sieb**zehn (not siebenzehn).
On the phone people often say **zwo** for 2, so it isn't confused with *drei*.
""",
        ["Ich bin zwanzig.", "Das kostet fünf Euro.", "Zimmer zwölf, bitte."],
    ),
]

U1_L1 = lesson(
    "Das Alphabet",
    grammar("Das Alphabet"),
    hear("A", "A", "E", "I", prompt="Which letter do you hear?"),
    hear("E", "E", "A", "I", prompt="Which letter do you hear?"),
    hear("I", "I", "E", "A", prompt="Which letter do you hear?"),
    hear("J", "J", "G", "Y", prompt="Which letter do you hear?"),
    hear("V", "V", "W", "F", prompt="Which letter do you hear?"),
    hear("W", "W", "V", "U", prompt="Which letter do you hear?"),
    hear("Z", "Z", "C", "S", prompt="Which letter do you hear?"),
    hear("H", "H", "A", "K", prompt="Which letter do you hear?"),
    match(
        [("E", "eh"), ("I", "ee"), ("J", "yott"), ("V", "fow"), ("W", "veh"), ("Z", "tsett")],
        "Match each letter to how it's said.",
    ),
    mc("How do you say the letter “W” in German?", "veh", "double-u", "fow"),
    mc("How do you say the letter “V” in German?", "fow", "veh", "vee"),
    mc("Which letter is called “yott”?", "J", "Y", "G"),
    group(
        "Listen to the spelling and type the name.",
        dictate("Max", say="M. A. X."),
        dictate("Lena", say="L. E. N. A."),
        dictate("Jan", say="J. A. N."),
    ),
    dictate("Eva", prompt="Listen to the spelling and type the name.", say="E. V. A."),
    dictate("Paul", prompt="Listen to the spelling and type the name.", say="P. A. U. L."),
    mc("“Wie schreibt man das?” means…", "How do you spell that?", "What is that?", "Who is that?"),
)

U1_L2 = lesson(
    "Umlaute und Laute",
    grammar("Umlaute und ß"),
    hear("schön", "schön", "schon", prompt="Which word do you hear?"),
    hear("müde", "müde", "Mode", prompt="Which word do you hear?"),
    hear("Käse", "Käse", "Kasse", prompt="Which word do you hear?"),
    match(
        [("ae", "ä"), ("oe", "ö"), ("ue", "ü"), ("ss", "ß")],
        "Match the keyboard spelling to the letter.",
    ),
    fill("Without an umlaut key, “schön” is written sch___n.", "oe"),
    fill("Without an ß key, “Straße” is written Stra___e.", "ss"),
    grammar("Laute: ei, ie, ch, sch"),
    hear("drei", "drei", "die", "Tee", prompt="Which word do you hear?"),
    hear("vier", "vier", "Wein", "Feuer", prompt="Which word do you hear?"),
    hear("mein", "mein", "Miene", prompt="Which word do you hear?"),
    hear("Bier", "Bier", "bei", prompt="Which word do you hear?"),
    hear("neun", "neun", "nein", "nie", prompt="Which word do you hear?"),
    hear("Schule", "Schule", "Suppe", "Kuli", prompt="Which word do you hear?"),
    mc("“ei” (as in “drei”) sounds like…", "eye", "ee", "ay"),
    mc("“ie” (as in “vier”) sounds like…", "ee", "eye", "ear"),
    mc("“w” (as in “Wasser”) sounds like English…", "v", "w", "f"),
    mc("“z” (as in “zehn”) sounds like…", "ts", "z", "s"),
    mc("“sch” (as in “Schule”) sounds like…", "sh", "sk", "ch in “chair”"),
    group(
        "Listen and type the word.",
        dictate("ja"),
        dictate("nein"),
        dictate("Wasser"),
        dictate("Schule"),
    ),
)

U1_L3 = lesson(
    "Zahlen bis 20",
    grammar("Zahlen 0 bis 20"),
    match(
        [("1", "eins"), ("2", "zwei"), ("3", "drei"), ("4", "vier"), ("5", "fünf"), ("6", "sechs")],
        "Match the numbers.",
    ),
    match(
        [
            ("7", "sieben"),
            ("8", "acht"),
            ("9", "neun"),
            ("10", "zehn"),
            ("11", "elf"),
            ("12", "zwölf"),
        ],
        "Match the numbers.",
    ),
    hear("drei", "3", "2", "8", prompt="Which number do you hear?"),
    hear("neun", "9", "7", "1", prompt="Which number do you hear?"),
    hear("sechzehn", "16", "6", "60", prompt="Which number do you hear?"),
    hear("siebzehn", "17", "7", "70", prompt="Which number do you hear?"),
    hear("zwölf", "12", "20", "2", prompt="Which number do you hear?"),
    hear("zwanzig", "20", "12", "2", prompt="Which number do you hear?"),
    group(
        "Write the number as a word.",
        fill("0 = ___", "null"),
        fill("5 = ___", "fünf|fuenf"),
        fill("8 = ___", "acht"),
        fill("13 = ___", "dreizehn"),
        fill("14 = ___", "vierzehn"),
        fill("19 = ___", "neunzehn"),
    ),
    mc("16 is…", "sechzehn", "sechszehn", "sechzig"),
    mc("17 is…", "siebzehn", "siebenzehn", "siebzig"),
    mc("On the phone, people often say “zwo” for…", "2", "3", "12"),
    group(
        "Listen and type the number as a word.",
        dictate("vier"),
        dictate("elf"),
        dictate("fünfzehn|fuenfzehn"),
    ),
    tr("I am twenty.", "Ich bin zwanzig.|Ich bin zwanzig"),
)

# ============================================================================
# Unit 2: Zahlen bis 100, erste Wörter, wie Deutsch funktioniert
# ============================================================================

U2_RULES = [
    rule(
        "Zahlen bis 100",
        "other",
        """
The tens: **zwanzig** (20), **dreißig** (30), **vierzig** (40), **fünfzig** (50),
**sechzig** (60), **siebzig** (70), **achtzig** (80), **neunzig** (90),
**hundert** (100).

Above 20, German says the **ones first**, then *und*, then the tens, all in
one word:

- 21 = **einund**zwanzig (one-and-twenty)
- 35 = **fünfund**dreißig
- 98 = **achtund**neunzig

Prices: *3,50 €* = **drei Euro fünfzig**. Phone numbers are read in pairs or
one digit at a time: *0176 …* = *null eins sieben sechs …*
""",
        [
            "Ich bin einunddreißig.",
            "Das kostet zwei Euro fünfzig.",
            "Meine Nummer ist null eins sieben sechs.",
        ],
    ),
    rule(
        "Erste Wörter",
        "other",
        """
Words you can use from day one:

- **Hallo!** / **Guten Tag!** (hello) · **Tschüs!** (bye)
- **Danke!** (thanks) · **Bitte!** (please / you're welcome)
- **Ja** (yes) · **Nein** (no) · **Entschuldigung!** (sorry / excuse me)
- **Ich heiße …** (my name is …) · **Ich komme aus …** (I'm from …)

Days: **Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag, Sonntag**.

Colours: **rot** (red), **blau** (blue), **grün** (green), **gelb** (yellow),
**schwarz** (black), **weiß** (white).
""",
        ["Hallo, ich heiße Tom.", "Danke! Bitte!", "Heute ist Montag."],
    ),
    rule(
        "So funktioniert Deutsch",
        "articles",
        """
Three things that surprise beginners:

1. **Every noun starts with a capital letter**, wherever it is in the sentence:
   *der Tisch, die Lampe, das Buch*.
2. **"The" has three forms**: **der**, **die**, **das**. Every noun has one of
   them, and you can't always guess which. Learn each noun *with* its article.
   (Plural is always **die**: *die Bücher*.)
3. **Two words for "you"**: **du** for friends, family and children; **Sie**
   (with a capital S) for adults you don't know, at work and in shops.

Bonus: the **verb is the second idea** in a normal sentence: *Ich **komme** aus Spanien.
Heute **komme** ich.*
""",
        ["Das Buch ist gut.", "Wie heißt du?", "Wie heißen Sie?"],
    ),
]

U2_L1 = lesson(
    "Zahlen bis 100",
    grammar("Zahlen bis 100"),
    match(
        [
            ("30", "dreißig"),
            ("40", "vierzig"),
            ("50", "fünfzig"),
            ("60", "sechzig"),
            ("70", "siebzig"),
            ("100", "hundert"),
        ],
        "Match the numbers.",
    ),
    hear("einundzwanzig", "21", "12", "20", prompt="Which number do you hear?"),
    hear("fünfunddreißig", "35", "53", "25", prompt="Which number do you hear?"),
    hear("achtundvierzig", "48", "84", "40", prompt="Which number do you hear?"),
    hear("sechzig", "60", "16", "70", prompt="Which number do you hear?"),
    hear("neunundneunzig", "99", "90", "19", prompt="Which number do you hear?"),
    mc("In “dreiundvierzig”, which part is said first?", "the 3", "the 40", "both together"),
    mc("67 is…", "siebenundsechzig", "sechzigsieben", "sechsundsiebzig"),
    mc("“2,50 €” is said…", "zwei Euro fünfzig", "fünfzig Euro zwei", "zwei fünfzig Cent"),
    group(
        "Write the number as a word.",
        fill("22 = ___", "zweiundzwanzig"),
        fill("31 = ___", "einunddreißig|einunddreissig"),
        fill("45 = ___", "fünfundvierzig|fuenfundvierzig"),
        fill("80 = ___", "achtzig"),
    ),
    hear(
        "Das kostet vier Euro neunzig.", "4,90 €", "9,40 €", "4,19 €", prompt="What does it cost?"
    ),
    hear("null eins sieben sechs", "0176", "0167", "0716", prompt="Which number do you hear?"),
    group(
        "Listen and type the number as a word.",
        dictate("dreißig|dreissig"),
        dictate("vierundzwanzig"),
        dictate("hundert"),
    ),
)

U2_L2 = lesson(
    "Erste Wörter",
    grammar("Erste Wörter"),
    match(
        [
            ("Hallo", "hello"),
            ("Tschüs", "bye"),
            ("Danke", "thanks"),
            ("Ja", "yes"),
            ("Nein", "no"),
            ("Entschuldigung", "sorry"),
        ],
        "Match the German to the English.",
    ),
    hear("Danke!", "Danke!", "Bitte!", "Hallo!", prompt="What do you hear?"),
    hear("Entschuldigung!", "Entschuldigung!", "Guten Tag!", "Tschüs!", prompt="What do you hear?"),
    mc("Someone says “Danke!”. You answer…", "Bitte!", "Tschüs!", "Nein!"),
    mc("You bump into someone. You say…", "Entschuldigung!", "Danke!", "Hallo!"),
    tr("My name is Anna.", "Ich heiße Anna.|Ich heiße Anna"),
    tr("I'm from Georgia.", "Ich komme aus Georgien.|Ich komme aus Georgien"),
    match(
        [
            ("Montag", "Monday"),
            ("Dienstag", "Tuesday"),
            ("Mittwoch", "Wednesday"),
            ("Donnerstag", "Thursday"),
            ("Freitag", "Friday"),
            ("Sonntag", "Sunday"),
        ],
        "Match the days.",
    ),
    hear("Mittwoch", "Mittwoch", "Montag", "Donnerstag", prompt="Which day do you hear?"),
    mc("Which day comes after “Freitag”?", "Samstag", "Sonntag", "Donnerstag"),
    match(
        [
            ("rot", "red"),
            ("blau", "blue"),
            ("grün", "green"),
            ("gelb", "yellow"),
            ("schwarz", "black"),
            ("weiß", "white"),
        ],
        "Match the colours.",
    ),
    hear("blau", "blau", "braun", "grau", prompt="Which colour do you hear?"),
    group(
        "Listen and type the word.",
        dictate("Hallo"),
        dictate("Danke"),
        dictate("rot"),
        dictate("Montag"),
    ),
)

U2_L3 = lesson(
    "So funktioniert Deutsch",
    grammar("So funktioniert Deutsch"),
    mc(
        "In “ich habe ein buch”, which word is a noun and needs a capital letter?",
        "Buch",
        "habe",
        "ein",
    ),
    mc(
        "In “der tisch ist neu”, which word is a noun and needs a capital letter?",
        "Tisch",
        "ist",
        "neu",
    ),
    mc("How many words for “the” does German have (der, die, das)?", "three", "one", "two"),
    mc("The plural article is always…", "die", "der", "das"),
    mc(
        "What's the best way to learn a new noun?",
        "with its article: der Tisch",
        "without the article",
        "only the plural",
    ),
    mc("You meet your friend's little sister. You say…", "Wie heißt du?", "Wie heißen Sie?"),
    mc("You speak to a police officer. You say…", "Wie heißen Sie?", "Wie heißt du?"),
    mc("In a shop, the seller says to you…", "Sie", "du"),
    mc("Which “Sie” means formal “you”?", "Sie (capital S)", "sie (small s)"),
    mc(
        "Where does the verb go in “Heute ___ ich.” (komme)?",
        "Heute komme ich.",
        "Heute ich komme.",
        "Komme heute ich.",
    ),
    hear("Wie heißen Sie?", "Wie heißen Sie?", "Wie heißt du?", prompt="What do you hear?"),
    group(
        "Listen and type the sentence.",
        dictate("Wie heißt du?|Wie heißt du|Wie heisst du"),
        dictate("Ich heiße Max.|Ich heiße Max|Ich heisse Max"),
    ),
)

A0_UNITS = [
    unit(1, "Buchstaben und Zahlen", "Grundlagen", [], U1_RULES, [U1_L1, U1_L2, U1_L3]),
    unit(2, "Erste Schritte", "Grundlagen", [], U2_RULES, [U2_L1, U2_L2, U2_L3]),
]
