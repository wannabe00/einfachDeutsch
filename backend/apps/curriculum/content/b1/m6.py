"""Modul 6 (B1.2): Lektion 16 (Wir brauchten uns um nichts zu kümmern.), 17 (Guck
mal! Das ist schön!), 18 (Davon halte ich nicht viel.)."""

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
# Lektion 16: Wir brauchten uns um nichts zu kümmern.
# ============================================================================

L16_WORDS = [
    ("the memory", "die Erinnerung", "noun", "Pl. die Erinnerungen"),
    ("the upbringing", "die Erziehung", "noun"),
    ("the generation", "die Generation", "noun", "Pl. die Generationen"),
    ("the marriage", "die Ehe", "noun", "Pl. die Ehen"),
    ("the conflict", "der Konflikt", "noun", "Pl. die Konflikte"),
    ("the war", "der Krieg", "noun", "Pl. die Kriege"),
    ("the kiss", "der Kuss", "noun", "Pl. die Küsse"),
    ("the lie", "die Lüge", "noun", "Pl. die Lügen"),
    ("the piece of advice", "der Ratschlag", "noun", "Pl. die Ratschläge"),
    ("the argument / quarrel", "der Streit", "noun", "Pl. die Streite"),
    ("the tear", "die Träne", "noun", "Pl. die Tränen"),
    ("the pocket money", "das Taschengeld", "noun"),
    ("the school-leaving exam", "das Abitur", "noun", "das Abitur machen"),
    ("the harvest", "die Ernte", "noun", "Pl. die Ernten"),
    ("the piano", "das Klavier", "noun", "Pl. die Klaviere"),
    ("the make-up", "die Schminke", "noun"),
    ("the cosmetics", "die Kosmetik", "noun"),
    ("the midnight", "die Mitternacht", "noun", "um Mitternacht"),
    ("the value", "der Wert", "noun", "Wert legen auf + Akk."),
    ("the travel acquaintance", "die Reisebekanntschaft", "noun", "Pl. die Reisebekanntschaften"),
    ("to look after / to deal with", "kümmern", "verb", "sich kümmern um + Akk."),
    (
        "to get on (with someone)",
        "vertragen",
        "verb",
        "sich vertragen, verträgt sich, hat sich vertragen",
    ),
    ("to get worked up", "aufregen", "verb", "sich aufregen über + Akk."),
    ("to go out", "ausgehen", "verb", "ging aus, ist ausgegangen"),
    ("to meet (by chance)", "begegnen", "verb", "begegnen + Dat., ist begegnet"),
    ("to kiss", "küssen", "verb", "hat geküsst"),
    ("to go there", "hingehen", "verb", "ging hin, ist hingegangen"),
    ("dependent", "abhängig", "adjective", "abhängig von + Dat."),
    ("unusual", "ungewöhnlich", "adjective"),
    ("upwards", "aufwärts", "adverb"),
    ("nowadays", "heutzutage", "adverb"),
    ("on weekdays", "wochentags", "adverb"),
    ("Ah, that was a wonderful time!", "Ach, das war eine herrliche Zeit!", "phrase"),
    ("That was out of the question for us.", "Bei uns kam das nicht infrage.", "phrase"),
]

L16_RULES = [
    rule(
        "brauchen + nicht / nur + zu",
        "verbs",
        """
**nicht brauchen + zu + Infinitiv** = it is **not necessary** (= *nicht
müssen*):
- *Du **brauchst** heute **nicht zu** kochen.* = *Du musst heute nicht kochen.*
- *Wir **brauchten** uns um nichts **zu** kümmern.*

**nur brauchen + zu + Infinitiv** = all you need to do is ...:
- *Sie **brauchen nur** an**zu**rufen.*
- *Du **brauchst nur** eine E-Mail **zu** schreiben.*

*zu* goes inside separable verbs: *nicht auf**zu**stehen, nur ein**zu**kaufen*.

Compare the meanings:
| | |
|---|---|
| *Ich musste arbeiten.* | it was an obligation |
| *Ich brauchte nicht zu arbeiten.* | it wasn't necessary |
| *Ich durfte nicht arbeiten.* | it was not allowed |

*müssen* never takes *zu*: ~~Ich muss zu arbeiten~~.
""",
        [
            "Wir brauchten uns um nichts zu kümmern.",
            "Du brauchst morgen nicht früh aufzustehen.",
            "Sie brauchen nur das Formular zu unterschreiben.",
            "Als Kind brauchte ich nie im Haushalt zu helfen.",
        ],
    ),
    rule(
        "Erinnerungen erzählen und reagieren",
        "other",
        """
**Telling:** *Früher musste ich ... · Damals brauchte ich nicht zu ... · Ich kann
mich gut daran erinnern, dass ... · Ich konnte es kaum erwarten, ... · Bei uns
kam das nicht infrage.*

**Reacting:** *Das kann ich gut verstehen. · Bei mir war das ganz anders. ·
Darüber habe ich noch nie nachgedacht. · Ich kann mir gut vorstellen, dass ... ·
Das klingt interessant.*

**Then and now:** *früher / damals* vs *heute / heutzutage*.
""",
        [
            "Ich kann mich gut daran erinnern, dass wir nie Taschengeld bekommen haben.",
            "Bei mir war das ganz anders.",
            "Heutzutage brauchen Kinder nicht mehr auf dem Feld zu helfen.",
        ],
    ),
]

L16_LESSONS = [
    lesson(
        "Jugend früher und heute",
        review("die Erinnerung"),
        review("die Generation"),
        match(
            [
                ("das Taschengeld", "Geld, das Kinder jede Woche bekommen"),
                ("das Abitur", "die Prüfung am Ende vom Gymnasium"),
                ("die Ernte", "Im Herbst holt man das Obst vom Feld."),
                ("der Ratschlag", "ein guter Tipp"),
                ("die Lüge", "Etwas ist nicht wahr."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Die beiden Geschwister streiten nie. Sie ___ sich gut.",
            "vertragen",
            "begegnen",
            "küssen",
        ),
        mc(
            "Sie weinte. Sie hatte ___ in den Augen.",
            "Tränen",
            "Kosmetik",
            "Ernte",
        ),
        fill("Meine Oma hat sich um fünf Kinder ___. (kümmern)", "gekümmert"),
        fill("Früher sind wir am Wochenende oft ___. (ausgehen)", "ausgegangen"),
        fill("Im Zug bin ich einer alten Freundin ___. (begegnen)", "begegnet"),
        tr("Ah, that was a wonderful time!", "Ach, das war eine herrliche Zeit!"),
    ),
    lesson(
        "Du brauchst nicht zu ...",
        grammar("brauchen + nicht / nur + zu"),
        mc(
            "Es ist nicht nötig, dass du kochst. → Du brauchst nicht ___.",
            "zu kochen",
            "kochen",
            "gekocht",
        ),
        mc(
            "Sie ___ nur anzurufen.",
            "brauchen",
            "müssen",
            "dürfen",
        ),
        mc(
            "Ich ___ morgen arbeiten. (obligation)",
            "muss",
            "brauche",
            "brauche zu",
        ),
        fill("Wir brauchten uns um nichts ___ kümmern.", "zu"),
        fill("Du brauchst morgen nicht früh ___. (aufstehen)", "aufzustehen"),
        fill("Sie brauchen nur das Formular ___ unterschreiben.", "zu"),
        fill("Als Kind ___ ich nie im Haushalt zu helfen. (brauchen, Präteritum)", "brauchte"),
        order("Du brauchst nur eine E-Mail zu schreiben."),
        tr(
            "You don't need to tidy up today. (du)",
            "Du brauchst heute nicht aufzuräumen.",
        ),
        tr("We didn't have to worry about anything.", "Wir brauchten uns um nichts zu kümmern."),
    ),
    lesson(
        "Bei mir war das ganz anders",
        grammar("Erinnerungen erzählen und reagieren"),
        bank(
            "Meine Großmutter erzählt: Als Kind musste ich jeden Tag bei der ___ helfen. "
            "Ich ___ nicht in die Schule zu gehen, wenn auf dem Feld viel Arbeit war. "
            "___ bekam ich nicht. Aber ich kann mich gut ___ erinnern, dass wir viel "
            "gelacht haben. Ach, das war eine ___ Zeit!",
            ["Ernte", "brauchte", "Taschengeld", "daran", "herrliche"],
            "Schminke",
            "musste",
        ),
        mc(
            "Your friend tells you about her strict parents. You answer:",
            "Bei mir war das ganz anders.",
            "Du brauchst nur anzurufen.",
            "Um Mitternacht!",
        ),
        fill("Sie ___ sich über alles auf. (aufregen)", "regt"),
        fill("Meine Eltern legen großen ___ auf Pünktlichkeit. (value)", "Wert"),
        fill("Kinder sind lange von ihren Eltern ___. (dependent)", "abhängig"),
        fill("___ arbeite ich, am Wochenende habe ich frei. (on weekdays)", "Wochentags"),
        tr("That was out of the question for us.", "Bei uns kam das nicht infrage."),
    ),
    lesson(
        "Lektion 16: Test",
        fill("Du brauchst nicht ___ kommen.", "zu"),
        fill("Sie brauchen nur ___. (anrufen)", "anzurufen"),
        mc("Ich ___ heute nicht zu arbeiten.", "brauche", "muss", "darf"),
        mc("Ich ___ heute arbeiten.", "muss", "brauche", "brauche zu"),
        fill("Wir sind uns zufällig ___. (begegnen)", "begegnet"),
        order("Als Kind brauchte ich nicht im Haushalt zu helfen."),
        tr("I can remember it well.", "Ich kann mich gut daran erinnern."),
        tr("They kissed at midnight.", "Sie haben sich um Mitternacht geküsst."),
    ),
]

LEKTION_16 = unit(
    16,
    "Wir brauchten uns um nichts zu kümmern.",
    "Erinnerungen und Generationen",
    L16_WORDS,
    L16_RULES,
    sections(L16_LESSONS, vocab_lessons(L16_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 17: Guck mal! Das ist schön!
# ============================================================================

L17_WORDS = [
    ("the painting (art form)", "die Malerei", "noun"),
    ("the painting (picture)", "das Gemälde", "noun", "Pl. die Gemälde"),
    ("the drawing", "die Zeichnung", "noun", "Pl. die Zeichnungen"),
    ("the gallery", "die Galerie", "noun", "Pl. die Galerien"),
    ("the painter", "der Maler", "noun", "f. die Malerin"),
    ("the sculptor", "der Bildhauer", "noun", "f. die Bildhauerin"),
    ("the brush", "der Pinsel", "noun", "Pl. die Pinsel"),
    ("the work (of art)", "das Werk", "noun", "Pl. die Werke"),
    ("the hill", "der Hügel", "noun", "Pl. die Hügel"),
    ("the art academy", "die Kunstakademie", "noun", "Pl. die Kunstakademien"),
    ("the biography", "die Biografie", "noun", "Pl. die Biografien"),
    ("the recognition", "die Anerkennung", "noun"),
    ("the influence", "der Einfluss", "noun", "Pl. die Einflüsse"),
    ("the prejudice", "das Vorurteil", "noun", "Pl. die Vorurteile"),
    ("the world war", "der Weltkrieg", "noun", "Pl. die Weltkriege"),
    ("the century", "das Jahrhundert", "noun", "Pl. die Jahrhunderte"),
    ("the place of birth", "der Geburtsort", "noun", "Pl. die Geburtsorte"),
    ("the year of birth", "das Geburtsjahr", "noun", "Pl. die Geburtsjahre"),
    ("the proposal (of marriage)", "der Heiratsantrag", "noun", "Pl. die Heiratsanträge"),
    ("the enemy", "der Feind", "noun", "Pl. die Feinde"),
    ("the darling / favourite", "der Liebling", "noun", "Pl. die Lieblinge"),
    ("the human right", "das Menschenrecht", "noun", "Pl. die Menschenrechte"),
    ("the lightning", "der Blitz", "noun", "Pl. die Blitze"),
    ("the thunder", "der Donner", "noun"),
    ("the thief", "der Dieb", "noun", "Pl. die Diebe"),
    ("the headline", "die Überschrift", "noun", "Pl. die Überschriften"),
    ("to exhibit", "ausstellen", "verb", "hat ausgestellt"),
    ("to recognise (achievement)", "anerkennen", "verb", "erkannte an, hat anerkannt"),
    ("to fight", "kämpfen", "verb", "kämpfen gegen + Akk."),
    ("to stand up for", "einsetzen", "verb", "sich einsetzen für + Akk."),
    ("to destroy", "zerstören", "verb", "hat zerstört"),
    ("to come into being", "entstehen", "verb", "entstand, ist entstanden"),
    ("to found", "gründen", "verb", "hat gegründet"),
    ("to teach", "unterrichten", "verb", "hat unterrichtet"),
    ("to impress", "beeindrucken", "verb", "hat beeindruckt"),
    ("to arrest", "verhaften", "verb", "hat verhaftet"),
    ("colourful", "farbig", "adjective"),
    ("with equal rights", "gleichberechtigt", "adjective"),
    ("great (spoken)", "klasse", "adjective", "Das ist klasse!"),
    ("Look! That's beautiful!", "Guck mal! Das ist schön!", "phrase"),
]

L17_RULES = [
    rule(
        "Ausdrücke mit es",
        "pronouns",
        """
Many fixed expressions use **es** without it standing for a noun:

| use | examples |
|---|---|
| weather | *Es regnet. Es blitzt und donnert. Es ist kalt.* |
| time | *Es ist spät. Es ist Sommer. Es war 1911.* |
| how someone is | *Es geht mir gut. Wie geht es Ihnen?* |
| difficult / easy | ***Es fällt** ihr **schwer**, allein zu arbeiten.* (+ Dativ) |
| it depends | *Es kommt darauf an.* |
| there is | ***Es gibt** eine neue Ausstellung.* (+ Akkusativ) |
| worthwhile | *Es lohnt sich, das Museum zu besuchen.* |

**es** can also point forward to a *dass*- or *zu*-clause: ***Es** ist schön,
dass du gekommen bist.* · ***Es** ist schwer, Nein zu sagen.*

If another word stands in position 1, this "preview" *es* disappears: *Dass du
gekommen bist, ist schön.* (But *es gibt, es geht, es regnet* keep their *es*.)
""",
        [
            "Es fällt mir schwer, diese Farben zu beschreiben.",
            "Im Museum gibt es eine neue Ausstellung.",
            "Es lohnt sich, die Galerie zu besuchen.",
            "Gestern hat es den ganzen Tag geregnet.",
        ],
    ),
    rule(
        "Eine Biografie erzählen",
        "other",
        """
**Dates:** *Sie wurde **1877** in Berlin geboren.* (never ~~in 1877~~) · *im Jahr
1911 · im 20. Jahrhundert · am 19. Februar 1877*

**Order:** *Zuerst ... · Danach / Später zog sie nach ... · In den folgenden
Jahren ... · Zur gleichen Zeit ... · Nach dem Krieg ... · Schließlich ...*

**Life events:** *geboren werden, aufwachsen, studieren, heiraten, sich trennen,
umziehen, ausstellen, sterben*

**Your opinion of a work:** *Mich beeindruckt besonders ... · Das Bild erinnert
mich an ... · Die Farben gefallen mir.*
""",
        [
            "Die Malerin wurde 1877 in Berlin geboren.",
            "Später zog sie aufs Land und malte Landschaften.",
            "Mich beeindrucken besonders die starken Farben.",
        ],
    ),
]

L17_LESSONS = [
    lesson(
        "Im Museum",
        review("das Gemälde"),
        review("die Galerie"),
        match(
            [
                ("der Maler", "malt Bilder"),
                ("der Bildhauer", "macht Figuren aus Stein"),
                ("der Pinsel", "Damit malt man."),
                ("die Galerie", "Hier kann man Bilder kaufen."),
                ("die Biografie", "die Geschichte von einem Leben"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Die Bilder der Malerin werden im Museum ...",
            "ausgestellt.",
            "verhaftet.",
            "zerstört.",
        ),
        mc(
            "Ein Bild mit vielen Farben ist ...",
            "farbig.",
            "gleichberechtigt.",
            "klasse.",
        ),
        fill("Das Bild ist im 19. ___ entstanden. (century)", "Jahrhundert"),
        fill("Die Bilder haben mich sehr ___. (beeindrucken)", "beeindruckt"),
        fill("Sie hat lange für ___ gekämpft. (recognition)", "Anerkennung"),
        tr("Look! That's beautiful!", "Guck mal! Das ist schön!"),
    ),
    lesson(
        "Es fällt mir schwer",
        grammar("Ausdrücke mit es"),
        mc("___ fällt mir schwer, früh aufzustehen.", "Es", "Er", "Das ist"),
        mc("Im Museum ___ es eine neue Ausstellung.", "gibt", "ist", "hat"),
        mc("Wie ___ es Ihnen?", "geht", "gibt", "fällt"),
        fill("Es ___ sich, die Galerie zu besuchen. (lohnen)", "lohnt"),
        fill("Es kommt ___ an. (it depends)", "darauf"),
        fill("Es blitzt und ___. (donnern)", "donnert"),
        fill("Es ist schön, ___ du gekommen bist.", "dass"),
        mc(
            "Which sentence is correct?",
            "Dass du gekommen bist, ist schön.",
            "Dass du gekommen bist, es ist schön.",
            "Es dass du gekommen bist, ist schön.",
        ),
        order("Es fällt ihr schwer, allein zu arbeiten."),
        tr("It is worth visiting the museum.", "Es lohnt sich, das Museum zu besuchen."),
    ),
    lesson(
        "Das Leben einer Malerin",
        grammar("Eine Biografie erzählen"),
        bank(
            "Die Malerin wurde ___ in Berlin geboren. Sie studierte an einer ___. Später "
            "___ sie mit einem anderen Maler einen Künstlerkreis. Ihre Bilder zeigen oft "
            "Häuser und ___. Nach dem ___ waren viele Bilder zerstört. Heute sind ihre Werke "
            "sehr berühmt.",
            ["1877", "Kunstakademie", "gründete", "Hügel", "Krieg"],
            "im 1877",
            "Feind",
        ),
        mc(
            "She was born in 1877:",
            "Sie wurde 1877 geboren.",
            "Sie wurde in 1877 geboren.",
            "Sie ist am 1877 geboren.",
        ),
        mc(
            "Die Polizei hat den ___ verhaftet.",
            "Dieb",
            "Liebling",
            "Pinsel",
        ),
        fill("Sie hat sich für die Menschenrechte ___. (einsetzen)", "eingesetzt"),
        fill("Er ___ Kunst an einer Schule. (unterrichten)", "unterrichtet"),
        fill("Das Bild ___ mich an meine Kindheit. (erinnern)", "erinnert"),
        tr("The painting was made in 1911.", "Das Gemälde ist 1911 entstanden."),
    ),
    lesson(
        "Lektion 17: Test",
        fill("___ regnet schon den ganzen Tag.", "Es"),
        fill("Es ___ ihm schwer, Nein zu sagen. (fallen)", "fällt"),
        mc("In der Stadt ___ es drei Museen.", "gibt", "sind", "haben"),
        mc("Er macht Figuren aus Stein. Er ist ...", "Bildhauer", "Maler", "Dieb"),
        fill("Die Stadt wurde im Krieg ___. (zerstören)", "zerstört"),
        order("Es lohnt sich, die Ausstellung zu sehen."),
        tr("It depends.", "Es kommt darauf an."),
        tr("The colours impress me.", "Die Farben beeindrucken mich."),
    ),
]

LEKTION_17 = unit(
    17,
    "Guck mal! Das ist schön!",
    "Kunst und Biografien",
    L17_WORDS,
    L17_RULES,
    sections(L17_LESSONS, vocab_lessons(L17_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 18: Davon halte ich nicht viel.
# ============================================================================

L18_WORDS = [
    ("the democracy", "die Demokratie", "noun", "Pl. die Demokratien"),
    ("the government", "die Regierung", "noun", "Pl. die Regierungen"),
    ("the opposition", "die Opposition", "noun"),
    ("the parliament", "das Parlament", "noun", "Pl. die Parlamente"),
    ("the party (political)", "die Partei", "noun", "Pl. die Parteien"),
    ("the chancellor", "der Bundeskanzler", "noun", "f. die Bundeskanzlerin"),
    ("the minister", "der Minister", "noun", "f. die Ministerin"),
    ("the representative", "der Vertreter", "noun", "f. die Vertreterin"),
    ("the people / nation", "das Volk", "noun", "Pl. die Völker"),
    ("the citizens' initiative", "die Bürgerinitiative", "noun", "Pl. die Bürgerinitiativen"),
    ("the demonstration", "die Demonstration", "noun", "Pl. die Demonstrationen"),
    ("the protest", "der Protest", "noun", "Pl. die Proteste"),
    ("the scandal", "der Skandal", "noun", "Pl. die Skandale"),
    ("the peace", "der Frieden", "noun"),
    ("the protection", "der Schutz", "noun", "der Klimaschutz, der Datenschutz"),
    ("the law", "das Gesetz", "noun", "Pl. die Gesetze"),
    ("the power station", "das Kraftwerk", "noun", "Pl. die Kraftwerke"),
    ("the national holiday", "der Nationalfeiertag", "noun", "Pl. die Nationalfeiertage"),
    ("the majority", "die Mehrheit", "noun", "Pl. die Mehrheiten"),
    ("the minority", "die Minderheit", "noun", "Pl. die Minderheiten"),
    ("the unemployment", "die Arbeitslosigkeit", "noun"),
    ("the equality (of rights)", "die Gleichberechtigung", "noun"),
    ("the economy", "die Wirtschaft", "noun"),
    ("the point of view", "der Standpunkt", "noun", "Pl. die Standpunkte"),
    ("the voluntary work", "das Ehrenamt", "noun", "Pl. die Ehrenämter"),
    ("the pensioner", "der Rentner", "noun", "f. die Rentnerin"),
    ("the pension", "die Rente", "noun", "Pl. die Renten"),
    (
        "the speed limit",
        "die Geschwindigkeitsbeschränkung",
        "noun",
        "Pl. die Geschwindigkeitsbeschränkungen",
    ),
    ("to govern", "regieren", "verb", "hat regiert"),
    ("to introduce", "einführen", "verb", "hat eingeführt"),
    ("to act", "handeln", "verb", "hat gehandelt"),
    ("to get involved", "engagieren", "verb", "sich engagieren für + Akk."),
    ("to agree", "zustimmen", "verb", "zustimmen + Dat., hat zugestimmt"),
    ("to contradict", "widersprechen", "verb", "widerspricht + Dat., hat widersprochen"),
    ("to vote (on)", "abstimmen", "verb", "abstimmen über + Akk."),
    ("to amount to", "betragen", "verb", "beträgt, hat betragen"),
    ("to lift / to abolish", "aufheben", "verb", "hob auf, hat aufgehoben"),
    ("to distinguish", "unterscheiden", "verb", "unterschied, hat unterschieden"),
    ("democratic", "demokratisch", "adjective"),
    ("political", "politisch", "adjective"),
    ("popular", "populär", "adjective"),
    ("voluntary (unpaid)", "ehrenamtlich", "adjective"),
    ("neither ... nor", "weder ... noch", "other"),
    ("either ... or", "entweder ... oder", "other"),
    ("admittedly ... but", "zwar ... aber", "other"),
    ("I don't think much of that.", "Davon halte ich nicht viel.", "phrase"),
]

L18_RULES = [
    rule(
        "weder ... noch, entweder ... oder, zwar ... aber",
        "sentence_structure",
        """
More **two-part connectors**:

| | meaning | example |
|---|---|---|
| **weder ... noch** | neither ... nor | *Ich wähle **weder** Partei A **noch** Partei B.* |
| **entweder ... oder** | either ... or | ***Entweder** treffen wir uns heute **oder** wir telefonieren morgen.* |
| **zwar ... aber** | admittedly ..., but | *Die Idee ist **zwar** gut, **aber** sehr teuer.* |

- *weder ... noch* is already negative: no extra *nicht* or *kein*.
- After *entweder* at the start the verb comes next (*Entweder **treffen** wir
  ...*); after *oder* normal word order.
- Comma before *aber*; no comma before *noch* or *oder* when only two words are
  joined.

Remember *sowohl ... als auch* (both) and *nicht nur ... sondern auch* from
Lektion 15.
""",
        [
            "Jugendliche interessieren sich weder für Politik noch für Nachrichten.",
            "Entweder wir fahren mit dem Rad oder wir gehen zu Fuß.",
            "Das Kraftwerk ist zwar modern, aber es macht viel Lärm.",
        ],
    ),
    rule(
        "Wortbildung: -heit, -keit, -ismus, -ist, -ant",
        "other",
        """
Endings turn words into **nouns**:

| ending | from | example | gender |
|---|---|---|---|
| **-heit** | adjective | *frei → die Freiheit, sicher → die Sicherheit* | die |
| **-keit** | adjective on -bar, -ig, -lich | *möglich → die Möglichkeit, dankbar → die Dankbarkeit* | die |
| **-ismus** | adjective / noun | *sozial → der Sozialismus, Tour → der Tourismus* | der |
| **-ist / -istin** | person | *Optimist, Journalist* | der / die |
| **-ant / -ent** | person | *demonstrieren → der Demonstrant, studieren → der Student* | der |
| **-er / -erin** | person | *Sport → der Sportler, wählen → der Wähler* | der / die |

*-heit / -keit* nouns are always **feminine**.
""",
        [
            "Freiheit und Sicherheit sind wichtig.",
            "Die Demonstranten fordern mehr Klimaschutz.",
            "Ich bin Optimistin.",
        ],
    ),
    rule(
        "Meinungen äußern, zustimmen, widersprechen",
        "other",
        """
**Opinion:** *Meiner Meinung nach ... · Ich bin der Meinung, dass ... · Ich finde,
...*

**Agreeing:** *Da bin ich ganz deiner / Ihrer Meinung. · Das sehe ich auch so.
· Ich stimme dir / Ihnen zu.*

**Disagreeing:** *Davon halte ich nicht viel. · Da bin ich anderer Meinung. · Da
muss ich widersprechen. · Das kann ich nicht nachvollziehen.*

**Both sides:** *Einerseits ..., andererseits ...*
""",
        [
            "Meiner Meinung nach sollten mehr Menschen wählen gehen.",
            "Davon halte ich nicht viel.",
            "Einerseits ist das teuer, andererseits hilft es der Umwelt.",
        ],
    ),
]

L18_LESSONS = [
    lesson(
        "Politik in Deutschland",
        review("die Regierung"),
        review("das Parlament"),
        match(
            [
                ("die Regierung", "Sie regiert das Land."),
                ("die Opposition", "die Parteien, die nicht regieren"),
                ("die Mehrheit", "mehr als die Hälfte"),
                ("die Bürgerinitiative", "Bürger kämpfen für ein Ziel."),
                ("das Ehrenamt", "Man arbeitet ohne Geld für andere."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Wer ist der Chef der Regierung in Deutschland?",
            "der Bundeskanzler",
            "der Rentner",
            "der Vertreter",
        ),
        mc(
            "Viele Menschen haben keine Arbeit. Die ___ ist hoch.",
            "Arbeitslosigkeit",
            "Gleichberechtigung",
            "Energie",
        ),
        fill("Sie ___ sich für den Klimaschutz. (engagieren)", "engagiert"),
        fill("Das Parlament hat über das Gesetz ___. (abstimmen)", "abgestimmt"),
        fill("Die Stadt hat eine Geschwindigkeitsbeschränkung ___. (einführen)", "eingeführt"),
        tr("I don't think much of that.", "Davon halte ich nicht viel."),
    ),
    lesson(
        "Weder ... noch",
        grammar("weder ... noch, entweder ... oder, zwar ... aber"),
        mc(
            "Ich lese ___ Zeitung noch sehe ich Nachrichten.",
            "weder",
            "entweder",
            "zwar",
        ),
        mc(
            "Entweder wir fahren mit dem Rad ___ wir gehen zu Fuß.",
            "oder",
            "noch",
            "aber",
        ),
        mc(
            "Die Idee ist zwar gut, ___ sehr teuer.",
            "aber",
            "oder",
            "noch",
        ),
        fill("Er wählt ___ Partei A noch Partei B. (neither)", "weder"),
        fill("___ kommst du mit, oder du bleibst zu Hause. (either)", "Entweder"),
        fill("Das Kraftwerk ist ___ modern, aber laut. (admittedly)", "zwar"),
        mc(
            "Which sentence is correct?",
            "Ich habe weder Zeit noch Geld.",
            "Ich habe weder keine Zeit noch Geld.",
            "Ich habe nicht weder Zeit noch Geld.",
        ),
        order("Jugendliche interessieren sich weder für Politik noch für Nachrichten."),
        tr(
            "Either we meet today or we phone tomorrow.",
            "Entweder treffen wir uns heute oder wir telefonieren morgen.",
        ),
    ),
    lesson(
        "Freiheit und Sicherheit",
        grammar("Wortbildung: -heit, -keit, -ismus, -ist, -ant"),
        match(
            [
                ("frei", "die Freiheit"),
                ("möglich", "die Möglichkeit"),
                ("sicher", "die Sicherheit"),
                ("dankbar", "die Dankbarkeit"),
                ("demonstrieren", "der Demonstrant"),
            ],
            "Make the noun.",
        ),
        mc("gesund → die ...", "Gesundheit", "Gesundkeit", "Gesundismus"),
        mc("ehrlich → die ...", "Ehrlichkeit", "Ehrlichheit", "Ehrlichist"),
        fill("Jemand, der immer positiv denkt, ist ein ___. (optimist)", "Optimist"),
        fill(
            "Viele Leute kommen als Touristen. Der ___ ist wichtig für die Region. (tourism)",
            "Tourismus",
        ),
        mc("die Freiheit: which article for all -heit words?", "die", "der", "das"),
        tr(
            "Peace is the most important thing.",
            "Frieden ist das Wichtigste.|Der Frieden ist das Wichtigste.",
        ),
    ),
    lesson(
        "Gelebte Demokratie",
        grammar("Meinungen äußern, zustimmen, widersprechen"),
        bank(
            "Herr Stein arbeitet ___ in einer Bürgerinitiative. Er ___ sich für mehr "
            "Radwege. ___ halten Radwege die Autofahrer auf, ___ sind sie gut für die Umwelt. "
            "Viele Bürger ___ ihm zu.",
            ["ehrenamtlich", "engagiert", "Einerseits", "andererseits", "stimmen"],
            "widersprechen",
            "zwar",
        ),
        mc(
            "To disagree politely:",
            "Da bin ich anderer Meinung.",
            "Das sehe ich auch so.",
            "Ich stimme Ihnen zu.",
        ),
        fill("Ich muss Ihnen leider ___. (contradict)", "widersprechen"),
        fill("Das kann ich gut ___. (understand: nachvollziehen)", "nachvollziehen"),
        fill("Die Rente ___ 1200 Euro im Monat. (betragen)", "beträgt"),
        fill("Die Regierung will das Verbot ___. (abolish)", "aufheben"),
        tr("I agree with you. (dir)", "Ich stimme dir zu."),
    ),
    lesson(
        "Lektion 18: Test",
        fill("Ich habe ___ Zeit noch Lust. (neither)", "weder"),
        fill("Entweder du rufst an, ___ du schreibst.", "oder"),
        fill("Das ist ___ teuer, aber gut.", "zwar"),
        mc("sicher → die ...", "Sicherheit", "Sicherkeit", "Sicherung"),
        mc("Da bin ich anderer ...", "Meinung", "Mehrheit", "Partei"),
        order("Die Idee ist zwar gut, aber sehr teuer."),
        tr(
            "The government wants to introduce a new law.",
            "Die Regierung will ein neues Gesetz einführen.",
        ),
        tr("She works voluntarily.", "Sie arbeitet ehrenamtlich."),
    ),
    lesson(
        "Modul 6: Wiederholung",
        fill("Du brauchst morgen nicht ___ kommen.", "zu"),
        fill("Sie brauchen nur hier ___. (unterschreiben)", "zu unterschreiben"),
        fill("___ fällt mir schwer, früh aufzustehen.", "Es"),
        mc("In Berlin ___ es viele Museen.", "gibt", "sind", "hat"),
        mc("Ich wähle ___ Partei A noch Partei B.", "weder", "entweder", "zwar"),
        fill("Entweder wir gehen ins Museum ___ ins Kino.", "oder"),
        bank(
            "Als Kind ___ ich nicht im Haushalt zu helfen. ___ gab immer viel zu essen. "
            "Meine Eltern waren ___ streng, aber sehr liebevoll. Ich hatte ___ Sorgen noch "
            "Probleme.",
            ["brauchte", "Es", "zwar", "weder"],
            "musste",
            "entweder",
        ),
        tr("We didn't have to worry about anything.", "Wir brauchten uns um nichts zu kümmern."),
        order("Es lohnt sich, die Ausstellung zu besuchen."),
    ),
]

LEKTION_18 = unit(
    18,
    "Davon halte ich nicht viel.",
    "Politik und Gesellschaft",
    L18_WORDS,
    L18_RULES,
    sections(L18_LESSONS, vocab_lessons(L18_WORDS, "Wörter")),
)


UNITS = [LEKTION_16, LEKTION_17, LEKTION_18]
