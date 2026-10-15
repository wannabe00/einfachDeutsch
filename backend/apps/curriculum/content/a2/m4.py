"""Modul 4 (A2.1): Lektion 10 (Gut, dass du reserviert hast.), 11 (Ich freue
mich so.), 12 (Wenn es warm ist, essen wir meist Salat.)."""

from ..dsl import (
    bank,
    fill,
    grammar,
    lesson,
    match,
    mc,
    order,
    review,
    rule,
    sections,
    tr,
    unit,
    vocab_lessons,
)

# ============================================================================
# Lektion 10: Gut, dass du reserviert hast.
# ============================================================================

L10_WORDS = [
    ("the reservation", "die Reservierung", "noun", "Pl. die Reservierungen"),
    ("the main course", "die Hauptspeise", "noun", "Pl. die Hauptspeisen"),
    ("the dessert", "die Nachspeise", "noun", "Pl. die Nachspeisen"),
    ("the side dish", "die Beilage", "noun", "Pl. die Beilagen"),
    ("the sauce", "die Soße", "noun", "Pl. die Soßen"),
    ("the dish (meal)", "das Gericht", "noun", "Pl. die Gerichte"),
    ("the tip", "das Trinkgeld", "noun"),
    ("the cook", "der Koch", "noun", "f. die Köchin"),
    ("the service (waiting staff)", "die Bedienung", "noun"),
    ("the plate", "der Teller", "noun", "Pl. die Teller"),
    ("the fork", "die Gabel", "noun", "Pl. die Gabeln"),
    ("the spoon", "der Löffel", "noun", "Pl. die Löffel"),
    ("the napkin", "die Serviette", "noun", "Pl. die Servietten"),
    ("the carbonation", "die Kohlensäure", "noun", "mit / ohne Kohlensäure"),
    ("the chips / fries", "die Pommes", "noun", "plural"),
    ("to reserve", "reservieren", "verb", "hat reserviert"),
    ("to serve (guests)", "bedienen", "verb", "hat bedient"),
    ("vegetarian", "vegetarisch", "adjective"),
    ("salty", "salzig", "adjective"),
    ("delicious", "lecker", "adjective"),
    ("still (water)", "still", "adjective"),
    ("full (not hungry)", "satt", "adjective"),
    ("separately", "getrennt", "adjective", "getrennt zahlen"),
    ("Good that you booked.", "Gut, dass du reserviert hast.", "phrase"),
    ("The bill, please!", "Zahlen, bitte!", "phrase"),
    ("Keep the change.", "Stimmt so.", "phrase"),
    ("Enjoy your meal!", "Lass es dir schmecken!", "phrase"),
]

L10_RULES = [
    rule(
        "Gut, dass ...: dass-Sätze",
        "sentence_structure",
        """
After expressions like *Gut, dass ... · Schade, dass ... · Ich finde, dass ...*
comes a **dass**-clause with the verb at the end.

In the **Perfekt**, the helping verb *haben / sein* is the very last word:

- *Gut, dass du einen Tisch reserviert **hast**.*
- *Schade, dass das Restaurant schon geschlossen **ist**.*
- *Ich finde, dass die Soße zu salzig **ist**.*
- *Toll, dass ihr gekommen **seid**!*
""",
        [
            "Gut, dass du reserviert hast.",
            "Schade, dass der Koch krank ist.",
            "Ich finde, dass das Essen hier sehr lecker ist.",
        ],
    ),
    rule(
        "weil: Gründe nennen",
        "sentence_structure",
        """
**weil** (because) also sends the verb **to the end**:

- *Ich nehme die Suppe, **weil** ich keinen Hunger **habe**.*
- *Wir kommen später, **weil** der Bus nicht gekommen **ist**.*

Compare with **denn**, which keeps the normal word order:
*Ich nehme die Suppe, **denn** ich **habe** keinen Hunger.*

Question and answer: ***Warum** gehst du nicht mit? · **Weil** ich müde bin.*
""",
        [
            "Ich bestelle den Salat, weil ich vegetarisch esse.",
            "Wir zahlen getrennt, weil jeder etwas anderes gegessen hat.",
            "Warum gibst du kein Trinkgeld? Weil die Bedienung unfreundlich war.",
        ],
    ),
]

L10_LESSONS = [
    lesson(
        "Im Restaurant",
        review("das Gericht"),
        review("die Beilage"),
        match(
            [
                ("die Gabel", "the fork"),
                ("der Löffel", "the spoon"),
                ("der Teller", "the plate"),
                ("die Serviette", "the napkin"),
                ("die Nachspeise", "the dessert"),
            ]
        ),
        mc(
            "Ein Gericht ohne Fleisch und Fisch ist ...",
            "vegetarisch.",
            "salzig.",
            "getrennt.",
        ),
        mc(
            "Mineralwasser ohne Kohlensäure heißt ...",
            "stilles Wasser.",
            "salziges Wasser.",
            "leckeres Wasser.",
        ),
        mc(
            "Stimmt so. means:",
            "Keep the change.",
            "That's wrong.",
            "That's right, I agree.",
        ),
        fill("Ich bin ___, ich kann nichts mehr essen. (full)", "satt"),
        tr("The sauce is too salty.", "Die Soße ist zu salzig."),
    ),
    lesson(
        "Gut, dass ...",
        grammar("Gut, dass ...: dass-Sätze"),
        mc(
            "Which sentence is correct?",
            "Gut, dass du reserviert hast.",
            "Gut, dass du hast reserviert.",
            "Gut, dass hast du reserviert.",
        ),
        fill("Schade, dass das Restaurant geschlossen ___. (sein)", "ist"),
        fill("Toll, dass ihr gekommen ___! (sein)", "seid"),
        fill("Gut, dass du einen Tisch reserviert ___. (haben)", "hast"),
        fill("Ich finde, dass die Pommes sehr lecker ___. (sein)", "sind"),
        order("Ich finde, dass das Essen hier sehr gut ist."),
        tr("It's a pity that the cook is ill.", "Schade, dass der Koch krank ist."),
    ),
    lesson(
        "Weil ...",
        grammar("weil: Gründe nennen"),
        mc(
            "Ich nehme den Salat, weil ich keinen Hunger ___.",
            "habe",
            "hat",
            "hatte habe",
        ),
        mc(
            "Which sentence is correct?",
            "Wir zahlen getrennt, weil jeder etwas anderes gegessen hat.",
            "Wir zahlen getrennt, weil jeder hat etwas anderes gegessen.",
            "Wir zahlen getrennt, weil hat jeder etwas anderes gegessen.",
        ),
        mc(
            "Same meaning: Ich bleibe zu Hause, denn ich bin müde.",
            "Ich bleibe zu Hause, weil ich müde bin.",
            "Ich bleibe zu Hause, weil bin ich müde.",
            "Ich bleibe zu Hause, dass ich müde bin.",
        ),
        fill("Warum gehst du nicht mit? ___ ich keine Zeit habe.", "Weil"),
        fill("Ich bestelle Wasser, weil ich Auto fahren ___. (müssen)", "muss"),
        order("Wir kommen später, weil der Bus nicht gekommen ist."),
        tr(
            "I'm ordering the soup because I'm not hungry.",
            "Ich bestelle die Suppe, weil ich keinen Hunger habe.",
        ),
    ),
    lesson(
        "Einen Tisch reservieren",
        bank(
            "Restaurant Linde, guten Abend! Guten Abend, ich möchte einen Tisch für vier "
            "Personen ___. Für wann? Für Samstag um 19 Uhr. Gern. Auf welchen Namen? "
            "Auf Müller. Und haben Sie auch ___ Gerichte? Ja, wir haben drei ohne Fleisch. "
            "Gut, dass ich ___ habe!",
            ["reservieren", "vegetarische", "gefragt"],
            "bestellen",
            "salzige",
        ),
        mc(
            "How many people is the table for?",
            "Four.",
            "Three.",
            "Nineteen.",
        ),
        mc(
            "Zahlen Sie zusammen oder getrennt? The waiter asks ...",
            "if you pay together or separately.",
            "if you want a dessert.",
            "if you have a reservation.",
        ),
        fill("Die ___ war sehr freundlich. (service staff)", "Bedienung"),
        fill("Der Kellner hat uns schnell ___. (bedienen)", "bedient"),
        order("Ich habe einen Tisch für zwei Personen reserviert."),
        tr("The bill, please!", "Zahlen, bitte!|Die Rechnung, bitte!"),
    ),
    lesson(
        "Was empfehlen Sie?",
        mc(
            "Als Hauptspeise nehme ich das Steak, und als ___ die Pommes.",
            "Beilage",
            "Nachspeise",
            "Vorspeise",
        ),
        mc(
            "Der Gast ist zufrieden. Er gibt viel ...",
            "Trinkgeld.",
            "Kohlensäure.",
            "Soße.",
        ),
        fill("Lass es dir ___! (enjoy: schmecken)", "schmecken"),
        fill("Der ___ kocht heute Fisch. (cook)", "Koch"),
        tr("We'd like to pay separately.", "Wir möchten getrennt zahlen.|Wir zahlen getrennt."),
        tr("The dessert was delicious.", "Die Nachspeise war lecker."),
    ),
    lesson(
        "Lektion 10: Test",
        fill("Gut, dass du reserviert ___.", "hast"),
        mc("Ich trinke Wasser, weil ich Durst ___.", "habe", "hat"),
        fill("Schade, dass du nicht mitkommen ___. (können)", "kannst"),
        mc("Was ist süß?", "die Nachspeise", "die Beilage", "die Soße"),
        fill("Möchten Sie das Wasser still oder mit ___?", "Kohlensäure"),
        order("Ich nehme die Suppe, weil ich wenig Hunger habe."),
        tr("Good that you booked.", "Gut, dass du reserviert hast."),
    ),
]

LEKTION_10 = unit(
    10,
    "Gut, dass du reserviert hast.",
    "Im Restaurant",
    L10_WORDS,
    L10_RULES,
    sections(L10_LESSONS, vocab_lessons(L10_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 11: Ich freue mich so.
# ============================================================================

L11_WORDS = [
    ("the message / news", "die Nachricht", "noun", "Pl. die Nachrichten"),
    ("the surprise", "die Überraschung", "noun", "Pl. die Überraschungen"),
    ("the joy", "die Freude", "noun"),
    ("the birth", "die Geburt", "noun", "Pl. die Geburten"),
    ("the engagement", "die Verlobung", "noun", "Pl. die Verlobungen"),
    ("the separation", "die Trennung", "noun", "Pl. die Trennungen"),
    ("the divorce", "die Scheidung", "noun", "Pl. die Scheidungen"),
    ("the relationship", "die Beziehung", "noun", "Pl. die Beziehungen"),
    ("the reunion", "das Wiedersehen", "noun"),
    ("the brother-in-law", "der Schwager", "noun", "Pl. die Schwäger"),
    ("the sister-in-law", "die Schwägerin", "noun", "Pl. die Schwägerinnen"),
    ("to be pleased / to look forward", "sich freuen", "verb", "auf / über + Akk."),
    ("to feel", "fühlen", "verb", "sich fühlen"),
    ("to be interested", "interessieren", "verb", "sich interessieren für"),
    ("to fall in love", "verlieben", "verb", "sich verlieben in + Akk."),
    ("to separate / to split up", "trennen", "verb", "sich trennen"),
    ("surprised", "überrascht", "adjective"),
    ("nervous", "nervös", "adjective"),
    ("proud", "stolz", "adjective", "stolz auf + Akk."),
    ("curious", "neugierig", "adjective", "neugierig auf + Akk."),
    ("excited (to see what happens)", "gespannt", "adjective", "Ich bin gespannt, ob ..."),
    ("engaged", "verlobt", "adjective"),
    ("warm / heartfelt", "herzlich", "adjective"),
    ("I'm so happy.", "Ich freue mich so.", "phrase"),
    ("I'm happy for you.", "Ich freue mich für dich.", "phrase"),
    ("Congratulations on the wedding!", "Herzlichen Glückwunsch zur Hochzeit!", "phrase"),
]

L11_RULES = [
    rule(
        "Reflexive Verben: sich freuen, sich treffen",
        "pronouns",
        """
Reflexive verbs need a pronoun that refers back to the subject:

| ich | du | er / sie / es | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| freue **mich** | freust **dich** | freut **sich** | freuen **uns** | freut **euch** | freuen **sich** |

Common ones: *sich freuen, sich treffen, sich fühlen, sich verlieben, sich
interessieren, sich trennen, sich ausruhen*.

The pronoun comes right after the verb, or after the subject when the verb is
first: *Wir treffen **uns** um acht. · Freust du **dich**?*
""",
        [
            "Ich fühle mich heute sehr gut.",
            "Wir treffen uns am Sonntag bei meiner Schwester.",
            "Mein Bruder hat sich in eine Spanierin verliebt.",
        ],
    ),
    rule(
        "sich freuen auf / über",
        "verbs",
        """
Both take the **Akkusativ**, but they mean different things:

| sich freuen **auf** | sich freuen **über** |
|---|---|
| something that is **coming** | something that **is here / has happened** |
| *Ich freue mich **auf** den Urlaub.* | *Ich freue mich **über** deine Nachricht.* |
| *Wir freuen uns **aufs** Wiedersehen.* | *Sie freut sich **über** das Geschenk.* |

And: *Ich freue mich **für** dich.* (I'm happy **for** you.)
Similar: *stolz **auf** ... · neugierig **auf** ...*
""",
        [
            "Ich freue mich so über die Geburt von eurem Baby!",
            "Wir freuen uns schon auf die Hochzeit.",
            "Meine Eltern sind sehr stolz auf mich.",
        ],
    ),
    rule(
        "Indirekte Fragen mit ob",
        "sentence_structure",
        """
A **yes/no question** inside another sentence starts with **ob** (whether). The
verb goes **to the end**:

| Direct question | Indirect question |
|---|---|
| *Kommt Anna auch?* | *Weißt du, **ob** Anna auch **kommt**?* |
| *Ist sie schon angekommen?* | *Ich bin gespannt, **ob** sie schon angekommen **ist**.* |

Typical starts: *Weißt du, ob ...? · Ich weiß nicht, ob ... · Ich frage mich, ob ...*
""",
        [
            "Weißt du, ob Paul seine Freundin heiratet?",
            "Ich weiß nicht, ob sie sich getrennt haben.",
            "Ich bin gespannt, ob es ein Junge oder ein Mädchen ist.",
        ],
    ),
]

L11_LESSONS = [
    lesson(
        "Gute Nachrichten",
        review("die Nachricht"),
        review("die Überraschung"),
        match(
            [
                ("die Geburt", "a baby is born"),
                ("die Verlobung", "a couple plans to marry"),
                ("die Hochzeit", "a couple marries"),
                ("die Trennung", "a couple splits up"),
                ("das Wiedersehen", "you meet again"),
            ],
            "What happens?",
        ),
        mc(
            "Mein Sohn hat die Prüfung bestanden. Ich bin sehr ...",
            "stolz.",
            "nervös.",
            "verlobt.",
        ),
        mc(
            "Der Mann von meiner Schwester ist mein ...",
            "Schwager.",
            "Schwiegervater.",
            "Cousin.",
        ),
        fill("Morgen ist meine Prüfung, ich bin so ___. (nervous)", "nervös"),
        tr("I'm happy for you.", "Ich freue mich für dich."),
    ),
    lesson(
        "Ich freue mich",
        grammar("Reflexive Verben: sich freuen, sich treffen"),
        fill("Ich freue ___ so!", "mich"),
        fill("Freust du ___ auch?", "dich"),
        fill("Wir treffen ___ um acht Uhr.", "uns"),
        fill("Habt ihr ___ verliebt?", "euch"),
        fill("Sie fühlt ___ heute nicht gut.", "sich"),
        mc("Er interessiert ___ für Musik.", "sich", "ihn", "ihm"),
        order("Wir treffen uns am Sonntag bei meinen Eltern."),
        tr("I feel very good today.", "Ich fühle mich heute sehr gut."),
    ),
    lesson(
        "Freuen auf oder über?",
        grammar("sich freuen auf / über"),
        mc("Ich freue mich ___ den Urlaub nächste Woche.", "auf", "über"),
        mc("Sie freut sich ___ das Geschenk.", "über", "auf"),
        mc("Wir freuen uns ___ das Wiedersehen im Mai.", "auf", "über"),
        mc("Ich freue mich ___ deine Nachricht von gestern.", "über", "auf"),
        fill("Meine Eltern sind stolz ___ mich.", "auf"),
        fill("Ich freue mich ___ dich. (for)", "für"),
        fill("Ich bin neugierig ___ das Baby.", "auf"),
        tr("We're looking forward to the wedding.", "Wir freuen uns auf die Hochzeit."),
    ),
    lesson(
        "Weißt du, ob ...?",
        grammar("Indirekte Fragen mit ob"),
        mc(
            "Kommt Anna auch? → Weißt du, ...",
            "ob Anna auch kommt?",
            "ob kommt Anna auch?",
            "dass Anna auch kommt?",
        ),
        mc(
            "Which sentence is correct?",
            "Ich weiß nicht, ob sie sich getrennt haben.",
            "Ich weiß nicht, ob sie haben sich getrennt.",
            "Ich weiß nicht, ob haben sie sich getrennt.",
        ),
        fill("Ich bin gespannt, ___ es ein Junge oder ein Mädchen ist.", "ob"),
        fill("Weißt du, ob Paul heute ___? (kommen)", "kommt"),
        fill("Ich frage mich, ob sie schon angekommen ___. (sein)", "ist"),
        order("Weißt du, ob sie verlobt sind?", "Build the question."),
        tr("I don't know if he is at home.", "Ich weiß nicht, ob er zu Hause ist."),
    ),
    lesson(
        "Eine Karte",
        bank(
            "Liebe Maria, lieber Stefan, wir haben uns so über eure ___ gefreut! Herzlichen "
            "Glückwunsch zur ___! Wir sind schon sehr ___ auf das Fest. Weißt du, ___ deine "
            "Schwester auch kommt? Wir freuen uns auf das ___! Herzliche Grüße, Eva und Tim",
            ["Nachricht", "Verlobung", "gespannt", "ob", "Wiedersehen"],
            "dass",
            "Scheidung",
        ),
        mc(
            "Why do Eva and Tim write?",
            "Maria and Stefan got engaged.",
            "Maria and Stefan split up.",
            "Maria had a baby.",
        ),
        mc(
            "Ich bin gespannt, ob ... means:",
            "I can't wait to see if ...",
            "I'm tired because ...",
            "I'm angry that ...",
        ),
        fill("Wo habt ihr euch ___? (kennenlernen)", "kennengelernt"),
        tr(
            "Congratulations on the wedding!",
            "Herzlichen Glückwunsch zur Hochzeit!",
        ),
    ),
    lesson(
        "Lektion 11: Test",
        fill("Wir freuen ___ sehr.", "uns"),
        mc("Ich freue mich ___ das Wochenende.", "auf", "über"),
        mc("Er freut sich ___ den Brief, den er heute bekommen hat.", "über", "auf"),
        fill("Weißt du, ___ sie verheiratet ist?", "ob"),
        fill("Sie haben sich ___. (trennen)", "getrennt"),
        order("Ich freue mich so über deine Nachricht."),
        tr("I'm so happy.", "Ich freue mich so."),
    ),
]

LEKTION_11 = unit(
    11,
    "Ich freue mich so.",
    "Familiennachrichten und Gefühle",
    L11_WORDS,
    L11_RULES,
    sections(L11_LESSONS, vocab_lessons(L11_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 12: Wenn es warm ist, essen wir meist Salat.
# ============================================================================

L12_WORDS = [
    ("the nutrition / diet", "die Ernährung", "noun"),
    ("the meal", "die Mahlzeit", "noun", "Pl. die Mahlzeiten"),
    ("the ingredient", "die Zutat", "noun", "Pl. die Zutaten"),
    ("the spice", "das Gewürz", "noun", "Pl. die Gewürze"),
    ("the vitamin", "das Vitamin", "noun", "Pl. die Vitamine"),
    ("the pasta / noodles", "die Nudeln", "noun", "plural"),
    ("the muesli", "das Müsli", "noun"),
    ("the yoghurt", "der Joghurt", "noun", "also: das Joghurt"),
    ("the oil", "das Öl", "noun"),
    ("the salt", "das Salz", "noun"),
    ("the pepper", "der Pfeffer", "noun"),
    ("the sugar", "der Zucker", "noun"),
    ("the pan", "die Pfanne", "noun", "Pl. die Pfannen"),
    ("the pot", "der Topf", "noun", "Pl. die Töpfe"),
    ("the knife", "das Messer", "noun", "Pl. die Messer"),
    ("the chopping board", "das Schneidebrett", "noun", "Pl. die Schneidebretter"),
    ("the diet (to lose weight)", "die Diät", "noun", "eine Diät machen"),
    ("to cut", "schneiden", "verb", "hat geschnitten"),
    ("to mix", "mischen", "verb", "hat gemischt"),
    ("to stir", "rühren", "verb", "hat gerührt"),
    ("to add", "hinzufügen", "verb", "hat hinzugefügt"),
    ("to season", "würzen", "verb", "hat gewürzt"),
    ("to peel", "schälen", "verb", "hat geschält"),
    ("to fry", "braten", "verb", "brät, hat gebraten"),
    ("to lose weight", "abnehmen", "verb", "hat abgenommen"),
    ("to gain weight", "zunehmen", "verb", "hat zugenommen"),
    ("unhealthy", "ungesund", "adjective"),
    ("regional / local", "regional", "adjective"),
    ("vegan", "vegan", "adjective"),
    ("mostly / usually", "meistens", "adverb", "also: meist"),
    ("rarely", "selten", "adverb"),
    ("normally", "normalerweise", "adverb"),
    ("When it's warm, we mostly eat salad.", "Wenn es warm ist, essen wir meist Salat.", "phrase"),
]

L12_RULES = [
    rule(
        "wenn: Bedingungen und Gewohnheiten",
        "sentence_structure",
        """
**wenn** (if / whenever) starts a subordinate clause with the verb **at the end**.

If the *wenn*-clause comes **first**, the main clause starts with its **verb**:

| wenn-clause | main clause |
|---|---|
| ***Wenn** es warm **ist**,* | ***essen** wir meist Salat.* |
| ***Wenn** ich Zeit **habe**,* | ***koche** ich selbst.* |

Or the other way round: *Wir essen meist Salat, **wenn** es warm **ist**.*

Don't mix up: **wenn** (whenever / if) · **als** (one time in the past) ·
**wann** (question: when?).
""",
        [
            "Wenn ich Hunger habe, esse ich ein Müsli.",
            "Wenn wir Gäste haben, kochen wir regional.",
            "Ich trinke viel Wasser, wenn es heiß ist.",
        ],
    ),
    rule(
        "Rezepte: Imperativ und Reihenfolge",
        "verbs",
        """
Recipes give instructions with the **imperative** (or the infinitive):

| du | ihr | Sie |
|---|---|---|
| Schneid(e) die Zwiebel! | Schneidet die Zwiebel! | Schneiden Sie die Zwiebel! |
| Gib Salz dazu! | Gebt Salz dazu! | Geben Sie Salz dazu! |

Order the steps with: ***zuerst** (first), **dann**, **danach** (after that),
**anschließend** (then), **zum Schluss** (finally)*. After these words the verb
comes next: ***Danach brätst** du das Gemüse.*

How often: *immer, **meistens**, oft, manchmal, **selten**, nie*.
""",
        [
            "Zuerst schälst du die Kartoffeln.",
            "Dann schneiden Sie das Gemüse.",
            "Zum Schluss würzt ihr alles mit Salz und Pfeffer.",
        ],
    ),
]

L12_LESSONS = [
    lesson(
        "Gesund essen",
        review("die Ernährung"),
        review("die Zutat"),
        match(
            [
                ("die Pfanne", "the pan"),
                ("der Topf", "the pot"),
                ("das Messer", "the knife"),
                ("das Gewürz", "the spice"),
                ("die Mahlzeit", "the meal"),
            ]
        ),
        mc(
            "Obst und Gemüse haben viele ...",
            "Vitamine.",
            "Gewürze.",
            "Töpfe.",
        ),
        mc(
            "Sie isst kein Fleisch, keine Milch und keine Eier. Sie ist ...",
            "vegan.",
            "regional.",
            "ungesund.",
        ),
        fill("Pommes und Cola sind ___. (unhealthy)", "ungesund"),
        fill("Ich mache eine Diät, ich will ___. (lose weight)", "abnehmen"),
        tr("Breakfast is the most important meal.", "Das Frühstück ist die wichtigste Mahlzeit."),
    ),
    lesson(
        "Wenn es warm ist, ...",
        grammar("wenn: Bedingungen und Gewohnheiten"),
        mc(
            "Which sentence is correct?",
            "Wenn es warm ist, essen wir Salat.",
            "Wenn es warm ist, wir essen Salat.",
            "Wenn ist es warm, essen wir Salat.",
        ),
        fill("Wenn ich Zeit ___, koche ich selbst. (haben)", "habe"),
        fill("Wenn es kalt ist, ___ ich Suppe. (essen)", "esse"),
        fill("Ich trinke viel Wasser, wenn es heiß ___. (sein)", "ist"),
        mc("___ ich Hunger habe, esse ich ein Brötchen.", "Wenn", "Als", "Wann"),
        mc("___ ich klein war, habe ich nie Gemüse gegessen.", "Als", "Wenn", "Wann"),
        order("Wenn wir Gäste haben, kochen wir immer regional."),
        tr(
            "When it's warm, we mostly eat salad.",
            "Wenn es warm ist, essen wir meist Salat.|Wenn es warm ist, essen wir meistens Salat.",
        ),
    ),
    lesson(
        "Ein Rezept",
        grammar("Rezepte: Imperativ und Reihenfolge"),
        fill("Zuerst ___ du die Kartoffeln. (schälen)", "schälst"),
        fill("___ Sie die Zwiebel. (schneiden)", "Schneiden"),
        fill("___ alles gut! (rühren, ihr)", "Rührt"),
        fill("Zum ___ würzt du alles mit Salz. (finally)", "Schluss"),
        mc(
            "Which word starts a recipe?",
            "Zuerst",
            "Zum Schluss",
            "Danach",
        ),
        mc(
            "Danach ___ du das Gemüse in der Pfanne.",
            "brätst",
            "bratest",
            "braten",
        ),
        order("Dann geben Sie etwas Öl in die Pfanne."),
        tr(
            "First cut the onions. (du)",
            "Schneid zuerst die Zwiebeln.|Schneide zuerst die Zwiebeln.|Zuerst schneidest du die Zwiebeln.",
        ),
    ),
    lesson(
        "Kartoffelsuppe",
        bank(
            "Zuerst ___ Sie die Kartoffeln und schneiden sie klein. Dann geben Sie die "
            "Kartoffeln in einen ___ mit Wasser. ___ kochen Sie alles 20 Minuten. "
            "Anschließend ___ Sie Salz und Pfeffer hinzu. Zum ___ rühren Sie die Suppe gut.",
            ["schälen", "Topf", "Danach", "fügen", "Schluss"],
            "Pfanne",
            "Zuerst",
        ),
        mc(
            "How long does the soup cook?",
            "20 minutes.",
            "Two hours.",
            "Five minutes.",
        ),
        mc(
            "anschließend means:",
            "afterwards / then",
            "at the beginning",
            "never",
        ),
        fill("Bitte ___ die Suppe mit Pfeffer. (würzen, du)", "würz|würze"),
        fill("Ich habe das Fleisch in der Pfanne ___. (braten)", "gebraten"),
        tr("Mix the ingredients. (Sie)", "Mischen Sie die Zutaten."),
    ),
    lesson(
        "Essgewohnheiten",
        mc(
            "Ich esse ___ Fleisch, nur einmal im Monat.",
            "selten",
            "meistens",
            "immer",
        ),
        mc(
            "___ esse ich zum Frühstück Müsli mit Joghurt.",
            "Normalerweise",
            "Zum Schluss",
            "Anschließend",
        ),
        fill("Im Winter habe ich drei Kilo ___. (gain weight)", "zugenommen"),
        fill("Ich kaufe gern ___ Obst vom Markt. (local)", "regionales"),
        tr("I rarely eat pasta.", "Ich esse selten Nudeln."),
        tr(
            "We mostly cook in the evening.",
            "Wir kochen meistens abends.|Meistens kochen wir abends.",
        ),
    ),
    lesson(
        "Lektion 12: Test",
        fill("Wenn es regnet, ___ ich zu Hause. (bleiben)", "bleibe"),
        mc("___ es heiß ist, trinke ich viel.", "Wenn", "Als"),
        fill("___ Sie die Tomaten. (schneiden)", "Schneiden"),
        mc("Zuerst ___ du die Kartoffeln.", "schälst", "schälen"),
        fill("Ich esse ___ Fisch. (rarely)", "selten"),
        order("Wenn ich Zeit habe, koche ich selbst."),
        tr("When I'm hungry, I eat an apple.", "Wenn ich Hunger habe, esse ich einen Apfel."),
    ),
    lesson(
        "Modul 4: Wiederholung",
        fill("Gut, dass du gekommen ___. (sein)", "bist"),
        fill("Ich bleibe hier, weil ich müde ___. (sein)", "bin"),
        fill("Wir freuen ___ auf die Party.", "uns"),
        mc("Sie freut sich ___ die Blumen, die sie bekommen hat.", "über", "auf"),
        fill("Weißt du, ___ das Restaurant offen ist?", "ob"),
        fill("Wenn es warm ist, ___ wir draußen. (essen)", "essen"),
        mc("Zuerst ___ Sie das Gemüse.", "waschen", "wäscht"),
        fill("Ich bin ___, ich habe genug gegessen. (full)", "satt"),
        bank(
            "Schade, ___ du nicht kommen kannst. Ich freue ___ trotzdem, weil wir uns bald "
            "sehen. Weißt du, ___ Lisa auch kommt?",
            ["dass", "mich", "ob"],
            "weil",
            "dich",
        ),
        tr("I'm looking forward to the holiday.", "Ich freue mich auf den Urlaub."),
        order("Wenn es kalt ist, essen wir gern Suppe."),
    ),
]

LEKTION_12 = unit(
    12,
    "Wenn es warm ist, essen wir meist Salat.",
    "Ernährung und Rezepte",
    L12_WORDS,
    L12_RULES,
    sections(L12_LESSONS, vocab_lessons(L12_WORDS, "Wörter")),
)


UNITS = [LEKTION_10, LEKTION_11, LEKTION_12]
