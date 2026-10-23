"""Modul 3 (B1.1): Lektion 7 (Kann ich Ihnen helfen?), 8 (Während andere lange
nachdenken, ...), 9 (Sport trägt zu einem größeren Wohlbefinden bei.)."""

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
# Lektion 7: Kann ich Ihnen helfen?
# ============================================================================

L7_WORDS = [
    ("the pet", "das Haustier", "noun", "Pl. die Haustiere"),
    ("the rabbit", "das Kaninchen", "noun", "Pl. die Kaninchen"),
    ("the guinea pig", "das Meerschweinchen", "noun", "Pl. die Meerschweinchen"),
    ("the hamster", "der Hamster", "noun", "Pl. die Hamster"),
    ("the animal shelter", "das Tierheim", "noun", "Pl. die Tierheime"),
    ("the pet shop", "die Tierhandlung", "noun", "Pl. die Tierhandlungen"),
    ("the vet", "der Tierarzt", "noun", "Pl. die Tierärzte, f. die Tierärztin"),
    ("the (animal) food", "das Futter", "noun"),
    ("the cage", "der Käfig", "noun", "Pl. die Käfige"),
    ("the enclosure", "das Gehege", "noun", "Pl. die Gehege"),
    ("the hay", "das Heu", "noun"),
    ("the bowl (for an animal)", "der Napf", "noun", "Pl. die Näpfe"),
    ("the fur", "das Fell", "noun", "Pl. die Felle"),
    ("the care", "die Pflege", "noun"),
    ("the advantage", "der Vorteil", "noun", "Pl. die Vorteile"),
    ("the disadvantage", "der Nachteil", "noun", "Pl. die Nachteile"),
    ("the advice (session)", "die Beratung", "noun", "Pl. die Beratungen"),
    ("the tip / hint", "der Hinweis", "noun", "Pl. die Hinweise"),
    ("the duty", "die Pflicht", "noun", "Pl. die Pflichten"),
    ("the advice", "der Rat", "noun", "einen Rat geben"),
    ("the carrot", "die Möhre", "noun", "Pl. die Möhren"),
    ("the company (being with others)", "die Gesellschaft", "noun", "also: the society"),
    ("to feed", "füttern", "verb", "hat gefüttert"),
    ("to stroke", "streicheln", "verb", "hat gestreichelt"),
    ("to brush", "bürsten", "verb", "hat gebürstet"),
    ("to look after / to care for", "pflegen", "verb", "hat gepflegt"),
    ("to eat (of animals)", "fressen", "verb", "frisst, fraß, hat gefressen"),
    ("to get (oneself) / to buy", "anschaffen", "verb", "sich etwas anschaffen"),
    ("to take into account", "berücksichtigen", "verb", "hat berücksichtigt"),
    ("to think about", "nachdenken", "verb", "nachdenken über + Akk."),
    ("to advise", "raten", "verb", "rät, riet, hat geraten"),
    ("to reckon / to count on", "rechnen", "verb", "rechnen mit + Dat."),
    ("to spend (money)", "ausgeben", "verb", "gibt aus, hat ausgegeben"),
    ("to bring up (children)", "erziehen", "verb", "erzog, hat erzogen"),
    ("to inform / to clear up", "aufklären", "verb", "hat aufgeklärt"),
    ("to try on", "anprobieren", "verb", "hat anprobiert"),
    ("easy to look after", "pflegeleicht", "adjective"),
    ("trusting / tame", "zutraulich", "adjective"),
    ("waterproof", "wasserdicht", "adjective"),
    ("first (of all)", "zunächst", "adverb"),
    ("at the moment", "momentan", "adverb"),
    ("during the day", "tagsüber", "adverb"),
    ("each / respectively", "jeweils", "adverb"),
    ("seriously", "ernsthaft", "adverb"),
    ("What do you advise me?", "Was raten Sie mir?", "phrase"),
]

L7_RULES = [
    rule(
        "Infinitiv mit zu",
        "verbs",
        """
After many verbs and expressions a second verb comes as **zu + infinitive** at
the end, usually after a comma:

| after ... | example |
|---|---|
| verbs: *versuchen, anfangen, aufhören, vergessen, raten, empfehlen, sich vorstellen* | *Ich **versuche**, mehr Zeit **zu finden**.* |
| noun + *haben*: *Lust / Zeit / Angst / Interesse haben* | *Hast du **Lust**, das Kaninchen **zu füttern**?* |
| *es ist* + adjective, *es macht Spaß* | ***Es ist wichtig**, sich vorher **zu informieren**.* |

**Separable verbs** put *zu* **between** prefix and verb: *nachdenken →
nach**zu**denken, aufräumen → auf**zu**räumen, anschaffen → an**zu**schaffen*.

**Modal verbs never take zu:** *Ich **muss** den Käfig putzen.* but *Ich
**versuche**, den Käfig **zu** putzen.*
""",
        [
            "Hast du Lust, jeden Tag die Kaninchen zu füttern?",
            "Es ist nicht leicht, so schnell eine Entscheidung zu treffen.",
            "Ich rate Ihnen, gut darüber nachzudenken.",
            "Vergiss nicht, den Napf sauber zu machen!",
        ],
    ),
    rule(
        "Ein Beratungsgespräch führen",
        "other",
        """
**The adviser:**
- *Kann ich Ihnen helfen? · Was kann ich für Sie tun?*
- *Zunächst muss ich Ihnen sagen, dass ...*
- *Sie sollten auch bedenken / berücksichtigen, dass ...*
- *Denken Sie daran, ... zu ... · Vergessen Sie nicht, ...*
- *Dann würde ich Ihnen ... empfehlen.*

**The customer:**
- *Ich möchte mich informieren. · Ich möchte mir ... anschaffen.*
- *Können Sie mir ... empfehlen? · Was raten Sie mir?*
- *Danke, das ist ein guter Hinweis. · Das muss ich mir noch überlegen.*
- *Ich habe mich entschieden: Ich nehme ...*
""",
        [
            "Ich möchte mir einen Hund anschaffen. Was raten Sie mir?",
            "Sie sollten bedenken, dass ein Hund viel Bewegung braucht.",
            "Danke, das ist ein guter Hinweis.",
        ],
    ),
]

L7_LESSONS = [
    lesson(
        "Tiere im Haus",
        review("das Haustier"),
        review("das Kaninchen"),
        match(
            [
                ("das Heu", "Das frisst das Kaninchen."),
                ("der Käfig", "Hier wohnt der Hamster."),
                ("der Napf", "Hier ist das Wasser für den Hund."),
                ("das Fell", "Das bürstet man bei der Katze."),
                ("das Tierheim", "Hier warten Tiere auf ein neues Zuhause."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Wer hilft, wenn das Tier krank ist?",
            "der Tierarzt",
            "der Hamster",
            "die Tierhandlung",
        ),
        mc(
            "Eine Katze, die gern zu Menschen kommt, ist ...",
            "zutraulich.",
            "wasserdicht.",
            "pflegeleicht.",
        ),
        fill("Die Kinder ___ die Kaninchen jeden Morgen. (füttern)", "füttern"),
        fill("Der Hund ___ am liebsten Fleisch. (fressen)", "frisst"),
        fill("Sie ___ die Katze ganz vorsichtig. (streicheln)", "streichelt"),
        tr("A guinea pig is easy to look after.", "Ein Meerschweinchen ist pflegeleicht."),
    ),
    lesson(
        "Hast du Lust, ... zu ...?",
        grammar("Infinitiv mit zu"),
        mc("Hast du Lust, mit dem Hund ___?", "rauszugehen", "zu rausgehen", "rausgehen"),
        mc("Ich muss den Käfig ___.", "putzen", "zu putzen", "putzen zu"),
        mc("Ich versuche, mehr Zeit ___.", "zu finden", "finden", "gefunden"),
        fill("Es ist wichtig, sich vorher ___ informieren.", "zu"),
        fill("Ich rate dir, gut darüber ___. (nachdenken)", "nachzudenken"),
        fill("Vergiss nicht, dein Zimmer ___! (aufräumen)", "aufzuräumen"),
        fill("Wir haben keine Zeit, ein Haustier ___. (anschaffen)", "anzuschaffen"),
        fill("Es macht Spaß, die Katze zu ___. (bürsten)", "bürsten"),
        order("Hast du Lust, die Kaninchen zu füttern?", "Build the question."),
        tr("It is not easy to decide.", "Es ist nicht leicht, sich zu entscheiden."),
        tr("I'm afraid of buying a dog.", "Ich habe Angst, einen Hund zu kaufen."),
    ),
    lesson(
        "In der Tierhandlung",
        grammar("Ein Beratungsgespräch führen"),
        bank(
            "Kann ich Ihnen ___? Ja, ich möchte mir ein Haustier ___. ___ muss ich Ihnen "
            "sagen, dass ein Hund viel Zeit braucht. Sie sollten auch ___, dass Sie tagsüber "
            "arbeiten. Danke, das ist ein guter ___. Dann ___ ich Ihnen eine Katze empfehlen.",
            ["helfen", "anschaffen", "Zunächst", "bedenken", "Hinweis", "würde"],
            "Pflicht",
            "werde",
        ),
        mc(
            "Was raten Sie mir? means:",
            "What do you advise me?",
            "What are you guessing?",
            "What do you count?",
        ),
        mc(
            "Kann ich die Jacke einmal ...?",
            "anprobieren",
            "anschaffen",
            "aufklären",
        ),
        fill("Sie müssen mit Kosten von 50 Euro im Monat ___. (rechnen)", "rechnen"),
        fill("Für das Futter ___ wir viel Geld aus. (ausgeben)", "geben"),
        fill("Die Jacke ist ___, also gut für den Regen. (waterproof)", "wasserdicht"),
        tr("I've decided: I'll take the cat.", "Ich habe mich entschieden: Ich nehme die Katze."),
    ),
    lesson(
        "Vorteile und Nachteile",
        match(
            [
                ("Ein Hund ist treu.", "Vorteil"),
                ("Ein Hund braucht viel Bewegung.", "Nachteil"),
                ("Eine Katze ist pflegeleicht.", "Vorteil"),
                ("Ein Tier kostet viel Geld.", "Nachteil"),
            ],
            "Vorteil oder Nachteil?",
        ),
        mc(
            "Ein Haustier ist eine große ___. Man muss jeden Tag für es sorgen.",
            "Pflicht",
            "Möhre",
            "Gesellschaft",
        ),
        fill("Das Kaninchen frisst gern ___. (carrots)", "Möhren"),
        fill("___ habe ich keine Zeit für ein Tier. (at the moment)", "Momentan"),
        fill("Ein Tier ist gute ___ für alte Menschen. (company)", "Gesellschaft"),
        fill("Man muss ein Tier auch ___ wie ein Kind. (bring up)", "erziehen"),
        tr("Have you thought about it seriously?", "Hast du ernsthaft darüber nachgedacht?"),
    ),
    lesson(
        "Lektion 7: Test",
        fill("Hast du Zeit, mir ___ helfen?", "zu"),
        fill("Ich habe vergessen, die Katze ___. (füttern)", "zu füttern"),
        mc("Ich darf den Hund nicht ___.", "mitbringen", "mitzubringen", "zu mitbringen"),
        fill("Es ist nicht gut, zu viel Futter ___ geben.", "zu"),
        mc(
            "Wo kann man ein Tier aus zweiter Hand bekommen?",
            "im Tierheim",
            "beim Tierarzt",
            "im Käfig",
        ),
        order("Ich rate Ihnen, eine Katze zu nehmen."),
        tr("Can I help you? (Sie)", "Kann ich Ihnen helfen?"),
        tr("The dog eats a lot.", "Der Hund frisst viel."),
    ),
]

LEKTION_7 = unit(
    7,
    "Kann ich Ihnen helfen?",
    "Haustiere und Beratung",
    L7_WORDS,
    L7_RULES,
    sections(L7_LESSONS, vocab_lessons(L7_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 8: Während andere lange nachdenken, ...
# ============================================================================

L8_WORDS = [
    ("the personality", "die Persönlichkeit", "noun", "Pl. die Persönlichkeiten"),
    ("the talent", "die Begabung", "noun", "Pl. die Begabungen"),
    ("the result", "das Ergebnis", "noun", "Pl. die Ergebnisse"),
    ("the evaluation (of a test)", "die Auswertung", "noun", "Pl. die Auswertungen"),
    ("the careers advice", "die Berufsberatung", "noun"),
    ("the choice of career", "die Berufswahl", "noun"),
    ("the craftsman / tradesman", "der Handwerker", "noun", "f. die Handwerkerin"),
    ("the nurse (male)", "der Krankenpfleger", "noun", "f. die Krankenpflegerin"),
    ("the mechanic", "der Mechaniker", "noun", "f. die Mechanikerin"),
    ("the writer", "der Schriftsteller", "noun", "f. die Schriftstellerin"),
    ("the psychologist", "der Psychologe", "noun", "den Psychologen, f. die Psychologin"),
    ("the psychology", "die Psychologie", "noun"),
    ("the freedom", "die Freiheit", "noun", "Pl. die Freiheiten"),
    ("the solution", "die Lösung", "noun", "Pl. die Lösungen"),
    ("the boredom", "die Langeweile", "noun"),
    ("the lawn", "der Rasen", "noun", "Pl. die Rasen"),
    ("helpful", "hilfsbereit", "adjective"),
    ("organised", "organisiert", "adjective"),
    ("sociable", "kontaktfreudig", "adjective"),
    ("gifted", "begabt", "adjective"),
    ("suitable", "geeignet", "adjective", "geeignet sein für + Akk."),
    ("shy", "schüchtern", "adjective"),
    ("ambitious", "ehrgeizig", "adjective"),
    ("impatient", "ungeduldig", "adjective"),
    ("logical", "logisch", "adjective"),
    ("practical (with your hands)", "handwerklich", "adjective"),
    ("to correspond to / to match", "entsprechen", "verb", "entspricht + Dat., hat entsprochen"),
    ("to type", "tippen", "verb", "hat getippt"),
    ("to build", "bauen", "verb", "hat gebaut"),
    ("to hold on to / to note down", "festhalten", "verb", "hält fest, hat festgehalten"),
    ("to count", "zählen", "verb", "hat gezählt"),
    ("to add up", "zusammenzählen", "verb", "hat zusammengezählt"),
    ("at the same time", "gleichzeitig", "adverb"),
    ("for hours", "stundenlang", "adverb"),
    ("only / just", "bloß", "adverb"),
    ("since / because", "da", "other", "Da ich gern helfe, ..."),
    ("before", "bevor", "other"),
    ("That suits me very well.", "Das passt sehr gut zu mir.", "phrase"),
    ("I wouldn't have expected that.", "Das hätte ich nicht erwartet.", "phrase"),
]

L8_RULES = [
    rule(
        "da, bevor, während",
        "sentence_structure",
        """
Three more words that start a **subordinate clause** (verb at the end):

| word | meaning | example |
|---|---|---|
| **da** | because, since (a known reason) | *Da Sie gern mit Menschen **arbeiten**, passt ein sozialer Beruf zu Ihnen.* |
| **bevor** | before (B comes after A) | *Ich frühstücke, bevor ich zur Arbeit **fahre**.* |
| **während** | while (A and B at the same time) | *Ich höre Musik, während ich **koche**.* |

- *da* is like *weil*, but often comes **first** in the sentence and gives a
  reason the listener already knows.
- *während* can also contrast two people: ***Während** andere lange
  nachdenken, entscheidet sie sofort.*
- After a fronted subordinate clause the main clause starts with the verb:
  *Bevor ich schlafe, **putze** ich die Zähne.*
""",
        [
            "Da ich gern mit den Händen arbeite, möchte ich Handwerker werden.",
            "Bevor du dich bewirbst, solltest du den Test machen.",
            "Während andere lange nachdenken, entscheidet sie sofort.",
        ],
    ),
    rule(
        "Über ein Testergebnis sprechen",
        "other",
        """
- *Der Test sagt, dass ich ein kreativer Typ bin.*
- *Das **passt** (überhaupt nicht) **zu mir**.*
- *Das **entspricht** (nicht) meinen Fähigkeiten.*
- *Für technische Berufe bin ich (nicht) **geeignet**.*
- *Das kann ich mir gut / gar nicht vorstellen.*
- *Das **hätte ich nicht erwartet**.*
- *Ich glaube eher, dass ich sozial **begabt** bin.*

Asking for advice: *Welche Stärken habe ich? · Wozu würden Sie mir raten?*
""",
        [
            "Das Ergebnis entspricht meinen Fähigkeiten.",
            "Für technische Berufe bin ich nicht geeignet.",
            "Das hätte ich nicht erwartet!",
        ],
    ),
]

L8_LESSONS = [
    lesson(
        "Welcher Beruf passt zu mir?",
        review("die Persönlichkeit"),
        review("die Begabung"),
        match(
            [
                ("der Handwerker", "arbeitet gern mit den Händen"),
                ("der Krankenpfleger", "hilft kranken Menschen"),
                ("der Mechaniker", "repariert Autos und Maschinen"),
                ("der Schriftsteller", "schreibt Bücher"),
                ("der Psychologe", "spricht mit Menschen über ihre Probleme"),
            ],
            "Who does what?",
        ),
        mc(
            "Er lernt gern neue Leute kennen. Er ist ...",
            "kontaktfreudig.",
            "schüchtern.",
            "ungeduldig.",
        ),
        mc(
            "Sie will immer die Beste sein. Sie ist ...",
            "ehrgeizig.",
            "hilfsbereit.",
            "logisch.",
        ),
        fill("Er hilft gern anderen Leuten. Er ist sehr ___. (helpful)", "hilfsbereit"),
        fill("Sie kann gut malen. Sie ist künstlerisch ___. (gifted)", "begabt"),
        fill("Am Ende habe ich alle Punkte ___. (add up)", "zusammengezählt"),
        tr("That suits me very well.", "Das passt sehr gut zu mir."),
    ),
    lesson(
        "Bevor, während, da",
        grammar("da, bevor, während"),
        mc(
            "Ich putze die Zähne, ___ ich ins Bett gehe.",
            "bevor",
            "während",
            "da",
        ),
        mc(
            "Ich höre Musik, ___ ich koche.",
            "während",
            "bevor",
            "obwohl",
        ),
        mc(
            "___ ich gern mit Menschen arbeite, möchte ich Lehrerin werden.",
            "Da",
            "Bevor",
            "Trotzdem",
        ),
        fill("___ andere lange nachdenken, entscheidet sie sofort. (while)", "Während"),
        fill("Bevor du dich bewirbst, ___ du den Test machen. (sollen)", "solltest"),
        fill("Da er nicht gern am Schreibtisch ___, wird er Gärtner. (sitzen)", "sitzt"),
        order("Während ich koche, telefoniere ich mit meiner Mutter."),
        order("Bevor ich schlafe, lese ich ein Buch."),
        tr(
            "I have breakfast before I go to work.",
            "Ich frühstücke, bevor ich zur Arbeit gehe.",
        ),
        tr(
            "Since I like working with my hands, I'd like to be a craftsman.",
            "Da ich gern mit den Händen arbeite, möchte ich Handwerker werden.",
        ),
    ),
    lesson(
        "Das Testergebnis",
        grammar("Über ein Testergebnis sprechen"),
        bank(
            "Ich habe einen Berufstest gemacht. Das ___ sagt, dass ich ein technischer Typ "
            "bin. Das ___ meinen Fähigkeiten, denn ich repariere gern Maschinen. Für soziale "
            "Berufe bin ich nicht so ___. Das hätte ich nicht ___!",
            ["Ergebnis", "entspricht", "geeignet", "erwartet"],
            "Rasen",
            "begabt",
        ),
        mc(
            "Das kann ich mir gar nicht vorstellen. means:",
            "I can't imagine that at all.",
            "I can't introduce myself.",
            "I don't want to imagine that.",
        ),
        fill("Ich habe ___ am Computer gesessen. (for hours)", "stundenlang"),
        fill("Sie kann ___ telefonieren und schreiben. (at the same time)", "gleichzeitig"),
        fill("Am Wochenende ___ er den Rasen. (mähen)", "mäht"),
        fill("Sie ___ schneller als alle anderen. (tippen)", "tippt"),
        tr("I wouldn't have expected that.", "Das hätte ich nicht erwartet."),
    ),
    lesson(
        "Lektion 8: Test",
        fill("___ ich koche, höre ich Radio. (while)", "Während"),
        fill("Ich dusche, ___ ich frühstücke. (before)", "bevor"),
        mc("___ es regnet, bleiben wir zu Hause.", "Da", "Bevor", "Trotzdem"),
        mc(
            "Er spricht nicht gern mit fremden Leuten. Er ist ...",
            "schüchtern",
            "ehrgeizig",
            "logisch",
        ),
        fill("Das ___ nicht meinen Fähigkeiten. (entsprechen)", "entspricht"),
        order("Bevor ich mich bewerbe, mache ich einen Test."),
        tr("She is suitable for the job.", "Sie ist für den Beruf geeignet."),
        tr("He built a house.", "Er hat ein Haus gebaut."),
    ),
]

LEKTION_8 = unit(
    8,
    "Während andere lange nachdenken, ...",
    "Beruf und Fähigkeiten",
    L8_WORDS,
    L8_RULES,
    sections(L8_LESSONS, vocab_lessons(L8_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 9: Sport trägt zu einem größeren Wohlbefinden bei.
# ============================================================================

L9_WORDS = [
    ("the well-being", "das Wohlbefinden", "noun"),
    ("the relaxation", "die Entspannung", "noun"),
    ("the satisfaction", "die Zufriedenheit", "noun"),
    ("the strain / burden", "die Belastung", "noun", "Pl. die Belastungen"),
    ("the prevention", "die Prävention", "noun"),
    ("the food (item)", "das Nahrungsmittel", "noun", "Pl. die Nahrungsmittel"),
    ("the health insurance", "die Krankenkasse", "noun", "Pl. die Krankenkassen"),
    ("the non-smoker", "der Nichtraucher", "noun", "f. die Nichtraucherin"),
    ("the smoker", "der Raucher", "noun", "f. die Raucherin"),
    ("the risk", "das Risiko", "noun", "Pl. die Risiken"),
    ("the addiction", "die Sucht", "noun", "Pl. die Süchte"),
    ("the behaviour", "das Verhalten", "noun"),
    ("the ban", "das Verbot", "noun", "Pl. die Verbote"),
    ("the smoking ban", "das Rauchverbot", "noun", "Pl. die Rauchverbote"),
    ("the average", "der Durchschnitt", "noun", "im Durchschnitt"),
    ("the fact", "die Tatsache", "noun", "Pl. die Tatsachen"),
    ("the relationship / ratio", "das Verhältnis", "noun", "Pl. die Verhältnisse"),
    ("the connection / context", "der Zusammenhang", "noun", "Pl. die Zusammenhänge"),
    ("the management (of a company)", "die Leitung", "noun", "die Unternehmensleitung"),
    ("the talk / presentation", "der Vortrag", "noun", "Pl. die Vorträge"),
    ("the slide", "die Folie", "noun", "Pl. die Folien"),
    ("the wellness", "die Wellness", "noun"),
    ("the outdoors", "das Freie", "noun", "im Freien"),
    ("to contribute", "beitragen", "verb", "beitragen zu + Dat., hat beigetragen"),
    ("to breathe", "atmen", "verb", "hat geatmet"),
    ("to use", "nutzen", "verb", "hat genutzt"),
    ("to harm", "schaden", "verb", "schaden + Dat., hat geschadet"),
    ("to cause", "verursachen", "verb", "hat verursacht"),
    ("to prevent", "verhindern", "verb", "hat verhindert"),
    ("to promote / to support", "fördern", "verb", "hat gefördert"),
    ("to reduce", "reduzieren", "verb", "hat reduziert"),
    ("to improve", "verbessern", "verb", "hat verbessert"),
    ("to concentrate", "konzentrieren", "verb", "sich konzentrieren auf + Akk."),
    ("to explain (in detail)", "erläutern", "verb", "hat erläutert"),
    ("to summarise", "zusammenfassen", "verb", "hat zusammengefasst"),
    ("deep", "tief", "adjective"),
    ("Thank you for listening.", "Vielen Dank fürs Zuhören.", "phrase"),
]

L9_RULES = [
    rule(
        "Komparativ und Superlativ vor dem Nomen",
        "adjectives",
        """
Before a noun, the **comparative** (*-er*) and the **superlative** (*-st*) take
the **normal adjective endings** on top:

| | der / die / das | ein / eine |
|---|---|---|
| Nom. m. | der gesünd**ere** / gesünd**este** Weg | ein gesünd**erer** Weg |
| Akk. m. | den gesünd**eren** / gesünd**esten** Weg | einen gesünd**eren** Weg |
| Dat. m./n. | dem gesünd**eren** / gesünd**esten** Weg | einem gesünd**eren** Weg |
| Nom./Akk. f. | die wichtig**ere** / wichtig**ste** Regel | eine wichtig**ere** Regel |
| Dat. f. | der wichtig**eren** / wichtig**sten** Regel | einer wichtig**eren** Regel |
| Plural | die bess**eren** / best**en** Ideen | bess**ere** Ideen |

So: comparative stem **+ er + ending**, superlative stem **+ (e)st + ending**.

*Sport trägt zu **einem größeren** Wohlbefinden bei.* (zu + Dativ)

Irregular: *gut → besser → best-*, *viel → mehr* (no ending: *mehr Zeit*),
*hoch → höher → höchst-*, *nah → näher → nächst-*.
""",
        [
            "Sport trägt zu einem größeren Wohlbefinden bei.",
            "Das ist die wichtigste Regel in unserer Firma.",
            "Wir suchen einen ruhigeren Arbeitsplatz.",
            "Mit dem besten Ergebnis gewinnt man.",
        ],
    ),
    rule(
        "Eine Präsentation halten",
        "other",
        """
**Start:** *In meiner Präsentation geht es um ... · Zuerst möchte ich ...
erläutern. · Danach zeige ich Ihnen ... · Fragen beantworte ich gern am Schluss.*

**Middle:** *Damit komme ich zum nächsten Punkt. · Aus meiner Erfahrung ... · In
meinem Heimatland ... · Ein großer Vorteil / Nachteil ist ... · Meiner Ansicht
nach ...*

**End:** *Ich fasse kurz zusammen: ... · Damit bin ich am Ende meines Vortrags.
· Haben Sie noch Fragen? · Vielen Dank fürs Zuhören / für Ihre Aufmerksamkeit.*
""",
        [
            "In meiner Präsentation geht es um das Rauchverbot.",
            "Damit komme ich zum nächsten Punkt.",
            "Vielen Dank für Ihre Aufmerksamkeit.",
        ],
    ),
    rule(
        "Entspannungsübungen: Anweisungen",
        "verbs",
        """
Instructions use the **imperative** (du, ihr or Sie):

| du | Sie |
|---|---|
| *Setz dich bequem hin.* | *Setzen Sie sich bequem hin.* |
| *Schließ die Augen.* | *Schließen Sie die Augen.* |
| *Atme tief ein und aus.* | *Atmen Sie tief ein und aus.* |
| *Entspann dein Gesicht.* | *Entspannen Sie Ihr Gesicht.* |
| *Heb langsam den Kopf.* | *Heben Sie langsam den Kopf.* |

Verbs ending in *-men, -ten, -den* keep an **-e** in the du-form: *atm**e**,
warte, rede*. The separable prefix goes to the end: *Atme tief **ein**.*
""",
        [
            "Leg dich bequem hin und schließ die Augen.",
            "Atmen Sie langsam ein und wieder aus.",
            "Entspann deine Schultern.",
        ],
    ),
]

L9_LESSONS = [
    lesson(
        "Gesund am Arbeitsplatz",
        review("das Wohlbefinden"),
        review("die Entspannung"),
        match(
            [
                ("der Nichtraucher", "Er raucht nicht."),
                ("das Rauchverbot", "Hier darf man nicht rauchen."),
                ("die Krankenkasse", "Sie bezahlt den Arzt."),
                ("die Sucht", "Man kann nicht mehr aufhören."),
                ("im Freien", "draußen, an der frischen Luft"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Zu viel Stress ist eine große ...",
            "Belastung.",
            "Zufriedenheit.",
            "Folie.",
        ),
        mc(
            "Rauchen ___ der Gesundheit.",
            "schadet",
            "fördert",
            "verbessert",
        ),
        fill("Die Firma ___ den Sport ihrer Mitarbeiter. (fördern)", "fördert"),
        fill("___ Sie tief ein und aus! (atmen)", "Atmen"),
        fill("Im ___ arbeiten die Leute acht Stunden am Tag. (average)", "Durchschnitt"),
        tr("We want to reduce stress.", "Wir wollen den Stress reduzieren."),
    ),
    lesson(
        "Ein größeres Wohlbefinden",
        grammar("Komparativ und Superlativ vor dem Nomen"),
        mc("Sport trägt zu einem ___ Wohlbefinden bei.", "größeren", "größer", "größerem"),
        mc("Das ist die ___ Regel.", "wichtigste", "wichtigsten", "wichtigster"),
        fill("Wir suchen einen ___ Arbeitsplatz. (ruhig, Komparativ)", "ruhigeren"),
        fill("Er hat das ___ Ergebnis. (gut, Superlativ)", "beste"),
        fill("Ein ___ Lebensstil hilft gegen Stress. (gesund, Komparativ)", "gesünderer"),
        fill("Wir helfen den ___ Mitarbeitern. (alt, Komparativ)", "älteren"),
        fill("Mit dem ___ Zug sind wir in zwei Stunden da. (schnell, Superlativ)", "schnellsten"),
        mc("Wir brauchen ___ Zeit für Pausen.", "mehr", "mehre", "mehrere"),
        order("Das ist der gesündeste Weg zur Arbeit."),
        tr(
            "We need a bigger room for the sport.",
            "Wir brauchen einen größeren Raum für den Sport.",
        ),
    ),
    lesson(
        "Ich möchte Ihnen unser Konzept vorstellen",
        grammar("Eine Präsentation halten"),
        match(
            [
                ("Am Anfang", "In meiner Präsentation geht es um ..."),
                ("In der Mitte", "Damit komme ich zum nächsten Punkt."),
                ("Am Ende", "Vielen Dank für Ihre Aufmerksamkeit."),
            ],
            "Which part of the talk?",
        ),
        bank(
            "In meinem ___ geht es um das Rauchverbot. Zuerst möchte ich die ___ "
            "erläutern: Rauchen ___ viele Krankheiten. Damit komme ich zum nächsten ___. "
            "Ich ___ kurz zusammen: Ein Verbot schützt alle. Haben Sie noch Fragen?",
            ["Vortrag", "Tatsachen", "verursacht", "Punkt", "fasse"],
            "Folie",
            "verhindert",
        ),
        fill("Fragen ___ ich gern am Schluss. (beantworten)", "beantworte"),
        fill("Auf dieser ___ sehen Sie die Zahlen. (slide)", "Folie"),
        fill("Ich kann mich bei Lärm nicht ___. (concentrate)", "konzentrieren"),
        tr("Thank you for listening.", "Vielen Dank fürs Zuhören."),
    ),
    lesson(
        "Entspannung im Büro",
        grammar("Entspannungsübungen: Anweisungen"),
        mc("___ dich bequem hin! (setzen)", "Setz", "Setzt", "Setzen"),
        mc("___ tief ein! (atmen, du)", "Atme", "Atm", "Atmet"),
        fill("___ Sie die Augen! (schließen)", "Schließen"),
        fill("Leg dich hin und ___ deine Schultern! (entspannen)", "entspann|entspanne"),
        fill("Atme langsam ___. (out)", "aus"),
        order("Setzen Sie sich bequem hin."),
        tr("Breathe deeply. (du)", "Atme tief."),
    ),
    lesson(
        "Lektion 9: Test",
        fill("Das ist die ___ Regel von allen. (wichtig)", "wichtigste"),
        fill("Wir suchen eine ___ Wohnung. (groß, Komparativ)", "größere"),
        mc("Er gibt den ___ Mitarbeitern frei.", "älteren", "älter", "älterer"),
        mc("Bewegung trägt zur Gesundheit ...", "bei", "mit", "zu"),
        fill("Zu viel Zucker ___ den Zähnen. (schaden)", "schadet"),
        order("Sport trägt zu einem größeren Wohlbefinden bei."),
        tr("We want to improve the behaviour.", "Wir wollen das Verhalten verbessern."),
        tr("Close your eyes. (Sie)", "Schließen Sie die Augen."),
    ),
    lesson(
        "Modul 3: Wiederholung",
        fill("Hast du Lust, ins Tierheim ___ gehen?", "zu"),
        fill("Ich habe vergessen, dich ___. (anrufen)", "anzurufen"),
        mc("___ ich zur Arbeit fahre, frühstücke ich.", "Bevor", "Während", "Da"),
        mc("___ es kalt ist, bleiben wir drinnen.", "Da", "Bevor", "Obwohl"),
        fill("Das ist der ___ Weg. (kurz, Superlativ)", "kürzeste"),
        fill("Wir brauchen einen ___ Plan. (gut, Komparativ)", "besseren"),
        bank(
            "___ ich mir ein Haustier anschaffe, möchte ich mich gut informieren. Ich habe "
            "keine Zeit, jeden Tag mit einem Hund ___ gehen. ___ ich viel arbeite, passt eine "
            "Katze besser. Sie ist das ___ Tier für mich.",
            ["Bevor", "spazieren zu", "Da", "beste"],
            "Während",
            "zu spazieren",
        ),
        tr("It's important to move a lot.", "Es ist wichtig, sich viel zu bewegen."),
        order("Während ich koche, höre ich Musik."),
    ),
]

LEKTION_9 = unit(
    9,
    "Sport trägt zu einem größeren Wohlbefinden bei.",
    "Gesundheit am Arbeitsplatz",
    L9_WORDS,
    L9_RULES,
    sections(L9_LESSONS, vocab_lessons(L9_WORDS, "Wörter")),
)


UNITS = [LEKTION_7, LEKTION_8, LEKTION_9]
