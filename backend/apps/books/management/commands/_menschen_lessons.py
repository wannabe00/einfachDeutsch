"""Original A1 grammar notes and practice exercises, matched to each Menschen
lesson's topics and vocabulary. Written fresh (not copied from the textbook).

GRAMMAR[section] -> list of dicts: title, category, content (Markdown),
examples (one sentence per line).
EXERCISES[section] -> list of dicts: type, prompt, answer, hint, explanation.
"""

GRAMMAR = {
    1: [
        {
            "title": "Personal pronouns & the verb sein (to be)",
            "category": "verbs",
            "content": (
                "German subject pronouns and the present tense of **sein** (to be):\n\n"
                "| Pronoun | sein |\n|---|---|\n"
                "| ich (I) | bin |\n| du (you, informal) | bist |\n"
                "| er/sie/es (he/she/it) | ist |\n| wir (we) | sind |\n"
                "| ihr (you, plural) | seid |\n| sie/Sie (they/you formal) | sind |\n\n"
                "Use **Sie** (capitalised) for formal address, **du** with friends and family."
            ),
            "examples": "Ich bin Student.\nDu bist nett.\nSie ist Journalistin.\nWir sind aus Österreich.",
        },
        {
            "title": "W-questions (question words)",
            "category": "sentence_structure",
            "content": (
                "Open questions begin with a **W-word**, then the verb, then the subject:\n\n"
                "`W-Wort + Verb + Subjekt … ?`\n\n"
                "Common ones: **wer** (who), **was** (what), **wie** (how), "
                "**woher** (from where), **wo** (where)."
            ),
            "examples": "Wie heißt du?\nWoher kommst du?\nWer ist das?",
        },
    ],
    2: [
        {
            "title": "Present tense: regular verb endings",
            "category": "verbs",
            "content": (
                "Most German verbs take regular endings on the stem (infinitive minus **-en**). "
                "Stem of *machen* = *mach-*:\n\n"
                "| Pronoun | ending | machen |\n|---|---|---|\n"
                "| ich | -e | mache |\n| du | -st | machst |\n| er/sie/es | -t | macht |\n"
                "| wir | -en | machen |\n| ihr | -t | macht |\n| sie/Sie | -en | machen |"
            ),
            "examples": "Ich wohne in Berlin.\nDu arbeitest viel.\nEr lebt allein.",
        },
        {
            "title": "Jobs: no article with professions",
            "category": "articles",
            "content": (
                "When stating someone's profession after **sein**, German uses **no article**:\n\n"
                "`Subjekt + sein + Beruf`\n\n"
                "Many feminine job titles add **-in** to the masculine form "
                "(*der Lehrer → die Lehrerin*)."
            ),
            "examples": "Ich bin Arzt.\nSie ist Lehrerin.\nEr ist Student.",
        },
    ],
    3: [
        {
            "title": "Definite & indefinite articles (gender)",
            "category": "articles",
            "content": (
                "Every German noun has a gender. The article shows it:\n\n"
                "| Gender | definite | indefinite |\n|---|---|---|\n"
                "| masculine | **der** | ein |\n| feminine | **die** | eine |\n"
                "| neuter | **das** | ein |\n\n"
                "Always learn a noun **together with its article** — the gender is rarely predictable."
            ),
            "examples": "der Tisch – ein Tisch\ndie Lampe – eine Lampe\ndas Sofa – ein Sofa",
        },
        {
            "title": "Possessive articles: mein / dein",
            "category": "pronouns",
            "content": (
                "Possessive articles agree with the **owned noun's** gender:\n\n"
                "- masculine/neuter: **mein** (my), **dein** (your)\n"
                "- feminine/plural: **meine**, **deine**\n"
            ),
            "examples": "Das ist mein Vater.\nDas ist meine Mutter.\nDeine Eltern sind nett.",
        },
    ],
    5: [
        {
            "title": "Noun plurals",
            "category": "other",
            "content": (
                "German has several plural patterns — there is no single rule. The plural "
                "article is always **die**. Common endings: **-e**, **-en/-n**, **-er**, "
                "**-s**, or no ending (sometimes with an umlaut).\n\n"
                "Learn the plural with the noun."
            ),
            "examples": "der Tisch → die Tische\ndie Brille → die Brillen\ndas Glas → die Gläser\ndas Auto → die Autos",
        },
    ],
    6: [
        {
            "title": "Possessive articles for he/she & negation kein",
            "category": "pronouns",
            "content": (
                "**sein** = his, **ihr** = her (add **-e** for feminine/plural nouns).\n\n"
                "To negate a noun, use **kein/keine** (= not a / no):\n\n"
                "`Das ist kein Problem.`"
            ),
            "examples": "Das ist sein Büro.\nDas ist ihre Firma.\nIch habe kein Handy.",
        },
    ],
    7: [
        {
            "title": "The modal verb können",
            "category": "verbs",
            "content": (
                "Modal verbs change their stem vowel and put the **main verb (infinitive) "
                "at the end** of the sentence:\n\n"
                "`Subjekt + Modalverb + … + Infinitiv`\n\n"
                "| ich kann | du kannst | er/sie kann |\n|---|---|---|\n"
                "| wir können | ihr könnt | sie können |"
            ),
            "examples": "Ich kann gut kochen.\nKannst du schwimmen?\nWir können Fußball spielen.",
        },
        {
            "title": "Saying you like doing something: gern",
            "category": "sentence_structure",
            "content": (
                "Add **gern** after the verb to say you like doing the activity. "
                "**nicht gern** = don't like to."
            ),
            "examples": "Ich lese gern.\nEr tanzt nicht gern.\nWir spielen gern Fußball.",
        },
    ],
    8: [
        {
            "title": "Time prepositions: am / um / in",
            "category": "other",
            "content": (
                "- **am** + day or part of day: *am Montag*, *am Abend*\n"
                "- **um** + clock time: *um 8 Uhr*\n"
                "- **in der** Nacht (exception)\n\n"
                "Time-when expressions usually come right after the verb."
            ),
            "examples": "Am Samstag gehe ich ins Kino.\nDer Kurs beginnt um 9 Uhr.\nIn der Nacht schlafe ich.",
        },
    ],
    9: [
        {
            "title": "The accusative case (direct object)",
            "category": "cases",
            "content": (
                "The direct object takes the **accusative**. Only the **masculine** article "
                "changes — feminine, neuter and plural stay the same:\n\n"
                "| | Nominativ | Akkusativ |\n|---|---|---|\n"
                "| masc. | der/ein | **den/einen** |\n| fem. | die/eine | die/eine |\n"
                "| neut. | das/ein | das/ein |\n\n"
                "Verbs like *essen, trinken, haben, brauchen, kaufen* take the accusative."
            ),
            "examples": "Ich esse einen Apfel.\nIch trinke eine Limonade.\nSie kauft das Brot.",
        },
        {
            "title": "ich möchte (I would like)",
            "category": "verbs",
            "content": (
                "**möchte** is polite for ordering and wishes; the second verb (if any) goes "
                "to the end.\n\n"
                "| ich möchte | du möchtest | er/sie möchte |\n|---|---|---|\n"
                "| wir möchten | ihr möchtet | sie möchten |"
            ),
            "examples": "Ich möchte einen Kaffee, bitte.\nMöchtest du etwas essen?",
        },
    ],
    10: [
        {
            "title": "Separable verbs",
            "category": "verbs",
            "content": (
                "Many verbs have a **prefix that separates** and jumps to the end of the "
                "sentence in the present tense:\n\n"
                "`abfahren → Der Zug fährt um 8 Uhr ab.`\n\n"
                "Common prefixes: *ab-, an-, auf-, aus-, ein-, mit-, um-*."
            ),
            "examples": "Ich kaufe im Supermarkt ein.\nWann fährt der Bus ab?\nSie steigt in Köln um.",
        },
    ],
    11: [
        {
            "title": "The Perfekt (past tense) with haben",
            "category": "verbs",
            "content": (
                "Spoken German uses the **Perfekt** for the past:\n\n"
                "`haben (conjugated) + … + Partizip II (at the end)`\n\n"
                "Regular participle: **ge- + stem + -t** (*machen → gemacht*). "
                "Many verbs are irregular and must be learned (*lesen → gelesen*)."
            ),
            "examples": "Ich habe Deutsch gelernt.\nWir haben einen Film gesehen.\nHast du das gemacht?",
        },
    ],
    12: [
        {
            "title": "The Perfekt with sein (movement & change)",
            "category": "verbs",
            "content": (
                "Verbs of **movement** or **change of state** form the Perfekt with **sein**, "
                "not haben:\n\n"
                "`sein (conjugated) + … + Partizip II`\n\n"
                "Examples: *gehen → gegangen*, *fahren → gefahren*, *fliegen → geflogen*, "
                "*kommen → gekommen*."
            ),
            "examples": "Ich bin nach Berlin gefahren.\nSie ist nach Hause gegangen.\nWir sind geflogen.",
        },
    ],
    13: [
        {
            "title": "Asking for & giving directions (imperative)",
            "category": "sentence_structure",
            "content": (
                "The **Sie-imperative** keeps the pronoun and puts the verb first:\n\n"
                "`Gehen Sie geradeaus.` / `Biegen Sie links ab.`\n\n"
                "Useful: *geradeaus* (straight on), *links/rechts* (left/right), "
                "*die erste Straße* (the first street)."
            ),
            "examples": "Gehen Sie geradeaus.\nBiegen Sie rechts ab.\nNehmen Sie die erste Straße links.",
        },
    ],
    14: [
        {
            "title": "Two-way prepositions (Wechselpräpositionen)",
            "category": "cases",
            "content": (
                "These prepositions take the **dative** for *location* (where? — no movement) "
                "and the **accusative** for *direction* (where to? — movement):\n\n"
                "**in, auf, an, über, unter, vor, hinter, neben, zwischen**\n\n"
                "*Location:* Das Auto steht **in der** Tiefgarage. (dative)\n"
                "*Direction:* Ich fahre **in die** Tiefgarage. (accusative)"
            ),
            "examples": "Das Bild hängt an der Wand.\nDie Lampe steht neben dem Sofa.\nDer Schlüssel ist auf dem Tisch.",
        },
    ],
}

EXERCISES = {
    1: [
        {
            "type": "translation",
            "prompt": 'Translate to German: "Good morning"',
            "answer": "Guten Morgen",
            "hint": "A standard greeting.",
            "explanation": "",
        },
        {
            "type": "fill_blank",
            "prompt": "Complete: Ich ___ aus Österreich. (sein)",
            "answer": "bin",
            "hint": "ich form of sein",
            "explanation": "ich → bin.",
        },
        {
            "type": "fill_blank",
            "prompt": "Complete the question: ___ kommst du? (from where)",
            "answer": "Woher",
            "hint": "One W-word.",
            "explanation": "Woher = from where.",
        },
    ],
    2: [
        {
            "type": "conjugation",
            "prompt": "Conjugate 'wohnen' for 'du': du ___",
            "answer": "wohnst",
            "hint": "stem + -st",
            "explanation": "du → stem + -st.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "She is a teacher."',
            "answer": "Sie ist Lehrerin",
            "hint": "No article before the job.",
            "explanation": "No article with professions; feminine adds -in.",
        },
        {
            "type": "fill_blank",
            "prompt": "Complete: Wir ___ in Hamburg. (wohnen)",
            "answer": "wohnen",
            "hint": "wir form",
            "explanation": "wir → -en.",
        },
    ],
    3: [
        {
            "type": "article",
            "prompt": "Choose the article: ___ Sofa",
            "answer": "das",
            "hint": "neuter",
            "explanation": "Sofa is neuter → das.",
        },
        {
            "type": "article",
            "prompt": "Choose the article: ___ Lampe",
            "answer": "die",
            "hint": "feminine",
            "explanation": "Lampe is feminine → die.",
        },
        {
            "type": "article",
            "prompt": "Choose the article: ___ Tisch",
            "answer": "der",
            "hint": "masculine",
            "explanation": "Tisch is masculine → der.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "That is my mother."',
            "answer": "Das ist meine Mutter",
            "hint": "Mutter is feminine → meine.",
            "explanation": "Feminine noun takes meine.",
        },
    ],
    5: [
        {
            "type": "fill_blank",
            "prompt": "Give the plural: das Glas → die ___",
            "answer": "Gläser",
            "hint": "umlaut + -er",
            "explanation": "Glas → Gläser.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "the umbrella"',
            "answer": "der Regenschirm",
            "hint": "masculine",
            "explanation": "",
        },
        {
            "type": "translation",
            "prompt": 'Translate the colour: "green"',
            "answer": "grün",
            "hint": "",
            "explanation": "",
        },
    ],
    6: [
        {
            "type": "translation",
            "prompt": 'Translate: "the appointment"',
            "answer": "der Termin",
            "hint": "masculine",
            "explanation": "",
        },
        {
            "type": "fill_blank",
            "prompt": "Negate: Ich habe ___ Handy. (no)",
            "answer": "kein",
            "hint": "kein/keine",
            "explanation": "Handy is neuter → kein.",
        },
    ],
    7: [
        {
            "type": "conjugation",
            "prompt": "Conjugate 'können' for 'ich': ich ___",
            "answer": "kann",
            "hint": "modal vowel change",
            "explanation": "ich kann.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "I like reading."',
            "answer": "Ich lese gern",
            "hint": "Use gern.",
            "explanation": "verb + gern.",
        },
        {
            "type": "fill_blank",
            "prompt": "Word order: Ich ___ gut schwimmen. (können)",
            "answer": "kann",
            "hint": "modal in position 2, infinitive at end",
            "explanation": "Ich kann gut schwimmen.",
        },
    ],
    8: [
        {
            "type": "fill_blank",
            "prompt": "Complete: ___ Samstag gehe ich ins Kino. (on)",
            "answer": "Am",
            "hint": "am + day",
            "explanation": "am + day of week.",
        },
        {
            "type": "fill_blank",
            "prompt": "Complete: Der Film beginnt ___ 20 Uhr. (at)",
            "answer": "um",
            "hint": "um + clock time",
            "explanation": "um + time.",
        },
    ],
    9: [
        {
            "type": "fill_blank",
            "prompt": "Accusative: Ich esse ___ Apfel. (ein, masc.)",
            "answer": "einen",
            "hint": "masculine accusative",
            "explanation": "ein → einen (masc. acc.).",
        },
        {
            "type": "fill_blank",
            "prompt": "Accusative: Ich trinke ___ Milch. (die)",
            "answer": "die",
            "hint": "feminine unchanged",
            "explanation": "Feminine stays die.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "I would like a coffee."',
            "answer": "Ich möchte einen Kaffee",
            "hint": "möchte + accusative",
            "explanation": "Kaffee is masculine → einen.",
        },
    ],
    10: [
        {
            "type": "fill_blank",
            "prompt": "Separable verb: Der Zug ___ um 8 Uhr ___. (abfahren)",
            "answer": "fährt … ab",
            "hint": "prefix goes to the end",
            "explanation": "fährt ... ab — prefix separates.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "I go shopping." (einkaufen)',
            "answer": "Ich kaufe ein",
            "hint": "separable verb",
            "explanation": "kaufe ... ein.",
        },
    ],
    11: [
        {
            "type": "fill_blank",
            "prompt": "Perfekt: Ich habe Deutsch ___. (lernen)",
            "answer": "gelernt",
            "hint": "ge- + stem + -t",
            "explanation": "Regular: gelernt.",
        },
        {
            "type": "translation",
            "prompt": 'Translate (Perfekt): "We watched a film."',
            "answer": "Wir haben einen Film gesehen",
            "hint": "haben + Partizip II",
            "explanation": "sehen → gesehen, at the end.",
        },
    ],
    12: [
        {
            "type": "fill_blank",
            "prompt": "Perfekt with sein: Ich ___ nach Berlin gefahren.",
            "answer": "bin",
            "hint": "movement → sein",
            "explanation": "fahren uses sein.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "the wedding"',
            "answer": "die Hochzeit",
            "hint": "feminine",
            "explanation": "",
        },
    ],
    13: [
        {
            "type": "translation",
            "prompt": 'Translate: "Turn right." (Sie-form)',
            "answer": "Biegen Sie rechts ab",
            "hint": "imperative, separable verb",
            "explanation": "abbiegen → Biegen Sie ... ab.",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "the bridge"',
            "answer": "die Brücke",
            "hint": "feminine",
            "explanation": "",
        },
    ],
    14: [
        {
            "type": "fill_blank",
            "prompt": "Location (dative): Der Schlüssel ist auf ___ Tisch. (der)",
            "answer": "dem",
            "hint": "auf + dative for location",
            "explanation": "der → dem (dative masc.).",
        },
        {
            "type": "translation",
            "prompt": 'Translate: "the lift / elevator"',
            "answer": "der Aufzug",
            "hint": "masculine",
            "explanation": "",
        },
    ],
}
