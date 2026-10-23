"""Modul 4 (B1.1): Lektion 10 (Hätte ich das bloß anders gemacht!), 11 (Nachdem
wir jahrelang Pech gehabt hatten, ...), 12 (Ausflug des Jahres)."""

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
# Lektion 10: Hätte ich das bloß anders gemacht!
# ============================================================================

L10_WORDS = [
    ("the mishap", "das Missgeschick", "noun", "Pl. die Missgeschicke"),
    ("the annoyance / trouble", "der Ärger", "noun"),
    ("the fault / blame", "die Schuld", "noun", "Das ist meine Schuld."),
    ("the battery", "die Batterie", "noun", "Pl. die Batterien"),
    ("the wallet / purse", "das Portemonnaie", "noun", "Pl. die Portemonnaies"),
    ("the wallet (for notes)", "die Brieftasche", "noun", "Pl. die Brieftaschen"),
    ("the lottery ticket", "der Lottoschein", "noun", "Pl. die Lottoscheine"),
    ("the win / prize", "der Gewinn", "noun", "Pl. die Gewinne"),
    ("the hairstyle", "die Frisur", "noun", "Pl. die Frisuren"),
    ("the thought", "der Gedanke", "noun", "den Gedanken, Pl. die Gedanken"),
    ("the speech", "die Rede", "noun", "Pl. die Reden"),
    ("the stuff", "das Zeug", "noun"),
    ("the quarter of an hour", "die Viertelstunde", "noun", "Pl. die Viertelstunden"),
    ("to regret", "bereuen", "verb", "hat bereut"),
    ("to get lost (on foot)", "verlaufen", "verb", "sich verlaufen, hat sich verlaufen"),
    ("to comfort", "trösten", "verb", "hat getröstet"),
    ("to check", "prüfen", "verb", "hat geprüft"),
    ("to go wrong", "schiefgehen", "verb", "ging schief, ist schiefgegangen"),
    ("to leave (the key) in", "stecken lassen", "verb", "hat den Schlüssel stecken lassen"),
    ("to leave behind", "liegen lassen", "verb", "hat liegen lassen"),
    ("to notice", "bemerken", "verb", "hat bemerkt"),
    ("to occur to (someone)", "einfallen", "verb", "fällt ein, ist eingefallen"),
    ("to pull", "ziehen", "verb", "zog, hat gezogen"),
    ("wet", "nass", "adjective"),
    ("furious", "zornig", "adjective"),
    ("annoying", "ärgerlich", "adjective"),
    ("stupid / silly", "blöd", "adjective"),
    ("by chance", "zufällig", "adverb"),
    ("completely", "völlig", "adverb"),
    ("for weeks", "wochenlang", "adverb"),
    ("why (formal)", "weshalb", "adverb"),
    ("That went badly.", "Das ist dumm gelaufen.", "phrase"),
    ("There's nothing you can do.", "Da kann man nichts machen.", "phrase"),
    ("If only I had done that differently!", "Hätte ich das bloß anders gemacht!", "phrase"),
]

L10_RULES = [
    rule(
        "Konjunktiv II der Vergangenheit",
        "verbs",
        """
To say that something in the **past** should have been different (a regret, an
unreal wish), use **hätte / wäre + Partizip II**:

| | haben | sein |
|---|---|---|
| ich | hätte | wäre |
| du | hättest | wär(e)st |
| er / sie / es | hätte | wäre |
| wir | hätten | wären |
| ihr | hättet | wär(e)t |
| sie / Sie | hätten | wären |

Choose *hätte* or *wäre* exactly as in the **Perfekt**: *Ich habe den Bus
genommen → Ich **hätte** den Bus **genommen**. Ich bin früher losgegangen → Ich
**wäre** früher **losgegangen**.*

A wish starts with the verb and usually adds **doch, nur, bloß**:
- ***Hätte** ich **doch** den Schlüssel **mitgenommen**!*
- ***Wäre** ich **bloß** früher **aufgestanden**!*

With *wenn*: *Wenn ich früher aufgestanden **wäre**, **hätte** ich den Bus nicht
verpasst.*

Careful: ***hatte*** (Präteritum, it happened) vs ***hätte*** (Konjunktiv, it
didn't happen).
""",
        [
            "Hätte ich das bloß anders gemacht!",
            "Wäre ich doch nur zu Hause geblieben!",
            "Wenn ich getankt hätte, wäre das Auto nicht stehen geblieben.",
            "Ich hätte gern Lotto gespielt, aber ich hatte keine Zeit.",
        ],
    ),
    rule(
        "Enttäuschung ausdrücken und reagieren",
        "other",
        """
**Telling a mishap:** *Stell dir vor, was mir passiert ist! · Leider habe ich erst
später bemerkt, dass ... · Ich habe mich so über mich geärgert!*

**Regret:** *Das war vielleicht blöd! · Hätte ich doch nur ...! · Das nächste Mal
mache ich es ganz anders.*

**Reacting with sympathy:** *Oh je, das ist dumm gelaufen! · Das ist wirklich
schade / ärgerlich. · Das kann ich gut verstehen. · Da kann man nichts machen. ·
Vielleicht klappt es ja beim nächsten Mal. · Wer weiß, wofür es gut ist.*
""",
        [
            "Stell dir vor, ich habe meine Brieftasche im Zug liegen lassen!",
            "Oh je, das ist wirklich ärgerlich.",
            "Vielleicht klappt es ja beim nächsten Mal.",
        ],
    ),
]

L10_LESSONS = [
    lesson(
        "Dumm gelaufen!",
        review("das Missgeschick"),
        review("die Batterie"),
        match(
            [
                ("den Bus verpassen", "zu spät an der Haltestelle sein"),
                ("den Schlüssel stecken lassen", "der Schlüssel ist noch in der Tür"),
                ("die Batterie ist leer", "das Handy geht nicht mehr"),
                ("die Brieftasche liegen lassen", "die Brieftasche nicht mitnehmen"),
                ("sich verlaufen", "den Weg nicht mehr finden"),
            ],
            "Match the mishap to what it means.",
        ),
        mc(
            "Es hat geregnet und ich hatte keinen Schirm. Ich war völlig ...",
            "nass.",
            "zufällig.",
            "blöd.",
        ),
        fill("Leider ist der Plan ___. (schiefgehen)", "schiefgegangen"),
        fill("Erst zu Hause habe ich ___, dass mein Portemonnaie weg war. (bemerken)", "bemerkt"),
        fill("Ich habe den Schlüssel in der Tür stecken ___. (lassen)", "lassen"),
        fill("Plötzlich ist mir die Antwort ___. (einfallen)", "eingefallen"),
        tr("That's my fault.", "Das ist meine Schuld."),
    ),
    lesson(
        "Hätte ich doch ...!",
        grammar("Konjunktiv II der Vergangenheit"),
        conj("haben (Konjunktiv II)", "ich", "hätte"),
        conj("sein (Konjunktiv II)", "wir", "wären"),
        conj("haben (Konjunktiv II)", "du", "hättest"),
        mc("___ ich doch früher losgegangen!", "Wäre", "Hätte", "War"),
        mc("___ ich doch den Schirm mitgenommen!", "Hätte", "Wäre", "Hatte"),
        fill("Hätte ich bloß das Licht ___! (ausmachen)", "ausgemacht"),
        fill("Wäre er doch nur zu Hause ___! (bleiben)", "geblieben"),
        fill("Wenn ich getankt ___, wäre ich nicht stehen geblieben. (haben)", "hätte"),
        mc(
            "It didn't happen. Which sentence fits?",
            "Ich hätte den Zug genommen.",
            "Ich hatte den Zug genommen.",
            "Ich habe den Zug genommen.",
        ),
        order("Hätte ich das bloß anders gemacht!"),
        tr(
            "If only I had got up earlier!",
            "Wäre ich doch früher aufgestanden!|Wäre ich bloß früher aufgestanden!|Wäre ich nur früher aufgestanden!",
        ),
    ),
    lesson(
        "Das Sorgentelefon",
        grammar("Enttäuschung ausdrücken und reagieren"),
        match(
            [
                ("Ich habe den Lottoschein verloren!", "Oh je, das ist dumm gelaufen!"),
                (
                    "Ich habe die Prüfung nicht bestanden.",
                    "Vielleicht klappt es beim nächsten Mal.",
                ),
                ("Der Zug war schon weg.", "Da kann man nichts machen."),
            ],
            "Match the story to a good reaction.",
        ),
        mc(
            "Which is a reaction to someone's bad luck?",
            "Das ist wirklich ärgerlich.",
            "Herzlichen Glückwunsch!",
            "Das freut mich!",
        ),
        bank(
            "Stell dir vor, was mir ___ ist! Ich hatte endlich einen ___ im Lotto, aber dann "
            "habe ich den Schein im Bus liegen ___. Ich war so ___ auf mich! ___ ich ihn doch "
            "in die Tasche gesteckt!",
            ["passiert", "Gewinn", "lassen", "zornig", "Hätte"],
            "Wäre",
            "Gedanke",
        ),
        fill("Meine Freundin hat mich lange ___. (trösten)", "getröstet"),
        fill("Ich ___ die Entscheidung nicht. (bereuen)", "bereue"),
        tr("I was so annoyed with myself.", "Ich habe mich so über mich geärgert."),
    ),
    lesson(
        "Diskutieren Sie mit!",
        mc(
            "Your friend has a new hairstyle you don't like. A kind answer:",
            "Die Farbe gefällt mir, und sie passt gut zu deinem Kleid.",
            "Deine Frisur ist völlig blöd.",
            "Weshalb hast du das gemacht?",
        ),
        mc(
            "Weshalb? means:",
            "Why?",
            "When?",
            "Where to?",
        ),
        fill("Ich habe ___ nichts von ihr gehört. (for weeks)", "wochenlang"),
        fill("Wir haben uns ___ in der Stadt getroffen. (by chance)", "zufällig"),
        fill("Bitte ___ noch einmal, ob die Tür zu ist. (check, du)", "prüf|prüfe"),
        fill("Der ___ an eine Reise macht mich glücklich. (thought)", "Gedanke"),
        tr("I would have said the truth.", "Ich hätte die Wahrheit gesagt."),
    ),
    lesson(
        "Lektion 10: Test",
        fill("___ ich doch nur den Bus genommen! (haben)", "Hätte"),
        fill("___ sie bloß früher gekommen! (sein)", "Wäre"),
        mc("Wenn er mehr gelernt ___, hätte er bestanden.", "hätte", "wäre", "hatte"),
        fill("Ich habe meine Tasche im Café liegen ___. (lassen)", "lassen"),
        mc("Oh je, das ist ...", "dumm gelaufen!", "gut gelaufen!", "gelaufen dumm!"),
        order("Wäre ich doch zu Hause geblieben!"),
        tr("There's nothing you can do.", "Da kann man nichts machen."),
        tr("I got lost.", "Ich habe mich verlaufen."),
    ),
]

LEKTION_10 = unit(
    10,
    "Hätte ich das bloß anders gemacht!",
    "Pannen und Pech",
    L10_WORDS,
    L10_RULES,
    sections(L10_LESSONS, vocab_lessons(L10_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 11: Nachdem wir jahrelang Pech gehabt hatten, ...
# ============================================================================

L11_WORDS = [
    ("the moment of happiness", "der Glücksmoment", "noun", "Pl. die Glücksmomente"),
    ("the lucky charm", "der Glücksbringer", "noun", "Pl. die Glücksbringer"),
    ("the feeling", "das Gefühl", "noun", "Pl. die Gefühle"),
    ("the hope", "die Hoffnung", "noun", "Pl. die Hoffnungen"),
    ("the relief", "die Erleichterung", "noun"),
    ("the event", "das Ereignis", "noun", "Pl. die Ereignisse"),
    ("the experience (event)", "das Erlebnis", "noun", "Pl. die Erlebnisse"),
    ("the success", "der Erfolg", "noun", "Pl. die Erfolge"),
    ("the victory", "der Sieg", "noun", "Pl. die Siege"),
    ("the coincidence", "der Zufall", "noun", "Pl. die Zufälle"),
    ("the permanent job", "die Festanstellung", "noun", "Pl. die Festanstellungen"),
    ("the tournament", "das Turnier", "noun", "Pl. die Turniere"),
    ("the doctoral thesis", "die Doktorarbeit", "noun", "Pl. die Doktorarbeiten"),
    ("the solar eclipse", "die Sonnenfinsternis", "noun", "Pl. die Sonnenfinsternisse"),
    ("the star", "der Stern", "noun", "Pl. die Sterne"),
    ("the mushroom", "der Pilz", "noun", "Pl. die Pilze"),
    ("the tyre", "der Reifen", "noun", "Pl. die Reifen"),
    ("the pavement", "der Bürgersteig", "noun", "Pl. die Bürgersteige"),
    ("the cash machine", "der Geldautomat", "noun", "den Geldautomaten, Pl. die Geldautomaten"),
    ("the certificate", "das Zertifikat", "noun", "Pl. die Zertifikate"),
    ("to cheer", "jubeln", "verb", "hat gejubelt"),
    ("to cry", "weinen", "verb", "hat geweint"),
    ("to smile", "lächeln", "verb", "hat gelächelt"),
    ("to enjoy", "genießen", "verb", "genoss, hat genossen"),
    ("to succeed (it works)", "gelingen", "verb", "es gelingt mir, ist gelungen"),
    ("to hand in", "abgeben", "verb", "gibt ab, hat abgegeben"),
    ("to discover", "entdecken", "verb", "hat entdeckt"),
    ("to sleep through", "durchschlafen", "verb", "schläft durch, hat durchgeschlafen"),
    ("to wake up", "aufwachen", "verb", "ist aufgewacht"),
    ("to give up", "aufgeben", "verb", "gibt auf, hat aufgegeben"),
    ("to unpack", "auspacken", "verb", "hat ausgepackt"),
    ("to go camping", "campen", "verb", "hat gecampt"),
    ("to freeze / to be cold", "frieren", "verb", "fror, hat gefroren"),
    ("to inform / to tell", "mitteilen", "verb", "hat mitgeteilt"),
    ("bitter", "bitter", "adjective"),
    ("only / single", "einzig", "adjective", "der einzige Weg"),
    ("for years", "jahrelang", "adverb"),
    ("after (doing)", "nachdem", "other"),
    ("I was overjoyed!", "Ich war überglücklich!", "phrase"),
]

L11_RULES = [
    rule(
        "Plusquamperfekt",
        "verbs",
        """
The **Plusquamperfekt** is the "past of the past": it shows that something had
**already happened** before another past event. Form: **hatte / war +
Partizip II** (the Präteritum of *haben / sein*):

| | haben | sein |
|---|---|---|
| ich | hatte gewonnen | war gefahren |
| du | hattest gewonnen | warst gefahren |
| er / sie / es | hatte gewonnen | war gefahren |
| wir | hatten gewonnen | waren gefahren |
| ihr | hattet gewonnen | wart gefahren |
| sie / Sie | hatten gewonnen | waren gefahren |

*hatte* or *war* as in the Perfekt: *Er **war** schon **gegangen**, als ich kam.*

Don't confuse it with lesson 10: **hatte** gemacht (it happened earlier) vs
**hätte** gemacht (it didn't happen).
""",
        [
            "Als wir ankamen, hatte der Film schon begonnen.",
            "Sie war schon nach Hause gegangen.",
            "Wir hatten jahrelang Pech gehabt.",
        ],
    ),
    rule(
        "nachdem",
        "sentence_structure",
        """
**nachdem** (after) starts a subordinate clause (verb at the end). The
*nachdem*-clause happened **first**, so it takes the **Plusquamperfekt**; the
later event is usually in the **Präteritum**:

| first (Plusquamperfekt) | then (Präteritum) |
|---|---|
| *Nachdem wir jahrelang Pech gehabt **hatten**,* | *gewannen wir endlich das Turnier.* |
| *Nachdem sie die Doktorarbeit abgegeben **hatte**,* | *feierte sie mit Freunden.* |

The clause can also come second: *Sie feierte, nachdem sie die Arbeit abgegeben
hatte.*

*bevor* points **forward** (the next thing), *nachdem* points **back** (what was
already done).
""",
        [
            "Nachdem wir jahrelang Pech gehabt hatten, wurden wir Meister.",
            "Nachdem das Baby durchgeschlafen hatte, waren alle glücklich.",
            "Er rief an, nachdem er angekommen war.",
        ],
    ),
    rule(
        "Gefühle teilen und Interjektionen",
        "other",
        """
**Reacting to someone's joy:** *Das kann ich gut verstehen. · Darüber hätte ich
mich auch sehr gefreut! · Das berührt mich sehr. · So etwas habe ich auch schon
einmal erlebt.*

**Your own joy:** *Ich war überglücklich! · Ich konnte es kaum glauben. · Endlich
hat es geklappt! · Ich habe vor Freude geweint.*

**Interjections:**

| positive | negative |
|---|---|
| *Juhu! Hurra!* (joy) | *Igitt!* (disgust) · *Mist!* (annoyance) |
| *Ui!* (surprise) | *Au!* (pain) · *Brr!* (cold) |
| *Hihi!* (giggle) | *Oh je!* (pity) |
""",
        [
            "Juhu, ich habe die Prüfung bestanden!",
            "Igitt, die Milch ist sauer!",
            "Darüber hätte ich mich auch sehr gefreut.",
        ],
    ),
]

L11_LESSONS = [
    lesson(
        "Was macht Sie glücklich?",
        review("der Glücksmoment"),
        review("die Erleichterung"),
        match(
            [
                ("die Festanstellung", "ein Job ohne Ende"),
                ("die Doktorarbeit", "eine lange Arbeit an der Uni"),
                ("das Turnier", "viele Spiele, am Ende gibt es einen Sieger"),
                ("die Sonnenfinsternis", "Der Mond ist vor der Sonne."),
                ("der Glücksbringer", "Er soll Glück bringen."),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Nach drei Monaten hat das Baby endlich ___. Die Eltern waren glücklich.",
            "durchgeschlafen",
            "aufgegeben",
            "gefroren",
        ),
        fill("Die Fans haben laut ___. (jubeln)", "gejubelt"),
        fill("Wir haben den Urlaub sehr ___. (genießen)", "genossen"),
        fill("Es ist mir ___, die Prüfung zu bestehen. (gelingen)", "gelungen"),
        fill("Im Wald haben wir viele ___ gefunden. (mushrooms)", "Pilze"),
        tr("I was overjoyed!", "Ich war überglücklich!"),
    ),
    lesson(
        "Er hatte schon ...",
        grammar("Plusquamperfekt"),
        mc("Als ich kam, ___ der Film schon begonnen.", "hatte", "war", "hätte"),
        mc("Sie ___ schon nach Hause gegangen.", "war", "hatte", "wäre"),
        fill("Wir ___ jahrelang Pech gehabt. (haben)", "hatten"),
        fill("Ihr ___ schon angekommen. (sein)", "wart"),
        fill("Er hatte die Arbeit schon ___. (abgeben)", "abgegeben"),
        fill("Ich war früh ___. (aufwachen)", "aufgewacht"),
        mc(
            "Which sentence shows that it really happened earlier?",
            "Ich hatte das Buch gelesen.",
            "Ich hätte das Buch gelesen.",
        ),
        order("Sie hatte vorher nie gewonnen."),
        tr("The train had already left.", "Der Zug war schon abgefahren."),
    ),
    lesson(
        "Nachdem ...",
        grammar("nachdem"),
        mc(
            "Which sentence is correct?",
            "Nachdem sie die Arbeit abgegeben hatte, feierte sie.",
            "Nachdem sie hatte die Arbeit abgegeben, feierte sie.",
            "Nachdem sie die Arbeit abgegeben hatte, sie feierte.",
        ),
        mc(
            "Nachdem er angekommen ___, rief er an.",
            "war",
            "hatte",
            "ist",
        ),
        fill("Nachdem wir lange gesucht ___, fanden wir den Weg. (haben)", "hatten"),
        fill("Nachdem das Turnier zu Ende ___, gingen alle nach Hause. (sein)", "war"),
        fill("___ ich gegessen hatte, ging ich spazieren. (after)", "Nachdem"),
        order("Nachdem wir jahrelang Pech gehabt hatten, gewannen wir."),
        tr(
            "After I had unpacked, I called my mother.",
            "Nachdem ich ausgepackt hatte, rief ich meine Mutter an.",
        ),
        tr(
            "We cheered after we had won.",
            "Wir jubelten, nachdem wir gewonnen hatten.",
        ),
    ),
    lesson(
        "Juhu! Mist!",
        grammar("Gefühle teilen und Interjektionen"),
        match(
            [
                ("Juhu!", "Ich freue mich riesig."),
                ("Igitt!", "Das ist eklig."),
                ("Au!", "Das tut weh."),
                ("Brr!", "Es ist so kalt."),
                ("Mist!", "Das ist ärgerlich."),
            ],
            "What does each interjection express?",
        ),
        mc(
            "Your friend tells you she got a permanent job. You say:",
            "Darüber hätte ich mich auch sehr gefreut!",
            "Igitt!",
            "Da kann man nichts machen.",
        ),
        bank(
            "Mein schönster ___ im letzten Jahr: Nachdem ich ___ einen Job gesucht hatte, "
            "bekam ich endlich eine ___. Ich habe vor Freude ___. Meine Familie war sehr "
            "___ auf mich.",
            ["Glücksmoment", "jahrelang", "Festanstellung", "geweint", "stolz"],
            "gefroren",
            "Zufall",
        ),
        fill("Beim Campen haben wir in der Nacht ___. (frieren)", "gefroren"),
        fill(
            "Am Geldautomaten habe ich ___ meinen alten Lehrer getroffen. (by chance)", "zufällig"
        ),
        tr("That touches me very much.", "Das berührt mich sehr."),
    ),
    lesson(
        "Lektion 11: Test",
        fill("Nachdem er gegessen ___, ging er schlafen. (haben)", "hatte"),
        fill("Sie ___ schon nach Hause gefahren. (sein, Plusquamperfekt)", "war"),
        mc(
            "___ ich die Arbeit abgegeben hatte, war ich erleichtert.", "Nachdem", "Bevor", "Obwohl"
        ),
        mc("Igitt! means:", "That's disgusting!", "Great!", "Ouch!"),
        fill("Wir haben die Hoffnung nie ___. (aufgeben)", "aufgegeben"),
        order("Nachdem das Baby eingeschlafen war, sahen wir fern."),
        tr("We had bad luck for years.", "Wir hatten jahrelang Pech."),
        tr("She smiled.", "Sie lächelte.|Sie hat gelächelt."),
    ),
]

LEKTION_11 = unit(
    11,
    "Nachdem wir jahrelang Pech gehabt hatten, ...",
    "Glück und Glücksmomente",
    L11_WORDS,
    L11_RULES,
    sections(L11_LESSONS, vocab_lessons(L11_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 12: Ausflug des Jahres
# ============================================================================

L12_WORDS = [
    ("the company outing", "der Betriebsausflug", "noun", "Pl. die Betriebsausflüge"),
    ("the company party", "die Betriebsfeier", "noun", "Pl. die Betriebsfeiern"),
    ("the Christmas party", "die Weihnachtsfeier", "noun", "Pl. die Weihnachtsfeiern"),
    ("the summer party", "das Sommerfest", "noun", "Pl. die Sommerfeste"),
    ("the anniversary", "das Jubiläum", "noun", "Pl. die Jubiläen"),
    ("the farewell party (at work)", "der Ausstand", "noun", "seinen Ausstand geben"),
    ("the staff meeting", "die Betriebsversammlung", "noun", "Pl. die Betriebsversammlungen"),
    ("the works council", "der Betriebsrat", "noun", "Pl. die Betriebsräte"),
    ("the trade union", "die Gewerkschaft", "noun", "Pl. die Gewerkschaften"),
    ("the meeting / assembly", "die Versammlung", "noun", "Pl. die Versammlungen"),
    ("the agenda", "die Tagesordnung", "noun", "Pl. die Tagesordnungen"),
    ("the minutes (of a meeting)", "das Protokoll", "noun", "Pl. die Protokolle"),
    ("the occasion", "der Anlass", "noun", "Pl. die Anlässe"),
    ("the acceptance (yes to an invitation)", "die Zusage", "noun", "Pl. die Zusagen"),
    ("the refusal (no to an invitation)", "die Absage", "noun", "Pl. die Absagen"),
    ("the brochure", "die Broschüre", "noun", "Pl. die Broschüren"),
    ("the buffet", "das Buffet", "noun", "Pl. die Buffets"),
    ("the effort", "die Mühe", "noun", "sich Mühe geben"),
    ("the improvement", "die Verbesserung", "noun", "Pl. die Verbesserungen"),
    ("the election / choice", "die Wahl", "noun", "Pl. die Wahlen"),
    ("the beer garden", "der Biergarten", "noun", "Pl. die Biergärten"),
    ("the boat", "das Boot", "noun", "Pl. die Boote"),
    ("the circle", "der Kreis", "noun", "im Kreis der Kollegen"),
    ("the gossip", "der Klatsch", "noun"),
    ("the boss / superior", "der Vorgesetzte", "noun", "ein Vorgesetzter, Pl. die Vorgesetzten"),
    (
        "the relative (family member)",
        "der Angehörige",
        "noun",
        "ein Angehöriger, Pl. die Angehörigen",
    ),
    ("the weather report", "der Wetterbericht", "noun", "Pl. die Wetterberichte"),
    ("to chat", "plaudern", "verb", "hat geplaudert"),
    ("to ask (for)", "bitten", "verb", "bitten um + Akk., bat, hat gebeten"),
    ("to ask about / to enquire", "erkundigen", "verb", "sich erkundigen nach + Dat."),
    ("to stand in for", "vertreten", "verb", "vertritt, vertrat, hat vertreten"),
    ("to catch a cold", "erkälten", "verb", "sich erkälten, hat sich erkältet"),
    ("final", "endgültig", "adjective"),
    ("numerous", "zahlreich", "adjective"),
    ("today's", "heutig", "adjective", "die heutige Feier"),
    ("tomorrow's", "morgig", "adjective", "die morgige Versammlung"),
    ("in advance", "im Voraus", "phrase", "Vielen Dank im Voraus!"),
    ("in any case", "jedenfalls", "adverb"),
    ("why (spoken)", "wieso", "adverb"),
    ("as soon as", "sobald", "other", "Sobald ich Zeit habe, ..."),
    ("despite", "trotz", "other", "trotz + Genitiv"),
]

L12_RULES = [
    rule(
        "Der Genitiv",
        "cases",
        """
The **genitive** answers **Wessen?** (whose? / of what?) and joins two nouns:
*die Feier **des Jahres**, das Büro **der Chefin***.

| | masculine | neuter | feminine | plural |
|---|---|---|---|---|
| definite | **des** Betriebsrat**s** | **des** Jahr**es** | **der** Firma | **der** Kollegen |
| indefinite | **eines** Betriebsrat**s** | **eines** Jahr**es** | **einer** Firma | - |
| possessive | **meines** Chef**s** | **unseres** Teams | **meiner** Kollegin | **meiner** Kollegen |

- Masculine and neuter nouns add **-s** (or **-es** after one syllable or -s, -ß,
  -z: *des Jahres, des Hauses*).
- Feminine and plural nouns don't change.
- n-Deklination nouns take **-n**: *des Kollegen, des Kunden*.

In speaking, *von + Dativ* is common: *das Auto von meinem Bruder* = *das Auto
meines Bruders*.
""",
        [
            "Das ist der Ausflug des Jahres.",
            "Die Sitzung des Betriebsrats beginnt um zehn.",
            "Das Büro meiner Chefin ist im dritten Stock.",
            "Die Rede des neuen Kollegen war kurz.",
        ],
    ),
    rule(
        "trotz und Adjektive im Genitiv",
        "cases",
        """
**trotz** (despite) is a preposition with the **genitive**. After an article in
the genitive, the adjective always ends in **-en**:

| | with article | without article |
|---|---|---|
| m. | trotz **des** schlecht**en** Wetterbericht**s** | trotz schlecht**en** Wetterbericht**s** |
| n. | trotz **des** schlecht**en** Wetter**s** | trotz schlecht**en** Wetter**s** |
| f. | trotz **der** gut**en** Zusammenarbeit | trotz gut**er** Zusammenarbeit |
| Pl. | trotz **der** geplant**en** Umbauarbeiten | trotz geplant**er** Umbauarbeiten |

*trotz* + noun vs *obwohl* + clause:
- ***Trotz des Regens** findet der Ausflug statt.*
- ***Obwohl es regnet**, findet der Ausflug statt.*
""",
        [
            "Trotz des schlechten Wetters fahren wir mit dem Boot.",
            "Trotz der vielen Arbeit kommen alle zur Feier.",
            "Trotz guter Zusammenarbeit gibt es Probleme.",
        ],
    ),
    rule(
        "Einladungen: Zusage und Absage",
        "other",
        """
**Inviting:** *Liebe Kolleginnen und Kollegen, · Hiermit laden wir Sie herzlich
zu ... ein. · Die Feier findet am ... um ... Uhr in ... statt. · Bitte geben Sie
uns bis zum ... Bescheid.*

**Accepting (Zusage):** *Vielen Dank für die Einladung. · Ich komme sehr gern. ·
Ich freue mich darauf, euch zu sehen.*

**Declining (Absage):** *Vielen Dank für die Einladung. · Leider kann ich nicht
kommen, weil ... · Das tut mir sehr leid. · Ich wünsche euch eine schöne Feier.
· Vielleicht klappt es beim nächsten Mal.*

**Small talk at work:** good topics are *Urlaub, Wetter, Sport, Essen, Filme*;
better avoid *Geld, Religion, Krankheit, Klatsch über Kollegen*.
""",
        [
            "Hiermit laden wir Sie herzlich zu unserem Sommerfest ein.",
            "Leider kann ich nicht kommen, weil ich verreist bin.",
            "Vielen Dank im Voraus für Ihre Antwort.",
        ],
    ),
]

L12_LESSONS = [
    lesson(
        "Feiern in der Firma",
        review("der Betriebsausflug"),
        review("das Jubiläum"),
        match(
            [
                ("die Weihnachtsfeier", "eine Feier im Dezember"),
                ("der Ausstand", "eine Feier, wenn ein Kollege geht"),
                ("das Jubiläum", "Die Firma wird 25 Jahre alt."),
                ("die Betriebsversammlung", "Alle Mitarbeiter treffen sich und sprechen."),
                ("die Tagesordnung", "die Themen für eine Sitzung"),
            ],
            "Match the event to its meaning.",
        ),
        mc(
            "Wer vertritt die Mitarbeiter in einer Firma?",
            "der Betriebsrat",
            "der Biergarten",
            "das Buffet",
        ),
        mc(
            "Eine Antwort Ja, ich komme! ist eine ...",
            "Zusage.",
            "Absage.",
            "Mühe.",
        ),
        fill("Nach der Sitzung schreibt jemand das ___. (minutes)", "Protokoll"),
        fill("Zum Fest kamen ___ Gäste. (numerous)", "zahlreiche"),
        fill("Frau Kühn ___ den Chef, wenn er krank ist. (vertreten)", "vertritt"),
        tr("We are going on a boat trip.", "Wir machen eine Fahrt mit dem Boot."),
    ),
    lesson(
        "Die Feier des Jahres",
        grammar("Der Genitiv"),
        mc("Das ist der Ausflug ___ Jahres.", "des", "der", "dem"),
        mc("Das Büro ___ Chefin ist oben.", "der", "des", "die"),
        mc("Die Sitzung ___ Betriebsrats beginnt um zehn.", "des", "der", "dem"),
        fill("Das ist das Auto ___ Bruders. (mein)", "meines"),
        fill("Die Rede des neuen ___ war kurz. (Kollege)", "Kollegen"),
        fill("Der Plan ___ Firma ist gut. (unsere)", "unserer"),
        fill("Am Ende ___ Tages waren alle müde. (der)", "des"),
        fill("Das Programm des ___ ist toll. (Sommerfest)", "Sommerfests|Sommerfestes"),
        order("Das ist die Wohnung meiner Eltern."),
        tr("That is the party of the year.", "Das ist die Feier des Jahres."),
    ),
    lesson(
        "Trotz des Regens",
        grammar("trotz und Adjektive im Genitiv"),
        mc("___ des schlechten Wetters fahren wir los.", "Trotz", "Obwohl", "Wegen"),
        mc("Trotz des ___ Wetters war es schön.", "schlechten", "schlechte", "schlechtes"),
        fill("Trotz ___ vielen Arbeit kommen alle. (die)", "der"),
        fill("Trotz des ___ Wetterberichts gehen wir wandern. (schlecht)", "schlechten"),
        fill("Trotz ___ Zusammenarbeit gibt es Probleme. (gut, no article)", "guter"),
        mc(
            "Obwohl es regnet, ... = ",
            "Trotz des Regens ...",
            "Wegen des Regens ...",
            "Während des Regens ...",
        ),
        order("Trotz des Regens findet der Ausflug statt."),
        tr(
            "Despite the rain, we went to the beer garden.",
            "Trotz des Regens gingen wir in den Biergarten.|Trotz des Regens sind wir in den Biergarten gegangen.",
        ),
    ),
    lesson(
        "Vielen Dank für die Einladung",
        grammar("Einladungen: Zusage und Absage"),
        match(
            [
                ("Ich komme sehr gern.", "Zusage"),
                ("Leider kann ich nicht kommen.", "Absage"),
                ("Ich freue mich darauf, euch zu sehen.", "Zusage"),
                ("Ich wünsche euch eine schöne Feier.", "Absage"),
            ],
            "Zusage oder Absage?",
        ),
        bank(
            "Liebe Kolleginnen und Kollegen,\nhiermit ___ ich euch herzlich zu meinem ___ "
            "ein. Nach zwanzig Jahren verlasse ich die Firma. Die Feier findet am Freitag um 16 "
            "Uhr in der Kantine ___. Bitte gebt mir bis Mittwoch ___. Vielen Dank im ___!",
            ["lade", "Ausstand", "statt", "Bescheid", "Voraus"],
            "Absage",
            "trotz",
        ),
        mc(
            "Good small talk topic with a new colleague:",
            "der Urlaub",
            "das Gehalt",
            "Klatsch über den Chef",
        ),
        fill("Sie hat sich nach deiner Gesundheit ___. (erkundigen)", "erkundigt"),
        fill("Leider habe ich mich ___ und muss im Bett bleiben. (erkälten)", "erkältet"),
        fill("___ ich zu Hause bin, rufe ich dich an. (as soon as)", "Sobald"),
        tr(
            "Unfortunately I can't come because I'm away.",
            "Leider kann ich nicht kommen, weil ich verreist bin.",
        ),
    ),
    lesson(
        "Lektion 12: Test",
        fill("Das ist der Chef ___ Firma. (die)", "der"),
        fill("Das ist das Haus ___ Onkels. (mein)", "meines"),
        mc("Trotz ___ Regens fahren wir.", "des", "dem", "den"),
        mc("Ja, ich komme gern! ist eine ...", "Zusage", "Absage", "Tagesordnung"),
        fill("Die Versammlung ist ___: Der Termin bleibt. (final)", "endgültig"),
        order("Hiermit laden wir Sie herzlich zum Sommerfest ein."),
        tr("Thank you in advance!", "Vielen Dank im Voraus!"),
        tr("Despite the bad weather it was nice.", "Trotz des schlechten Wetters war es schön."),
    ),
    lesson(
        "Modul 4: Wiederholung",
        fill("___ ich doch den Schirm mitgenommen! (haben)", "Hätte"),
        fill("Wäre ich bloß früher ___! (losgehen)", "losgegangen"),
        fill("Nachdem wir gegessen ___, tanzten wir. (haben)", "hatten"),
        mc("Er war schon gegangen. This is ...", "Plusquamperfekt", "Konjunktiv II", "Futur"),
        mc("Das ist die Feier ___ Jahres.", "des", "der", "dem"),
        fill("Trotz ___ Kälte gingen wir spazieren. (die)", "der"),
        bank(
            "Letztes Jahr ist unser Betriebsausflug ___. Nachdem wir zwei Stunden im Bus "
            "gesessen ___, fing es an zu regnen. ___ des Regens wollten wir wandern, aber "
            "dann hat sich der Chef verlaufen. ___ wir doch im Biergarten geblieben!",
            ["schiefgegangen", "hatten", "Trotz", "Wären"],
            "Hätten",
            "Obwohl",
        ),
        tr(
            "If only I had done that differently!",
            "Hätte ich das bloß anders gemacht!|Hätte ich das doch anders gemacht!",
        ),
        order("Nachdem sie angekommen war, rief sie an."),
    ),
]

LEKTION_12 = unit(
    12,
    "Ausflug des Jahres",
    "Feste und Einladungen im Betrieb",
    L12_WORDS,
    L12_RULES,
    sections(L12_LESSONS, vocab_lessons(L12_WORDS, "Wörter")),
)


UNITS = [LEKTION_10, LEKTION_11, LEKTION_12]
