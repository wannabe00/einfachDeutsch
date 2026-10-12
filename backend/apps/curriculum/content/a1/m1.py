"""Modul 1: Lektion 1 (Hallo! Ich bin Nicole), 2 (Ich bin Journalistin),
3 (Das ist meine Mutter)."""

from ..dsl import (
    bank,
    conj,
    fill,
    grammar,
    interleave,
    lesson,
    match,
    mc,
    order,
    review,
    rule,
    tr,
    unit,
    vocab_lessons,
)

# ============================================================================
# Lektion 1: Hallo! Ich bin Nicole.
# ============================================================================

L1_WORDS = [
    ("hello", "Hallo", "phrase"),
    ("good morning", "Guten Morgen", "phrase"),
    ("good day / hello", "Guten Tag", "phrase"),
    ("good evening", "Guten Abend", "phrase"),
    ("good night", "Gute Nacht", "phrase"),
    ("bye (informal)", "Tschüs", "phrase", "Also spelled Tschüss."),
    ("goodbye", "Auf Wiedersehen", "phrase"),
    ("goodbye (on the phone)", "Auf Wiederhören", "phrase"),
    ("thank you", "Danke", "phrase"),
    ("please / you're welcome", "Bitte", "phrase"),
    ("pardon? / sorry, what?", "Wie bitte?", "phrase"),
    ("How are you? (informal)", "Wie geht's?", "phrase"),
    ("How are you? (formal)", "Wie geht es Ihnen?", "phrase"),
    ("very well", "sehr gut", "phrase"),
    ("good / well", "gut", "adjective"),
    ("so-so", "es geht", "phrase"),
    ("not so good", "nicht so gut", "phrase"),
    ("also / too", "auch", "adverb"),
    ("yes", "ja", "other"),
    ("no", "nein", "other"),
    ("and", "und", "other"),
    ("how", "wie", "other"),
    ("who", "wer", "other"),
    ("where from", "woher", "other"),
    ("to be called", "heißen", "verb"),
    ("to come", "kommen", "verb"),
    ("to be", "sein", "verb"),
    ("to spell", "buchstabieren", "verb"),
    ("to listen / to hear", "hören", "verb"),
    ("the name", "der Name", "noun", "Pl. die Namen"),
    ("the first name", "der Vorname", "noun", "Pl. die Vornamen"),
    ("the surname", "der Familienname", "noun", "Pl. die Familiennamen"),
    ("Mrs / the woman", "die Frau", "noun", "Pl. die Frauen"),
    ("Mr / the gentleman", "der Herr", "noun", "Pl. die Herren"),
    ("the alphabet", "das Alphabet", "noun"),
    ("the country", "das Land", "noun", "Pl. die Länder"),
    ("Germany", "Deutschland", "noun"),
    ("Austria", "Österreich", "noun"),
    ("Switzerland", "die Schweiz", "noun", "Ich komme aus der Schweiz."),
    ("France", "Frankreich", "noun"),
    ("Spain", "Spanien", "noun"),
    ("Italy", "Italien", "noun"),
    ("Turkey", "die Türkei", "noun", "Ich komme aus der Türkei."),
    ("Brazil", "Brasilien", "noun"),
    ("Georgia (the country)", "Georgien", "noun"),
]

L1_RULES = [
    rule(
        "heißen, kommen, sein",
        "verbs",
        """
The three verbs for introducing yourself. The verb ending changes with the person.

| | heißen | kommen | sein |
|---|---|---|---|
| ich | heiße | komme | **bin** |
| du | heißt | kommst | **bist** |
| er / sie | heißt | kommt | **ist** |
| Sie | heißen | kommen | **sind** |

- *sein* is irregular: learn its forms by heart.
- *heißen* adds only **-t** for *du* (not -st), because the stem already ends in **ß**.
""",
        [
            "Ich heiße Nicole.",
            "Du kommst aus Spanien.",
            "Das ist Herr Weber.",
            "Sind Sie Frau Roth?",
        ],
    ),
    rule(
        "W-Fragen",
        "sentence_structure",
        """
A W-question starts with a question word. The **verb comes second**, then the subject.

- **Wie** heißt du? (What's your name?)
- **Wer** ist das? (Who is that?)
- **Woher** kommst du? (Where are you from?)

Answer with **aus** + country: *Ich komme aus Spanien.*
A few countries take an article: *aus **der** Schweiz, aus **der** Türkei*.
""",
        ["Wie heißen Sie?", "Wer ist das? Das ist Anna.", "Woher kommt Paul? Aus Österreich."],
    ),
    rule(
        "du oder Sie?",
        "pronouns",
        """
German has two words for "you".

- **du**: friends, family, children, and most people your own age in casual settings.
- **Sie**: adults you don't know, people at work, officials. Use **Herr** / **Frau** + surname.

The verb form for **Sie** is the same as the infinitive: *Sie heißen, Sie kommen*.
*Sie* is always written with a capital S.

| du | Sie |
|---|---|
| Wie heißt du? | Wie heißen Sie? |
| Woher kommst du? | Woher kommen Sie? |
| Wie geht's? / Wie geht es dir? | Wie geht es Ihnen? |
""",
        ["Hallo, Lea! Wie geht's?", "Guten Tag, Frau Schmidt! Wie geht es Ihnen?"],
    ),
]

L1_LESSONS = [
    lesson(
        "Guten Tag!",
        review("Hallo"),
        review("Guten Morgen"),
        match(
            [
                ("Guten Morgen", "8:00"),
                ("Guten Tag", "13:00"),
                ("Guten Abend", "19:00"),
                ("Gute Nacht", "23:30"),
            ],
            "Which greeting fits the time?",
        ),
        mc(
            "You leave a shop. What do you say to the shop assistant?",
            "Auf Wiedersehen!",
            "Gute Nacht!",
            "Guten Morgen!",
            "Wie bitte?",
        ),
        mc(
            "You end a phone call with your bank. What do you say?",
            "Auf Wiederhören!",
            "Auf Wiedersehen!",
            "Hallo!",
            "Guten Tag!",
        ),
        mc("Which goodbye is informal?", "Tschüs!", "Auf Wiedersehen!", "Guten Abend!"),
        fill("Guten ___! (in the morning)", "Morgen"),
        fill("Gute ___! (before going to bed)", "Nacht"),
    ),
    lesson(
        "Ich heiße …",
        grammar("heißen, kommen, sein"),
        conj("heißen", "ich", "heiße"),
        conj("heißen", "du", "heißt"),
        conj("kommen", "du", "kommst"),
        conj("sein", "ich", "bin"),
        conj("sein", "du", "bist"),
        conj("sein", "er", "ist"),
        fill("Ich ___ Mila. (heißen)", "heiße"),
        fill("Das ___ Herr Weber. (sein)", "ist"),
    ),
    lesson(
        "Wer ist das?",
        fill("Wie ___ du? (heißen)", "heißt"),
        fill("Woher ___ Sie? (kommen)", "kommen"),
        fill("Sie ___ aus Österreich. (she, kommen)", "kommt"),
        conj("kommen", "er", "kommt"),
        conj("kommen", "Sie", "kommen"),
        conj("heißen", "Sie", "heißen"),
        conj("sein", "Sie", "sind"),
        mc("Wer ___ das? (Das ist Anna.)", "ist", "bin", "bist", "sind"),
        mc(
            "Which sentence is correct?",
            "Du kommst aus Polen.",
            "Du kommt aus Polen.",
            "Du kommen aus Polen.",
            "Du komme aus Polen.",
        ),
        order("Ich bin Stefan und komme aus Wien."),
    ),
    lesson(
        "du oder Sie?",
        grammar("du oder Sie?"),
        mc("Your new neighbour, Mr Klein, is about 60. du or Sie?", "Sie", "du"),
        mc("You talk to a child in the park. du or Sie?", "du", "Sie"),
        mc("A student your age at a party. du or Sie?", "du", "Sie"),
        mc("The receptionist at your hotel. du or Sie?", "Sie", "du"),
        mc("Ask Mrs Wagner her name.", "Wie heißen Sie?", "Wie heißt du?", "Wer bist du?"),
        mc("Ask a classmate how they are.", "Wie geht's?", "Wie geht es Ihnen?"),
        fill("Wie geht es ___? (formal you)", "Ihnen"),
        fill("Woher ___ du? (kommen)", "kommst"),
        tr("What is your name? (formal)", "Wie heißen Sie?"),
        tr("Where are you from? (informal)", "Woher kommst du?"),
    ),
    lesson(
        "Woher kommst du?",
        grammar("W-Fragen"),
        mc("___ heißt du? (Ich heiße Leon.)", "Wie", "Woher", "Wer"),
        mc("___ ist das? (Das ist Frau Schmidt.)", "Wer", "Wie", "Woher"),
        mc("___ kommen Sie? (Aus Italien.)", "Woher", "Wie", "Wer"),
        fill("Ich komme ___ Spanien.", "aus"),
        fill("Ich komme aus ___ Schweiz.", "der"),
        fill("Er kommt aus ___ Türkei.", "der"),
        order("Woher kommen Sie?", "Build the question."),
        order("Wie heißt du?", "Build the question."),
        order("Ich komme aus Georgien."),
        tr("I come from Germany.", "Ich komme aus Deutschland."),
    ),
    lesson(
        "Wie geht's?",
        review("Wie geht's?"),
        match(
            [
                ("Sehr gut, danke.", "very well, thanks"),
                ("Es geht.", "so-so"),
                ("Nicht so gut.", "not so good"),
                ("Auch gut.", "fine too"),
            ]
        ),
        mc(
            "Mrs Braun asks: Wie geht es Ihnen? You answer:",
            "Gut, danke. Und Ihnen?",
            "Gut, danke. Und dir?",
            "Ich heiße Braun.",
        ),
        mc(
            "Your friend asks: Wie geht's? You answer:",
            "Gut, danke. Und dir?",
            "Gut, danke. Und Ihnen?",
            "Aus Spanien.",
        ),
        bank(
            "Hallo, Tim! Wie ___ es dir? Danke, ___ gut. Und ___?",
            ["geht", "sehr", "dir"],
            "Ihnen",
            "heißt",
        ),
        order("Wie geht es Ihnen?", "Build the question."),
        fill("Danke, sehr ___! (good)", "gut"),
        mc("You feel so-so. What do you say?", "Es geht.", "Sehr gut!", "Gute Nacht."),
    ),
    lesson(
        "Name und Familienname",
        review("Wie bitte?"),
        mc(
            "You didn't understand someone's name. What do you say?",
            "Wie bitte?",
            "Danke!",
            "Tschüs!",
        ),
        mc("Anna Becker: what is her Familienname?", "Becker", "Anna"),
        mc("Anna Becker: what is her Vorname?", "Anna", "Becker"),
        mc(
            "Greet Thomas Weber formally.",
            "Guten Tag, Herr Weber!",
            "Guten Tag, Frau Weber!",
            "Hallo, Thomas!",
        ),
        mc(
            "Greet Sabine Roth formally.",
            "Guten Abend, Frau Roth!",
            "Guten Abend, Herr Roth!",
            "Hallo, Sabine!",
        ),
        order("Mein Name ist Frau Lindner."),
        fill("Ich ___: L-I-N-D-N-E-R. (spell)", "buchstabiere"),
    ),
    lesson(
        "Dialoge",
        bank(
            "Guten Tag! Ich ___ Herr Roth. Wie ___ Sie? Ich heiße Ana Lopes. "
            "Woher ___ Sie, Frau Lopes? Ich komme ___ Brasilien.",
            ["bin", "heißen", "kommen", "aus"],
            "heißt",
            "kommst",
        ),
        bank(
            "Hallo! Ich bin Tom. Und wer ___ du? Ich ___ Lea. Woher ___ du, Lea? Aus Frankreich.",
            ["bist", "bin", "kommst"],
            "sind",
            "kommen",
        ),
        order("Das ist Frau Yilmaz aus der Türkei."),
        tr(
            "This is Paul. He comes from Austria.",
            "Das ist Paul. Er kommt aus Österreich.",
        ),
        tr("Good evening, Mrs Klein!", "Guten Abend, Frau Klein!"),
        mc("Which reply fits? Woher kommst du?", "Aus Italien.", "Gut, danke.", "Ich heiße Luca."),
        mc("Which reply fits? Wer ist das?", "Das ist Herr Roth.", "Aus Spanien.", "Danke, gut."),
    ),
    lesson(
        "Lektion 1: Test",
        mc("Which answer is correct?", "Ich heiße Nina.", "Ich heißt Nina.", "Ich heißen Nina."),
        fill("___ kommst du? Aus Russland.", "Woher"),
        conj("sein", "sie (she)", "ist"),
        tr("Pardon?", "Wie bitte?"),
        tr("I am Clara.", "Ich bin Clara.|Ich heiße Clara."),
        order("Wie geht es dir?", "Build the question."),
        bank(
            "Guten ___, Frau Weber! Wie geht es ___? Danke, gut.",
            ["Morgen", "Ihnen"],
            "dir",
            "Nacht",
        ),
        mc("Which goodbye do you use on the phone?", "Auf Wiederhören!", "Auf Wiedersehen!"),
    ),
]

LEKTION_1 = unit(
    1,
    "Hallo! Ich bin Nicole.",
    "Begrüßung und Herkunft",
    L1_WORDS,
    L1_RULES,
    interleave(L1_LESSONS, vocab_lessons(L1_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 2: Ich bin Journalistin.
# ============================================================================

L2_WORDS = [
    ("the profession", "der Beruf", "noun", "Pl. die Berufe"),
    ("the journalist", "der Journalist", "noun", "f. die Journalistin"),
    ("the architect", "der Architekt", "noun", "f. die Architektin"),
    ("the doctor", "der Arzt", "noun", "f. die Ärztin"),
    ("the engineer", "der Ingenieur", "noun", "f. die Ingenieurin"),
    ("the teacher", "der Lehrer", "noun", "f. die Lehrerin"),
    ("the student (university)", "der Student", "noun", "f. die Studentin"),
    ("the pupil", "der Schüler", "noun", "f. die Schülerin"),
    ("the actor", "der Schauspieler", "noun", "f. die Schauspielerin"),
    ("the waiter", "der Kellner", "noun", "f. die Kellnerin"),
    ("the hairdresser", "der Friseur", "noun", "f. die Friseurin"),
    ("the salesperson", "der Verkäufer", "noun", "f. die Verkäuferin"),
    ("the secretary", "der Sekretär", "noun", "f. die Sekretärin"),
    ("the nurse", "die Krankenschwester", "noun", "Pl. die Krankenschwestern"),
    ("the employer", "der Arbeitgeber", "noun", "Pl. die Arbeitgeber"),
    ("the vocational training", "die Ausbildung", "noun"),
    ("the internship", "das Praktikum", "noun", "Pl. die Praktika"),
    ("the job", "der Job", "noun", "Pl. die Jobs"),
    ("the position (job opening)", "die Stelle", "noun", "Pl. die Stellen"),
    ("the school", "die Schule", "noun", "Pl. die Schulen"),
    ("the university", "die Universität", "noun", "Pl. die Universitäten"),
    ("the college (higher education)", "die Hochschule", "noun", "Pl. die Hochschulen"),
    ("the age", "das Alter", "noun"),
    ("the place of residence", "der Wohnort", "noun", "Pl. die Wohnorte"),
    ("the origin", "die Herkunft", "noun"),
    ("the marital status", "der Familienstand", "noun"),
    ("the year", "das Jahr", "noun", "Pl. die Jahre"),
    ("the child", "das Kind", "noun", "Pl. die Kinder"),
    ("the number", "die Zahl", "noun", "Pl. die Zahlen"),
    ("the phone number", "die Telefonnummer", "noun", "Pl. die Telefonnummern"),
    ("to work", "arbeiten", "verb", "du arbeitest, er arbeitet"),
    ("to live (reside)", "wohnen", "verb"),
    ("to live (be alive, live with)", "leben", "verb"),
    ("to have", "haben", "verb", "du hast, er hat"),
    ("to make / to do", "machen", "verb"),
    ("to study (at university)", "studieren", "verb"),
    ("to believe / to think", "glauben", "verb"),
    ("to write", "schreiben", "verb"),
    ("married", "verheiratet", "adjective"),
    ("divorced", "geschieden", "adjective"),
    ("alone", "allein", "adverb"),
    ("together", "zusammen", "adverb"),
    ("unemployed", "arbeitslos", "adjective"),
    ("old", "alt", "adjective"),
    ("correct / right", "richtig", "adjective"),
    ("wrong / false", "falsch", "adjective"),
    ("where", "wo", "other"),
    ("but", "aber", "other"),
    ("not", "nicht", "other"),
    ("What do you do for a living?", "Was machst du beruflich?", "phrase"),
    ("What is your job? (formal)", "Was sind Sie von Beruf?", "phrase"),
    ("How old are you?", "Wie alt bist du?", "phrase"),
    ("zero", "null", "other"),
    ("one", "eins", "other"),
    ("two", "zwei", "other"),
    ("three", "drei", "other"),
    ("four", "vier", "other"),
    ("five", "fünf", "other"),
    ("six", "sechs", "other"),
    ("seven", "sieben", "other"),
    ("eight", "acht", "other"),
    ("nine", "neun", "other"),
    ("ten", "zehn", "other"),
    ("eleven", "elf", "other"),
    ("twelve", "zwölf", "other"),
    ("twenty", "zwanzig", "other"),
    ("thirty", "dreißig", "other"),
    ("a hundred", "hundert", "other"),
]

L2_RULES = [
    rule(
        "Verben im Präsens",
        "verbs",
        """
Regular verbs take these endings on the stem (*wohn-en* → stem **wohn-**):

| | wohnen | arbeiten | haben | sein |
|---|---|---|---|---|
| ich | wohn**e** | arbeit**e** | hab**e** | bin |
| du | wohn**st** | arbeit**est** | ha**st** | bist |
| er / sie | wohn**t** | arbeit**et** | ha**t** | ist |
| wir | wohn**en** | arbeit**en** | hab**en** | sind |
| ihr | wohn**t** | arbeit**et** | hab**t** | seid |
| sie / Sie | wohn**en** | arbeit**en** | hab**en** | sind |

- Stems ending in **-t** or **-d** add an **e**: *du arbeitest, er arbeitet*.
- *haben* drops the **b** for *du hast, er hat*.
""",
        [
            "Wir wohnen in Hamburg.",
            "Arbeitest du bei Siemens?",
            "Ihr habt zwei Kinder.",
            "Sie sind verheiratet.",
        ],
    ),
    rule(
        "Über Arbeit sprechen",
        "other",
        """
- Profession **without an article**: *Ich bin Lehrer.* (not *ein Lehrer*)
- Job title: *Ich arbeite **als** Kellnerin.*
- Employer: *Ich arbeite **bei** Siemens.*
- Training / internship: *Ich mache eine Ausbildung / ein Praktikum.*

Most jobs have a female form ending in **-in**: *Lehrer → Lehrerin, Student → Studentin*.
Some change a vowel too: *Arzt → Ärztin*.
""",
        [
            "Ich bin Architektin.",
            "Er arbeitet als Kellner.",
            "Sie arbeitet bei Bosch.",
            "Was machst du beruflich?",
        ],
    ),
    rule(
        "Negation mit nicht",
        "sentence_structure",
        """
**nicht** says that something is not the case.

- *Ich bin **nicht** verheiratet.*
- *Sie wohnt **nicht** in Köln.*
- *Er arbeitet **nicht**.*

*nicht* usually stands before the word it negates (an adjective, a place),
or at the end when it negates the whole verb.
""",
        ["Wir sind nicht geschieden.", "Paul wohnt nicht in Berlin.", "Ich arbeite heute nicht."],
    ),
    rule(
        "Zahlen bis 100",
        "other",
        """
- 13 to 19: number + **zehn**: *dreizehn, vierzehn* (16 = **sech**zehn, 17 = **sieb**zehn)
- Tens: *zwanzig, dreißig, vierzig, fünfzig, sechzig, siebzig, achtzig, neunzig*
- 21 to 99: **ones + und + tens**, written as one word:
  *einundzwanzig* (21), *sechsunddreißig* (36), *siebenundsiebzig* (77)
- *eins* becomes **ein** before *und*: *ein*undzwanzig.
- Age: *Ich bin 25 Jahre alt.*
""",
        ["Ich bin dreiundzwanzig Jahre alt.", "Meine Telefonnummer ist 0176 45 82 39."],
    ),
]

L2_LESSONS = [
    lesson(
        "Berufe",
        review("der Beruf"),
        grammar("Über Arbeit sprechen"),
        mc(
            "Which sentence is correct?",
            "Ich bin Lehrer.",
            "Ich bin ein Lehrer.",
            "Ich bin der Lehrer.",
        ),
        fill("Sie ist Lehr___. (female teacher)", "erin"),
        mc("The female form of Arzt:", "die Ärztin", "die Arztin", "die Ärzterin"),
        mc("The female form of Student:", "die Studentin", "die Studenterin", "die Studentine"),
        fill("Er arbeitet ___ Kellner. (as)", "als"),
        fill("Sie arbeitet ___ Siemens. (at the company)", "bei"),
        tr("I am a journalist. (female)", "Ich bin Journalistin."),
        tr("He works as a waiter.", "Er arbeitet als Kellner."),
    ),
    lesson(
        "Was machst du beruflich?",
        review("Was machst du beruflich?"),
        match(
            [
                ("Lehrerin", "teaches at a school"),
                ("Kellner", "works in a restaurant"),
                ("Ärztin", "works in a hospital"),
                ("Friseur", "cuts hair"),
                ("Schauspieler", "works in films"),
            ]
        ),
        mc(
            "Was sind Sie von Beruf? Which answer fits?",
            "Ich bin Ingenieurin.",
            "Ich bin dreißig Jahre alt.",
            "Ich wohne in Bonn.",
        ),
        bank(
            "Ich mache eine ___ als Friseurin. Mein Bruder macht ein ___ bei BMW.",
            ["Ausbildung", "Praktikum"],
            "Stelle",
            "Schule",
        ),
        order("Was machst du beruflich?", "Build the question."),
        order("Ich arbeite als Verkäuferin."),
        fill("Ich bin ___. Ich habe keine Stelle. (unemployed)", "arbeitslos"),
        mc("Lena studiert in München. She is …", "Studentin", "Schülerin", "Lehrerin"),
    ),
    lesson(
        "Verben im Präsens",
        grammar("Verben im Präsens"),
        conj("wohnen", "ich", "wohne"),
        conj("wohnen", "wir", "wohnen"),
        conj("wohnen", "ihr", "wohnt"),
        conj("arbeiten", "du", "arbeitest"),
        conj("arbeiten", "er", "arbeitet"),
        conj("arbeiten", "ihr", "arbeitet"),
        conj("haben", "du", "hast"),
        conj("haben", "sie (she)", "hat"),
        conj("sein", "wir", "sind"),
        conj("sein", "ihr", "seid"),
    ),
    lesson(
        "Wo wohnst du?",
        review("wohnen"),
        fill("Wo ___ du? (wohnen)", "wohnst"),
        fill("Wir ___ in Dortmund. (wohnen)", "wohnen"),
        fill("___ ihr verheiratet? (sein)", "Seid"),
        fill("Herr und Frau Roth ___ zwei Kinder. (haben)", "haben"),
        fill("Was ___ ihr beruflich? (machen)", "macht"),
        mc("Wo wohnt Lukas?", "In Leipzig.", "Aus Leipzig.", "Er ist Lehrer."),
        order("Wir wohnen in Hamburg.", "Put the words in order."),
        order("Wo wohnen Sie?", "Build the question."),
        tr("Where do you live? (informal)", "Wo wohnst du?"),
    ),
    lesson(
        "Familienstand",
        review("verheiratet"),
        match(
            [
                ("verheiratet", "married"),
                ("geschieden", "divorced"),
                ("allein leben", "to live alone"),
                ("zusammenleben", "to live together"),
            ]
        ),
        mc("Ich habe einen Mann. Ich bin …", "verheiratet", "geschieden", "arbeitslos"),
        fill("Ich lebe ___. (alone)", "allein"),
        fill("Wir leben ___. (together)", "zusammen"),
        bank(
            "Maria ist ___ Jahre alt. Sie ist ___ und hat ___ Kinder.",
            ["34", "verheiratet", "zwei"],
            "alt",
            "allein",
        ),
        tr("I am divorced.", "Ich bin geschieden."),
        order("Sie leben zusammen in Köln."),
    ),
    lesson(
        "nicht",
        grammar("Negation mit nicht"),
        order("Ich bin nicht verheiratet."),
        order("Er wohnt nicht in Berlin."),
        order("Wir arbeiten heute nicht."),
        mc(
            "Paul ist Lehrer. Correct this: Paul ist Arzt.",
            "Paul ist nicht Arzt. Er ist Lehrer.",
            "Paul ist Arzt nicht. Er ist Lehrer.",
            "Paul nicht ist Arzt. Er ist Lehrer.",
        ),
        fill("Anna wohnt ___ in Wien, sie wohnt in Graz.", "nicht"),
        tr("She is not married.", "Sie ist nicht verheiratet."),
        tr("We don't live in Bonn.", "Wir wohnen nicht in Bonn."),
    ),
    lesson(
        "Zahlen",
        grammar("Zahlen bis 100"),
        match(
            [
                ("13", "dreizehn"),
                ("16", "sechzehn"),
                ("17", "siebzehn"),
                ("30", "dreißig"),
                ("60", "sechzig"),
            ]
        ),
        mc("21 in German:", "einundzwanzig", "einszwanzig", "zwanzigeins"),
        mc("47 in German:", "siebenundvierzig", "vierundsiebzig", "siebzigundvier"),
        fill("36 = sechsund___", "dreißig"),
        fill("99 = neunund___", "neunzig"),
        fill("12 = ___", "zwölf"),
        tr("I am 25 years old.", "Ich bin fünfundzwanzig Jahre alt.|Ich bin 25 Jahre alt."),
        mc(
            "Wie alt bist du? Which answer fits?",
            "Ich bin 19.",
            "Ich komme aus Polen.",
            "Gut, danke.",
        ),
    ),
    lesson(
        "Rechnen",
        fill("zwei + drei = ___", "fünf"),
        fill("zehn + zehn = ___", "zwanzig"),
        fill("acht + vier = ___", "zwölf"),
        fill("sieben + sieben = ___", "vierzehn"),
        fill("fünfzig + fünfzig = ___", "hundert"),
        fill("dreißig + elf = ___", "einundvierzig"),
        mc("achtzehn + zwei = ?", "zwanzig", "sechzehn", "achtundzwanzig"),
        mc("Which number is 76?", "sechsundsiebzig", "siebenundsechzig", "sechzigundsieben"),
    ),
    lesson(
        "Ein Profil",
        bank(
            "Das ist Jonas. Er ___ 31 Jahre alt und ___ in Stuttgart. Er ___ als Ingenieur "
            "bei Bosch. Er ___ nicht verheiratet.",
            ["ist", "wohnt", "arbeitet", "ist"],
            "hat",
            "bin",
        ),
        mc(
            "Lena ist 29. Sie arbeitet bei Bosch und ist verheiratet. Wo arbeitet Lena?",
            "Bei Bosch.",
            "In Bonn.",
            "Als Ärztin.",
        ),
        mc(
            "Lena ist 29. Sie arbeitet bei Bosch und ist verheiratet. Is Lena married?",
            "Ja, sie ist verheiratet.",
            "Nein, sie ist geschieden.",
            "Nein, sie lebt allein.",
        ),
        match(
            [
                ("Wie alt bist du?", "das Alter"),
                ("Wo wohnst du?", "der Wohnort"),
                ("Woher kommst du?", "die Herkunft"),
                ("Bist du verheiratet?", "der Familienstand"),
                ("Was machst du beruflich?", "der Beruf"),
            ],
            "Which form field does each question ask about?",
        ),
        tr("He has three children.", "Er hat drei Kinder."),
        order("Sie arbeitet als Ärztin in Graz."),
    ),
    lesson(
        "Lektion 2: Test",
        mc("Which form is correct?", "du arbeitest", "du arbeitst", "du arbeiten"),
        fill("Ihr ___ in Wien. (wohnen)", "wohnt"),
        conj("haben", "er", "hat"),
        mc("The female form of Verkäufer:", "die Verkäuferin", "die Verkäufin", "die Verkauferin"),
        fill("Ich bin ___ verheiratet. (not)", "nicht"),
        tr("We are students.", "Wir sind Studenten.|Wir sind Studentinnen."),
        mc("88 in German:", "achtundachtzig", "achtachtzig", "achtzigundacht"),
        order("Was sind Sie von Beruf?", "Build the question."),
    ),
]

LEKTION_2 = unit(
    2,
    "Ich bin Journalistin.",
    "Beruf, Wohnort, Zahlen",
    L2_WORDS,
    L2_RULES,
    interleave(L2_LESSONS, vocab_lessons(L2_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 3: Das ist meine Mutter.
# ============================================================================

L3_WORDS = [
    ("the family", "die Familie", "noun", "Pl. die Familien"),
    ("the father", "der Vater", "noun", "Pl. die Väter"),
    ("the mother", "die Mutter", "noun", "Pl. die Mütter"),
    ("the parents", "die Eltern", "noun", "plural only"),
    ("the son", "der Sohn", "noun", "Pl. die Söhne"),
    ("the daughter", "die Tochter", "noun", "Pl. die Töchter"),
    ("the brother", "der Bruder", "noun", "Pl. die Brüder"),
    ("the sister", "die Schwester", "noun", "Pl. die Schwestern"),
    ("the siblings", "die Geschwister", "noun", "plural only"),
    ("the grandfather", "der Großvater", "noun", "Pl. die Großväter"),
    ("the grandmother", "die Großmutter", "noun", "Pl. die Großmütter"),
    ("the grandparents", "die Großeltern", "noun", "plural only"),
    ("grandpa", "der Opa", "noun", "Pl. die Opas"),
    ("grandma", "die Oma", "noun", "Pl. die Omas"),
    ("the grandson", "der Enkel", "noun", "Pl. die Enkel"),
    ("the granddaughter", "die Enkelin", "noun", "Pl. die Enkelinnen"),
    ("the man / husband", "der Mann", "noun", "Pl. die Männer"),
    ("the husband (formal)", "der Ehemann", "noun", "Pl. die Ehemänner"),
    ("the wife (formal)", "die Ehefrau", "noun", "Pl. die Ehefrauen"),
    ("the niece", "die Nichte", "noun", "Pl. die Nichten"),
    ("the nephew", "der Neffe", "noun", "Pl. die Neffen"),
    ("the friend (m) / boyfriend", "der Freund", "noun", "Pl. die Freunde"),
    ("the friend (f) / girlfriend", "die Freundin", "noun", "Pl. die Freundinnen"),
    ("the colleague (m)", "der Kollege", "noun", "Pl. die Kollegen"),
    ("the colleague (f)", "die Kollegin", "noun", "Pl. die Kolleginnen"),
    ("the partner (m)", "der Partner", "noun", "Pl. die Partner"),
    ("the partner (f)", "die Partnerin", "noun", "Pl. die Partnerinnen"),
    ("the pensioner (f)", "die Rentnerin", "noun", "m. der Rentner"),
    ("the picture / photo", "das Bild", "noun", "Pl. die Bilder"),
    ("the language", "die Sprache", "noun", "Pl. die Sprachen"),
    ("German (language)", "Deutsch", "noun"),
    ("English (language)", "Englisch", "noun"),
    ("French (language)", "Französisch", "noun"),
    ("Spanish (language)", "Spanisch", "noun"),
    ("Italian (language)", "Italienisch", "noun"),
    ("Russian (language)", "Russisch", "noun"),
    ("Georgian (language)", "Georgisch", "noun"),
    ("to speak", "sprechen", "verb", "du sprichst, er spricht"),
    ("which", "welche", "other", "welcher / welche / welches"),
    ("how many", "wie viele", "other"),
    ("a little", "ein bisschen", "phrase"),
    ("exactly", "genau", "adverb"),
    ("very", "sehr", "adverb"),
    ("yes (contradicting a negative)", "doch", "other"),
    ("more", "mehr", "adverb"),
    ("no longer", "nicht mehr", "phrase"),
]

L3_RULES = [
    rule(
        "mein und dein",
        "pronouns",
        """
**mein** (my) and **dein** (your, informal) agree with the noun that follows:

| | masculine | neuter | feminine | plural |
|---|---|---|---|---|
| my | mein Vater | mein Kind | mein**e** Mutter | mein**e** Eltern |
| your | dein Bruder | dein Bild | dein**e** Schwester | dein**e** Geschwister |

Feminine and plural nouns take **-e**. Masculine and neuter take no ending here.
""",
        [
            "Das ist mein Bruder.",
            "Das sind meine Eltern.",
            "Ist das deine Schwester?",
            "Wie heißt dein Kind?",
        ],
    ),
    rule(
        "Ja/Nein-Fragen",
        "sentence_structure",
        """
A yes/no question starts with the **verb**. The subject comes second.

- Statement: *Du bist verheiratet.*
- Question: ***Bist** du verheiratet?*

Compare a W-question, where a question word comes first:
*Wo **wohnst** du?* / ***Wohnst** du in Berlin?*

Yes/no questions go **up** at the end; W-questions go **down**.
""",
        ["Ist das deine Mutter?", "Sprichst du Englisch?", "Haben Sie Kinder?"],
    ),
    rule(
        "ja, nein, doch",
        "other",
        """
- **Ja** confirms: *Sprichst du Deutsch? **Ja**, ein bisschen.*
- **Nein** says no: *Hast du Geschwister? **Nein**, ich habe keine Geschwister.*
- **Doch** contradicts a **negative** question or statement:
  *Du bist nicht verheiratet, oder? **Doch**, ich bin verheiratet.*

Use *doch* only after a negative (*nicht*, *kein*). After a positive question, "yes" is *ja*.
""",
        [
            "Bist du Lehrerin? Ja.",
            "Sprichst du kein Spanisch? Doch, ein bisschen.",
            "Ist das nicht dein Vater? Doch!",
        ],
    ),
    rule(
        "sprechen (e → i)",
        "verbs",
        """
Some verbs change their vowel in the **du** and **er/sie** forms:

- ich spr**e**che
- du spr**i**chst
- er / sie spr**i**cht
- wir sprechen, ihr sprecht, sie / Sie sprechen

Languages are written with a capital letter and no article: *Ich spreche Deutsch.*
""",
        [
            "Welche Sprachen sprichst du?",
            "Sie spricht sehr gut Englisch.",
            "Wir sprechen ein bisschen Russisch.",
        ],
    ),
]

L3_LESSONS = [
    lesson(
        "Meine Familie",
        review("die Familie"),
        review("die Eltern"),
        match(
            [
                ("der Vater", "die Mutter"),
                ("der Sohn", "die Tochter"),
                ("der Bruder", "die Schwester"),
                ("der Großvater", "die Großmutter"),
                ("der Enkel", "die Enkelin"),
            ],
            "Match each man to the matching woman.",
        ),
        mc("Mutter + Vater = …", "die Eltern", "die Geschwister", "die Großeltern"),
        mc("Bruder + Schwester = …", "die Geschwister", "die Eltern", "die Kinder"),
        mc("The parents of your parents are your …", "Großeltern", "Geschwister", "Enkel"),
        fill("Die Tochter von meiner Schwester ist meine ___. (niece)", "Nichte"),
        fill("Der Sohn von meinem Bruder ist mein ___. (nephew)", "Neffe"),
    ),
    lesson(
        "mein und dein",
        grammar("mein und dein"),
        mc("Das ist ___ Vater.", "mein", "meine"),
        mc("Das ist ___ Mutter.", "meine", "mein"),
        mc("Das sind ___ Eltern.", "meine", "mein"),
        mc("Das ist ___ Kind.", "mein", "meine"),
        fill("Wie heißt ___ Bruder? (your)", "dein"),
        fill("Wo wohnt ___ Schwester? (your)", "deine"),
        fill("Was machen ___ Geschwister? (your)", "deine"),
        fill("Das ist ___ Freundin Eva. (my)", "meine"),
        tr("This is my son.", "Das ist mein Sohn."),
        tr("Is that your sister? (informal)", "Ist das deine Schwester?"),
    ),
    lesson(
        "Wer ist das?",
        review("das Bild"),
        bank(
            "Das ist ___ Familie. Das sind ___ Eltern. ___ Vater heißt Karl und "
            "___ Mutter heißt Helga.",
            ["meine", "meine", "Mein", "meine"],
            "mein",
            "dein",
        ),
        mc("Karl is Helga's husband. Helga is Karl's …", "Ehefrau", "Tochter", "Schwester"),
        mc("Tom is Eva's son. Eva is Tom's …", "Mutter", "Oma", "Tochter"),
        mc("Lisa is Max's sister. Max is Lisa's …", "Bruder", "Vater", "Sohn"),
        order("Das ist meine Oma Gertrud."),
        order("Mein Opa ist Rentner."),
        tr("These are my grandparents.", "Das sind meine Großeltern."),
    ),
    lesson(
        "Ja/Nein-Fragen",
        grammar("Ja/Nein-Fragen"),
        order("Ist das deine Mutter?", "Build the question."),
        order("Sprichst du Englisch?", "Build the question."),
        order("Haben Sie Kinder?", "Build the question."),
        order("Wohnt dein Bruder in Graz?", "Build the question."),
        mc(
            "Which is a yes/no question?",
            "Bist du verheiratet?",
            "Wo wohnst du?",
            "Du bist verheiratet.",
        ),
        mc(
            "Make a question from: Du hast Geschwister.",
            "Hast du Geschwister?",
            "Du hast Geschwister?",
            "Geschwister hast du?",
        ),
        tr("Do you speak German? (informal)", "Sprichst du Deutsch?"),
    ),
    lesson(
        "ja, nein, doch",
        grammar("ja, nein, doch"),
        mc(
            "Sprichst du Spanisch? (You do.)",
            "Ja, ein bisschen.",
            "Doch, ein bisschen.",
            "Nein, ein bisschen.",
        ),
        mc(
            "Du bist nicht verheiratet, oder? (You are married.)",
            "Doch, ich bin verheiratet.",
            "Ja, ich bin verheiratet.",
            "Nein, ich bin verheiratet.",
        ),
        mc(
            "Hast du Kinder? (You don't.)",
            "Nein, ich habe keine Kinder.",
            "Doch, ich habe keine Kinder.",
            "Ja, ich habe keine Kinder.",
        ),
        fill("Ist das nicht dein Vater? ___, das ist mein Vater!", "Doch"),
        fill("Wohnst du in Köln? ___, in Bonn.", "Nein"),
        fill("Bist du Studentin? ___, ich studiere in Wien.", "Ja"),
        mc(
            "Du sprichst kein Englisch, oder? (You do.)",
            "Doch, ich spreche Englisch.",
            "Ja, ich spreche Englisch.",
            "Nein, ich spreche Englisch.",
        ),
    ),
    lesson(
        "Sprachen",
        grammar("sprechen (e → i)"),
        conj("sprechen", "ich", "spreche"),
        conj("sprechen", "du", "sprichst"),
        conj("sprechen", "er", "spricht"),
        conj("sprechen", "wir", "sprechen"),
        conj("sprechen", "ihr", "sprecht"),
        fill("Welche Sprachen ___ du? (sprechen)", "sprichst"),
        fill("Maria ___ sehr gut Spanisch. (sprechen)", "spricht"),
        match(
            [
                ("Frankreich", "Französisch"),
                ("Spanien", "Spanisch"),
                ("Italien", "Italienisch"),
                ("Georgien", "Georgisch"),
                ("Österreich", "Deutsch"),
            ],
            "Which language is spoken in each country?",
        ),
        tr("I speak a little German.", "Ich spreche ein bisschen Deutsch."),
    ),
    lesson(
        "Wie viele? Welche?",
        mc("___ Kinder habt ihr? (Zwei.)", "Wie viele", "Welche", "Wer"),
        mc("___ Sprachen sprichst du? (Deutsch und Englisch.)", "Welche", "Wie viele", "Wo"),
        mc("___ ist das? (Das ist mein Kollege.)", "Wer", "Was", "Wo"),
        mc("___ wohnen deine Eltern? (In Tiflis.)", "Wo", "Woher", "Wer"),
        order("Wie viele Sprachen sprichst du?", "Build the question."),
        order("Welche Sprachen sprechen Sie?", "Build the question."),
        bank(
            "Wie ___ Geschwister hast du? Ich habe ___ Bruder und eine ___.",
            ["viele", "einen", "Schwester"],
            "welche",
            "Mutter",
        ),
    ),
    lesson(
        "Freunde und Kollegen",
        review("der Kollege"),
        mc("A woman you work with is your …", "Kollegin", "Freundin", "Partnerin"),
        mc("Your female life partner is your …", "Partnerin", "Kollegin", "Nichte"),
        fill("Das ist mein ___ Mehmet. Wir arbeiten bei Siemens. (colleague)", "Kollege"),
        fill("Ich arbeite ___ mehr. Ich bin Rentnerin. (no longer)", "nicht"),
        tr("This is my friend Anna.", "Das ist meine Freundin Anna."),
        order("Mein Partner spricht sehr gut Französisch."),
    ),
    lesson(
        "Ich über mich",
        bank(
            "Ich ___ Giorgi und komme aus Georgien. Ich bin 28 Jahre ___. Ich ___ in Berlin "
            "und arbeite als Ingenieur. Ich ___ Georgisch, Russisch und ein bisschen Deutsch.",
            ["heiße", "alt", "wohne", "spreche"],
            "bin",
            "habe",
        ),
        bank(
            "Das ist ___ Schwester Nino. Sie ___ verheiratet und hat ___ Sohn.",
            ["meine", "ist", "einen"],
            "mein",
            "hat",
        ),
        mc(
            "Giorgi kommt aus Georgien und wohnt in Berlin. Wo wohnt Giorgi?",
            "In Berlin.",
            "In Georgien.",
            "Aus Georgien.",
        ),
        tr(
            "My parents live in Tbilisi.",
            "Meine Eltern wohnen in Tiflis.|Meine Eltern leben in Tiflis.",
        ),
        order("Meine Schwester hat zwei Kinder."),
    ),
    lesson(
        "Lektion 3: Test",
        mc("Das sind ___ Kinder.", "meine", "mein"),
        fill("___ du Italienisch? (sprechen)", "Sprichst"),
        mc("Hast du keine Zeit? (You do.)", "Doch!", "Ja!", "Nein!"),
        conj("sprechen", "sie (she)", "spricht"),
        tr("Is that your father? (informal)", "Ist das dein Vater?"),
        order("Wie viele Kinder habt ihr?", "Build the question."),
        mc("The daughter of your daughter is your …", "Enkelin", "Nichte", "Schwester"),
        fill("Meine Mutter und mein Vater sind meine ___.", "Eltern"),
    ),
    lesson(
        "Modul 1: Wiederholung",
        mc(
            "Formal: ask where someone comes from.",
            "Woher kommen Sie?",
            "Woher kommst du?",
            "Wo wohnen Sie?",
        ),
        fill("Klara ___ Ärztin in Graz. (sein)", "ist"),
        bank(
            "Guten Tag! Mein Name ___ Klara Novak. Ich komme ___ Tschechien und ___ "
            "in Wien. Ich bin ___ und habe zwei Kinder.",
            ["ist", "aus", "wohne", "verheiratet"],
            "bin",
            "allein",
        ),
        conj("arbeiten", "du", "arbeitest"),
        mc(
            "Du bist nicht Lehrer, oder? (You are.)", "Doch, ich bin Lehrer.", "Ja, ich bin Lehrer."
        ),
        tr("My brother is not married.", "Mein Bruder ist nicht verheiratet."),
        order("Sprechen Sie Englisch?", "Build the question."),
        mc("65 in German:", "fünfundsechzig", "sechsundfünfzig", "sechzigundfünf"),
        fill("Das ist ___ Familie. (my)", "meine"),
        tr("How are you? (formal)", "Wie geht es Ihnen?"),
    ),
]

LEKTION_3 = unit(
    3,
    "Das ist meine Mutter.",
    "Familie und Sprachen",
    L3_WORDS,
    L3_RULES,
    interleave(L3_LESSONS, vocab_lessons(L3_WORDS, "Wörter")),
)


UNITS = [LEKTION_1, LEKTION_2, LEKTION_3]
