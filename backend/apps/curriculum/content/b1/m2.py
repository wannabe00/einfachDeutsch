"""Modul 2 (B1.1): Lektion 4 (Obwohl ich Ihnen das erklärt habe, ...), 5 (Bald
wird in fast jedem Haushalt ein PC stehen.), 6 (Fühlen Sie sich wie zu Hause.)."""

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
# Lektion 4: Obwohl ich Ihnen das erklärt habe, ...
# ============================================================================

L4_WORDS = [
    ("the complaint (about a product)", "die Reklamation", "noun", "Pl. die Reklamationen"),
    ("the customer service", "der Kundendienst", "noun"),
    ("the subscription", "das Abonnement", "noun", "short: das Abo, Pl. die Abos"),
    ("the subscriber", "der Abonnent", "noun", "den Abonnenten, f. die Abonnentin"),
    ("the issue (of a magazine)", "die Ausgabe", "noun", "Pl. die Ausgaben"),
    ("the order", "die Bestellung", "noun", "Pl. die Bestellungen"),
    ("the confirmation", "die Bestätigung", "noun", "Pl. die Bestätigungen"),
    ("the contact person", "der Ansprechpartner", "noun", "f. die Ansprechpartnerin"),
    ("the subject line", "der Betreff", "noun"),
    ("the answering machine", "der Anrufbeantworter", "noun", "Pl. die Anrufbeantworter"),
    ("the extension (phone number)", "die Durchwahl", "noun", "Pl. die Durchwahlen"),
    ("the phone line / connection", "der Anschluss", "noun", "Pl. die Anschlüsse"),
    ("the hold queue", "die Warteschleife", "noun", "in der Warteschleife"),
    ("the recorded announcement", "die Ansage", "noun", "Pl. die Ansagen"),
    ("the information (desk)", "die Auskunft", "noun", "Pl. die Auskünfte"),
    ("the key / button", "die Taste", "noun", "Pl. die Tasten"),
    ("the reaction", "die Reaktion", "noun", "Pl. die Reaktionen"),
    ("the copy", "die Kopie", "noun", "Pl. die Kopien"),
    ("on the phone (speaking)", "am Apparat", "phrase", "Müller am Apparat."),
    ("to subscribe", "abonnieren", "verb", "hat abonniert"),
    ("to complain about (a product)", "reklamieren", "verb", "hat reklamiert"),
    ("to call on / to ask (formally)", "auffordern", "verb", "hat aufgefordert"),
    ("to receive", "erhalten", "verb", "erhält, erhielt, hat erhalten"),
    ("to keep", "behalten", "verb", "behält, behielt, hat behalten"),
    ("to disappoint", "enttäuschen", "verb", "hat enttäuscht"),
    ("to send", "senden", "verb", "hat gesendet"),
    ("to press", "drücken", "verb", "hat gedrückt"),
    ("to forward", "weiterleiten", "verb", "hat weitergeleitet"),
    ("to pass on (a message)", "ausrichten", "verb", "Soll ich etwas ausrichten?"),
    ("to have ready", "bereithalten", "verb", "hält bereit, hat bereitgehalten"),
    ("automatic", "automatisch", "adjective"),
    ("out of the office", "außer Haus", "phrase", "Sie ist heute außer Haus."),
    ("several times", "mehrfach", "adverb"),
    ("even", "sogar", "adverb"),
    ("although", "obwohl", "other"),
    ("nevertheless", "trotzdem", "adverb"),
    (
        "I'm not satisfied with your service.",
        "Ich bin mit Ihrem Service nicht zufrieden.",
        "phrase",
    ),
    ("Could you put me through to ...?", "Könnten Sie mich mit ... verbinden?", "phrase"),
]

L4_RULES = [
    rule(
        "obwohl und trotzdem",
        "sentence_structure",
        """
Both say that something happens **against expectation**, but they build the
sentence differently.

**obwohl** (although) starts a **subordinate clause**: the verb goes to the
**end**.
- *Es hat sich nichts geändert, **obwohl** ich angerufen **habe**.*
- ***Obwohl** ich angerufen **habe**, **hat** sich nichts geändert.* (the main
  clause then starts with the verb)

**trotzdem** (nevertheless) is part of a **main clause**: the verb comes
**right after** it.
- *Ich habe angerufen. **Trotzdem hat** sich nichts geändert.*
- *Es hat sich **trotzdem** nichts geändert.*

| reason that should stop it | what happens anyway |
|---|---|
| *Obwohl es regnet, ...* | *... gehen wir spazieren.* |
| *Es regnet. Trotzdem ...* | *... gehen wir spazieren.* |

Don't use both at once: ~~Obwohl es regnet, trotzdem gehen wir~~.
""",
        [
            "Obwohl ich zwei E-Mails geschrieben habe, hat niemand reagiert.",
            "Das Heft ist nicht gekommen. Trotzdem soll ich bezahlen.",
            "Sie ging zur Arbeit, obwohl sie krank war.",
            "Er war müde. Er hat trotzdem weitergearbeitet.",
        ],
    ),
    rule(
        "Am Telefon: verbinden und zurückrufen",
        "other",
        """
**The caller:**
- *Guten Tag, hier spricht ... Ich rufe wegen ... an.*
- *Könnten Sie mich bitte mit der zuständigen Abteilung **verbinden**?*
- *Wie ist die **Durchwahl** von Frau ...?*

**The company:**
- *Firma ..., mein Name ist ..., was kann ich für Sie tun?*
- *Einen Moment bitte, ich **verbinde** Sie. / Bleiben Sie bitte **am Apparat**.*
- *Der Anschluss ist leider **besetzt**. / Frau ... ist heute **außer Haus**.*
- *Soll ich etwas **ausrichten**? / Kann sie Sie **zurückrufen**?*

On automatic lines: *Drücken Sie bitte die „3“.* · *Bitte halten Sie Ihre
Kundennummer **bereit**.*
""",
        [
            "Könnten Sie mich bitte mit Herrn Weber verbinden?",
            "Einen Moment bitte, bleiben Sie am Apparat.",
            "Soll ich ihm etwas ausrichten?",
        ],
    ),
    rule(
        "Eine Reklamation schreiben",
        "other",
        """
A formal complaint has a fixed shape:

1. **Betreff:** *Reklamation: Abonnement Nr. 4471*
2. **Anrede:** *Sehr geehrte Damen und Herren,* (or *Sehr geehrte Frau ...,*)
3. **The problem:** *seit vier Wochen erhalte ich keine Ausgabe, obwohl ich ...*
4. **What you did:** *Ich habe Ihnen bereits zweimal geschrieben. Trotzdem ...*
5. **What you want:** *Ich fordere Sie auf, ... · Bitte bestätigen Sie mir
   schriftlich, dass ...*
6. **A deadline:** *Falls ich bis zum 15. Mai keine Antwort erhalte, werde ich
   das Abo kündigen.*
7. **Gruß:** *Mit freundlichen Grüßen* (no comma after it), then your name.

Firm but polite: no exclamation marks, no *echt* or *total*.
""",
        [
            "Ich bin mit Ihrem Service nicht zufrieden.",
            "Bitte bestätigen Sie mir die Kündigung schriftlich.",
            "Mit freundlichen Grüßen",
        ],
    ),
]

L4_LESSONS = [
    lesson(
        "Ärger mit dem Abo",
        review("das Abonnement"),
        review("die Reklamation"),
        match(
            [
                ("das Abonnement", "jeden Monat kommt die Zeitschrift"),
                ("die Ausgabe", "ein Heft von einer Zeitschrift"),
                ("die Reklamation", "Man sagt, dass etwas nicht in Ordnung ist."),
                ("die Bestätigung", "Man bekommt es schriftlich: Es ist okay."),
                ("der Betreff", "das Thema von einer E-Mail"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Sie liest jeden Monat die gleiche Zeitschrift und bezahlt einmal im Jahr. Sie hat ...",
            "ein Abo.",
            "eine Durchwahl.",
            "einen Anrufbeantworter.",
        ),
        fill("Ich habe die Zeitschrift vor einem Jahr ___. (abonnieren)", "abonniert"),
        fill("Ich habe die Rechnung, aber keine einzige Ausgabe ___. (erhalten)", "erhalten"),
        fill("Ihr Service hat mich sehr ___. (enttäuschen)", "enttäuscht"),
        tr("I'm not satisfied with your service.", "Ich bin mit Ihrem Service nicht zufrieden."),
    ),
    lesson(
        "Obwohl ich angerufen habe ...",
        grammar("obwohl und trotzdem"),
        mc(
            "Which sentence is correct?",
            "Obwohl ich angerufen habe, hat niemand reagiert.",
            "Obwohl ich habe angerufen, hat niemand reagiert.",
            "Obwohl ich angerufen habe, niemand hat reagiert.",
        ),
        mc(
            "Ich habe zweimal geschrieben. ___ habe ich keine Antwort bekommen.",
            "Trotzdem",
            "Obwohl",
            "Weil",
        ),
        mc(
            "Sie ist zur Arbeit gegangen, ___ sie krank war.",
            "obwohl",
            "trotzdem",
            "deshalb",
        ),
        fill("Ich bezahle, ___ das Heft nicht kommt. (although)", "obwohl"),
        fill("Es regnet. Wir gehen ___ spazieren. (nevertheless)", "trotzdem"),
        order("Obwohl es spät war, hat sie noch angerufen."),
        order("Trotzdem ist die Lieferung nicht gekommen."),
        tr(
            "Although I wrote twice, nothing happened.",
            "Obwohl ich zweimal geschrieben habe, ist nichts passiert.",
        ),
        tr(
            "He was tired. Nevertheless he kept working.",
            "Er war müde. Trotzdem hat er weitergearbeitet.",
        ),
    ),
    lesson(
        "Drücken Sie bitte die 3",
        grammar("Am Telefon: verbinden und zurückrufen"),
        match(
            [
                ("Könnten Sie mich mit Frau Klein verbinden?", "Einen Moment, ich verbinde."),
                ("Ist Herr Weber da?", "Nein, er ist heute außer Haus."),
                ("Soll ich etwas ausrichten?", "Ja, er soll mich bitte zurückrufen."),
                ("Wie ist ihre Durchwahl?", "Die 214."),
            ],
            "Match the question to the answer.",
        ),
        mc(
            "Der Anschluss ist ...",
            "besetzt.",
            "behalten.",
            "gedrückt.",
        ),
        mc(
            "Bitte halten Sie Ihre Kundennummer ...",
            "bereit.",
            "außer Haus.",
            "am Apparat.",
        ),
        fill("___ Sie bitte die Taste 3! (drücken)", "Drücken"),
        fill("Ich ___ Ihre E-Mail an die Abteilung weiter. (weiterleiten)", "leite"),
        fill("Bleiben Sie bitte am ___. (on the line)", "Apparat"),
        order("Kann sie mich heute noch zurückrufen?", "Build the question."),
        tr("Could you put me through to the manager?", "Könnten Sie mich mit dem Chef verbinden?"),
    ),
    lesson(
        "Ein Brief an den Verlag",
        grammar("Eine Reklamation schreiben"),
        bank(
            "___: Abonnement Nr. 4471\n___ geehrte Damen und Herren,\nseit vier Wochen erhalte "
            "ich keine Ausgabe, ___ ich bezahlt habe. Ich habe Ihnen ___ zweimal geschrieben. "
            "Bitte ___ Sie mir schriftlich, wann das Heft kommt.\nMit ___ Grüßen\nJana Roth",
            ["Betreff", "Sehr", "obwohl", "bereits", "bestätigen", "freundlichen"],
            "trotzdem",
            "Liebe",
        ),
        mc(
            "Which closing is right for a formal letter?",
            "Mit freundlichen Grüßen",
            "Viele liebe Grüße!",
            "Tschüs!",
        ),
        mc(
            "Which sentence sounds firm but polite?",
            "Ich fordere Sie auf, mir das Geld zurückzuzahlen.",
            "Gebt mir sofort mein Geld!",
            "Echt total schlechter Service!",
        ),
        fill("Ich ___ Sie auf, das Problem zu lösen. (auffordern)", "fordere"),
        fill("Ich habe schon ___ angerufen. (several times)", "mehrfach"),
        fill("Ich habe ___ eine Kopie der Rechnung geschickt. (even)", "sogar"),
        tr(
            "Please confirm the cancellation in writing.",
            "Bitte bestätigen Sie mir die Kündigung schriftlich.",
        ),
    ),
    lesson(
        "Lektion 4: Test",
        fill("___ ich gewartet habe, kam niemand. (although)", "Obwohl"),
        mc("Er war krank. ___ ist er gekommen.", "Trotzdem", "Obwohl", "Falls"),
        fill("Sie ___ jeden Monat eine Rechnung. (erhalten)", "erhält"),
        mc("Frau Berg ist heute ...", "außer Haus.", "am Haus.", "aus dem Haus raus."),
        fill("Soll ich etwas ___? (pass on)", "ausrichten"),
        order("Obwohl der Anschluss besetzt war, habe ich gewartet."),
        tr("I'm calling about a complaint.", "Ich rufe wegen einer Reklamation an."),
        tr("We kept the magazine.", "Wir haben die Zeitschrift behalten."),
    ),
]

LEKTION_4 = unit(
    4,
    "Obwohl ich Ihnen das erklärt habe, ...",
    "Kundenservice und Reklamation",
    L4_WORDS,
    L4_RULES,
    sections(L4_LESSONS, vocab_lessons(L4_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 5: Bald wird in fast jedem Haushalt ein PC stehen.
# ============================================================================

L5_WORDS = [
    ("the network", "das Netzwerk", "noun", "Pl. die Netzwerke"),
    ("the technology (field)", "die Technologie", "noun", "Pl. die Technologien"),
    ("the hard drive", "die Festplatte", "noun", "Pl. die Festplatten"),
    ("the drive (disk drive)", "das Laufwerk", "noun", "Pl. die Laufwerke"),
    ("the monitor", "der Monitor", "noun", "Pl. die Monitore"),
    ("the robot", "der Roboter", "noun", "Pl. die Roboter"),
    ("the device", "das Gerät", "noun", "Pl. die Geräte"),
    ("the technology", "die Technik", "noun"),
    ("the progress", "der Fortschritt", "noun", "Pl. die Fortschritte"),
    ("the development", "die Entwicklung", "noun", "Pl. die Entwicklungen"),
    ("the invention", "die Erfindung", "noun", "Pl. die Erfindungen"),
    ("the communication", "die Kommunikation", "noun"),
    ("the forecast / prediction", "die Vorhersage", "noun", "Pl. die Vorhersagen"),
    ("the guess / assumption", "die Vermutung", "noun", "Pl. die Vermutungen"),
    ("the warning", "die Warnung", "noun", "Pl. die Warnungen"),
    ("the resolution", "der Vorsatz", "noun", "Pl. die Vorsätze"),
    ("the promise", "das Versprechen", "noun", "Pl. die Versprechen"),
    ("the alternative", "die Alternative", "noun", "Pl. die Alternativen"),
    ("the sense / meaning", "der Sinn", "noun", "Das hat keinen Sinn."),
    ("the system", "das System", "noun", "Pl. die Systeme"),
    ("the opinion / view", "die Ansicht", "noun", "der Ansicht sein, dass ..."),
    ("the conviction", "die Überzeugung", "noun", "der Überzeugung sein, dass ..."),
    ("the transport", "der Transport", "noun", "Pl. die Transporte"),
    ("the file", "die Datei", "noun", "Pl. die Dateien"),
    ("to suspect / to assume", "vermuten", "verb", "hat vermutet"),
    ("to claim", "behaupten", "verb", "hat behauptet"),
    ("to warn", "warnen", "verb", "warnen vor + Dat."),
    ("to promise", "versprechen", "verb", "verspricht, versprach, hat versprochen"),
    ("to save (a file)", "speichern", "verb", "hat gespeichert"),
    ("to print out", "ausdrucken", "verb", "hat ausgedruckt"),
    ("to delete", "löschen", "verb", "hat gelöscht"),
    ("to invent", "erfinden", "verb", "erfand, hat erfunden"),
    ("to replace", "ersetzen", "verb", "hat ersetzt"),
    ("to be afraid", "fürchten", "verb", "sich fürchten vor + Dat."),
    ("to make an effort", "anstrengen", "verb", "sich anstrengen"),
    ("presumably", "vermutlich", "adverb"),
    ("technical", "technisch", "adjective"),
    ("personal", "persönlich", "adjective"),
    ("distant", "fern", "adjective", "in ferner Zukunft"),
    ("round the clock", "rund um die Uhr", "phrase"),
    (
        "Soon there'll be a PC in almost every household.",
        "Bald wird in fast jedem Haushalt ein PC stehen.",
        "phrase",
    ),
]

L5_RULES = [
    rule(
        "Futur I: werden + Infinitiv",
        "verbs",
        """
To talk about the future, German often just uses the **present tense with a
time word**: *Morgen **kaufe** ich einen Laptop.*

The **Futur I** is **werden** (in position 2) + the **infinitive at the end**:

| | werden | |
|---|---|---|
| ich | werde | *Ich **werde** mehr Sport **machen**.* |
| du | wirst | *Du **wirst** das schaffen.* |
| er / sie / es | wird | *Bald **wird** jeder einen Roboter **haben**.* |
| wir | werden | |
| ihr | werdet | |
| sie / Sie | werden | |

In a subordinate clause *werden* goes to the very end: *Ich glaube, dass es
bald mehr Roboter **geben wird**.*

Don't mix it up with *wollen*: *Ich **will** ...* = I want to, *Ich **werde**
...* = I will.
""",
        [
            "Bald wird in fast jedem Haushalt ein PC stehen.",
            "In zwanzig Jahren werden Roboter viele Arbeiten machen.",
            "Ich glaube, dass wir weniger Auto fahren werden.",
        ],
    ),
    rule(
        "Vorhersage, Vorsatz oder Aufforderung?",
        "verbs",
        """
The Futur I can do three different jobs:

| job | example | signal words |
|---|---|---|
| **Vorhersage / Vermutung** (guess) | *Es **wird** morgen **regnen**.* | *wohl, vermutlich, wahrscheinlich, bestimmt* |
| **Vorsatz / Versprechen** (plan, promise) | *Ich **werde** nie wieder zu spät **kommen**.* | *ab morgen, nie wieder, ganz sicher* |
| **Aufforderung / Warnung** (order) | *Du **wirst** jetzt dein Zimmer **aufräumen**!* | strong tone, often *jetzt, sofort* |

With *wohl* the Futur I makes a guess about **now**: *Er ist nicht da. Er
**wird wohl** krank **sein**.* (He's probably ill.)
""",
        [
            "Vermutlich wird es im Winter wieder kälter.",
            "Ich werde ab morgen jeden Tag Deutsch lernen.",
            "Ihr werdet jetzt sofort schlafen gehen!",
        ],
    ),
    rule(
        "Meinungen über die Zukunft",
        "other",
        """
To give your view on the future:

- *Ich **glaube / vermute / bin der Ansicht**, dass ...* (verb at the end)
- *Ich **bin der Überzeugung**, dass ...*
- *Ich **kann mir (nicht) vorstellen**, dass ...*
- *Das **halte ich für möglich / unmöglich**.*
- *Vermutlich / Wahrscheinlich wird ...*

To disagree: *Das glaube ich nicht. · Da bin ich anderer Ansicht. · Es gibt
doch eine Alternative.*
""",
        [
            "Ich bin der Ansicht, dass Roboter uns helfen werden.",
            "Ich kann mir nicht vorstellen, dass Bücher verschwinden.",
            "Das halte ich für unmöglich.",
        ],
    ),
]

L5_LESSONS = [
    lesson(
        "Computer früher und heute",
        review("die Festplatte"),
        review("der Roboter"),
        match(
            [
                ("die Festplatte", "Hier sind die Dateien gespeichert."),
                ("der Monitor", "Hier sieht man das Bild."),
                ("der Roboter", "eine Maschine, die selbst arbeitet"),
                ("der Laptop", "ein kleiner Computer zum Mitnehmen"),
                ("die Erfindung", "etwas ganz Neues"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Ich habe die Datei aus Versehen ...",
            "gelöscht.",
            "erfunden.",
            "versprochen.",
        ),
        fill("Vergiss nicht, die Datei zu ___! (save)", "speichern"),
        fill("Kannst du mir den Text ___? (print out)", "ausdrucken"),
        fill("Wer hat das Telefon ___? (erfinden)", "erfunden"),
        tr("The technology is making great progress.", "Die Technik macht große Fortschritte."),
    ),
    lesson(
        "Bald wird ...",
        grammar("Futur I: werden + Infinitiv"),
        conj("werden", "ich", "werde"),
        conj("werden", "du", "wirst"),
        conj("werden", "er", "wird"),
        conj("werden", "ihr", "werdet"),
        fill("In zehn Jahren ___ jeder einen Roboter haben. (werden)", "wird"),
        fill("Wir werden bald weniger Papier ___. (brauchen)", "brauchen"),
        mc(
            "Which sentence is correct?",
            "Ich glaube, dass es bald mehr Roboter geben wird.",
            "Ich glaube, dass es wird bald mehr Roboter geben.",
            "Ich glaube, dass es bald wird mehr Roboter geben.",
        ),
        mc("Ich ___ dir morgen helfen. (I will)", "werde", "will", "wurde"),
        order("Roboter werden viele Arbeiten machen."),
        tr("Soon everyone will work from home.", "Bald wird jeder von zu Hause arbeiten."),
    ),
    lesson(
        "Vorhersage, Vorsatz oder Aufforderung?",
        grammar("Vorhersage, Vorsatz oder Aufforderung?"),
        match(
            [
                ("Es wird wohl regnen.", "Vorhersage"),
                ("Ich werde nie wieder zu spät kommen.", "Vorsatz"),
                ("Du wirst jetzt sofort aufräumen!", "Aufforderung"),
            ],
            "What is the sentence doing?",
        ),
        mc(
            "Er geht nicht ans Telefon. Er ___ wohl schlafen.",
            "wird",
            "will",
            "wurde",
        ),
        mc(
            "Which is a promise (Versprechen)?",
            "Ich werde dich jeden Tag anrufen.",
            "Es wird morgen schneien.",
            "Vermutlich wird der Zug Verspätung haben.",
        ),
        fill("___ wird es morgen regnen. (presumably)", "Vermutlich|Wahrscheinlich"),
        fill("Ich ___ ab morgen mehr Sport machen. (werden)", "werde"),
        fill("Der Arzt hat mich vor zu viel Zucker ___. (warnen)", "gewarnt"),
        order("Ich werde mich mehr anstrengen."),
        tr("You will tidy your room now!", "Du wirst jetzt dein Zimmer aufräumen!"),
    ),
    lesson(
        "Sinn und Unsinn",
        grammar("Meinungen über die Zukunft"),
        bank(
            "Herr Lang ist der ___, dass Computer unser Leben besser machen. Er ___, dass "
            "Roboter bald viele Arbeiten übernehmen werden. Frau Kühn ist anderer ___: Sie "
            "fürchtet, dass Maschinen die Menschen ___. Für sie hat das keinen ___.",
            ["Überzeugung", "vermutet", "Ansicht", "ersetzen", "Sinn"],
            "Vorsatz",
            "speichert",
        ),
        mc(
            "Das halte ich für unmöglich. means:",
            "I think that's impossible.",
            "I keep it in my hand.",
            "I think that's possible.",
        ),
        fill("Ich kann mir nicht ___, ohne Handy zu leben. (imagine)", "vorstellen"),
        fill("Der Chef ___, dass er alles weiß. (behaupten)", "behauptet"),
        fill("Die Maschine arbeitet ___ um die Uhr. (round)", "rund"),
        fill("Es gibt doch eine ___! (alternative)", "Alternative"),
        tr(
            "I believe that robots will help us.",
            "Ich glaube, dass Roboter uns helfen werden.",
        ),
    ),
    lesson(
        "Lektion 5: Test",
        fill("Morgen ___ es bestimmt regnen. (werden)", "wird"),
        fill("Ihr ___ das sicher schaffen. (werden)", "werdet"),
        mc("Ich weiß, dass er morgen kommen ___.", "wird", "werden", "wirst"),
        mc("Es wird ___ schneien.", "wohl", "will", "werde"),
        fill("Hast du die Datei ___? (speichern)", "gespeichert"),
        order("In Zukunft werden wir weniger Auto fahren."),
        tr("I promise you that.", "Das verspreche ich dir."),
        tr("She will probably be ill.", "Sie wird wohl krank sein."),
    ),
]

LEKTION_5 = unit(
    5,
    "Bald wird in fast jedem Haushalt ein PC stehen.",
    "Technik und Zukunft",
    L5_WORDS,
    L5_RULES,
    sections(L5_LESSONS, vocab_lessons(L5_WORDS, "Wörter")),
)


# ============================================================================
# Lektion 6: Fühlen Sie sich wie zu Hause.
# ============================================================================

L6_WORDS = [
    ("the host", "der Gastgeber", "noun", "f. die Gastgeberin"),
    ("the host's gift", "das Gastgeschenk", "noun", "Pl. die Gastgeschenke"),
    ("the hospitality", "die Gastfreundschaft", "noun"),
    ("the greeting", "die Begrüßung", "noun", "Pl. die Begrüßungen"),
    ("the farewell", "der Abschied", "noun", "Pl. die Abschiede"),
    ("the aperitif", "der Aperitif", "noun", "Pl. die Aperitifs"),
    ("the dessert", "der Nachtisch", "noun", "zum Nachtisch"),
    ("the cutlery", "das Besteck", "noun"),
    ("the bunch of flowers", "der Blumenstrauß", "noun", "Pl. die Blumensträuße"),
    ("the sparkling wine", "der Sekt", "noun"),
    ("the business meal", "das Geschäftsessen", "noun", "Pl. die Geschäftsessen"),
    ("the table manners", "die Tischmanieren", "noun", "only plural"),
    ("the custom", "die Sitte", "noun", "Pl. die Sitten"),
    ("the punctuality", "die Pünktlichkeit", "noun"),
    ("the delay", "die Verspätung", "noun", "Pl. die Verspätungen"),
    ("the canteen", "die Kantine", "noun", "Pl. die Kantinen"),
    ("the order (sequence)", "die Reihenfolge", "noun", "Pl. die Reihenfolgen"),
    ("the conversation", "die Unterhaltung", "noun", "Pl. die Unterhaltungen"),
    ("the understanding", "das Verständnis", "noun", "Verständnis haben für + Akk."),
    ("the sign / signal", "das Zeichen", "noun", "Pl. die Zeichen"),
    ("the trouble / bother", "die Umstände", "noun", "only plural: Das macht keine Umstände."),
    ("to decline", "ablehnen", "verb", "hat abgelehnt"),
    ("to accept", "annehmen", "verb", "nimmt an, hat angenommen"),
    ("to greet / to welcome", "begrüßen", "verb", "hat begrüßt"),
    ("to say thank you", "bedanken", "verb", "sich bedanken für + Akk."),
    ("to behave", "verhalten", "verb", "sich verhalten, verhält sich, hat sich verhalten"),
    ("to observe (rules)", "beachten", "verb", "hat beachtet"),
    ("to offend", "beleidigen", "verb", "hat beleidigt"),
    ("to smell", "riechen", "verb", "roch, hat gerochen"),
    ("to spend (time)", "verbringen", "verb", "verbrachte, hat verbracht"),
    ("to leave (a place)", "verlassen", "verb", "verlässt, verließ, hat verlassen"),
    ("to fulfil", "erfüllen", "verb", "einen Wunsch erfüllen"),
    ("to happen", "geschehen", "verb", "geschieht, geschah, ist geschehen"),
    ("rude", "unhöflich", "adjective"),
    ("in time", "rechtzeitig", "adverb"),
    ("allergic", "allergisch", "adjective", "allergisch gegen + Akk."),
    ("drunk", "betrunken", "adjective"),
    ("in case / if", "falls", "other"),
    ("to be in a hurry", "es eilig haben", "phrase"),
    ("You're welcome.", "Gern geschehen.", "phrase"),
    ("Make yourself at home.", "Fühlen Sie sich wie zu Hause.", "phrase"),
]

L6_RULES = [
    rule(
        "falls: Bedingungen",
        "sentence_structure",
        """
**falls** (in case, if) introduces a **condition**. Like *wenn* and *weil* it
starts a subordinate clause, so the verb goes to the **end**:

- *Rufen Sie bitte an, **falls** Sie später **kommen**.*
- ***Falls** Sie später **kommen**, **rufen** Sie bitte an.* (main clause starts
  with the verb)

*falls* stresses that something **might or might not** happen; *wenn* is the
general "if / when". Often both are possible:
*Falls / Wenn Sie satt sind, legen Sie das Besteck auf den Teller.*

Don't confuse it with *obwohl*: *falls* = condition, *obwohl* = against
expectation.
""",
        [
            "Falls Sie Vegetarier sind, kochen wir Gemüse.",
            "Bring bitte Wein mit, falls du Zeit hast.",
            "Falls es regnet, essen wir drinnen.",
        ],
    ),
    rule(
        "Gastgeber und Gast",
        "other",
        """
**The host:**
- *Herzlich willkommen! Schön, dass Sie da sind. Kommen Sie doch rein.*
- *Fühlen Sie sich wie zu Hause. · Darf ich Ihnen etwas anbieten?*
- *Möchten Sie noch etwas? · Greifen Sie zu!*

**The guest:**
- *Vielen Dank für die Einladung. Die Blumen sind für Sie.*
- *Das riecht aber gut! · Das hat ausgezeichnet geschmeckt.*
- *Nein danke, ich bin schon satt. · Ich bin leider allergisch gegen Nüsse.*
- *Wenn es keine Umstände macht, hätte ich gern Wasser.*
- *Es ist schon spät, ich muss leider gehen.*

**Answers:** *Danke! **Gern geschehen**.* · *Kein Problem. · Das macht keine
Umstände.* · *Kommen Sie gut nach Hause!*
""",
        [
            "Darf ich Ihnen ein Glas Sekt anbieten?",
            "Vielen Dank, das hat wunderbar geschmeckt.",
            "Noch einmal herzlichen Dank für den schönen Abend!",
        ],
    ),
]

L6_LESSONS = [
    lesson(
        "Eine Einladung zum Essen",
        review("der Gastgeber"),
        review("das Gastgeschenk"),
        match(
            [
                ("der Aperitif", "ein Getränk vor dem Essen"),
                ("der Nachtisch", "etwas Süßes nach dem Essen"),
                ("das Besteck", "Messer, Gabel und Löffel"),
                ("das Gastgeschenk", "Blumen oder Wein für den Gastgeber"),
                ("die Begrüßung", "Hallo! Herzlich willkommen!"),
            ],
            "Match the word to its meaning.",
        ),
        mc(
            "Er kommt immer genau um acht Uhr. Für ihn ist ___ wichtig.",
            "die Pünktlichkeit",
            "die Verspätung",
            "der Abschied",
        ),
        mc(
            "Ich kann leider nicht kommen. Ich muss die Einladung ...",
            "ablehnen.",
            "annehmen.",
            "riechen.",
        ),
        fill("Wir haben einen schönen Abend zusammen ___. (verbringen)", "verbracht"),
        fill("Ich ___ mich herzlich für die Einladung. (bedanken)", "bedanke"),
        tr("Make yourself at home. (Sie)", "Fühlen Sie sich wie zu Hause."),
    ),
    lesson(
        "Falls Sie Vegetarier sind ...",
        grammar("falls: Bedingungen"),
        mc(
            "Which sentence is correct?",
            "Falls Sie später kommen, rufen Sie bitte an.",
            "Falls Sie kommen später, rufen Sie bitte an.",
            "Falls Sie später kommen, Sie rufen bitte an.",
        ),
        mc(
            "Bring bitte Wasser mit, ___ du Zeit hast.",
            "falls",
            "obwohl",
            "trotzdem",
        ),
        fill("___ Sie satt sind, legen Sie das Besteck auf den Teller. (in case)", "Falls"),
        fill("Falls es regnet, ___ wir drinnen. (essen)", "essen"),
        fill("Sagen Sie Bescheid, falls Sie allergisch gegen etwas ___. (sein)", "sind"),
        order("Falls du Hunger hast, gibt es noch Suppe."),
        order("Wir kochen Gemüse, falls die Gäste kein Fleisch essen."),
        tr(
            "In case you're late, please call. (Sie)",
            "Falls Sie zu spät kommen, rufen Sie bitte an.",
        ),
    ),
    lesson(
        "Schwierige Gäste",
        grammar("Gastgeber und Gast"),
        match(
            [
                ("Vielen Dank für die Blumen!", "Gern geschehen."),
                ("Möchten Sie noch etwas Braten?", "Nein danke, ich bin schon satt."),
                ("Darf ich Ihnen Sekt anbieten?", "Danke, aber ich trinke keinen Alkohol."),
                ("Es ist schon spät, ich muss gehen.", "Kommen Sie gut nach Hause!"),
            ],
            "Host or guest: match the answers.",
        ),
        mc(
            "Polite way to ask for something else:",
            "Wenn es keine Umstände macht, hätte ich gern Wasser.",
            "Ich will Wasser, sofort.",
            "Wasser! Schnell!",
        ),
        mc(
            "Das riecht aber gut! is said by ...",
            "the guest",
            "the host",
        ),
        fill("Ich bin leider ___ gegen Nüsse. (allergic)", "allergisch"),
        fill("Sie hat es ___, sie muss zum Zug. (in a hurry)", "eilig"),
        fill("Es ist nicht höflich, die Gastgeber zu ___. (offend)", "beleidigen"),
        tr("Thank you, that tasted excellent.", "Danke, das hat ausgezeichnet geschmeckt."),
    ),
    lesson(
        "Tipps für ein Geschäftsessen",
        bank(
            "Beim ___ sollten Sie pünktlich sein. ___ Sie zu spät kommen, rufen Sie an. "
            "Begrüßen Sie zuerst den ___. Beginnen Sie erst mit dem Essen, wenn alle etwas "
            "haben. Sprechen Sie nicht über Geld, das ist ___. Am Ende ___ Sie sich für die "
            "Einladung.",
            ["Geschäftsessen", "Falls", "Gastgeber", "unhöflich", "bedanken"],
            "Nachtisch",
            "Obwohl",
        ),
        mc(
            "Welche Sitte gilt in Deutschland oft?",
            "Man ist pünktlich.",
            "Man kommt eine Stunde zu spät.",
            "Man bringt kein Gastgeschenk.",
        ),
        mc(
            "Man sollte nach dem Essen nicht betrunken sein. betrunken means:",
            "drunk",
            "full",
            "rude",
        ),
        fill("Man sollte die Tischmanieren ___. (observe)", "beachten"),
        fill("Ich habe das Restaurant um elf ___. (verlassen)", "verlassen"),
        fill("Kommen Sie bitte ___. (in time)", "rechtzeitig"),
        tr("We had a great conversation.", "Wir hatten eine tolle Unterhaltung."),
    ),
    lesson(
        "Lektion 6: Test",
        fill("___ du kommst, bring bitte Brot mit. (in case)", "Falls"),
        mc("Falls Sie Fragen haben, ___ Sie mich an.", "rufen", "Sie rufen", "rief"),
        fill("Vielen Dank! Gern ___. (geschehen)", "geschehen"),
        mc("Nach dem Essen sagt man:", "Das hat sehr gut geschmeckt.", "Das riecht nicht gut."),
        fill("Sie hat die Einladung ___. (annehmen)", "angenommen"),
        order("Falls es regnet, bleiben wir zu Hause."),
        tr("Thank you for the invitation.", "Vielen Dank für die Einladung."),
        tr("He left the party early.", "Er hat die Party früh verlassen."),
    ),
    lesson(
        "Modul 2: Wiederholung",
        fill("___ ich angerufen habe, hat niemand reagiert. (although)", "Obwohl"),
        fill("Ich war müde. ___ bin ich mitgekommen. (nevertheless)", "Trotzdem"),
        fill("In Zukunft ___ wir mehr von zu Hause arbeiten. (werden)", "werden"),
        mc("Er ist nicht da. Er wird ___ krank sein.", "wohl", "will", "obwohl"),
        mc("___ Sie Vegetarier sind, kochen wir Gemüse.", "Falls", "Trotzdem", "Obwohl"),
        fill("Könnten Sie mich bitte mit Frau Weber ___? (put through)", "verbinden"),
        bank(
            "Liebe Mia, ___ ich viel Arbeit habe, komme ich gern zu deinem Fest. Ich ___ "
            "Kuchen mitbringen. ___ du noch etwas brauchst, schreib mir! Ich habe "
            "keine Zeit zum Einkaufen, aber ich komme ___.",
            ["obwohl", "werde", "Falls", "trotzdem"],
            "wird",
            "weil",
        ),
        tr("I'm calling about my order.", "Ich rufe wegen meiner Bestellung an."),
        order("Ich werde nie wieder zu spät kommen."),
    ),
]

LEKTION_6 = unit(
    6,
    "Fühlen Sie sich wie zu Hause.",
    "Einladungen und Gastfreundschaft",
    L6_WORDS,
    L6_RULES,
    sections(L6_LESSONS, vocab_lessons(L6_WORDS, "Wörter")),
)


UNITS = [LEKTION_4, LEKTION_5, LEKTION_6]
