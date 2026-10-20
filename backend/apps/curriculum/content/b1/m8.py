"""Modul 8 (B1.2): Lektion 22 (In der BRD wurde die Demokratie eingeführt.), 23
(Fahrradfahren ist in.), 24 (Das löst mehrere Probleme auf einmal.)."""

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
# Lektion 22: In der BRD wurde die Demokratie eingeführt.
# ============================================================================

L22_WORDS = [
    ("the Berlin Wall", "die Berliner Mauer", "phrase"),
    (
        "the Federal Republic of Germany",
        "die Bundesrepublik Deutschland",
        "phrase",
        "short: die BRD",
    ),
    (
        "the German Democratic Republic",
        "die Deutsche Demokratische Republik",
        "phrase",
        "short: die DDR",
    ),
    ("the dictatorship", "die Diktatur", "noun", "Pl. die Diktaturen"),
    ("the reunification", "die Wiedervereinigung", "noun"),
    ("the division", "die Teilung", "noun", "die Teilung Deutschlands"),
    ("the occupation zone", "die Besatzungszone", "noun", "Pl. die Besatzungszonen"),
    ("the airlift", "die Luftbrücke", "noun"),
    ("the opening of the Wall", "die Maueröffnung", "noun"),
    ("the post-war period", "die Nachkriegszeit", "noun"),
    ("the soldier", "der Soldat", "noun", "den Soldaten, f. die Soldatin"),
    ("the revolution", "die Revolution", "noun", "Pl. die Revolutionen"),
    ("the republic", "die Republik", "noun", "Pl. die Republiken"),
    ("the head of state", "das Staatsoberhaupt", "noun", "Pl. die Staatsoberhäupter"),
    ("the federal state", "der Bundesstaat", "noun", "Pl. die Bundesstaaten"),
    ("the federal government", "die Bundesregierung", "noun"),
    ("the European Union", "die Europäische Union", "phrase", "short: die EU"),
    ("the national anthem", "die Nationalhymne", "noun", "Pl. die Nationalhymnen"),
    ("the escape / flight", "die Flucht", "noun", "Pl. die Fluchten"),
    ("the opponent", "der Gegner", "noun", "f. die Gegnerin"),
    ("the violence", "die Gewalt", "noun"),
    ("the power", "die Macht", "noun", "Pl. die Mächte"),
    ("the loss", "der Verlust", "noun", "Pl. die Verluste"),
    ("the construction", "der Bau", "noun", "der Bau der Mauer"),
    ("the number (amount)", "die Anzahl", "noun"),
    ("the permit", "die Genehmigung", "noun", "Pl. die Genehmigungen"),
    ("the consequence (formal)", "die Konsequenz", "noun", "Pl. die Konsequenzen"),
    ("to occupy", "besetzen", "verb", "hat besetzt"),
    ("to divide up", "aufteilen", "verb", "hat aufgeteilt"),
    ("to unite", "vereinigen", "verb", "hat vereinigt"),
    ("to protest", "protestieren", "verb", "hat protestiert"),
    ("to demand", "fordern", "verb", "hat gefordert"),
    ("to force", "zwingen", "verb", "zwang, hat gezwungen"),
    ("to appear / to be published", "erscheinen", "verb", "erschien, ist erschienen"),
    ("to praise", "loben", "verb", "hat gelobt"),
    ("to approve / to permit", "genehmigen", "verb", "hat genehmigt"),
    ("European", "europäisch", "adjective"),
    ("violent", "gewaltvoll", "adjective"),
    ("allegedly", "angeblich", "adverb"),
    ("possibly", "eventuell", "adverb"),
    ("afterwards", "hinterher", "adverb"),
    ("I'd have liked to be there.", "Ich wäre gern dabei gewesen.", "phrase"),
]

L22_RULES = [
    rule(
        "Passiv Präteritum und Perfekt",
        "verbs",
        """
History texts often say **what was done**, not who did it: the **passive**.

| tense | form | example |
|---|---|---|
| Präsens | werden + Partizip II | *Die Mauer **wird geöffnet**.* |
| **Präteritum** | **wurde + Partizip II** | *Die Mauer **wurde** 1989 **geöffnet**.* |
| **Perfekt** | **ist + Partizip II + worden** | *Die Mauer **ist** 1989 **geöffnet worden**.* |

- In the passive Perfekt it is always **worden**, never ~~geworden~~.
- Who did it: **von + Dativ**: *Die Stadt wurde **von** den Alliierten besetzt.*
- Plural: *Die Grenzen **wurden** geöffnet.*

**Event or state?** *Das Museum **ist geschlossen worden**.* (someone closed it:
event) · *Das Museum **ist geschlossen**.* (it is closed now: state)
""",
        [
            "In der BRD wurde die Demokratie eingeführt.",
            "1961 wurde die Mauer gebaut.",
            "Deutschland ist 1990 wiedervereinigt worden.",
            "Berlin wurde in vier Sektoren aufgeteilt.",
        ],
    ),
    rule(
        "Über Geschichte sprechen",
        "other",
        """
**Facts:** *Im Jahr 1949 wurde die BRD gegründet. · Nach dem Krieg ... · Es wurde
beschlossen, dass ...*

**Asking politely (indirect questions):** *Wissen Sie, wann ...? · Könnten Sie
mir sagen, ...? · Ich weiß gar nicht, ob ...* (verb at the end)

**Not sure:** *Ich glaube, das wurde ... · Meines Wissens ... · Angeblich ...*

**Wishes about the past:** *Ich wäre gern dabei gewesen. · Ich hätte gern
erlebt, wie ...*
""",
        [
            "Wissen Sie, wann die Mauer gebaut wurde?",
            "Meines Wissens wurde der Euro 2002 eingeführt.",
            "Ich hätte gern erlebt, wie die Mauer geöffnet wurde.",
        ],
    ),
]

L22_LESSONS = [
    lesson(
        "Deutsche Geschichte",
        review("die Wiedervereinigung"),
        review("die Teilung"),
        match(
            [
                ("1945", "Ende des Zweiten Weltkriegs"),
                ("1949", "Gründung von BRD und DDR"),
                ("1961", "Bau der Mauer"),
                ("1989", "Öffnung der Mauer"),
                ("1990", "Wiedervereinigung"),
            ],
            "Match the year to the event.",
        ),
        mc(
            "Nach dem Krieg war Deutschland in vier ___ geteilt.",
            "Besatzungszonen",
            "Bundesstaaten",
            "Nationalhymnen",
        ),
        mc(
            "1948 brachten Flugzeuge Essen nach West-Berlin. Das war die ...",
            "Luftbrücke.",
            "Revolution.",
            "Diktatur.",
        ),
        fill("Viele Menschen haben gegen die Regierung ___. (protestieren)", "protestiert"),
        fill("Die Menschen ___ Freiheit. (fordern)", "forderten"),
        fill("Die Zeitung ist gestern ___. (erscheinen)", "erschienen"),
        tr("I'd have liked to be there.", "Ich wäre gern dabei gewesen."),
    ),
    lesson(
        "Die Mauer wurde gebaut",
        grammar("Passiv Präteritum und Perfekt"),
        mc("1961 ___ die Mauer gebaut.", "wurde", "wird", "ist"),
        mc("Deutschland ist 1990 wiedervereinigt ___.", "worden", "geworden", "wurde"),
        mc(
            "Man gründete 1949 die BRD. → Die BRD ...",
            "wurde 1949 gegründet.",
            "wurde 1949 gründet.",
            "ist 1949 gegründet geworden.",
        ),
        fill("Berlin ___ in vier Sektoren aufgeteilt. (Präteritum)", "wurde"),
        fill("Die Grenzen ___ geöffnet. (Präteritum, Pl.)", "wurden"),
        fill("Der Euro ist 2002 ___ worden. (einführen)", "eingeführt"),
        fill("Die Stadt wurde ___ den Soldaten besetzt. (by)", "von"),
        mc(
            "The museum is closed now (a state):",
            "Das Museum ist geschlossen.",
            "Das Museum ist geschlossen worden.",
            "Das Museum wurde geschlossen.",
        ),
        order("In der BRD wurde die Demokratie eingeführt."),
        tr(
            "The wall was opened in 1989.",
            "Die Mauer wurde 1989 geöffnet.|1989 wurde die Mauer geöffnet.",
        ),
    ),
    lesson(
        "Ein Geschichtsquiz",
        grammar("Über Geschichte sprechen"),
        bank(
            "Wissen Sie, ___ die Mauer gebaut wurde? Ich glaube, das war 1961. Meines ___ "
            "wurde sie am 9. November 1989 geöffnet. Danach ist Deutschland schnell "
            "wiedervereinigt ___. Ich wäre gern ___ gewesen!",
            ["wann", "Wissens", "worden", "dabei"],
            "geworden",
            "ob",
        ),
        mc(
            "Which question is correct?",
            "Könnten Sie mir sagen, wann der Euro eingeführt wurde?",
            "Könnten Sie mir sagen, wann wurde der Euro eingeführt?",
            "Könnten Sie mir sagen, wann der Euro wurde eingeführt?",
        ),
        mc(
            "angeblich means:",
            "allegedly",
            "afterwards",
            "possibly",
        ),
        fill("Die Soldaten ___ die Menschen, die Stadt zu verlassen. (zwingen)", "zwangen"),
        fill("Der Lehrer hat die Schüler ___. (loben)", "gelobt"),
        fill("___ komme ich später. (possibly)", "Eventuell"),
        tr(
            "Do you know when the GDR was founded? (Sie)",
            "Wissen Sie, wann die DDR gegründet wurde?",
        ),
    ),
    lesson(
        "Lektion 22: Test",
        fill("Die Mauer ___ 1961 gebaut. (Präteritum)", "wurde"),
        fill("Der Euro ist 2002 eingeführt ___.", "worden"),
        mc("Die BRD ___ 1949 gegründet.", "wurde", "würde", "worden"),
        mc("Die Teilung endete mit der ...", "Wiedervereinigung", "Luftbrücke", "Besatzungszone"),
        fill("Viele Menschen flohen. Die ___ war gefährlich. (escape)", "Flucht"),
        order("Deutschland ist 1990 wiedervereinigt worden."),
        tr("The city was divided.", "Die Stadt wurde geteilt."),
        tr(
            "Afterwards everyone celebrated.",
            "Hinterher haben alle gefeiert.|Hinterher feierten alle.",
        ),
    ),
]

LEKTION_22 = unit(
    22,
    "In der BRD wurde die Demokratie eingeführt.",
    "Deutsche Geschichte nach 1945",
    L22_WORDS,
    L22_RULES,
    sections(L22_LESSONS, vocab_lessons(L22_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 23: Fahrradfahren ist in.
# ============================================================================

L23_WORDS = [
    ("cycling", "das Fahrradfahren", "noun"),
    ("the cycle lane", "der Radweg", "noun", "Pl. die Radwege"),
    ("the cyclist", "der Radfahrer", "noun", "f. die Radfahrerin"),
    ("the recumbent bike", "das Liegerad", "noun", "Pl. die Liegeräder"),
    ("the brake", "die Bremse", "noun", "Pl. die Bremsen"),
    ("the bell", "die Klingel", "noun", "Pl. die Klingeln"),
    ("the spare part", "das Ersatzteil", "noun", "Pl. die Ersatzteile"),
    ("the pressure", "der Druck", "noun"),
    ("the iron", "das Eisen", "noun"),
    ("the car traffic", "der Autoverkehr", "noun"),
    ("the air pollution", "die Luftverschmutzung", "noun"),
    ("the climate change", "der Klimawandel", "noun"),
    ("the sustainability", "die Nachhaltigkeit", "noun"),
    ("the measure (action)", "die Maßnahme", "noun", "Pl. die Maßnahmen"),
    ("the waste", "der Abfall", "noun", "Pl. die Abfälle"),
    ("the consumption", "der Konsum", "noun"),
    ("the provider", "der Anbieter", "noun", "f. die Anbieterin"),
    ("the plug", "der Stecker", "noun", "Pl. die Stecker"),
    ("the socket", "die Steckdose", "noun", "Pl. die Steckdosen"),
    ("the station (charging, bike)", "die Station", "noun", "Pl. die Stationen"),
    ("the cleaning", "die Reinigung", "noun", "Pl. die Reinigungen"),
    ("the bathtub", "die Badewanne", "noun", "Pl. die Badewannen"),
    ("the research", "die Forschung", "noun", "Pl. die Forschungen"),
    ("to brake", "bremsen", "verb", "hat gebremst"),
    ("to avoid", "vermeiden", "verb", "vermied, hat vermieden"),
    ("to do without", "verzichten", "verb", "verzichten auf + Akk."),
    ("to use up / to consume", "verbrauchen", "verb", "hat verbraucht"),
    ("to consume (buy)", "konsumieren", "verb", "hat konsumiert"),
    ("to depend on", "abhängen", "verb", "abhängen von + Dat., hing ab, hat abgehangen"),
    ("to make an effort", "bemühen", "verb", "sich bemühen, hat sich bemüht"),
    ("to find / to establish", "feststellen", "verb", "hat festgestellt"),
    ("to prefer", "vorziehen", "verb", "zog vor, hat vorgezogen"),
    ("sustainable", "nachhaltig", "adjective"),
    ("mobile", "mobil", "adjective"),
    ("useful", "nützlich", "adjective"),
    ("wide", "breit", "adjective"),
    ("clean / pure", "rein", "adjective"),
    ("as far as I'm concerned", "meinetwegen", "adverb"),
    ("on the side", "nebenbei", "adverb"),
    ("apparently", "offenbar", "adverb"),
    ("anyway", "sowieso", "adverb"),
    ("instead of (doing)", "statt ... zu", "other", "also: anstatt ... zu"),
    ("without (doing)", "ohne ... zu", "other"),
    ("Cycling is in.", "Fahrradfahren ist in.", "phrase"),
]

L23_RULES = [
    rule(
        "(an)statt ... zu, ohne ... zu",
        "sentence_structure",
        """
With the **same subject** in both parts, use an **infinitive with zu**:

- ***statt / anstatt ... zu*** = instead of doing: *Sie fährt Rad, **statt** das
  Auto **zu nehmen**.*
- ***ohne ... zu*** = without doing: *Er ging, **ohne** sich **zu
  verabschieden**.*

With a **different subject**, use **statt dass / ohne dass** + a clause (verb at
the end):
- *Er fuhr weg, **ohne dass** seine Eltern es **wussten**.*
- ***Statt dass** die Stadt Radwege baut, baut sie Parkhäuser.*

*zu* goes inside separable verbs: *ohne ab**zu**schließen, statt ein**zu**kaufen*.
""",
        [
            "Ich fahre mit dem Rad, statt das Auto zu nehmen.",
            "Er ist über die Kreuzung gefahren, ohne zu bremsen.",
            "Wir haben das Ersatzteil gekauft, ohne dass der Verkäufer es erklärt hat.",
        ],
    ),
    rule(
        "Im Forum diskutieren",
        "other",
        """
A forum post: **claim → reason → example → (concession) → conclusion**.

- *Ich bin dafür / dagegen, dass ... · Ich halte es für sinnvoll, ...*
- *Ein wichtiges Argument ist ... · Zum Beispiel ...*
- *Das kann ich gut verstehen, aber ... · Da bin ich anderer Meinung.*
- *Ich finde, wir sollten ... · Es wäre besser, wenn ...*
- *Was denken die anderen darüber?*
""",
        [
            "Ich bin dafür, dass die Innenstadt autofrei wird.",
            "Das kann ich gut verstehen, aber ohne Auto geht es auf dem Land nicht.",
            "Es wäre besser, wenn es mehr Radwege gäbe.",
        ],
    ),
]

L23_LESSONS = [
    lesson(
        "Rund ums Fahrrad",
        review("der Radweg"),
        review("die Bremse"),
        match(
            [
                ("die Bremse", "Damit hält das Fahrrad an."),
                ("die Klingel", "Damit macht man andere aufmerksam."),
                ("der Radweg", "Hier fahren nur Fahrräder."),
                ("die Kreuzung", "Hier treffen sich zwei Straßen."),
                ("das Ersatzteil", "ein neues Teil für etwas Kaputtes"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Zu viele Autos machen die Luft schmutzig. Das ist ...",
            "Luftverschmutzung.",
            "Nachhaltigkeit.",
            "Mobilität.",
        ),
        mc(
            "Ein Fahrrad, auf dem man fast liegt, ist ein ...",
            "Liegerad.",
            "Stecker.",
            "Eisen.",
        ),
        fill("Vor der Kreuzung musst du ___. (bremsen)", "bremsen"),
        fill("Der Reifen braucht mehr ___. (pressure)", "Druck"),
        fill("Der Radweg ist hier sehr ___. (wide)", "breit"),
        tr("Cycling is in.", "Fahrradfahren ist in."),
    ),
    lesson(
        "Statt das Auto zu nehmen",
        grammar("(an)statt ... zu, ohne ... zu"),
        mc(
            "Sie fährt Rad, ___ das Auto zu nehmen.",
            "statt",
            "ohne",
            "damit",
        ),
        mc(
            "Er ging, ohne sich ___.",
            "zu verabschieden",
            "verabschieden",
            "verabschiedet",
        ),
        mc(
            "Er fuhr weg, ___ seine Eltern es wussten. (different subject)",
            "ohne dass",
            "ohne zu",
            "statt zu",
        ),
        fill("Ich gehe zu Fuß, statt mit dem Bus ___ fahren.", "zu"),
        fill("Sie ist losgefahren, ohne die Tür ___. (abschließen)", "abzuschließen"),
        fill("___ Auto zu fahren, nehme ich das Rad. (instead of: Anstatt)", "Anstatt"),
        fill("Er fuhr über die Kreuzung, ___ zu bremsen. (without)", "ohne"),
        order("Ich fahre mit dem Rad, statt das Auto zu nehmen."),
        tr(
            "She left without saying goodbye.",
            "Sie ging, ohne sich zu verabschieden.|Sie ist gegangen, ohne sich zu verabschieden.",
        ),
    ),
    lesson(
        "Was kann jeder tun?",
        bank(
            "Gegen den ___ kann jeder etwas tun. Man kann Abfall ___, statt alles neu zu "
            "kaufen. Man kann auf das Auto ___ und mit dem Rad fahren. Das ist ___ und "
            "billig. Es ___ aber auch davon ab, wo man wohnt.",
            ["Klimawandel", "vermeiden", "verzichten", "nachhaltig", "hängt"],
            "Konsum",
            "bremst",
        ),
        mc(
            "Eine Aktion gegen ein Problem ist eine ...",
            "Maßnahme.",
            "Steckdose.",
            "Badewanne.",
        ),
        fill("Ein Liegerad ___ weniger Energie als ein Auto. (verbrauchen)", "verbraucht"),
        fill("Ich ___ das Fahrrad dem Auto vor. (vorziehen)", "ziehe"),
        fill("Die Forscher haben ___, dass die Luft besser ist. (feststellen)", "festgestellt"),
        fill("Ich fahre ___ Rad, auch ohne Klimaschutz. (anyway)", "sowieso"),
        tr("We should avoid waste.", "Wir sollten Abfall vermeiden."),
    ),
    lesson(
        "Ein Beitrag im Forum",
        grammar("Im Forum diskutieren"),
        match(
            [
                ("Ich bin dafür, dass ...", "Meinung"),
                ("Ein wichtiges Argument ist ...", "Grund"),
                ("Das kann ich verstehen, aber ...", "Gegenargument"),
                ("Was denken die anderen?", "Schluss"),
            ],
            "What is each sentence doing?",
        ),
        mc(
            "meinetwegen means:",
            "as far as I'm concerned / fine by me",
            "because of me",
            "on the side",
        ),
        fill("Es wäre besser, ___ es mehr Radwege gäbe.", "wenn"),
        fill("Ich halte es für ___, das Rad zu nehmen. (useful)", "nützlich"),
        fill("Er hat ___ den Bus verpasst. (apparently)", "offenbar"),
        fill("Sie arbeitet ___ als Fahrradkurierin. (on the side)", "nebenbei"),
        tr("I am in favour of more cycle lanes.", "Ich bin für mehr Radwege."),
    ),
    lesson(
        "Lektion 23: Test",
        fill("Ich gehe zu Fuß, statt das Auto ___ nehmen.", "zu"),
        fill("Er ging, ___ etwas zu sagen. (without)", "ohne"),
        mc("Sie kam, ___ wir es wussten.", "ohne dass", "ohne zu", "statt zu"),
        mc("Hier fahren nur Fahrräder:", "der Radweg", "die Steckdose", "die Reinigung"),
        fill("Das ___ vom Wetter ab. (abhängen)", "hängt"),
        order("Wir sollten auf das Auto verzichten."),
        tr("Cycling is sustainable.", "Fahrradfahren ist nachhaltig."),
        tr("The bike needs a spare part.", "Das Fahrrad braucht ein Ersatzteil."),
    ),
]

LEKTION_23 = unit(
    23,
    "Fahrradfahren ist in.",
    "Umwelt und Mobilität",
    L23_WORDS,
    L23_RULES,
    sections(L23_LESSONS, vocab_lessons(L23_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 24: Das löst mehrere Probleme auf einmal.
# ============================================================================

L24_WORDS = [
    ("the living together", "das Zusammenleben", "noun"),
    ("the community project", "das Gemeinschaftsprojekt", "noun", "Pl. die Gemeinschaftsprojekte"),
    ("the mutual help", "die gegenseitige Hilfe", "phrase"),
    ("the compromise", "der Kompromiss", "noun", "Pl. die Kompromisse"),
    ("the age group", "die Altersgruppe", "noun", "Pl. die Altersgruppen"),
    ("the loneliness", "die Einsamkeit", "noun"),
    ("the childcare", "die Kinderbetreuung", "noun"),
    ("the intention", "die Absicht", "noun", "Pl. die Absichten"),
    ("the vision of the future", "die Zukunftsvision", "noun", "Pl. die Zukunftsvisionen"),
    ("the justice", "die Gerechtigkeit", "noun"),
    ("the change", "die Veränderung", "noun", "Pl. die Veränderungen"),
    ("the cooperation", "die Zusammenarbeit", "noun"),
    ("the criticism", "die Kritik", "noun", "Pl. die Kritiken"),
    ("the planning", "die Planung", "noun", "Pl. die Planungen"),
    ("the process", "der Prozess", "noun", "Pl. die Prozesse"),
    ("the smog", "der Smog", "noun"),
    ("the reality", "die Wirklichkeit", "noun"),
    ("the doubt", "der Zweifel", "noun", "Pl. die Zweifel"),
    ("the detail", "die Einzelheit", "noun", "Pl. die Einzelheiten"),
    ("the row / series", "die Reihe", "noun", "Pl. die Reihen"),
    ("the wheelchair user", "der Rollstuhlfahrer", "noun", "f. die Rollstuhlfahrerin"),
    ("the leaf / sheet", "das Blatt", "noun", "Pl. die Blätter"),
    ("to join forces", "zusammenschließen", "verb", "sich zusammenschließen"),
    ("to agree on", "einigen", "verb", "sich einigen auf + Akk."),
    ("to make possible", "ermöglichen", "verb", "hat ermöglicht"),
    ("to decide (formally)", "beschließen", "verb", "beschloss, hat beschlossen"),
    ("to complain (formally)", "klagen", "verb", "klagen über + Akk."),
    ("to realise (make happen)", "realisieren", "verb", "hat realisiert"),
    ("to increase / to grow bigger", "vergrößern", "verb", "sich vergrößern"),
    ("to doubt", "zweifeln", "verb", "zweifeln an + Dat."),
    ("to light", "anzünden", "verb", "hat angezündet"),
    ("to give reasons for", "begründen", "verb", "hat begründet"),
    ("independent", "unabhängig", "adjective"),
    ("eternal", "ewig", "adjective"),
    ("gradually", "allmählich", "adverb"),
    ("at first", "anfangs", "adverb"),
    ("apparently (seemingly)", "anscheinend", "adverb"),
    ("next door", "nebenan", "adverb"),
    ("so that (purpose)", "damit", "other"),
    ("in order to", "um ... zu", "other"),
    ("as if", "als ob", "other"),
    ("That solves several problems at once.", "Das löst mehrere Probleme auf einmal.", "phrase"),
    ("I'm convinced that ...", "Ich bin davon überzeugt, dass ...", "phrase"),
]

L24_RULES = [
    rule(
        "damit und um ... zu",
        "sentence_structure",
        """
Both say **what for** (the purpose).

**um ... zu + Infinitiv** when the **subject is the same** in both parts:
- *Ich lerne Deutsch, **um** in Deutschland **zu studieren**.* (I learn, I study)
- *Wir haben uns zusammengeschlossen, **um** Geld **zu sparen**.*

**damit + clause** (verb at the end) when the **subjects are different**:
- *Sie spricht langsam, **damit** die Kinder sie **verstehen**.*
- *Wir bauen einen Garten, **damit** die Kinder draußen spielen **können**.*

With the same subject, *damit* is possible too, but *um ... zu* is shorter:
*Ich spare, **damit** ich reisen kann.* = *Ich spare, **um** reisen **zu**
können.*

Not the same as *sodass* (Lektion 20): *damit* = the goal, *sodass* = the result.
""",
        [
            "Wir hatten uns zusammengeschlossen, damit niemand allein ist.",
            "Sie besucht den Kurs, um ihre Kenntnisse zu erweitern.",
            "Wir bilden eine Fahrgemeinschaft, damit alle Benzin sparen.",
        ],
    ),
    rule(
        "als ob + Konjunktiv II",
        "verbs",
        """
**als ob** (as if) describes something that **seems** so but **isn't** really.
The verb goes to the end, usually in the **Konjunktiv II**:

- *Er tut so, **als ob** er alles **wüsste**.* (but he doesn't)
- *Sie sieht aus, **als ob** sie müde **wäre**.*
- *Es ist, **als ob** wir eine große Familie **wären**.*
- *Er redet, **als ob** er schon lange hier **wohnen würde**.*

A shorter form drops *ob* and puts the verb right after *als*: *Er tut so, **als
wüsste** er alles.*
""",
        [
            "Er tut so, als ob er alles wüsste.",
            "Manchmal ist es, als ob wir eine große Familie wären.",
            "Sie lacht, als ob nichts passiert wäre.",
        ],
    ),
    rule(
        "Zukunftsvisionen und Abschied",
        "other",
        """
**Visions and arguments:** *Ich bin davon überzeugt, dass ... · Ich könnte mir
vorstellen, dass ... · Das wäre eine gute Lösung. · Dadurch könnten wir ... · Ich
finde das unrealistisch, weil ... · Ein Vorteil / Nachteil ist ...*

**Saying goodbye to a group:** *Es war schön, euch / Sie kennenzulernen. · Ich
wünsche dir / Ihnen alles Gute! · Viel Erfolg für die Zukunft! · Bleib(t) gesund!
· Lass uns in Kontakt bleiben!*
""",
        [
            "Ich bin davon überzeugt, dass wir in Zukunft mehr teilen werden.",
            "Es war schön, euch kennenzulernen.",
            "Viel Erfolg für die Zukunft!",
        ],
    ),
]

L24_LESSONS = [
    lesson(
        "Zusammen ist man weniger allein",
        review("das Zusammenleben"),
        review("die Einsamkeit"),
        match(
            [
                ("das Gemeinschaftsprojekt", "Viele machen zusammen etwas."),
                ("der Kompromiss", "Jeder gibt ein bisschen nach."),
                ("die Kinderbetreuung", "Jemand passt auf die Kinder auf."),
                ("die Einsamkeit", "Man ist allein und traurig."),
                ("die Altersgruppe", "Menschen, die gleich alt sind"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Junge und alte Menschen helfen sich. Das ist ...",
            "gegenseitige Hilfe.",
            "ein Verbrechen.",
            "Smog.",
        ),
        mc(
            "Nach langer Diskussion haben wir uns auf einen Plan ...",
            "geeinigt.",
            "gezweifelt.",
            "angezündet.",
        ),
        fill(
            "Das Projekt ___ alten Menschen ein Leben in Gemeinschaft. (ermöglichen)", "ermöglicht"
        ),
        fill("Wir haben uns zu einer Gruppe ___. (zusammenschließen)", "zusammengeschlossen"),
        fill("Die Nachbarin wohnt gleich ___. (next door)", "nebenan"),
        tr("That solves several problems at once.", "Das löst mehrere Probleme auf einmal."),
    ),
    lesson(
        "Damit oder um ... zu?",
        grammar("damit und um ... zu"),
        mc(
            "Ich lerne Deutsch, ___ in Wien zu studieren. (same subject)",
            "um",
            "damit",
            "sodass",
        ),
        mc(
            "Sie spricht langsam, ___ die Kinder sie verstehen. (different subject)",
            "damit",
            "um",
            "ohne",
        ),
        mc(
            "Which sentence is correct?",
            "Wir sparen, um ein Haus zu kaufen.",
            "Wir sparen, um wir ein Haus kaufen.",
            "Wir sparen, damit ein Haus zu kaufen.",
        ),
        fill("Sie besucht den Kurs, um ihre Kenntnisse zu ___. (erweitern)", "erweitern"),
        fill("Wir bauen einen Garten, ___ die Kinder draußen spielen können.", "damit"),
        fill("Er fährt Rad, ___ fit zu bleiben.", "um"),
        fill("Ich spare, um reisen zu ___. (können)", "können"),
        order("Wir bilden eine Fahrgemeinschaft, damit alle Benzin sparen."),
        tr(
            "I'm learning German in order to work in Germany.",
            "Ich lerne Deutsch, um in Deutschland zu arbeiten.",
        ),
        tr(
            "We help each other so that nobody is alone.",
            "Wir helfen uns, damit niemand allein ist.|Wir helfen einander, damit niemand allein ist.",
        ),
    ),
    lesson(
        "Als ob ...",
        grammar("als ob + Konjunktiv II"),
        mc("Er tut so, als ob er alles ___.", "wüsste", "weiß", "wusste"),
        mc("Sie sieht aus, als ob sie müde ___.", "wäre", "ist", "war"),
        fill("Es ist, als ___ wir eine Familie wären.", "ob"),
        fill("Er redet, als ob er der Chef ___. (sein)", "wäre"),
        fill("Sie lacht, als ob nichts passiert ___. (sein)", "wäre"),
        mc(
            "Er tut so, als wüsste er alles. means the same as:",
            "Er tut so, als ob er alles wüsste.",
            "Er weiß wirklich alles.",
            "Er will alles wissen.",
        ),
        order("Er tut so, als ob er alles wüsste."),
        tr("She acts as if she were ill.", "Sie tut so, als ob sie krank wäre."),
    ),
    lesson(
        "Unsere Zukunft in 50 Jahren",
        grammar("Zukunftsvisionen und Abschied"),
        bank(
            "Ich bin ___ überzeugt, dass wir in 50 Jahren anders leben. ___ werden viele "
            "Menschen in Gemeinschaftsprojekten wohnen. Das ist keine ___, sondern bald "
            "Wirklichkeit. ___ glaubte ich nicht daran, aber jetzt habe ich keinen ___ mehr.",
            ["davon", "Allmählich", "Zukunftsvision", "Anfangs", "Zweifel"],
            "damit",
            "Kritik",
        ),
        match(
            [
                ("Es war schön, euch kennenzulernen.", "Abschied"),
                ("Ich bin davon überzeugt, dass ...", "Meinung"),
                ("Das finde ich unrealistisch.", "Kritik"),
                ("Viel Erfolg für die Zukunft!", "Wunsch"),
            ],
            "What is each sentence?",
        ),
        fill("Die Stadt hat ___, einen neuen Park zu bauen. (beschließen)", "beschlossen"),
        fill("Sie möchte finanziell ___ sein. (independent)", "unabhängig"),
        fill("Bitte ___ Sie Ihre Meinung. (give reasons for)", "begründen"),
        tr(
            "All the best for the future!",
            "Viel Erfolg für die Zukunft!|Alles Gute für die Zukunft!",
        ),
    ),
    lesson(
        "Lektion 24: Test",
        fill("Ich lerne, ___ die Prüfung zu bestehen.", "um"),
        fill("Ich erkläre es dir, ___ du es verstehst.", "damit"),
        mc("Er tut so, als ob er krank ___.", "wäre", "ist", "würde"),
        mc(
            "Zwei Gruppen geben beide ein bisschen nach. Das ist ein ...",
            "Kompromiss",
            "Verbrechen",
            "Prozess",
        ),
        fill("Die Gruppe hat sich ___ vergrößert. (gradually)", "allmählich"),
        order("Wir hatten uns zusammengeschlossen, damit niemand allein ist."),
        tr("It was nice to meet you. (euch)", "Es war schön, euch kennenzulernen."),
        tr("I'm convinced that it works.", "Ich bin davon überzeugt, dass es funktioniert."),
    ),
    lesson(
        "Modul 8: Wiederholung",
        fill("Die Mauer ___ 1961 gebaut. (Präteritum)", "wurde"),
        fill("Der Euro ist 2002 eingeführt ___.", "worden"),
        fill("Sie fährt Rad, statt das Auto ___ nehmen.", "zu"),
        fill("Er ging, ohne ___ verabschieden. (sich ... zu)", "sich zu"),
        mc("Ich spare, ___ ein Auto zu kaufen.", "um", "damit", "statt"),
        mc("Er tut so, als ob er reich ___.", "wäre", "ist", "war"),
        bank(
            "1989 ___ die Mauer geöffnet. Viele Menschen fuhren nach Westen, ___ ihre Familien "
            "zu besuchen. Manche gingen, ohne ihre Wohnung ___ verkaufen. Es war, als ___ "
            "ein Traum wahr geworden wäre.",
            ["wurde", "um", "zu", "ob"],
            "worden",
            "damit",
        ),
        tr("In the FRG democracy was introduced.", "In der BRD wurde die Demokratie eingeführt."),
        order("Ich lerne Deutsch, um in Deutschland zu arbeiten."),
    ),
]

LEKTION_24 = unit(
    24,
    "Das löst mehrere Probleme auf einmal.",
    "Zusammenleben und Zukunft",
    L24_WORDS,
    L24_RULES,
    sections(L24_LESSONS, vocab_lessons(L24_WORDS, "Wörter")),
)


UNITS = [LEKTION_22, LEKTION_23, LEKTION_24]
