"""Modul 2 (A2.1): Lektion 4 (Was darf es sein?), 5 (Schaut mal, der schöne
Dom!), 6 (Meine Lieblingsveranstaltung)."""

from ..dsl import (
    bank,
    conj,
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
# Lektion 4: Was darf es sein?
# ============================================================================

L4_WORDS = [
    ("the banana", "die Banane", "noun", "Pl. die Bananen"),
    ("the pear", "die Birne", "noun", "Pl. die Birnen"),
    ("the bean", "die Bohne", "noun", "Pl. die Bohnen"),
    ("the grape", "die Traube", "noun", "Pl. die Trauben"),
    ("the sweet / candy", "das Bonbon", "noun", "Pl. die Bonbons"),
    ("the cola", "die Cola", "noun", "also: das Cola"),
    ("the jam", "die Marmelade", "noun", "Pl. die Marmeladen"),
    ("the flour", "das Mehl", "noun"),
    ("the quark (curd cheese)", "der Quark", "noun"),
    ("the chicken (food)", "das Hähnchen", "noun", "Pl. die Hähnchen"),
    ("the bottle", "die Flasche", "noun", "Pl. die Flaschen"),
    ("the can / tin", "die Dose", "noun", "Pl. die Dosen"),
    ("the packet", "die Packung", "noun", "Pl. die Packungen"),
    ("the piece", "das Stück", "noun", "Pl. die Stücke"),
    ("the gram", "das Gramm", "noun", "200 Gramm"),
    ("the kilo", "das Kilo", "noun", "zwei Kilo"),
    ("the litre", "der Liter", "noun", "zwei Liter"),
    ("the pound (500 g)", "das Pfund", "noun", "ein Pfund Tomaten"),
    ("the portion", "die Portion", "noun", "Pl. die Portionen"),
    ("the note / slip of paper", "der Zettel", "noun", "Pl. die Zettel"),
    ("the supermarket", "der Supermarkt", "noun", "Pl. die Supermärkte"),
    ("the butcher's", "die Metzgerei", "noun", "Pl. die Metzgereien"),
    ("the eating habit", "die Essgewohnheit", "noun", "Pl. die Essgewohnheiten"),
    ("to order", "bestellen", "verb", "hat bestellt"),
    ("to hope", "hoffen", "verb", "hat gehofft"),
    ("to weigh", "wiegen", "verb", "hat gewogen"),
    ("fatty", "fett", "adjective"),
    ("low-fat", "fettarm", "adjective"),
    ("hard", "hart", "adjective"),
    ("soft", "weich", "adjective"),
    ("ripe", "reif", "adjective"),
    ("sweet", "süß", "adjective"),
    ("sour", "sauer", "adjective"),
    ("spicy / hot", "scharf", "adjective"),
    ("namely / you see", "nämlich", "adverb"),
    ("What would you like?", "Was darf es sein?", "phrase"),
    ("Anything else?", "Darf es sonst noch etwas sein?", "phrase"),
    ("I'd like ...", "Ich hätte gern ...", "phrase"),
    ("That's all, thank you.", "Das ist alles, danke.", "phrase"),
]

L4_RULES = [
    rule(
        "Mengenangaben",
        "other",
        """
A quantity goes **directly** before the food, with no *of*:

- *eine Flasche Wasser* (a bottle of water)
- *200 Gramm Käse · ein Kilo Äpfel · ein Pfund Tomaten*
- *eine Packung Reis · eine Dose Bohnen · ein Stück Kuchen*

Measures stay **singular** after a number: *zwei **Kilo**, drei **Liter**,
500 **Gramm***. Containers take a plural: *zwei **Flaschen**, drei **Dosen***.

The quantity carries the article: ***eine** Flasche Saft* (die Flasche),
***ein** Stück Käse* (das Stück).
""",
        [
            "Ich brauche zwei Kilo Kartoffeln.",
            "Wir kaufen drei Flaschen Wasser und eine Dose Bohnen.",
            "Ein Stück Kuchen, bitte.",
        ],
    ),
    rule(
        "Ich hätte gern ...",
        "verbs",
        """
In shops and cafés, *ich hätte gern* (I would like) is the polite way to ask for
something. *hätte* is the Konjunktiv II of *haben*:

| ich | du | er / sie | wir | ihr | sie / Sie |
|---|---|---|---|---|---|
| hätte | hättest | hätte | hätten | hättet | hätten |

- *Ich **hätte gern** 300 Gramm Käse.*
- *Wir **hätten gern** zwei Kaffee.*

*Ich möchte* works just as well: *Ich möchte ein Brot, bitte.*
Typical questions from the seller: *Was darf es sein? · Darf es sonst noch
etwas sein? · Das macht zusammen 8,50 Euro.*
""",
        [
            "Ich hätte gern ein Kilo Birnen.",
            "Hätten Sie auch fettarmen Quark?",
            "Wir hätten gern die Rechnung.",
        ],
    ),
    rule(
        "etwas, ein paar, viel, wenig",
        "other",
        """
For amounts without a number:

| | with uncountable nouns | with plural nouns |
|---|---|---|
| a little / some | **etwas** Milch, **ein bisschen** Zucker | **ein paar** Eier |
| a lot | **viel** Käse | **viele** Äpfel |
| little / few | **wenig** Mehl | **wenige** Bananen |

- *etwas* and *ein paar* never change their ending.
- *viel* and *wenig* take **-e** with plural nouns: *viel**e** Leute*.
""",
        [
            "Ich hätte gern etwas Quark.",
            "Wir brauchen noch ein paar Bananen.",
            "Im Kühlschrank ist nur wenig Milch.",
        ],
    ),
]

L4_LESSONS = [
    lesson(
        "Auf dem Markt",
        review("die Birne"),
        review("die Traube"),
        match(
            [
                ("die Banane", "the banana"),
                ("die Bohne", "the bean"),
                ("das Mehl", "the flour"),
                ("die Marmelade", "the jam"),
                ("das Hähnchen", "the chicken"),
            ]
        ),
        mc("Eine Zitrone ist ...", "sauer", "süß", "fett"),
        mc("Fleisch kauft man in der ...", "Metzgerei", "Bäckerei", "Apotheke"),
        mc(
            "Fettarmer Quark hat ...",
            "wenig Fett.",
            "viel Fett.",
            "kein Wasser.",
        ),
        fill("Die Bananen sind noch grün, sie sind nicht ___. (ripe)", "reif"),
        tr("The bread is very hard.", "Das Brot ist sehr hart."),
    ),
    lesson(
        "Eine Flasche Wasser",
        grammar("Mengenangaben"),
        match(
            [
                ("eine Flasche", "Wasser"),
                ("eine Dose", "Bohnen"),
                ("eine Packung", "Reis"),
                ("ein Stück", "Kuchen"),
                ("200 Gramm", "Käse"),
            ],
            "What goes together?",
        ),
        mc("Ich kaufe zwei ___ Kartoffeln.", "Kilo", "Kilos", "Kilogramme"),
        mc("Wir brauchen drei ___ Saft.", "Flaschen", "Flasche", "Flaschens"),
        mc(
            "Which is correct?",
            "Ich hätte gern ein Glas Wasser.",
            "Ich hätte gern ein Glas von Wasser.",
            "Ich hätte gern ein Glas mit von Wasser.",
        ),
        fill("Ich nehme ein ___ Tomaten. (500 g)", "Pfund"),
        fill("Eine ___ Pommes, bitte! (portion)", "Portion"),
        fill("Zwei ___ Milch, bitte. (litre)", "Liter"),
        tr("A piece of cake, please.", "Ein Stück Kuchen, bitte."),
    ),
    lesson(
        "Ich hätte gern ...",
        grammar("Ich hätte gern ..."),
        conj("hätten", "ich", "hätte"),
        conj("hätten", "du", "hättest"),
        conj("hätten", "wir", "hätten"),
        conj("hätten", "ihr", "hättet"),
        fill("Ich ___ gern 300 Gramm Käse.", "hätte"),
        fill("___ Sie auch frische Birnen?", "Hätten"),
        mc(
            "The seller asks what you want:",
            "Was darf es sein?",
            "Was hätten Sie?",
            "Was macht das?",
        ),
        mc(
            "Darf es sonst noch etwas sein? You say no:",
            "Nein, danke. Das ist alles.",
            "Ja, das ist alles.",
            "Nein, das darf es.",
        ),
        order("Ich hätte gern ein Kilo Birnen."),
        tr("We would like two coffees.", "Wir hätten gern zwei Kaffee."),
    ),
    lesson(
        "etwas, ein paar, viel",
        grammar("etwas, ein paar, viel, wenig"),
        mc("Wir brauchen noch ___ Eier.", "ein paar", "etwas", "viel"),
        mc("Gib mir bitte ___ Zucker.", "etwas", "ein paar", "viele"),
        mc("Auf dem Markt sind heute ___ Leute.", "viele", "viel", "etwas"),
        fill("Im Kühlschrank ist nur ___ Milch. (little)", "wenig"),
        fill("Ich esse ___ Obst, das ist gesund. (a lot of)", "viel"),
        fill("Kauf bitte noch ___ paar Bananen.", "ein"),
        tr("I would like some quark.", "Ich hätte gern etwas Quark."),
    ),
    lesson(
        "Beim Einkaufen",
        bank(
            "Guten Tag! Was ___ es sein? Ich hätte gern ein ___ Äpfel und 200 ___ Käse. "
            "Darf es ___ noch etwas sein? Ja, eine ___ Milch, bitte. Das ___ zusammen 6,40 Euro.",
            ["darf", "Kilo", "Gramm", "sonst", "Flasche", "macht"],
            "kostet",
            "Stück",
        ),
        mc(
            "Was macht das zusammen? means:",
            "How much is that altogether?",
            "What are you doing together?",
            "What does it make?",
        ),
        mc(
            "Ich schreibe die Sachen auf einen ___.",
            "Zettel",
            "Liter",
            "Supermarkt",
        ),
        fill("Kannst du den Käse ___? (weigh)", "wiegen"),
        fill("Ich habe beim Bäcker einen Kuchen ___. (bestellen)", "bestellt"),
        order("Darf es sonst noch etwas sein?", "Build the question."),
        tr("That's all, thank you.", "Das ist alles, danke."),
    ),
    lesson(
        "Essgewohnheiten",
        mc(
            "Ich esse keine Bonbons, sie sind mir zu ___.",
            "süß",
            "sauer",
            "weich",
        ),
        mc(
            "Das Curry ist sehr ___. Ich brauche Wasser!",
            "scharf",
            "fettarm",
            "reif",
        ),
        fill("Ich ___, der Markt ist morgen offen. (hope)", "hoffe"),
        fill("Ich kaufe keine Cola. Ich trinke ___ keine süßen Getränke. (you see)", "nämlich"),
        tr("I eat little meat.", "Ich esse wenig Fleisch."),
        tr("My eating habits are healthy.", "Meine Essgewohnheiten sind gesund."),
    ),
    lesson(
        "Lektion 4: Test",
        fill("Ich ___ gern zwei Brötchen. (would like: haben)", "hätte"),
        mc("drei ___ Tomaten", "Kilo", "Kilos"),
        mc("zwei ___ Wasser", "Flaschen", "Flasche"),
        mc("Wir brauchen ___ Eier.", "ein paar", "etwas"),
        fill("Eine ___ Bohnen, bitte. (can)", "Dose"),
        order("Ich hätte gern 300 Gramm Käse."),
        tr("What would you like?", "Was darf es sein?"),
        tr("The pears are soft.", "Die Birnen sind weich."),
    ),
]

LEKTION_4 = unit(
    4,
    "Was darf es sein?",
    "Einkaufen und Mengen",
    L4_WORDS,
    L4_RULES,
    sections(L4_LESSONS, vocab_lessons(L4_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 5: Schaut mal, der schöne Dom!
# ============================================================================

L5_WORDS = [
    ("the castle / fortress", "die Burg", "noun", "Pl. die Burgen"),
    ("the market square", "der Marktplatz", "noun", "Pl. die Marktplätze"),
    ("the monument", "das Denkmal", "noun", "Pl. die Denkmäler"),
    ("the wall (outside)", "die Mauer", "noun", "Pl. die Mauern"),
    ("the sight / attraction", "die Sehenswürdigkeit", "noun", "Pl. die Sehenswürdigkeiten"),
    ("the guided tour", "die Führung", "noun", "Pl. die Führungen"),
    ("the walk around / tour", "der Rundgang", "noun", "Pl. die Rundgänge"),
    ("the tourist", "der Tourist", "noun", "f. die Touristin"),
    ("the visit", "der Besuch", "noun", "Pl. die Besuche"),
    ("the brochure", "der Prospekt", "noun", "Pl. die Prospekte"),
    ("the camera", "die Kamera", "noun", "Pl. die Kameras"),
    ("the club", "der Club", "noun", "Pl. die Clubs"),
    ("the holidays (school)", "die Ferien", "noun", "plural only"),
    ("to visit (a sight)", "besichtigen", "verb", "hat besichtigt"),
    ("to show", "zeigen", "verb", "hat gezeigt"),
    ("to cross", "überqueren", "verb", "hat überquert"),
    ("to change (money)", "wechseln", "verb", "Geld wechseln"),
    ("historic", "historisch", "adjective"),
    ("famous", "berühmt", "adjective"),
    ("impressive", "beeindruckend", "adjective"),
    ("worth seeing", "sehenswert", "adjective"),
    ("open", "offen", "adjective"),
    ("closed", "geschlossen", "adjective"),
    ("certainly / surely", "bestimmt", "adverb"),
    ("in agreement", "einverstanden", "adjective"),
    ("along", "entlang", "other", "die Straße entlang"),
    ("opposite", "gegenüber", "other", "gegenüber vom Rathaus"),
    ("Look, the beautiful cathedral!", "Schaut mal, der schöne Dom!", "phrase"),
    ("How do I get to the cathedral?", "Wie komme ich zum Dom?", "phrase"),
    ("How beautiful!", "Wie schön!", "phrase"),
]

L5_RULES = [
    rule(
        "Adjektive nach dieser, welcher, jeder",
        "adjectives",
        """
*dieser* (this), *welcher* (which) and *jeder* (every) have the same endings as
*der, die, das*, and the adjective after them behaves exactly as after *der*:

| | masculine | feminine | neuter | plural |
|---|---|---|---|---|
| Nominativ | dies**er** alt**e** Dom | dies**e** alt**e** Burg | dies**es** alt**e** Denkmal | dies**e** alt**en** Häuser |
| Akkusativ | dies**en** alt**en** Dom | dies**e** alt**e** Burg | dies**es** alt**e** Denkmal | dies**e** alt**en** Häuser |
| Dativ | dies**em** alt**en** Dom | dies**er** alt**en** Burg | dies**em** alt**en** Denkmal | dies**en** alt**en** Häusern |

*jeder* has no plural (use *alle*: *alle alten Häuser*).
""",
        [
            "Schaut mal, der schöne Dom!",
            "Welches historische Gebäude möchtet ihr besichtigen?",
            "Jeder neue Tourist bekommt einen Prospekt.",
        ],
    ),
    rule(
        "Wege beschreiben: durch, über, entlang, gegenüber",
        "cases",
        """
To give directions, use the **imperative** and these prepositions:

| Preposition | Case | Example |
|---|---|---|
| **durch** (through) | Akkusativ | *Gehen Sie **durch den** Park.* |
| **über** (across) | Akkusativ | *Geh **über die** Brücke.* |
| **entlang** (along, after the noun) | Akkusativ | *Gehen Sie **die Straße entlang**.* |
| **gegenüber von** (opposite) | Dativ | *Das Café ist **gegenüber vom** Dom.* |
| **bis zum / bis zur** (as far as) | Dativ | *Gehen Sie **bis zur** Ampel.* |
| **an ... vorbei** (past) | Dativ | *Gehen Sie **am** Rathaus **vorbei**.* |

*Biegen Sie links ab. · Nehmen Sie die erste Straße rechts.*
""",
        [
            "Gehen Sie geradeaus bis zum Marktplatz.",
            "Überqueren Sie die Kreuzung und gehen Sie am Museum vorbei.",
            "Die Burg liegt gegenüber vom Bahnhof.",
        ],
    ),
]

L5_LESSONS = [
    lesson(
        "Sehenswürdigkeiten",
        review("die Sehenswürdigkeit"),
        review("die Führung"),
        match(
            [
                ("die Burg", "the castle"),
                ("das Denkmal", "the monument"),
                ("der Marktplatz", "the market square"),
                ("die Mauer", "the wall"),
                ("der Rundgang", "the tour"),
            ]
        ),
        mc(
            "Das Museum ist heute nicht offen. Es ist ...",
            "geschlossen.",
            "sehenswert.",
            "berühmt.",
        ),
        mc(
            "Ein Reiseführer im Museum macht eine ...",
            "Führung.",
            "Mauer.",
            "Kamera.",
        ),
        fill("Morgen ___ wir die alte Burg. (besichtigen)", "besichtigen"),
        tr("The cathedral is very famous.", "Der Dom ist sehr berühmt."),
    ),
    lesson(
        "Der schöne Dom!",
        grammar("Adjektive nach dieser, welcher, jeder"),
        fill("Schaut mal, der ___ Dom! (schön)", "schöne"),
        fill("Diese ___ Burg ist 800 Jahre alt. (alt)", "alte"),
        fill("Siehst du diesen ___ Turm? (groß)", "großen"),
        fill("Welches ___ Museum ist am besten? (historisch)", "historische"),
        fill("Wir wohnen in dieser ___ Straße. (ruhig)", "ruhigen"),
        mc("Jeder ___ Besuch ist interessant.", "neue", "neuen", "neuer"),
        mc("Welchen ___ Platz meinst du?", "großen", "große", "großer"),
        mc("Die Fotos von diesen ___ Denkmälern sind toll.", "berühmten", "berühmte", "berühmter"),
        tr("Which old church do you mean? (du)", "Welche alte Kirche meinst du?"),
    ),
    lesson(
        "Wie komme ich zum Dom?",
        grammar("Wege beschreiben: durch, über, entlang, gegenüber"),
        mc("Gehen Sie ___ den Park.", "durch", "gegenüber", "bis"),
        mc("Das Café ist gegenüber ___ Dom.", "vom", "den", "durch"),
        mc("Gehen Sie die Straße ___.", "entlang", "durch", "über"),
        fill("Geh ___ die Brücke! (across)", "über"),
        fill("Gehen Sie bis ___ Ampel. (zu der)", "zur"),
        fill("Gehen Sie am Rathaus ___. (past)", "vorbei"),
        fill("___ Sie die Kreuzung. (cross)", "Überqueren"),
        order("Gehen Sie geradeaus bis zum Marktplatz."),
        tr("How do I get to the cathedral?", "Wie komme ich zum Dom?"),
    ),
    lesson(
        "Ein Stadtrundgang",
        bank(
            "Willkommen zum ___! Zuerst gehen wir durch die ___ Altstadt. Dann ___ wir die "
            "Brücke und sehen die alte ___. Das Denkmal auf dem Marktplatz ist sehr ___. Zum "
            "Schluss besuchen wir den ___ Dom.",
            ["Rundgang", "historische", "überqueren", "Burg", "berühmt", "schönen"],
            "geschlossen",
            "schöne",
        ),
        mc(
            "Wie schön! is ...",
            "a reaction to something beautiful.",
            "a question about the way.",
            "a goodbye.",
        ),
        mc(
            "Bist du einverstanden? means:",
            "Do you agree?",
            "Are you finished?",
            "Are you tired?",
        ),
        fill("Kannst du mir die Fotos ___? (zeigen)", "zeigen"),
        fill("Ich muss noch Geld ___. (change)", "wechseln"),
        order("Die Burg ist wirklich beeindruckend."),
        tr("The castle is worth seeing.", "Die Burg ist sehenswert."),
    ),
    lesson(
        "In den Ferien",
        mc(
            "Die Touristen ___ viele Fotos mit der Kamera.",
            "machen",
            "zeigen",
            "wechseln",
        ),
        mc(
            "In den Ferien ...",
            "haben Schüler keine Schule.",
            "ist das Museum immer geschlossen.",
            "gibt es keine Touristen.",
        ),
        fill("Das Museum hat ___ offen. Es ist ja Samstag. (certainly)", "bestimmt"),
        fill("Im Hotel liegt ein ___ über die Stadt. (brochure)", "Prospekt"),
        tr("Thank you for your visit!", "Danke für Ihren Besuch!|Danke für deinen Besuch!"),
        tr("The museum is opposite the town hall.", "Das Museum ist gegenüber vom Rathaus."),
    ),
    lesson(
        "Lektion 5: Test",
        fill("Schaut mal, diese ___ Mauer! (alt)", "alte"),
        mc("Gehen Sie ___ die Altstadt.", "durch", "gegenüber"),
        fill("Gehen Sie bis ___ Marktplatz. (zu dem)", "zum"),
        mc("Welchen ___ Turm meinst du?", "alten", "alte"),
        fill("Wir haben die Burg ___. (besichtigen)", "besichtigt"),
        order("Biegen Sie an der Ampel links ab."),
        tr("How beautiful!", "Wie schön!"),
    ),
]

LEKTION_5 = unit(
    5,
    "Schaut mal, der schöne Dom!",
    "Stadtbesichtigung",
    L5_WORDS,
    L5_RULES,
    sections(L5_LESSONS, vocab_lessons(L5_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 6: Meine Lieblingsveranstaltung
# ============================================================================

L6_WORDS = [
    ("the event", "die Veranstaltung", "noun", "Pl. die Veranstaltungen"),
    ("the favourite event", "die Lieblingsveranstaltung", "noun"),
    ("the opera", "die Oper", "noun", "Pl. die Opern"),
    ("the musical", "das Musical", "noun", "Pl. die Musicals"),
    ("the festival", "das Festival", "noun", "Pl. die Festivals"),
    ("the ballet", "das Ballett", "noun"),
    ("the play", "das Theaterstück", "noun", "Pl. die Theaterstücke"),
    ("the ticket (admission)", "die Eintrittskarte", "noun", "Pl. die Eintrittskarten"),
    ("the stage", "die Bühne", "noun", "Pl. die Bühnen"),
    ("the entrance", "der Eingang", "noun", "Pl. die Eingänge"),
    ("the musician", "der Musiker", "noun", "f. die Musikerin"),
    ("the band", "die Band", "noun", "Pl. die Bands"),
    ("the music genre", "die Musikrichtung", "noun", "Pl. die Musikrichtungen"),
    ("the audience", "das Publikum", "noun"),
    ("the applause", "der Applaus", "noun"),
    ("the fan", "der Fan", "noun", "Pl. die Fans"),
    ("the art", "die Kunst", "noun"),
    ("to accept (an invitation)", "zusagen", "verb", "hat zugesagt"),
    ("to clap", "klatschen", "verb", "hat geklatscht"),
    ("classical", "klassisch", "adjective"),
    ("exciting", "spannend", "adjective"),
    ("entertaining", "unterhaltsam", "adjective"),
    ("great / fantastic", "super", "adjective"),
    ("Do you feel like coming along?", "Hast du Lust mitzukommen?", "phrase"),
    ("That sounds interesting.", "Das klingt interessant.", "phrase"),
    ("Thanks for the invitation.", "Danke für die Einladung.", "phrase"),
]

L6_RULES = [
    rule(
        "Adjektive nach ein, kein, mein",
        "adjectives",
        """
After *ein, kein* and the possessives (*mein, dein, unser ...*) the adjective
shows the gender where the article can't:

| | masculine | feminine | neuter | plural (kein/mein) |
|---|---|---|---|---|
| Nominativ | ein spannend**er** Film | eine spannend**e** Oper | ein spannend**es** Konzert | keine spannend**en** Filme |
| Akkusativ | einen spannend**en** Film | eine spannend**e** Oper | ein spannend**es** Konzert | keine spannend**en** Filme |
| Dativ | einem spannend**en** Film | einer spannend**en** Oper | einem spannend**en** Konzert | keinen spannend**en** Filmen |

The three special endings: **-er** (ein ... der-word), **-es** (ein ... das-word,
nominative and accusative). Everything else is like after *der*.
""",
        [
            "Das war ein unterhaltsames Musical.",
            "Ich habe einen klassischen Musiker kennengelernt.",
            "Meine Lieblingsveranstaltung ist ein großes Festival im Sommer.",
        ],
    ),
    rule(
        "Einladen: Hast du Lust, ... zu ...?",
        "sentence_structure",
        """
After *Hast du Lust, ...? / Hast du Zeit, ...?* the second verb comes **at the
end with zu**:

- *Hast du Lust, ins Konzert **zu gehen**?*
- *Hast du Zeit, mit mir **zu essen**?*
- Separable verbs put *zu* in the middle: *Hast du Lust, **mitzukommen**?*

Answering an invitation:

| zusagen (yes) | absagen (no) |
|---|---|
| *Gern! Das klingt gut.* | *Danke für die Einladung, aber ich kann leider nicht.* |
| *Super, ich komme mit.* | *Vielleicht ein anderes Mal.* |
""",
        [
            "Hast du Lust, am Samstag in die Oper zu gehen?",
            "Hast du Zeit, mitzukommen?",
            "Danke für die Einladung, aber ich kann leider nicht.",
        ],
    ),
]

L6_LESSONS = [
    lesson(
        "Kultur in der Stadt",
        review("die Veranstaltung"),
        review("die Eintrittskarte"),
        match(
            [
                ("die Oper", "the opera"),
                ("die Bühne", "the stage"),
                ("das Publikum", "the audience"),
                ("der Eingang", "the entrance"),
                ("die Musikrichtung", "the music genre"),
            ]
        ),
        mc(
            "Am Ende klatscht das Publikum. Das ist ...",
            "der Applaus.",
            "der Eingang.",
            "die Kunst.",
        ),
        mc(
            "Mozart und Beethoven machen ... Musik.",
            "klassische",
            "spannende",
            "unterhaltsame",
        ),
        fill("Nach dem Konzert haben alle laut ___. (klatschen)", "geklatscht"),
        tr("My favourite event is the festival.", "Meine Lieblingsveranstaltung ist das Festival."),
    ),
    lesson(
        "Ein spannender Film",
        grammar("Adjektive nach ein, kein, mein"),
        fill("Das ist ein ___ Film. (spannend)", "spannender"),
        fill("Das war ein ___ Konzert. (toll)", "tolles"),
        fill("Ich habe eine ___ Oper gesehen. (klassisch)", "klassische"),
        fill("Wir haben einen ___ Abend gehabt. (schön)", "schönen"),
        fill("Er spielt in einer ___ Band. (bekannt)", "bekannten"),
        mc("Das ist kein ___ Theaterstück.", "langweiliges", "langweilige", "langweiligen"),
        mc("Meine ___ Musikrichtung ist Jazz.", "liebste", "liebster", "liebstes"),
        mc("mit einem ___ Musiker", "berühmten", "berühmter", "berühmtes"),
        tr(
            "It was an entertaining musical.",
            "Es war ein unterhaltsames Musical.|Das war ein unterhaltsames Musical.",
        ),
    ),
    lesson(
        "Hast du Lust?",
        grammar("Einladen: Hast du Lust, ... zu ...?"),
        mc(
            "Which is correct?",
            "Hast du Lust, ins Kino zu gehen?",
            "Hast du Lust, zu gehen ins Kino?",
            "Hast du Lust, ins Kino gehen zu?",
        ),
        fill("Hast du Zeit, mit mir ___ essen?", "zu"),
        fill("Hast du Lust, ___? (mitkommen)", "mitzukommen"),
        mc(
            "You want to say yes:",
            "Gern! Das klingt gut.",
            "Leider kann ich nicht.",
            "Vielleicht ein anderes Mal.",
        ),
        mc(
            "You want to say no politely:",
            "Danke für die Einladung, aber ich kann leider nicht.",
            "Super, ich komme mit.",
            "Das klingt interessant.",
        ),
        fill("Anna hat ___. Sie kommt mit. (zusagen)", "zugesagt"),
        order("Hast du Lust, in die Oper zu gehen?", "Build the question."),
        tr(
            "Do you have time to come along?",
            "Hast du Zeit mitzukommen?|Hast du Zeit, mitzukommen?",
        ),
    ),
    lesson(
        "Eine Einladung",
        bank(
            "Hallo Lukas, am Samstag spielt meine Lieblings___ im Stadtpark. Hast du ___, "
            "mitzukommen? Die ___ kosten nur 15 Euro. Wir treffen uns um 19 Uhr am ___. "
            "Es wird ein ___ Abend! Lisa",
            ["band", "Lust", "Eintrittskarten", "Eingang", "toller"],
            "Bühne",
            "tolle",
        ),
        mc(
            "Where do Lisa and Lukas meet?",
            "At the entrance.",
            "On the stage.",
            "At the ticket office.",
        ),
        mc(
            "Das klingt interessant. Wann fängt es an? This person ...",
            "is interested.",
            "says no.",
            "is angry.",
        ),
        fill("Ich bin ein großer ___ von dieser Band. (fan)", "Fan"),
        tr("Thanks for the invitation.", "Danke für die Einladung."),
    ),
    lesson(
        "Lektion 6: Test",
        fill("Das war ein ___ Theaterstück. (spannend)", "spannendes"),
        mc("Ich mag keine ___ Musik.", "klassische", "klassischer"),
        fill("Hast du Lust, ins Ballett ___ gehen?", "zu"),
        mc("Der Film gefällt ___.", "mir", "mich"),
        fill("Ich habe einen ___ Musiker gesehen. (gut)", "guten"),
        order("Das Publikum hat laut geklatscht."),
        tr("That sounds interesting.", "Das klingt interessant."),
    ),
    lesson(
        "Modul 2: Wiederholung",
        fill("Ich ___ gern ein Pfund Bohnen. (haben)", "hätte"),
        mc("zwei ___ Mehl", "Kilo", "Kilos"),
        mc("Wir brauchen noch ___ Eier.", "ein paar", "etwas"),
        fill("Schaut mal, die ___ Burg! (alt)", "alte"),
        fill("Gehen Sie ___ den Park. (through)", "durch"),
        fill("Das Café liegt gegenüber ___ Bahnhof. (von dem)", "vom"),
        fill("Das ist ein ___ Festival. (groß)", "großes"),
        fill("Hast du Zeit, morgen ___? (anrufen)", "anzurufen"),
        bank(
            "Am Wochenende besichtigen wir die ___ Altstadt. Danach gehen wir in ein ___ "
            "Konzert. Vorher kaufen wir noch ein ___ Kuchen.",
            ["historische", "klassisches", "Stück"],
            "historischen",
            "Kilo",
        ),
        tr("Which castle do you mean? (du)", "Welche Burg meinst du?"),
        order("Hast du Zeit, mit mir ins Theater zu gehen?", "Build the question."),
    ),
]

LEKTION_6 = unit(
    6,
    "Meine Lieblingsveranstaltung",
    "Kultur und Einladungen",
    L6_WORDS,
    L6_RULES,
    sections(L6_LESSONS, vocab_lessons(L6_WORDS, "Wörter")),
)


UNITS = [LEKTION_4, LEKTION_5, LEKTION_6]
