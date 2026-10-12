"""Modul 6 (A1.2): Lektion 16 (Wir haben hier ein Problem), 17 (Wer will Popstar
werden?), 18 (Geben Sie ihm doch diesen Tee!)."""

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
# Lektion 16: Wir haben hier ein Problem.
# ============================================================================

L16_WORDS = [
    ("the guest", "der Gast", "noun", "Pl. die Gäste"),
    ("the shower", "die Dusche", "noun", "Pl. die Duschen"),
    ("the television (set)", "der Fernseher", "noun", "Pl. die Fernseher"),
    ("the hairdryer", "der Föhn", "noun", "Pl. die Föhne"),
    ("the towel", "das Handtuch", "noun", "Pl. die Handtücher"),
    ("the bathrobe", "der Bademantel", "noun", "Pl. die Bademäntel"),
    ("the heating", "die Heizung", "noun", "Pl. die Heizungen"),
    ("the air conditioning", "die Klimaanlage", "noun", "Pl. die Klimaanlagen"),
    ("the alarm clock", "der Wecker", "noun", "Pl. die Wecker"),
    ("the technician", "der Techniker", "noun", "f. die Technikerin"),
    ("the connection", "die Verbindung", "noun", "Pl. die Verbindungen"),
    ("the course / class", "der Kurs", "noun", "Pl. die Kurse"),
    ("the meeting (formal)", "die Sitzung", "noun", "Pl. die Sitzungen"),
    ("the business trip", "die Geschäftsreise", "noun", "Pl. die Geschäftsreisen"),
    ("the fear", "die Angst", "noun", "Angst haben"),
    ("the life", "das Leben", "noun"),
    ("to bring", "bringen", "verb"),
    ("to work (function)", "funktionieren", "verb"),
    ("to repair", "reparieren", "verb"),
    ("to send", "schicken", "verb"),
    ("to wait", "warten", "verb", "du wartest, er wartet"),
    ("to do", "tun", "verb"),
    ("to postpone", "verschieben", "verb"),
    ("to cancel (an appointment)", "absagen", "verb", "Ich sage den Termin ab."),
    ("to arrange (an appointment)", "vereinbaren", "verb"),
    ("to suit / to fit", "passen", "verb", "Passt es Ihnen?"),
    ("to switch off", "ausmachen", "verb"),
    ("to take along", "mitnehmen", "verb", "du nimmst mit"),
    ("broken", "kaputt", "adjective"),
    ("on time / punctual", "pünktlich", "adjective"),
    ("cold", "kalt", "adjective"),
    ("funny", "lustig", "adjective"),
    ("strange", "seltsam", "adjective"),
    ("sure / safe", "sicher", "adjective"),
    ("stupid / silly", "dumm", "adjective"),
    ("nothing", "nichts", "other"),
    ("(one)self", "selbst", "other"),
    ("after", "nach", "other", "nach dem Essen"),
    ("to let someone know", "Bescheid sagen", "phrase"),
    ("How silly!", "Wie dumm!", "phrase"),
    ("That doesn't matter.", "Das macht nichts.", "phrase"),
    ("Dear Sir or Madam (letter)", "Sehr geehrte Damen und Herren", "phrase"),
    ("Yours sincerely (letter)", "Mit freundlichen Grüßen", "phrase"),
]

L16_RULES = [
    rule(
        "vor, nach, in (Zeit)",
        "other",
        """
For **when**, these take the **dative**:

| | meaning | example |
|---|---|---|
| **vor** | ago / before | *vor einer Stunde* (an hour ago), *vor dem Frühstück* |
| **nach** | after | *nach dem Essen*, *nach einer Woche* |
| **in** | in (from now) | *in einer Stunde* (an hour from now), *in zwei Tagen* |

Dative forms: *einem Tag, einem Monat, einem Jahr, einer Stunde, einer Woche*, plural *zwei Tag**en***.
""",
        [
            "Der Techniker kommt in einer Stunde.",
            "Vor zwei Tagen war der Aufzug kaputt.",
            "Nach der Sitzung gehe ich nach Hause.",
        ],
    ),
    rule(
        "für + Akkusativ",
        "other",
        """
**für** answers *Für wie lange?* (for how long?) and takes the **accusative**:

*für **einen** Tag, für **eine** Woche, für **ein** Jahr, für zwei Nächte*

Compare:
- ***in** einer Woche* = one week from now
- ***für** eine Woche* = lasting one week
""",
        ["Ich bleibe für eine Woche im Hotel.", "Wir buchen das Zimmer für zwei Nächte."],
    ),
    rule(
        "Höflich bitten, Termine verschieben",
        "other",
        """
- Polite request: ***Können Sie bitte** einen Techniker schicken?*
- Problem: *Die Heizung **funktioniert nicht**. Die Dusche ist **kaputt**.*
- Move an appointment: *Ich möchte den Termin **verschieben**. **Passt es Ihnen** am Freitag?*
- Being late: *Entschuldigung, ich komme zu spät.* Replies: *Kein Problem! / Das macht nichts.*
""",
        [
            "Können Sie mir bitte ein Handtuch bringen?",
            "Passt es dir am Montag um zehn?",
            "Ich muss den Termin leider absagen.",
        ],
    ),
]

L16_LESSONS = [
    lesson(
        "Im Hotel",
        review("der Gast"),
        review("die Heizung"),
        match(
            [
                ("der Wecker", "wakes you up"),
                ("der Föhn", "dries your hair"),
                ("die Klimaanlage", "makes the room cool"),
                ("die Heizung", "makes the room warm"),
                ("das Handtuch", "you dry yourself with it"),
            ]
        ),
        mc("The TV doesn't work. It is …", "kaputt", "pünktlich", "lustig"),
        fill("Die Dusche ___ nicht. (funktionieren)", "funktioniert"),
        fill("Der Techniker kann den Fernseher ___. (repair)", "reparieren"),
    ),
    lesson(
        "Wir haben ein Problem.",
        grammar("Höflich bitten, Termine verschieben"),
        bank(
            "Guten Abend, hier ist Zimmer 214. Wir haben ein ___: Die Heizung ist ___. "
            "Können Sie bitte einen Techniker ___? Natürlich, ich kümmere mich sofort darum.",
            ["Problem", "kaputt", "schicken"],
            "pünktlich",
            "bringen",
        ),
        mc(
            "Polite request:",
            "Können Sie bitte ein Handtuch bringen?",
            "Bring ein Handtuch!",
            "Ein Handtuch!",
        ),
        mc(
            "Someone apologises for being late. You say:",
            "Das macht nichts.",
            "Wie dumm!",
            "Mit freundlichen Grüßen.",
        ),
        conj("warten", "du", "wartest"),
        conj("warten", "er", "wartet"),
        order("Können Sie mir bitte helfen?", "Build the question."),
        tr("The heating doesn't work.", "Die Heizung funktioniert nicht."),
    ),
    lesson(
        "vor, nach, in",
        grammar("vor, nach, in (Zeit)"),
        mc(
            "The technician will come an hour from now: Er kommt ___ einer Stunde.",
            "in",
            "vor",
            "nach",
        ),
        mc("It broke two days ago: Es ist ___ zwei Tagen kaputt gegangen.", "vor", "in", "nach"),
        mc(
            "I'll go home after the meeting: ___ der Sitzung gehe ich nach Hause.",
            "Nach",
            "Vor",
            "In",
        ),
        fill("Ich komme in ___ Woche zurück. (a)", "einer"),
        fill("Vor ___ Jahr war ich in Wien. (a)", "einem"),
        fill("Nach ___ Kurs gehen wir essen. (the)", "dem"),
        tr("In an hour.", "In einer Stunde."),
    ),
    lesson(
        "Für wie lange?",
        grammar("für + Akkusativ"),
        mc("Ich bleibe ___ eine Woche.", "für", "in", "vor"),
        mc("Wir buchen das Zimmer für ___ Tag.", "einen", "einem", "ein"),
        fill("Er fährt für ___ Monat nach Spanien. (a)", "einen"),
        fill("Sie bleibt für ___ Jahr in Berlin. (a)", "ein"),
        mc("Which means 'lasting a week'?", "für eine Woche", "in einer Woche"),
        tr(
            "I stay in the hotel for two nights.",
            "Ich bleibe für zwei Nächte im Hotel.|Ich bleibe zwei Nächte im Hotel.",
        ),
    ),
    lesson(
        "Termine",
        review("verschieben"),
        mc(
            "Ich kann am Montag nicht. I want to …",
            "den Termin verschieben",
            "den Termin vereinbaren",
            "den Termin bringen",
        ),
        mc(
            "Passt es Ihnen am Freitag? means:",
            "Does Friday suit you?",
            "Do you fit on Friday?",
            "Are you free on Friday evening?",
        ),
        bank(
            "Sehr geehrte Frau Klein, leider kann ich am Dienstag nicht. Ich habe eine ___. "
            "Können wir den Termin ___? ___ es Ihnen am Donnerstag? Mit freundlichen ___, Jonas Lehmann",
            ["Geschäftsreise", "verschieben", "Passt", "Grüßen"],
            "absagen",
            "Gruß",
        ),
        fill("Ich sage dir morgen ___. (let you know)", "Bescheid"),
        order("Ich muss den Termin leider absagen."),
        tr("Unfortunately I'm coming late.", "Leider komme ich zu spät.|Ich komme leider zu spät."),
    ),
    lesson(
        "Lektion 16: Test",
        mc("Der Bus kommt ___ zehn Minuten.", "in", "vor", "für"),
        fill("Ich bleibe für ___ Woche. (a)", "eine"),
        mc("The alarm clock:", "der Wecker", "der Föhn", "die Verbindung"),
        fill("___ du deinen Laptop mit? (mitnehmen)", "Nimmst"),
        order("Passt es Ihnen am Montag?", "Build the question."),
        tr("The shower is broken.", "Die Dusche ist kaputt."),
        mc("How do you end a formal letter?", "Mit freundlichen Grüßen", "Liebe Grüße", "Tschüs"),
    ),
]

LEKTION_16 = unit(
    16,
    "Wir haben hier ein Problem.",
    "Im Hotel, Termine",
    L16_WORDS,
    L16_RULES,
    interleave(L16_LESSONS, vocab_lessons(L16_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 17: Wer will Popstar werden?
# ============================================================================

L17_WORDS = [
    ("the pop star", "der Popstar", "noun", "Pl. die Popstars"),
    ("the star (famous person)", "der Star", "noun", "Pl. die Stars"),
    ("the singer", "der Sänger", "noun", "f. die Sängerin"),
    ("the politician", "der Politiker", "noun", "f. die Politikerin"),
    ("the guitar", "die Gitarre", "noun", "Pl. die Gitarren"),
    ("the instrument", "das Instrument", "noun", "Pl. die Instrumente"),
    ("the song", "das Lied", "noun", "Pl. die Lieder"),
    ("the exam", "die Prüfung", "noun", "Pl. die Prüfungen"),
    ("the entrance exam", "die Aufnahmeprüfung", "noun", "Pl. die Aufnahmeprüfungen"),
    ("the place at university", "der Studienplatz", "noun", "Pl. die Studienplätze"),
    ("the foreign language", "die Fremdsprache", "noun", "Pl. die Fremdsprachen"),
    ("the mother tongue", "die Muttersprache", "noun", "Pl. die Muttersprachen"),
    ("abroad", "das Ausland", "noun", "im Ausland"),
    ("the chance", "die Chance", "noun", "Pl. die Chancen"),
    ("the money", "das Geld", "noun"),
    ("the world", "die Welt", "noun"),
    ("the wish", "der Wunsch", "noun", "Pl. die Wünsche"),
    ("the driving licence", "der Führerschein", "noun", "Pl. die Führerscheine"),
    ("the credit card", "die Kreditkarte", "noun", "Pl. die Kreditkarten"),
    ("the motorbike", "das Motorrad", "noun", "Pl. die Motorräder"),
    ("Europe", "Europa", "noun"),
    ("to want (to)", "wollen", "verb", "ich will, du willst, er will"),
    ("to become", "werden", "verb", "du wirst, er wird"),
    ("to complete / to finish", "abschließen", "verb", "eine Ausbildung abschließen"),
    ("to register / sign up", "anmelden", "verb", "sich anmelden"),
    ("to earn", "verdienen", "verb", "Geld verdienen"),
    ("to marry", "heiraten", "verb"),
    ("to travel", "reisen", "verb"),
    ("to run / to walk", "laufen", "verb", "du läufst, er läuft"),
    ("to clean", "putzen", "verb"),
    ("to manage / to pass (an exam)", "schaffen", "verb", "eine Prüfung schaffen"),
    ("absolutely / definitely", "unbedingt", "adverb"),
    ("under no circumstances", "auf keinen Fall", "phrase"),
    ("with", "mit", "other", "+ Dativ"),
    ("without", "ohne", "other", "+ Akkusativ"),
    ("hopefully", "hoffentlich", "adverb"),
    ("finally", "endlich", "adverb"),
    ("tired", "müde", "adjective"),
    ("nobody", "niemand", "other"),
    ("so far", "bisher", "adverb"),
]

L17_RULES = [
    rule(
        "wollen",
        "verbs",
        """
**wollen** says what someone wants or plans to do. Like *können*, the other verb goes to the end:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| will | willst | will | wollen | wollt | wollen |

- *Ich **will** Sängerin **werden**.*
- *Wir **wollen** im Ausland **leben**.*

Careful: *ich will* means "I want", not "I will".
""",
        [
            "Willst du heiraten?",
            "Er will unbedingt den Führerschein machen.",
            "Ich will auf keinen Fall Politiker werden.",
        ],
    ),
    rule(
        "werden",
        "verbs",
        """
**werden** = to become. It is irregular:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| werde | **wirst** | **wird** | werden | werdet | werden |

- With a job, no article: *Sie wird Ärztin.*
- With an adjective: *Es wird kalt. Er wird müde.*
""",
        ["Ich werde bald dreißig.", "Was willst du werden?", "Mein Bruder wird Lehrer."],
    ),
    rule(
        "mit + Dativ, ohne + Akkusativ",
        "cases",
        """
- **mit** + **dative**: *mit **dem** Handy, mit **der** Gitarre, mit **meinem** Freund*
- **ohne** + **accusative**: *ohne **das** Handy, ohne **die** Gitarre, ohne **meinen** Freund*

| | mit (dative) | ohne (accusative) |
|---|---|---|
| der Freund | mit dem Freund | ohne den Freund |
| das Geld | mit dem Geld | ohne das Geld |
| die Kreditkarte | mit der Kreditkarte | ohne die Kreditkarte |
""",
        [
            "Ich reise mit meiner Schwester.",
            "Er fährt ohne Führerschein.",
            "Ich kann nicht ohne Musik leben.",
        ],
    ),
]

L17_LESSONS = [
    lesson(
        "Wünsche",
        review("der Wunsch"),
        review("die Fremdsprache"),
        match(
            [
                ("Geld verdienen", "to earn money"),
                ("im Ausland leben", "to live abroad"),
                ("um die Welt reisen", "to travel around the world"),
                ("eine Prüfung schaffen", "to pass an exam"),
                ("den Führerschein machen", "to get a driving licence"),
            ]
        ),
        mc("Your first language is your …", "Muttersprache", "Fremdsprache", "Prüfung"),
        mc(
            "You need it to drive a car:",
            "einen Führerschein",
            "eine Gitarre",
            "einen Studienplatz",
        ),
        fill("Sie singt Lieder und spielt ___. (guitar)", "Gitarre"),
    ),
    lesson(
        "wollen",
        grammar("wollen"),
        conj("wollen", "ich", "will"),
        conj("wollen", "du", "willst"),
        conj("wollen", "er", "will"),
        conj("wollen", "ihr", "wollt"),
        fill("Ich ___ Sängerin werden. (wollen)", "will"),
        fill("___ du im Ausland leben? (wollen)", "Willst"),
        order("Ich will unbedingt Spanisch lernen."),
        order("Wir wollen um die Welt reisen."),
        tr("I want to earn money.", "Ich will Geld verdienen."),
    ),
    lesson(
        "werden",
        grammar("werden"),
        conj("werden", "ich", "werde"),
        conj("werden", "du", "wirst"),
        conj("werden", "er", "wird"),
        conj("werden", "wir", "werden"),
        fill("Sie ___ Ärztin. (werden)", "wird"),
        fill("Was ___ du von Beruf? (werden)", "wirst"),
        mc("Im Winter ___ es kalt.", "wird", "will", "werdet"),
        tr("I want to become a singer.", "Ich will Sänger werden.|Ich will Sängerin werden."),
    ),
    lesson(
        "unbedingt, vielleicht, auf keinen Fall",
        mc(
            "Ich will ___ heiraten. Das ist mein großer Wunsch!",
            "unbedingt",
            "auf keinen Fall",
            "nie",
        ),
        mc(
            "Ich will ___ Politiker werden. Das finde ich schrecklich!",
            "auf keinen Fall",
            "unbedingt",
            "endlich",
        ),
        fill("___ schaffe ich die Prüfung! (hopefully)", "Hoffentlich"),
        fill("Ich habe ___ den Führerschein! (finally)", "endlich"),
        order("Ich will auf keinen Fall Motorrad fahren."),
        tr(
            "Hopefully I'll find a place at university.",
            "Hoffentlich finde ich einen Studienplatz.",
        ),
    ),
    lesson(
        "mit oder ohne?",
        grammar("mit + Dativ, ohne + Akkusativ"),
        mc("Ich fahre ___ dem Fahrrad.", "mit", "ohne"),
        mc("Er reist ___ seine Familie. Er ist allein.", "ohne", "mit"),
        mc("Ich bezahle mit ___ Kreditkarte.", "der", "die", "dem"),
        mc("Ich gehe nicht ohne ___ Handy aus dem Haus.", "das", "dem", "der"),
        fill("Sie singt mit ___ Freund. (her)", "ihrem"),
        fill("Ich kann nicht ohne ___ Gitarre leben. (my)", "meine"),
        tr("I'm travelling with my sister.", "Ich reise mit meiner Schwester."),
        tr("He drives without a driving licence.", "Er fährt ohne Führerschein."),
    ),
    lesson(
        "Wer will Popstar werden?",
        bank(
            "Lena ist 19. Sie ___ Popstar werden. Sie spielt ___ und singt eigene ___. "
            "Nächste Woche hat sie eine ___ an der Musikhochschule.",
            ["will", "Gitarre", "Lieder", "Aufnahmeprüfung"],
            "wird",
            "Instrument",
        ),
        mc(
            "Lena will Popstar werden. Nächste Woche hat sie eine Aufnahmeprüfung. What happens next week?",
            "She has an entrance exam.",
            "She gives a concert.",
            "She gets married.",
        ),
        conj("laufen", "du", "läufst"),
        conj("laufen", "er", "läuft"),
        order("Ich will mich an der Universität anmelden."),
        mc("Bisher means:", "so far", "finally", "nobody"),
    ),
    lesson(
        "Lektion 17: Test",
        mc("___ ihr Musik studieren?", "Wollt", "Willst", "Will"),
        fill("Mein Bruder ___ Lehrer. (werden)", "wird"),
        mc("Ich trinke Kaffee ohne ___ Milch.", "die", "der", "dem"),
        mc("Ich will … means:", "I want …", "I will …", "I wish …"),
        order("Willst du im Ausland leben?", "Build the question."),
        tr("We want to travel around the world.", "Wir wollen um die Welt reisen."),
        mc("die Fremdsprache means:", "the foreign language", "the mother tongue", "the exam"),
    ),
]

LEKTION_17 = unit(
    17,
    "Wer will Popstar werden?",
    "Pläne und Wünsche",
    L17_WORDS,
    L17_RULES,
    interleave(L17_LESSONS, vocab_lessons(L17_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 18: Geben Sie ihm doch diesen Tee!
# ============================================================================

L18_WORDS = [
    ("the head", "der Kopf", "noun", "Pl. die Köpfe"),
    ("the neck / throat", "der Hals", "noun", "Pl. die Hälse"),
    ("the back", "der Rücken", "noun", "Pl. die Rücken"),
    ("the chest", "die Brust", "noun"),
    ("the stomach / belly", "der Bauch", "noun", "Pl. die Bäuche"),
    ("the arm", "der Arm", "noun", "Pl. die Arme"),
    ("the hand", "die Hand", "noun", "Pl. die Hände"),
    ("the finger", "der Finger", "noun", "Pl. die Finger"),
    ("the leg", "das Bein", "noun", "Pl. die Beine"),
    ("the foot", "der Fuß", "noun", "Pl. die Füße"),
    ("the knee", "das Knie", "noun", "Pl. die Knie"),
    ("the ear", "das Ohr", "noun", "Pl. die Ohren"),
    ("the eye", "das Auge", "noun", "Pl. die Augen"),
    ("the tooth", "der Zahn", "noun", "Pl. die Zähne"),
    ("the nose", "die Nase", "noun", "Pl. die Nasen"),
    ("the mouth", "der Mund", "noun", "Pl. die Münder"),
    ("the pain", "der Schmerz", "noun", "Pl. die Schmerzen"),
    ("the headache", "die Kopfschmerzen", "noun", "plural"),
    ("the sore throat", "die Halsschmerzen", "noun", "plural"),
    ("the stomach ache", "die Bauchschmerzen", "noun", "plural"),
    ("the cold (runny nose)", "der Schnupfen", "noun"),
    ("the cough", "der Husten", "noun"),
    ("the fever", "das Fieber", "noun"),
    ("the pharmacy", "die Apotheke", "noun", "Pl. die Apotheken"),
    ("the doctor's practice", "die Praxis", "noun", "Pl. die Praxen"),
    ("the medicine (drug)", "das Medikament", "noun", "Pl. die Medikamente"),
    ("the tablet / pill", "die Tablette", "noun", "Pl. die Tabletten"),
    ("the ointment", "die Salbe", "noun", "Pl. die Salben"),
    ("the plaster", "das Pflaster", "noun", "Pl. die Pflaster"),
    ("the herbal tea", "der Kräutertee", "noun", "Pl. die Kräutertees"),
    ("healthy", "gesund", "adjective"),
    ("ill / sick", "krank", "adjective"),
    ("to hurt", "wehtun", "verb", "Mein Kopf tut weh."),
    ("should / to be supposed to", "sollen", "verb", "ich soll, du sollst"),
    ("against (for an illness)", "gegen", "other", "+ Akkusativ: Was hilft gegen Husten?"),
    ("this (one)", "dieser", "other", "dieser / diese / dieses"),
    ("Get well soon!", "Gute Besserung!", "phrase"),
    ("What's wrong with him?", "Was hat er denn?", "phrase"),
]

L18_RULES = [
    rule(
        "sollen",
        "verbs",
        """
**sollen** passes on advice or an instruction **from someone else**:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| soll | sollst | soll | sollen | sollt | sollen |

*Der Arzt sagt, ich **soll** viel Tee **trinken**.* (The doctor says I should drink a lot of tea.)
*Was **soll** ich **machen**?*
""",
        [
            "Du sollst im Bett bleiben.",
            "Er soll keinen Kaffee trinken.",
            "Wir sollen um acht Uhr da sein.",
        ],
    ),
    rule(
        "Imperativ mit Sie",
        "verbs",
        """
To tell or advise someone formally: **infinitive + Sie**, verb first.

- *Trinken **Sie** viel Wasser!*
- *Gehen **Sie** zum Arzt!*
- *Bleiben **Sie** im Bett!*
- separable: *Rufen **Sie** den Arzt **an**!*
- *sein*: ***Seien Sie** vorsichtig!*

Add **doch** (and *mal*) to make it a friendly suggestion: *Nehmen Sie **doch** diesen Tee!*
""",
        ["Nehmen Sie diese Tablette!", "Machen Sie doch eine Pause!", "Rufen Sie mich morgen an!"],
    ),
    rule(
        "Was tut weh?",
        "other",
        """
Two ways to say where it hurts:

- **tut weh** (one thing) / **tun weh** (more than one):
  *Mein Kopf **tut weh**. Meine Beine **tun weh**.*
- **-schmerzen** (always plural) with *haben*:
  *Ich habe **Kopfschmerzen / Halsschmerzen / Bauchschmerzen / Rückenschmerzen**.*

Ask: *Was **fehlt** Ihnen? Was **hast** du? Was tut dir weh?*
""",
        ["Mir tut der Rücken weh.", "Er hat Fieber und Husten.", "Meine Augen tun weh."],
    ),
    rule(
        "dieser, diese, dieses",
        "articles",
        """
**dieser** (this / this one) points to something specific. It takes the endings of *der, die, das*:

| | masculine | neuter | feminine | plural |
|---|---|---|---|---|
| nominative | dies**er** Tee | dies**es** Medikament | dies**e** Salbe | dies**e** Tabletten |
| accusative | dies**en** Tee | dies**es** Medikament | dies**e** Salbe | dies**e** Tabletten |

*Geben Sie ihm doch **diesen** Tee!*
""",
        [
            "Diese Salbe hilft gegen Schmerzen.",
            "Nehmen Sie dieses Medikament.",
            "Ich möchte diesen Tee.",
        ],
    ),
]

L18_LESSONS = [
    lesson(
        "Der Körper",
        review("der Kopf"),
        review("die Hand"),
        match(
            [
                ("das Auge", "you see"),
                ("das Ohr", "you hear"),
                ("die Nase", "you smell"),
                ("der Mund", "you eat and speak"),
                ("der Fuß", "you walk"),
            ],
            "What do you do with it?",
        ),
        mc("You have five on each hand:", "Finger", "Zähne", "Knie"),
        mc("It's between your head and your body:", "der Hals", "der Bauch", "der Rücken"),
        fill("Der Zahnarzt kontrolliert die ___. (teeth)", "Zähne"),
    ),
    lesson(
        "Was tut weh?",
        grammar("Was tut weh?"),
        mc("Mein Kopf ___ weh.", "tut", "tun"),
        mc("Meine Füße ___ weh.", "tun", "tut"),
        mc("Ich habe ___.", "Kopfschmerzen", "Kopfschmerz weh", "Kopf weh"),
        fill("Mein Bauch tut ___.", "weh"),
        fill("Ich habe ___. Mein Hals tut weh. (sore throat)", "Halsschmerzen"),
        match(
            [
                ("Ich habe Husten.", "I have a cough."),
                ("Ich habe Schnupfen.", "I have a runny nose."),
                ("Ich habe Fieber.", "I have a fever."),
                ("Ich bin krank.", "I'm ill."),
            ]
        ),
        tr("My back hurts.", "Mein Rücken tut weh.|Mir tut der Rücken weh."),
    ),
    lesson(
        "sollen",
        grammar("sollen"),
        conj("sollen", "ich", "soll"),
        conj("sollen", "du", "sollst"),
        conj("sollen", "er", "soll"),
        conj("sollen", "ihr", "sollt"),
        fill("Der Arzt sagt, ich ___ viel trinken. (sollen)", "soll"),
        fill("Du ___ im Bett bleiben. (sollen)", "sollst"),
        order("Was soll ich gegen Husten machen?", "Build the question."),
        tr("You should go to the doctor. (informal)", "Du sollst zum Arzt gehen."),
    ),
    lesson(
        "Imperativ mit Sie",
        grammar("Imperativ mit Sie"),
        mc("Formal advice: drink a lot!", "Trinken Sie viel!", "Sie trinken viel!", "Trinkt viel!"),
        mc(
            "Formal advice: stay in bed!",
            "Bleiben Sie im Bett!",
            "Bleib im Bett!",
            "Sie bleiben im Bett?",
        ),
        fill("___ Sie zum Arzt! (gehen)", "Gehen"),
        fill("___ Sie doch eine Pause! (machen)", "Machen"),
        fill("Rufen Sie den Arzt ___! (anrufen)", "an"),
        order("Nehmen Sie diese Tablette."),
        tr("Go to the pharmacy! (formal)", "Gehen Sie zur Apotheke!|Gehen Sie in die Apotheke!"),
    ),
    lesson(
        "dieser, diese, dieses",
        grammar("dieser, diese, dieses"),
        mc("___ Tee hilft gegen Husten.", "Dieser", "Diese", "Dieses"),
        mc("___ Salbe ist sehr gut.", "Diese", "Dieser", "Dieses"),
        mc("Nehmen Sie ___ Medikament!", "dieses", "diesen", "dieser"),
        mc("Geben Sie ihm doch ___ Tee!", "diesen", "dieser", "dieses"),
        fill("___ Tabletten sind gegen Fieber. (these)", "Diese"),
        tr("This tea is good.", "Dieser Tee ist gut."),
    ),
    lesson(
        "In der Apotheke",
        review("die Apotheke"),
        bank(
            "Guten Tag. Ich habe ___ und Halsschmerzen. Haben Sie etwas ___ Husten? "
            "Ja, nehmen Sie ___ Tee. Trinken Sie viel! Danke. Gute ___!",
            ["Husten", "gegen", "diesen", "Besserung"],
            "für",
            "dieser",
        ),
        mc(
            "Someone is ill. You say:",
            "Gute Besserung!",
            "Guten Appetit!",
            "Herzlichen Glückwunsch!",
        ),
        mc("You have a cut on your finger. You need a …", "Pflaster", "Tablette", "Kräutertee"),
        mc("Was hilft gegen Kopfschmerzen?", "eine Tablette", "ein Pflaster", "ein Handtuch"),
        order("Was hilft gegen Schnupfen?", "Build the question."),
        tr("I'm ill. I have a fever.", "Ich bin krank. Ich habe Fieber."),
    ),
    lesson(
        "Lektion 18: Test",
        mc("Meine Ohren ___ weh.", "tun", "tut"),
        fill("Du ___ keinen Kaffee trinken. (sollen)", "sollst"),
        mc(
            "Formal: take this medicine!",
            "Nehmen Sie dieses Medikament!",
            "Nimm dieses Medikament!",
            "Sie nehmen dieses Medikament.",
        ),
        mc("___ Salbe hilft.", "Diese", "Dieser", "Dieses"),
        order("Was hat er denn?", "Build the question."),
        tr("Get well soon!", "Gute Besserung!"),
        fill("Er ist nicht krank, er ist ___. (healthy)", "gesund"),
    ),
    lesson(
        "Modul 6: Wiederholung",
        mc("Der Techniker kommt ___ einer Stunde.", "in", "vor", "für"),
        fill("Ich bleibe für ___ Woche in Wien. (a)", "eine"),
        conj("wollen", "du", "willst"),
        conj("werden", "er", "wird"),
        mc("Ich fahre ___ dem Zug.", "mit", "ohne"),
        conj("sollen", "wir", "sollen"),
        mc("Formal: wait here!", "Warten Sie hier!", "Wartet hier!", "Sie warten hier!"),
        bank(
            "Ich ___ Ärztin werden. Aber jetzt bin ich krank: Mein Kopf ___ weh. "
            "Der Arzt sagt, ich ___ im Bett bleiben.",
            ["will", "tut", "soll"],
            "wird",
            "tun",
        ),
        tr("Can we postpone the appointment?", "Können wir den Termin verschieben?"),
        order("Nehmen Sie doch diesen Tee!"),
    ),
]

LEKTION_18 = unit(
    18,
    "Geben Sie ihm doch diesen Tee!",
    "Gesundheit und Ratschläge",
    L18_WORDS,
    L18_RULES,
    interleave(L18_LESSONS, vocab_lessons(L18_WORDS, "Wörter")),
)


UNITS = [LEKTION_16, LEKTION_17, LEKTION_18]
