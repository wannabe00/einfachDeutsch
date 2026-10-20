"""Modul 7 (B1.2): Lektion 19 (Je älter ich wurde, desto ...), 20 (Die anderen
werden es dir danken!), 21 (Vorher muss natürlich fleißig geübt werden.)."""

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
# Lektion 19: Je älter ich wurde, desto ...
# ============================================================================

L19_WORDS = [
    ("the tourism", "der Tourismus", "noun"),
    ("the heath", "die Heide", "noun", "die Lüneburger Heide"),
    ("the bog / moor", "das Moor", "noun", "Pl. die Moore"),
    ("the stream", "der Bach", "noun", "Pl. die Bäche"),
    ("the field (farmland)", "der Acker", "noun", "Pl. die Äcker"),
    ("the herd", "die Herde", "noun", "Pl. die Herden"),
    ("the sheep", "das Schaf", "noun", "Pl. die Schafe"),
    ("the honey", "der Honig", "noun"),
    ("the bee", "die Biene", "noun", "Pl. die Bienen"),
    ("the grass", "das Gras", "noun", "Pl. die Gräser"),
    ("the cattle", "das Vieh", "noun"),
    ("the wool", "die Wolle", "noun"),
    ("the agriculture", "die Landwirtschaft", "noun"),
    ("the nature conservation", "der Naturschutz", "noun"),
    ("the season (tourist)", "die Saison", "noun", "Pl. die Saisons"),
    ("the tradition", "die Tradition", "noun", "Pl. die Traditionen"),
    ("the press conference", "die Pressekonferenz", "noun", "Pl. die Pressekonferenzen"),
    ("the follow-up question", "die Nachfrage", "noun", "Pl. die Nachfragen"),
    ("the speaker (giving a talk)", "der Redner", "noun", "f. die Rednerin"),
    ("the public", "die Öffentlichkeit", "noun"),
    ("the carnival", "der Fasching", "noun"),
    ("the apricot", "die Aprikose", "noun", "Pl. die Aprikosen"),
    ("to happen / to take place", "ereignen", "verb", "sich ereignen, hat sich ereignet"),
    ("to represent / to depict", "darstellen", "verb", "hat dargestellt"),
    ("to heat", "heizen", "verb", "hat geheizt"),
    ("to afford", "leisten", "verb", "sich etwas leisten"),
    ("to drive (cattle) / to do (sport)", "treiben", "verb", "trieb, hat getrieben"),
    ("flat", "flach", "adjective"),
    ("employed (working)", "berufstätig", "adjective"),
    ("grateful", "dankbar", "adjective"),
    ("fine", "fein", "adjective"),
    ("tolerant", "tolerant", "adjective"),
    ("free (of charge) / in vain", "umsonst", "adverb"),
    ("the same (thing)", "dasselbe", "other"),
    ("however", "jedoch", "adverb"),
    ("the more ... the more", "je ... desto", "other", "also: je ... umso"),
    ("I'd have one more question about that.", "Ich hätte dazu noch eine Frage.", "phrase"),
]

L19_RULES = [
    rule(
        "je ... desto / umso",
        "sentence_structure",
        """
**je ... desto** (or **je ... umso**) = the more ... the more. Both parts take a
**comparative**:

| je + comparative ... verb at the END | desto / umso + comparative + VERB ... |
|---|---|
| ***Je** länger ich **übe**,* | ***desto** sicherer **spreche** ich.* |
| ***Je** älter sie **wurde**,* | ***umso** mehr **reiste** sie.* |
| ***Je** mehr Touristen **kommen**,* | ***desto** voller **wird** die Heide.* |

- The *je*-part is a subordinate clause (verb at the end).
- The *desto*-part is a main clause: the comparative comes first, then the verb.
- *mehr* and *weniger* work too: *Je weniger ich schlafe, desto müder bin ich.*
""",
        [
            "Je älter ich wurde, desto mehr gefiel mir die Heide.",
            "Je früher wir losfahren, umso weniger Stau gibt es.",
            "Je mehr Schafe es gibt, desto schöner bleibt die Landschaft.",
        ],
    ),
    rule(
        "Modalpartikeln: denn, doch, ja, eigentlich",
        "other",
        """
These small words don't change the facts, but they change the **tone**:

| particle | effect | example |
|---|---|---|
| **denn** | interest in a question | *Was ist **denn** passiert?* |
| **doch** | encouragement, or "you know that" | *Kommen Sie **doch** mit! · Das weißt du **doch**!* |
| **ja** | surprise, shared knowledge | *Das ist **ja** interessant! · Du bist **ja** schon da!* |
| **eigentlich** | softens, asks by the way | *Was bedeutet das **eigentlich**?* |

They stand in the middle of the sentence, after the verb and usually after the
pronoun. Don't translate them word for word.
""",
        [
            "Wie meinen Sie das denn?",
            "Das ist ja eine schöne Landschaft!",
            "Wie viele Schafe gibt es eigentlich in der Heide?",
        ],
    ),
    rule(
        "Fragen nach einer Präsentation",
        "other",
        """
- *Darf ich Sie etwas fragen? · Ich hätte dazu noch eine Frage.*
- *Ich würde gern wissen, ... · Wissen Sie vielleicht, ...?*
- *Könnten Sie das bitte näher erklären? · Was bedeutet das denn genau?*
- *Vielen Dank für die Antwort.*

The speaker: *Gute Frage! · Das kann ich Ihnen gern erklären. · Darauf komme ich
gleich noch.*
""",
        [
            "Ich hätte dazu noch eine Frage.",
            "Könnten Sie das bitte näher erklären?",
            "Ich würde gern wissen, wie viele Touristen jedes Jahr kommen.",
        ],
    ),
]

L19_LESSONS = [
    lesson(
        "Die Lüneburger Heide",
        review("die Heide"),
        review("das Schaf"),
        match(
            [
                ("die Biene", "Sie macht Honig."),
                ("das Schaf", "Es gibt uns Wolle."),
                ("der Bach", "ein kleiner Fluss"),
                ("das Moor", "nasser, weicher Boden"),
                ("die Herde", "viele Tiere zusammen"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Die Landschaft hat keine Berge. Sie ist ...",
            "flach.",
            "dankbar.",
            "berufstätig.",
        ),
        mc(
            "Im Sommer kommen die meisten Touristen. Dann ist ...",
            "Saison.",
            "Fasching.",
            "Vieh.",
        ),
        fill("Der Eintritt ist ___: Man muss nichts bezahlen. (free)", "umsonst"),
        fill("Die Bauern ___ die Herde auf die Wiese. (treiben)", "treiben"),
        fill("Ein Hotel können wir uns nicht ___. (afford)", "leisten"),
        tr(
            "Nature conservation is important for tourism.",
            "Der Naturschutz ist wichtig für den Tourismus.",
        ),
    ),
    lesson(
        "Je älter, desto ...",
        grammar("je ... desto / umso"),
        mc(
            "Which sentence is correct?",
            "Je länger ich übe, desto sicherer spreche ich.",
            "Je länger ich übe, desto sicherer ich spreche.",
            "Je ich länger übe, desto spreche ich sicherer.",
        ),
        mc(
            "Je mehr Touristen kommen, ___ voller wird es.",
            "desto",
            "dann",
            "als",
        ),
        fill("Je ___ wir losfahren, desto weniger Stau gibt es. (früh)", "früher"),
        fill("Je älter ich wurde, desto ___ gefiel mir die Heide. (viel)", "mehr"),
        fill("Je weniger ich schlafe, umso ___ bin ich. (müde)", "müder"),
        fill("Je mehr man reist, ___ toleranter wird man. (the more: umso)", "umso"),
        order("Je früher wir anfangen, desto schneller sind wir fertig."),
        tr(
            "The more I learn, the better I understand.",
            "Je mehr ich lerne, desto besser verstehe ich.|Je mehr ich lerne, umso besser verstehe ich.",
        ),
    ),
    lesson(
        "Was ist denn passiert?",
        grammar("Modalpartikeln: denn, doch, ja, eigentlich"),
        match(
            [
                ("Was ist denn passiert?", "interested question"),
                ("Kommen Sie doch mit!", "encouragement"),
                ("Das ist ja interessant!", "surprise"),
                ("Was bedeutet das eigentlich?", "a softened question"),
            ],
            "What does the particle do?",
        ),
        mc("Wie meinen Sie das ___?", "denn", "ja", "doch"),
        mc("Das weißt du ___!", "doch", "denn", "eigentlich"),
        fill("Du bist ___ schon da! (surprise)", "ja"),
        fill("Wo wohnst du ___? (by the way)", "eigentlich"),
        fill("Probier ___ mal den Honig! (encouragement)", "doch"),
        tr("That is interesting!", "Das ist ja interessant!"),
    ),
    lesson(
        "Die Pressekonferenz",
        grammar("Fragen nach einer Präsentation"),
        bank(
            "Auf der ___ stellt der Verein ein neues Projekt vor. Der ___ erklärt, wie man die "
            "Heide schützen will. Danach gibt es ___. Eine Journalistin sagt: Ich hätte ___ "
            "noch eine Frage. Wie viele ___ gibt es jedes Jahr?",
            ["Pressekonferenz", "Redner", "Nachfragen", "dazu", "Übernachtungen"],
            "Herde",
            "denn",
        ),
        mc(
            "Polite way to ask after a talk:",
            "Darf ich Sie etwas fragen?",
            "Was willst du?",
            "Erklären Sie das sofort!",
        ),
        fill("Das Bild ___ eine alte Tradition dar. (darstellen)", "stellt"),
        fill("Hier hat sich letztes Jahr ein Unfall ___. (ereignen)", "ereignet"),
        fill("Die Idee ist gut, ___ ist sie teuer. (however)", "jedoch"),
        fill("Wir haben ___ Zimmer wie letztes Jahr. (the same)", "dasselbe"),
        tr(
            "Could you explain that in more detail? (Sie)",
            "Könnten Sie das bitte näher erklären?|Könnten Sie das näher erklären?",
        ),
    ),
    lesson(
        "Lektion 19: Test",
        fill("Je mehr ich übe, ___ besser werde ich.", "desto|umso"),
        fill("Je ___ es ist, desto mehr Leute kommen. (warm)", "wärmer"),
        mc("Was machst du ___ hier? (interest)", "denn", "doch", "jedoch"),
        mc("Bienen machen ...", "Honig", "Wolle", "Gras"),
        fill("Ich bin dir sehr ___. (grateful)", "dankbar"),
        order("Je älter ich wurde, desto mehr reiste ich."),
        tr("I'd have one more question about that.", "Ich hätte dazu noch eine Frage."),
        tr("We heat with wood.", "Wir heizen mit Holz."),
    ),
]

LEKTION_19 = unit(
    19,
    "Je älter ich wurde, desto ...",
    "Landschaft und Tourismus",
    L19_WORDS,
    L19_RULES,
    sections(L19_LESSONS, vocab_lessons(L19_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 20: Die anderen werden es dir danken!
# ============================================================================

L20_WORDS = [
    ("the mountain hut", "die Hütte", "noun", "die Berghütte, Pl. die Hütten"),
    ("the hut keeper / landlord", "der Wirt", "noun", "der Hüttenwirt, f. die Wirtin"),
    ("the mountaineer", "der Bergsteiger", "noun", "f. die Bergsteigerin"),
    ("the dormitory", "das Lager", "noun", "Pl. die Lager"),
    ("the sleeping bag", "der Schlafsack", "noun", "Pl. die Schlafsäcke"),
    ("the headlamp", "die Stirnlampe", "noun", "Pl. die Stirnlampen"),
    ("the earplug", "der Ohrstöpsel", "noun", "Pl. die Ohrstöpsel"),
    ("the mattress", "die Matratze", "noun", "Pl. die Matratzen"),
    ("the boot", "der Stiefel", "noun", "Pl. die Stiefel"),
    ("the stone", "der Stein", "noun", "Pl. die Steine"),
    ("the valley", "das Tal", "noun", "Pl. die Täler"),
    ("the summit", "der Gipfel", "noun", "Pl. die Gipfel"),
    ("the dirt", "der Dreck", "noun"),
    ("the snack bar", "der Imbiss", "noun", "Pl. die Imbisse"),
    ("the mortal danger", "die Lebensgefahr", "noun"),
    ("the accident / disaster", "das Unglück", "noun", "Pl. die Unglücke"),
    ("the guestbook", "das Gästebuch", "noun", "Pl. die Gästebücher"),
    ("the consideration", "die Rücksicht", "noun", "Rücksicht nehmen auf + Akk."),
    ("the regulation", "die Vorschrift", "noun", "Pl. die Vorschriften"),
    ("the community", "die Gemeinschaft", "noun", "Pl. die Gemeinschaften"),
    ("the well-being / good", "das Wohl", "noun", "zum Wohl der Gäste"),
    ("the purpose", "der Zweck", "noun", "Pl. die Zwecke"),
    ("the result", "das Resultat", "noun", "Pl. die Resultate"),
    ("the difficulty", "die Schwierigkeit", "noun", "Pl. die Schwierigkeiten"),
    ("the reward", "die Belohnung", "noun", "Pl. die Belohnungen"),
    ("to have an accident", "verunglücken", "verb", "ist verunglückt"),
    ("to take off (clothes)", "ausziehen", "verb", "zog aus, hat ausgezogen"),
    ("to say Sie to someone", "siezen", "verb", "hat gesiezt"),
    ("to take care of / to ensure", "sorgen", "verb", "sorgen für + Akk."),
    ("to serve (a purpose)", "dienen", "verb", "hat gedient"),
    ("to be valid / to apply", "gelten", "verb", "es gilt, galt, hat gegolten"),
    ("to regulate", "regeln", "verb", "hat geregelt"),
    ("to demand", "verlangen", "verb", "hat verlangt"),
    ("to be enough", "ausreichen", "verb", "hat ausgereicht"),
    ("to deal with", "umgehen", "verb", "umgehen mit + Dat., ist umgegangen"),
    ("steep", "steil", "adjective"),
    ("considerate", "rücksichtsvoll", "adjective"),
    ("sensible / meaningful", "sinnvoll", "adjective"),
    ("on principle / basically", "grundsätzlich", "adverb"),
    ("constantly", "dauernd", "adverb"),
    ("nowhere", "nirgends", "adverb"),
    ("by (doing)", "indem", "other"),
    ("so that (as a result)", "sodass", "other"),
    ("The others will thank you for it!", "Die anderen werden es dir danken!", "phrase"),
]

L20_RULES = [
    rule(
        "indem und sodass",
        "sentence_structure",
        """
Two subordinate-clause words (verb at the **end**):

**indem** = **by** doing something (how? the method):
- *Du schützt die Natur, **indem** du deinen Müll **mitnimmst**.*
- *Man spart Energie, **indem** man das Licht **ausschaltet**.*

**sodass** = **so that / with the result that** (what happened because of it):
- *Es schneite stark, **sodass** wir in der Hütte bleiben **mussten**.*
- *Er war leise, **sodass** niemand **aufwachte**.*

**so ... dass** stresses an adjective: *Der Weg war **so** steil, **dass** wir
langsam gehen mussten.*

Don't confuse *sodass* (result, it happened) with *damit* (purpose, the goal):
*Ich nehme Ohrstöpsel mit, **damit** ich schlafen kann.*
""",
        [
            "Ihr helft dem Wirt, indem ihr eure Teller selbst abräumt.",
            "Der Weg war vereist, sodass niemand weitergehen konnte.",
            "Es war so laut, dass ich nicht schlafen konnte.",
        ],
    ),
    rule(
        "Regeln bewerten",
        "other",
        """
- *Diese Regel finde ich sinnvoll, weil ... · Das ist für mich
  selbstverständlich.*
- *Ich lege großen Wert darauf, dass ... · Die Hauptsache ist, dass ...*
- *Darüber kann man streiten. · Das überzeugt mich nicht.*
- *Damit bin ich (nicht) einverstanden.*

**In a guestbook:** *Vielen Dank für die Gastfreundschaft! · Es hat uns sehr gut
gefallen. · Besonders schön war ... · Nur ... war ein bisschen schade. · Wir
kommen gern wieder!*
""",
        [
            "Die Nachtruhe finde ich sinnvoll, weil alle früh aufstehen.",
            "Damit bin ich nicht einverstanden.",
            "Vielen Dank für die Gastfreundschaft, wir kommen gern wieder!",
        ],
    ),
]

L20_LESSONS = [
    lesson(
        "Auf der Hütte",
        review("die Hütte"),
        review("der Schlafsack"),
        match(
            [
                ("der Hüttenwirt", "Er kocht und kümmert sich um die Gäste."),
                ("das Lager", "Hier schlafen viele Leute in einem Raum."),
                ("die Stirnlampe", "Licht auf dem Kopf"),
                ("der Ohrstöpsel", "Damit hört man nichts."),
                ("der Gipfel", "der höchste Punkt vom Berg"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Der Weg geht stark nach oben. Er ist ...",
            "steil.",
            "sinnvoll.",
            "rücksichtsvoll.",
        ),
        mc(
            "Bitte ___ Sie die Stiefel vor der Tür aus!",
            "ziehen",
            "dienen",
            "gelten",
        ),
        fill("Im Winter ist ein Bergsteiger ___. (verunglücken)", "verunglückt"),
        fill("Der Wirt ___ für Ruhe in der Nacht. (sorgen)", "sorgt"),
        fill("Auf der Hütte ___ man sich nicht: Alle sagen du. (siezen)", "siezt"),
        tr("The view from the summit is great.", "Die Aussicht vom Gipfel ist toll."),
    ),
    lesson(
        "Indem du ...",
        grammar("indem und sodass"),
        mc(
            "Du schützt die Natur, ___ du deinen Müll mitnimmst.",
            "indem",
            "sodass",
            "obwohl",
        ),
        mc(
            "Es schneite stark, ___ wir in der Hütte bleiben mussten.",
            "sodass",
            "indem",
            "damit",
        ),
        mc(
            "Which sentence is correct?",
            "Man spart Strom, indem man das Licht ausschaltet.",
            "Man spart Strom, indem man schaltet das Licht aus.",
            "Man spart Strom, indem das Licht man ausschaltet.",
        ),
        fill("Der Weg war ___ steil, dass wir langsam gingen.", "so"),
        fill("Er war leise, ___ niemand aufwachte. (so that)", "sodass"),
        fill("Ihr helft dem Wirt, ___ ihr die Teller abräumt. (by)", "indem"),
        order("Wir lernen Rücksicht, indem wir die Regeln beachten."),
        tr(
            "It rained a lot, so that we stayed in the hut.",
            "Es regnete viel, sodass wir in der Hütte blieben.|Es hat viel geregnet, sodass wir in der Hütte geblieben sind.",
        ),
    ),
    lesson(
        "Unsere Hüttenregeln",
        grammar("Regeln bewerten"),
        bank(
            "Unsere Hüttenregeln: Ab 22 Uhr ist Nachtruhe. Bitte nehmt ___ auf die anderen "
            "Gäste. Zieht die ___ vor der Tür aus. Nehmt euren Müll wieder mit ins ___. Die "
            "Regeln ___ für alle. Die anderen werden es euch ___!",
            ["Rücksicht", "Stiefel", "Tal", "gelten", "danken"],
            "Belohnung",
            "dienen",
        ),
        mc(
            "Diese Regel finde ich ___, weil alle früh aufstehen.",
            "sinnvoll",
            "steil",
            "nirgends",
        ),
        mc(
            "In a guestbook you write:",
            "Vielen Dank für die Gastfreundschaft!",
            "Das überzeugt mich nicht.",
            "Ich verlange mein Geld zurück!",
        ),
        fill("Ich habe den Schlüssel ___ gefunden. (nowhere)", "nirgends"),
        fill("Die Kinder streiten ___. (constantly)", "dauernd"),
        fill("Eine Decke ___ nicht, es ist zu kalt. (ausreichen)", "reicht"),
        tr("I don't agree with that.", "Damit bin ich nicht einverstanden."),
    ),
    lesson(
        "Lektion 20: Test",
        fill("Man spart Wasser, ___ man kurz duscht. (by)", "indem"),
        fill("Es war neblig, ___ wir nichts sehen konnten. (so that)", "sodass"),
        mc("Der Berg war ___ hoch, dass wir müde waren.", "so", "sodass", "indem"),
        mc("Wer kocht auf der Hütte?", "der Wirt", "der Gipfel", "der Imbiss"),
        fill("Die Regeln ___ für alle Gäste. (gelten)", "gelten"),
        order("Es schneite stark, sodass wir bleiben mussten."),
        tr("The others will thank you for it! (dir)", "Die anderen werden es dir danken!"),
        tr("We'll gladly come again.", "Wir kommen gern wieder."),
    ),
]

LEKTION_20 = unit(
    20,
    "Die anderen werden es dir danken!",
    "In den Bergen: Regeln auf der Hütte",
    L20_WORDS,
    L20_RULES,
    sections(L20_LESSONS, vocab_lessons(L20_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 21: Vorher muss natürlich fleißig geübt werden.
# ============================================================================

L21_WORDS = [
    ("the tour (of a band)", "die Tournee", "noun", "Pl. die Tourneen"),
    ("the rehearsal", "die Probe", "noun", "Pl. die Proben"),
    ("the performance / appearance", "der Auftritt", "noun", "Pl. die Auftritte"),
    ("the organiser", "der Veranstalter", "noun", "f. die Veranstalterin"),
    ("the poster", "das Plakat", "noun", "Pl. die Plakate"),
    ("the loudspeaker", "der Lautsprecher", "noun", "Pl. die Lautsprecher"),
    ("the volume", "die Lautstärke", "noun"),
    ("the cable", "das Kabel", "noun", "Pl. die Kabel"),
    ("the drums", "das Schlagzeug", "noun", "Pl. die Schlagzeuge"),
    ("the atmosphere", "die Atmosphäre", "noun"),
    ("the reception", "der Empfang", "noun", "Pl. die Empfänge"),
    ("the cloakroom", "die Garderobe", "noun", "Pl. die Garderoben"),
    ("the failure", "der Misserfolg", "noun", "Pl. die Misserfolge"),
    ("the (musical) note / mark", "die Note", "noun", "Pl. die Noten"),
    ("the studio", "das Studio", "noun", "Pl. die Studios"),
    ("the pleasure", "das Vergnügen", "noun", "Viel Vergnügen!"),
    ("the city walk", "der Stadtrundgang", "noun", "Pl. die Stadtrundgänge"),
    ("the pedestrian zone", "die Fußgängerzone", "noun", "Pl. die Fußgängerzonen"),
    ("the exit (motorway)", "die Ausfahrt", "noun", "Pl. die Ausfahrten"),
    ("the building", "das Gebäude", "noun", "Pl. die Gebäude"),
    ("the indoor pool", "das Hallenbad", "noun", "Pl. die Hallenbäder"),
    ("the multi-storey car park", "das Parkhaus", "noun", "Pl. die Parkhäuser"),
    ("the stadium", "das Stadion", "noun", "Pl. die Stadien"),
    ("the surrounding area", "die Umgebung", "noun"),
    ("the restaurant (pub)", "die Gaststätte", "noun", "Pl. die Gaststätten"),
    ("the state / condition", "der Zustand", "noun", "Pl. die Zustände"),
    ("the comparison", "der Vergleich", "noun", "Pl. die Vergleiche"),
    ("to rehearse", "proben", "verb", "hat geprobt"),
    ("to perform", "auftreten", "verb", "tritt auf, ist aufgetreten"),
    ("to miss (an opportunity)", "versäumen", "verb", "hat versäumt"),
    ("to distribute / to hand out", "verteilen", "verb", "hat verteilt"),
    ("to sort / to arrange", "ordnen", "verb", "hat geordnet"),
    ("to look up (in a book)", "nachschlagen", "verb", "schlägt nach, hat nachgeschlagen"),
    ("to be silent", "schweigen", "verb", "schwieg, hat geschwiegen"),
    ("unique / one-off", "einmalig", "adjective"),
    ("inside / within", "innerhalb", "other", "innerhalb + Genitiv"),
    ("around", "um ... herum", "other", "um + Akk. ... herum"),
    ("by the way", "übrigens", "adverb"),
    ("as long as", "solange", "other"),
    ("the day after tomorrow", "übermorgen", "adverb"),
    (
        "Beforehand there must of course be a lot of practice.",
        "Vorher muss natürlich fleißig geübt werden.",
        "phrase",
    ),
]

L21_RULES = [
    rule(
        "Passiv mit Modalverb",
        "verbs",
        """
You know the passive: *Die Bühne **wird aufgebaut**.* With a modal verb, the
modal is in **position 2**, and **Partizip II + werden** go to the end:

| active (man) | passive with modal |
|---|---|
| *Man muss die Bühne aufbauen.* | *Die Bühne **muss aufgebaut werden**.* |
| *Man soll die Plakate verteilen.* | *Die Plakate **sollen verteilt werden**.* |
| *Man kann die Karten online kaufen.* | *Die Karten **können** online **gekauft werden**.* |

In a subordinate clause the modal goes to the very end: *..., weil die
Instrumente noch **geprüft werden müssen**.*

**Without a subject** (impersonal passive): *Vorher **muss** fleißig **geübt
werden**.* · *Vor dem Konzert **wird geprobt**.*
""",
        [
            "Vorher muss natürlich fleißig geübt werden.",
            "Die Lautsprecher müssen noch aufgebaut werden.",
            "Die Karten können an der Kasse gekauft werden.",
        ],
    ),
    rule(
        "innerhalb, außerhalb, entlang, um ... herum",
        "cases",
        """
Prepositions for **place** (and some for **time**):

| preposition | case | place | time |
|---|---|---|---|
| **innerhalb** | Genitiv | *innerhalb **der** Stadt* | *innerhalb **einer** Woche* |
| **außerhalb** | Genitiv | *außerhalb **des** Zentrums* | *außerhalb **der** Öffnungszeiten* |
| **entlang** (after the noun) | Akkusativ | *den Fluss **entlang*** | |
| **an ... entlang** | Dativ | ***am** Fluss **entlang*** | |
| **um ... herum** | Akkusativ | ***um den** See **herum*** | |

*innerhalb* and *außerhalb* can mean **space** or **time**: *innerhalb des
Parks* (in the park) vs *innerhalb einer Stunde* (within an hour).
""",
        [
            "Wir sind den Bach entlang gewandert.",
            "Um den Platz herum gibt es viele Cafés.",
            "Das Stadion liegt außerhalb der Stadt.",
            "Die Karten waren innerhalb einer Stunde verkauft.",
        ],
    ),
    rule(
        "Einen Ort empfehlen",
        "other",
        """
- *... ist immer einen Besuch wert. · Das kann ich nur empfehlen.*
- *Die Stadt hat einiges zu bieten. · Es gibt ein großes kulturelles Angebot.*
- *Besonders beeindruckt hat mich ... · Am besten hat mir ... gefallen.*
- *Das war ein einmaliges Erlebnis. · Es hat sich gelohnt.*
- *Wir waren begeistert von ...*
""",
        [
            "Die Altstadt ist immer einen Besuch wert.",
            "Besonders beeindruckt hat mich das alte Stadion.",
            "Das Konzert war ein einmaliges Erlebnis.",
        ],
    ),
]

L21_LESSONS = [
    lesson(
        "Die Band auf Tournee",
        review("die Tournee"),
        review("der Auftritt"),
        match(
            [
                ("die Probe", "Die Band übt vor dem Konzert."),
                ("der Veranstalter", "Er organisiert das Konzert."),
                ("das Plakat", "Hier sieht man den Termin vom Konzert."),
                ("die Garderobe", "Hier gibt man die Jacke ab."),
                ("der Lautsprecher", "Damit ist die Musik laut."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Die Band ___ heute Abend im Stadion auf.",
            "tritt",
            "probt",
            "versäumt",
        ),
        mc(
            "Das Konzert war super! Die ___ war toll.",
            "Atmosphäre",
            "Ausfahrt",
            "Garderobe",
        ),
        fill("Vor dem Konzert ___ die Band drei Stunden. (proben)", "probt"),
        fill("Ich habe das Konzert leider ___. (versäumen)", "versäumt"),
        fill("Viel ___ beim Konzert! (pleasure)", "Vergnügen"),
        tr("The tour was a great success.", "Die Tournee war ein großer Erfolg."),
    ),
    lesson(
        "Die Bühne muss aufgebaut werden",
        grammar("Passiv mit Modalverb"),
        mc(
            "Man muss die Bühne aufbauen. → Die Bühne muss ...",
            "aufgebaut werden.",
            "aufbauen werden.",
            "werden aufgebaut.",
        ),
        mc(
            "Which sentence is correct?",
            "Die Karten können online gekauft werden.",
            "Die Karten können online werden gekauft.",
            "Die Karten werden online gekauft können.",
        ),
        fill("Die Plakate sollen morgen ___ werden. (verteilen)", "verteilt"),
        fill("Die Instrumente müssen noch geprüft ___.", "werden"),
        fill("Vorher muss fleißig ___ werden. (üben)", "geübt"),
        fill("..., weil die Kabel noch geordnet werden ___. (müssen)", "müssen"),
        fill("Vor dem Konzert ___ geprobt. (passive, Präsens)", "wird"),
        order("Die Lautsprecher müssen noch aufgebaut werden."),
        tr(
            "The tickets must be sold today.",
            "Die Karten müssen heute verkauft werden.|Die Tickets müssen heute verkauft werden.",
        ),
    ),
    lesson(
        "Am Fluss entlang",
        grammar("innerhalb, außerhalb, entlang, um ... herum"),
        mc("Wir sind den Bach ___ gewandert.", "entlang", "herum", "innerhalb"),
        mc("Um den See ___ gibt es einen Weg.", "herum", "entlang", "außerhalb"),
        mc("Das Stadion liegt außerhalb ___ Stadt.", "der", "die", "dem"),
        fill("Die Karten waren ___ einer Stunde verkauft. (within)", "innerhalb"),
        fill("Wir sind am Fluss ___ gefahren. (along)", "entlang"),
        fill("Außerhalb ___ Zentrums gibt es ein Parkhaus. (das)", "des"),
        fill("___ den Platz herum sind viele Gaststätten.", "Um"),
        order("Das Hallenbad liegt außerhalb des Zentrums."),
        tr(
            "We walked around the old town.",
            "Wir sind um die Altstadt herum gelaufen.|Wir sind um die Altstadt herumgelaufen.",
        ),
    ),
    lesson(
        "Ein Besuch, der sich lohnt",
        grammar("Einen Ort empfehlen"),
        bank(
            "Die Altstadt ist immer einen ___ wert. In der ___ gibt es viele kleine Läden. "
            "Besonders ___ hat mich das alte Rathaus. Das Konzert im Stadion war ein ___ "
            "Erlebnis. Ich kann die Stadt nur ___!",
            ["Besuch", "Fußgängerzone", "beeindruckt", "einmaliges", "empfehlen"],
            "Ausfahrt",
            "versäumt",
        ),
        mc(
            "Die Stadt hat einiges zu bieten. means:",
            "The city has a lot to offer.",
            "The city wants a lot of money.",
            "The city is very small.",
        ),
        fill("Ich weiß das Wort nicht. Ich muss es ___. (look up)", "nachschlagen"),
        fill("___ habe ich morgen frei. (by the way)", "Übrigens"),
        fill("Wir fahren ___, nicht morgen. (the day after tomorrow)", "übermorgen"),
        fill("___ es nicht regnet, sitzen wir draußen. (as long as)", "Solange"),
        tr("The concert was worth it.", "Das Konzert hat sich gelohnt."),
    ),
    lesson(
        "Lektion 21: Test",
        fill("Die Bühne muss ___ werden. (aufbauen)", "aufgebaut"),
        fill("Die Karten können online ___ werden. (kaufen)", "gekauft"),
        mc("Wir wandern den Fluss ...", "entlang", "herum", "außerhalb"),
        mc("innerhalb ___ Woche", "einer", "eine", "einem"),
        fill("Das Stadion liegt ___ der Stadt. (outside)", "außerhalb"),
        order("Vorher muss natürlich fleißig geübt werden."),
        tr("The old town is always worth a visit.", "Die Altstadt ist immer einen Besuch wert."),
        tr("The band is rehearsing in the studio.", "Die Band probt im Studio."),
    ),
    lesson(
        "Modul 7: Wiederholung",
        fill("Je länger ich übe, ___ besser spiele ich.", "desto|umso"),
        fill("Je ___ wir losfahren, desto weniger Stau. (früh)", "früher"),
        fill("Man spart Energie, ___ man das Licht ausschaltet. (by)", "indem"),
        fill("Es schneite, ___ wir bleiben mussten. (so that)", "sodass"),
        mc("Die Plakate müssen noch ___ werden.", "verteilt", "verteilen", "verteilte"),
        mc("Wir sind um den See ___ gelaufen.", "herum", "entlang", "innerhalb"),
        bank(
            "Je mehr Fans kommen, ___ größer muss die Bühne sein. Die Lautsprecher müssen "
            "deshalb früh ___ werden. Wir sparen Zeit, ___ alle zusammen helfen. Das Stadion "
            "liegt ___ der Stadt.",
            ["desto", "aufgebaut", "indem", "außerhalb"],
            "sodass",
            "herum",
        ),
        tr("That is interesting!", "Das ist ja interessant!"),
        order("Je älter ich wurde, desto mehr reiste ich."),
    ),
]

LEKTION_21 = unit(
    21,
    "Vorher muss natürlich fleißig geübt werden.",
    "Konzerte und Städte",
    L21_WORDS,
    L21_RULES,
    sections(L21_LESSONS, vocab_lessons(L21_WORDS, "Wörter")),
)


UNITS = [LEKTION_19, LEKTION_20, LEKTION_21]
