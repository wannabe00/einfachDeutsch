"""A1 check content: what the review of each Lektion and each Modul test asks
beyond the generated word batches (see apps.curriculum.checks).

Per Lektion: five gap sentences ("Ich [heiße] Anna.", answers in brackets,
alternatives as "[Räum|Räume]") with a couple of distractor chips, and four
English -> German translations that only need words and grammar taught so far.
Per Modul (three Lektionen): the extra test formats. `modul_check` keeps only
the formats the difficulty ramp allows at that point, and `lektion_check` turns
gaps and translations into chips, tiles or typing the same way.

All sentences are original.
"""

from ..dsl import lektion_check, modul_check

LEVEL = "A1"


def _l(n, gaps, translations, distractors=()):
    return n, lektion_check(LEVEL, n, gaps, translations, distractors)


LEKTION_CHECKS = dict(
    [
        _l(
            1,
            [
                "Ich [heiße] Nicole.",
                "Woher [kommst] du?",
                "Ich komme aus [Österreich].",
                "[Wie] geht es Ihnen?",
                "Guten [Morgen], Frau Weber!",
            ],
            [
                ("My name is Anna.", "Ich heiße Anna."),
                ("Where do you come from?", "Woher kommst du?"),
                ("I come from Georgia.", "Ich komme aus Georgien."),
                ("I come from Spain too.", "Ich komme auch aus Spanien."),
            ],
            ["woher", "bist"],
        ),
        _l(
            2,
            [
                "Ich [arbeite] als Journalistin.",
                "Wo [wohnst] du?",
                "Ich bin nicht [verheiratet].",
                "Was [machst] du beruflich?",
                "Ich bin [zwanzig] Jahre alt.",
            ],
            [
                ("I live in Berlin.", "Ich wohne in Berlin."),
                ("What do you do for a living?", "Was machst du beruflich?"),
                ("I am not married.", "Ich bin nicht verheiratet."),
                ("We work together.", "Wir arbeiten zusammen."),
            ],
            ["wohnt", "falsch"],
        ),
        _l(
            3,
            [
                "Das ist [meine] Mutter.",
                "Ist das [dein] Bruder?",
                "[Sprichst] du Englisch?",
                "Du sprichst nicht Spanisch? – [Doch], ein bisschen.",
                "Wie [viele] Geschwister hast du?",
            ],
            [
                ("This is my father.", "Das ist mein Vater."),
                ("Do you speak French?", "Sprichst du Französisch?"),
                (
                    "My sister speaks a little Italian.",
                    "Meine Schwester spricht ein bisschen Italienisch.",
                ),
                ("Are those your parents?", "Sind das deine Eltern?"),
            ],
            ["mein", "spricht"],
        ),
        _l(
            4,
            [
                "[Der] Tisch ist schön.",
                "Die Lampe ist toll. [Sie] ist modern.",
                "Wie viel [kostet] das Sofa?",
                "Das ist zu [teuer].",
                "Das Bett ist schön. [Es] kostet 300 Euro.",
            ],
            [
                ("The chair costs 50 euros.", "Der Stuhl kostet 50 Euro."),
                ("The lamp is very modern.", "Die Lampe ist sehr modern."),
                ("I find the sofa ugly.", "Ich finde das Sofa hässlich."),
                ("How much does the table cost?", "Wie viel kostet der Tisch?"),
            ],
            ["Er", "billig"],
        ),
        _l(
            5,
            [
                "Das ist [ein] Stift.",
                "Ist das eine Uhr? – Nein, das ist [keine] Uhr.",
                "Ich habe zwei [Bücher].",
                "Die Tasche ist [rot].",
                "Wie heißt das auf [Deutsch]?",
            ],
            [
                ("That is a key.", "Das ist ein Schlüssel."),
                ("That is not a book.", "Das ist kein Buch."),
                ("The glasses are new.", "Die Brille ist neu."),
                ("The bag is black.", "Die Tasche ist schwarz."),
            ],
            ["eine", "Buch"],
        ),
        _l(
            6,
            [
                "Ich brauche [einen] Computer.",
                "Wir suchen [eine] Sekretärin.",
                "Ich brauche [kein] Büro.",
                "Ich habe heute [keinen] Termin.",
                "Hier [ist] Anna Weber. Ich habe eine Frage.",
            ],
            [
                ("I need a printer.", "Ich brauche einen Drucker."),
                ("We are looking for a laptop.", "Wir suchen einen Laptop."),
                ("I don't have a mobile phone.", "Ich habe kein Handy."),
                ("I have a question.", "Ich habe eine Frage."),
            ],
            ["ein", "nicht"],
        ),
        _l(
            7,
            [
                "[Kannst] du schwimmen?",
                "Ich [kann] leider nicht tanzen.",
                "Er [liest] gern Bücher.",
                "Anna [trifft] heute Freunde.",
                "Ich koche [gern], aber ich backe [nie].",
            ],
            [
                ("Can you dance?", "Kannst du tanzen?"),
                ("I like reading.", "Ich lese gern."),
                ("We often go for a walk.", "Wir gehen oft spazieren."),
                ("Unfortunately I can't swim.", "Ich kann leider nicht schwimmen."),
            ],
            ["können", "fährt"],
        ),
        _l(
            8,
            [
                "Wie spät [ist] es?",
                "Das Konzert ist [um] acht Uhr.",
                "[Am] Montag habe ich keine Zeit.",
                "Hast du [Lust]? Wir gehen ins Kino.",
                "Morgen [gehe] ich ins Museum.",
            ],
            [
                ("On Saturday I am going to the theatre.", "Am Samstag gehe ich ins Theater."),
                ("Do you have time tomorrow?", "Hast du morgen Zeit?"),
                ("The concert is at nine o'clock.", "Das Konzert ist um neun Uhr."),
                ("Maybe another time.", "Vielleicht ein anderes Mal."),
            ],
            ["im", "Zeit"],
        ),
        _l(
            9,
            [
                "Ich [möchte] einen Kaffee, bitte.",
                "[Magst] du Fisch?",
                "Wir [mögen] keinen Käse.",
                "Ich esse ein [Brötchen] mit Butter.",
                "Das [schmeckt] gut!",
            ],
            [
                ("I would like a tea.", "Ich möchte einen Tee."),
                ("Do you like vegetables?", "Magst du Gemüse?"),
                ("The soup tastes good.", "Die Suppe schmeckt gut."),
                ("We would like to eat something.", "Wir möchten etwas essen."),
            ],
            ["möchtest", "Brot"],
        ),
        _l(
            10,
            [
                "Ich [steige] in Köln [um].",
                "Wann [fährt] der Zug ab?",
                "Ich [nehme] den Bus.",
                "Wir [rufen] Oma [an].",
                "Ich gehe zu [Fuß].",
            ],
            [
                ("I get up at seven o'clock.", "Ich stehe um sieben Uhr auf."),
                ("The train leaves at ten o'clock.", "Der Zug fährt um zehn Uhr ab."),
                ("I take the tram.", "Ich nehme die Straßenbahn."),
                ("We're going shopping today.", "Wir kaufen heute ein."),
            ],
            ["ab", "nimmst"],
        ),
        _l(
            11,
            [
                "Ich [habe] gestern Fußball gespielt.",
                "Was hast du heute [gemacht]?",
                "Wir haben lange [geschlafen].",
                "Hast du die Wohnung [aufgeräumt]?",
                "Sie hat zwei Stunden mit Oma [telefoniert].",
            ],
            [
                ("I bought a present.", "Ich habe ein Geschenk gekauft."),
                ("What did you do yesterday?", "Was hast du gestern gemacht?"),
                ("We learned German.", "Wir haben Deutsch gelernt."),
                ("She tidied up.", "Sie hat aufgeräumt."),
            ],
            ["hat", "gelacht"],
        ),
        _l(
            12,
            [
                "Was ist [passiert]?",
                "Wir [sind] nach Hamburg gefahren.",
                "Mein Geburtstag ist im [Mai].",
                "Im Sommer [gibt] es viele Feste.",
                "Ich bin zu Hause [geblieben].",
            ],
            [
                ("I stayed at home.", "Ich bin zu Hause geblieben."),
                ("My birthday is in June.", "Mein Geburtstag ist im Juni."),
                ("What happened?", "Was ist passiert?"),
                ("We drove to Vienna.", "Wir sind nach Wien gefahren."),
            ],
            ["habe", "hat"],
        ),
        _l(
            13,
            [
                ("Die Post ist neben [der] Bank.", "die Bank"),
                ("Das Auto steht vor [dem] Hotel.", "das Hotel"),
                ("Gehen Sie hier [links].", "left"),
                ("Das Café ist [zwischen] der Post und der Bank.", "between"),
                ("Fahren Sie [geradeaus] bis zur Ampel.", "straight on"),
            ],
            [
                ("The hotel is next to the bridge.", "Das Hotel ist neben der Brücke."),
                ("Turn right at the traffic light.", "Biegen Sie an der Ampel rechts ab."),
                ("I'm not from here.", "Ich bin nicht von hier."),
                ("The bank is behind the cathedral.", "Die Bank ist hinter dem Dom."),
            ],
        ),
        _l(
            14,
            [
                ("Das ist Paul und das ist [sein] Haus.", "his"),
                ("Lisa liebt [ihren] Garten.", "her"),
                ("Wie findest du [Ottos] Wohnung?", "Otto"),
                ("Die Wohnung hat einen [Balkon].", "balcony"),
                ("Die Miete [kostet] 800 Euro.", "kosten"),
            ],
            [
                ("His kitchen is small.", "Seine Küche ist klein."),
                ("Her apartment has a garden.", "Ihre Wohnung hat einen Garten."),
                ("The bathroom is upstairs.", "Das Bad ist oben."),
                ("How do you like Anna's room?", "Wie findest du Annas Zimmer?"),
            ],
        ),
        _l(
            15,
            [
                ("Das Buch gehört [mir].", "ich"),
                ("Wie geht es [dir]?", "du"),
                ("Ich gratuliere [ihm] zum Geburtstag.", "er"),
                ("Die Stadt gefällt [uns] sehr.", "wir"),
                ("Mir [fehlt] meine Heimat.", "fehlen"),
            ],
            [
                ("I like the old town.", "Die Altstadt gefällt mir."),
                ("I thank you.", "Ich danke dir."),
                ("The bag belongs to him.", "Die Tasche gehört ihm."),
                ("The market is around the corner.", "Der Markt ist um die Ecke."),
            ],
        ),
        _l(
            16,
            [
                ("Der Kurs fängt in [einer] Stunde an.", "eine"),
                ("[Nach] dem Kurs gehe ich nach Hause.", "after"),
                ("Der Föhn [funktioniert] nicht.", "funktionieren"),
                ("Können Sie [bitte] den Techniker schicken?", "please"),
                ("Das Geschenk ist [für] meine Mutter.", "for"),
            ],
            [
                ("The heating doesn't work.", "Die Heizung funktioniert nicht."),
                (
                    "Can you repair the TV, please?",
                    "Können Sie bitte den Fernseher reparieren?",
                    "Können Sie den Fernseher bitte reparieren?",
                ),
                ("I'd like to postpone the appointment.", "Ich möchte den Termin verschieben."),
                ("The present is for my sister.", "Das Geschenk ist für meine Schwester."),
            ],
        ),
        _l(
            17,
            [
                ("Ich [will] Popstar werden.", "wollen"),
                ("Er [wird] Arzt.", "werden"),
                ("Ich fahre mit [dem] Motorrad.", "das Motorrad"),
                ("Ich trinke Kaffee ohne [Milch].", "milk"),
                ("Wir [wollen] im Ausland studieren.", "wollen"),
            ],
            [
                ("I want to learn the guitar.", "Ich will Gitarre lernen."),
                ("She is becoming a singer.", "Sie wird Sängerin."),
                ("He travels without money.", "Er reist ohne Geld."),
                ("I'm going with my brother.", "Ich fahre mit meinem Bruder."),
            ],
        ),
        _l(
            18,
            [
                ("Der Arzt sagt, ich [soll] viel Tee trinken.", "sollen"),
                ("[Nehmen] Sie diese Tabletten.", "nehmen"),
                ("Mein Kopf [tut] weh.", "wehtun"),
                ("Ich habe [Fieber].", "a fever"),
                ("Trinken Sie [diesen] Tee.", "dieser"),
            ],
            [
                ("My back hurts.", "Mein Rücken tut weh."),
                ("Take this medicine.", "Nehmen Sie dieses Medikament."),
                ("He should sleep a lot.", "Er soll viel schlafen."),
                ("Get well soon!", "Gute Besserung!"),
            ],
        ),
        _l(
            19,
            [
                ("Früher [war] er schlank.", "sein"),
                ("Gestern [hatte] ich Kopfschmerzen.", "haben"),
                ("Ich habe die Telefonnummer [vergessen].", "vergessen"),
                ("Er ist nicht freundlich, er ist [unfreundlich].", "un-"),
                ("Wir [waren] letzte Woche in Rom.", "sein"),
            ],
            [
                ("He used to have a beard.", "Früher hatte er einen Bart."),
                ("She was very happy.", "Sie war sehr glücklich."),
                ("I have forgotten the name.", "Ich habe den Namen vergessen."),
                ("He is young and nice.", "Er ist jung und sympathisch."),
            ],
        ),
        _l(
            20,
            [
                ("[Räum|Räume] bitte dein Zimmer auf!", "aufräumen"),
                ("Kinder, [bringt] bitte den Müll raus!", "rausbringen"),
                ("Kannst du [mich] abholen?", "ich"),
                ("Wo ist Paul? Ich sehe [ihn] nicht.", "er"),
                ("Sei so lieb und [spül|spüle] das Geschirr!", "spülen"),
            ],
            [
                (
                    "Do the washing-up, please!",
                    "Spül bitte das Geschirr!",
                    "Spüle bitte das Geschirr!",
                ),
                ("Come down immediately!", "Komm sofort runter!", "Komme sofort runter!"),
                ("I love you.", "Ich liebe dich."),
                ("Kids, tidy up your room!", "Kinder, räumt euer Zimmer auf!"),
            ],
        ),
        _l(
            21,
            [
                ("Bei Rot [muss] man stehen.", "müssen"),
                ("Hier [darf] man nicht parken.", "dürfen"),
                ("Du [musst] einen Helm tragen.", "müssen"),
                ("Der Hund muss an der [Leine] gehen.", "lead"),
                ("Hier ist Rauchen [verboten].", "forbidden"),
            ],
            [
                (
                    "You can't park here.",
                    "Hier darf man nicht parken.",
                    "Man darf hier nicht parken.",
                ),
                ("I have to work today.", "Ich muss heute arbeiten.", "Heute muss ich arbeiten."),
                ("You don't have to come.", "Du musst nicht kommen."),
                ("Cyclists have to wear a helmet.", "Fahrradfahrer müssen einen Helm tragen."),
            ],
        ),
        _l(
            22,
            [
                ("Der Mantel ist [teurer] als die Jacke.", "teuer"),
                ("Mein Bruder ist genauso groß [wie] ich.", "as"),
                ("Die Hose ist länger [als] der Rock.", "than"),
                ("Am [besten] gefällt mir das Kleid.", "gut"),
                ("Das Hemd ist [schöner] als die Bluse.", "schön"),
            ],
            [
                ("The skirt is cheaper than the dress.", "Der Rock ist billiger als das Kleid."),
                ("I like the shoes best.", "Die Schuhe gefallen mir am besten."),
                ("My sister is as tall as me.", "Meine Schwester ist genauso groß wie ich."),
                ("He is older than me.", "Er ist älter als ich."),
            ],
        ),
        _l(
            23,
            [
                ("Heute [scheint] die Sonne.", "scheinen"),
                ("Morgen [regnet] es.", "regnen"),
                ("Ich bleibe zu Hause, [denn] es schneit.", "because"),
                ("Der Himmel ist [wolkenlos].", "no clouds"),
                ("Im Süden ist es [heiß].", "hot"),
            ],
            [
                ("The sun is shining.", "Die Sonne scheint."),
                ("It's windy today.", "Heute ist es windig.", "Es ist heute windig."),
                (
                    "We're staying at home because it's raining.",
                    "Wir bleiben zu Hause, denn es regnet.",
                ),
                ("It's cold in the north.", "Im Norden ist es kalt.", "Es ist kalt im Norden."),
            ],
        ),
        _l(
            24,
            [
                ("Ich [würde] gern nach Paris fahren.", "werden"),
                ("Ich trinke gern Tee, aber [lieber] Kaffee.", "gern"),
                ("Am [liebsten] esse ich Pizza.", "gern"),
                ("Heute ist der [erste] Mai.", "1."),
                ("Wir [würden] uns sehr freuen!", "werden"),
            ],
            [
                (
                    "I would like to celebrate every day.",
                    "Ich würde gern jeden Tag feiern.",
                    "Ich würde jeden Tag gern feiern.",
                ),
                ("Today is the third of June.", "Heute ist der dritte Juni."),
                ("I prefer to drink tea.", "Ich trinke lieber Tee."),
                ("Happy New Year!", "Frohes neues Jahr!"),
            ],
        ),
    ]
)


MODUL_CHECKS = {
    1: modul_check(
        LEVEL,
        3,
        dialogue=(
            [
                "A: Hallo, ich bin Tom. Wie heißt du?",
                "B: ___",
                "A: Woher kommst du, Lara?",
                "B: Ich komme aus Italien.",
            ],
            "Ich heiße Lara.",
            "Ich komme aus Lara.",
            "Sehr gut, danke.",
        ),
        qa=[
            ("Wie heißt du?", "Ich heiße Ben."),
            ("Woher kommst du?", "Aus Brasilien."),
            ("Wie geht's?", "Sehr gut, danke."),
            ("Was machst du beruflich?", "Ich bin Ärztin."),
            ("Wie alt bist du?", "Ich bin 30."),
        ],
        odd=[
            ("der Lehrer", "die Mutter", "der Vater", "die Schwester"),
            ("Spanien", "Deutsch", "Englisch", "Französisch"),
            ("wohnen", "zwölf", "drei", "zwanzig"),
            ("Tschüs", "Hallo", "Guten Tag", "Guten Morgen"),
        ],
        reading=(
            """
Das ist Mira. Sie kommt aus Georgien und wohnt in Wien. Mira ist Ärztin. Sie
ist verheiratet und hat zwei Kinder. Mira spricht Georgisch, Russisch und ein
bisschen Deutsch.
""",
            [
                ("Mira kommt aus Österreich.", False),
                ("Mira wohnt in Wien.", True),
                ("Mira hat zwei Kinder.", True),
                ("Mira ist Lehrerin.", False),
            ],
        ),
        form=[
            ("ich ___ (heißen)", "heiße", "heißt", "heißen"),
            ("du ___ (kommen)", "kommst", "komme", "kommt"),
            ("er ___ (sprechen)", "spricht", "sprecht", "sprichst"),
            ("wir ___ (sein)", "sind", "seid", "ist"),
            ("Das ist ___ Mutter. (mein)", "meine", "mein", "meinen"),
        ],
    ),
    2: modul_check(
        LEVEL,
        6,
        dialogue=(
            [
                "A: Kann ich Ihnen helfen?",
                "B: Ja, bitte. Wie viel kostet die Lampe?",
                "A: ___",
                "B: Das ist zu teuer.",
            ],
            "Sie kostet 120 Euro.",
            "Er kostet 120 Euro.",
            "Das finde ich auch.",
        ),
        qa=[
            ("Was ist das?", "Das ist ein Kalender."),
            ("Wie viel kostet der Tisch?", "99 Euro."),
            ("Wie findest du das Sofa?", "Sehr schön!"),
            ("Brauchst du einen Drucker?", "Nein, ich brauche keinen."),
            ("Welche Farbe hat die Tasche?", "Sie ist schwarz."),
        ],
        odd=[
            ("die Maus", "rot", "blau", "grün"),
            ("das Bett", "der Stift", "der Kugelschreiber", "der Bleistift"),
            ("billig", "der Tisch", "der Stuhl", "der Schrank"),
            ("der Euro", "die Tastatur", "die Maus", "der Bildschirm"),
        ],
        reading=(
            """
Herr Kaya hat ein Büro in Hamburg. Das Büro ist klein, aber modern. Er hat
einen Computer, einen Drucker und ein Telefon. Er braucht keinen Laptop. Heute
sucht Herr Kaya einen Schreibtisch. Der Schreibtisch im Angebot kostet 150
Euro. Das findet er günstig.
""",
            [
                ("Das Büro ist groß.", False),
                ("Herr Kaya hat einen Drucker.", True),
                ("Er braucht einen Laptop.", False),
                ("Der Schreibtisch kostet 150 Euro.", True),
            ],
        ),
        form=[
            ("ein Buch – zwei ___", "Bücher", "Buchs", "Buche"),
            ("ein Stift – zwei ___", "Stifte", "Stiften", "Stifts"),
            ("Ich brauche ___ Computer. (ein)", "einen", "ein", "eine"),
            ("Das ist ___ Uhr. (kein)", "keine", "kein", "keinen"),
            ("Der Tisch? ___ ist schön.", "Er", "Sie", "Es"),
        ],
    ),
    3: modul_check(
        LEVEL,
        9,
        dialogue=(
            [
                "A: Hast du am Freitag Zeit?",
                "B: ___",
                "A: Schade! Und am Samstag?",
                "B: Ja, gern. Um acht Uhr?",
            ],
            "Das geht leider nicht.",
            "Ja, gern.",
            "Ich habe Hunger.",
        ),
        qa=[
            ("Wie spät ist es?", "Es ist halb drei."),
            ("Was möchtest du trinken?", "Einen Saft, bitte."),
            ("Kannst du kochen?", "Ja, sehr gut."),
            ("Wann hast du Zeit?", "Am Sonntag."),
            ("Wie oft gehst du schwimmen?", "Manchmal."),
        ],
        odd=[
            ("der Montag", "der Morgen", "der Mittag", "der Abend"),
            ("der Käse", "der Apfel", "die Orange", "die Zitrone"),
            ("die Butter", "das Kino", "das Theater", "das Museum"),
            ("nie", "schwimmen", "tanzen", "singen"),
        ],
        reading=(
            """
Lena und Tim haben am Samstag Zeit. Um zehn Uhr frühstücken sie im Café: Tim
möchte Brötchen mit Käse, Lena isst Obst. Am Nachmittag fahren sie Rad. Am
Abend gehen sie ins Kino. Tim mag den Film sehr, aber Lena findet ihn nicht so
gut.
""",
            [
                ("Lena und Tim frühstücken um zehn Uhr.", True),
                ("Tim möchte Obst.", False),
                ("Am Nachmittag fahren sie Rad.", True),
                ("Lena findet den Film sehr gut.", False),
            ],
        ),
        form=[
            ("du ___ (können)", "kannst", "könnst", "kann"),
            ("er ___ (lesen)", "liest", "lest", "lesst"),
            ("ich ___ (möchten)", "möchte", "möchtet", "möchtest"),
            ("sie (she) ___ (fahren)", "fährt", "fahrt", "fährst"),
            ("der Apfel + der Saft = der ___", "Apfelsaft", "Saftapfel", "Apfelsafte"),
        ],
        mistake=[
            ("Ich *kannst* gut schwimmen.", "Ich kann gut schwimmen."),
            ("Er *lest* gern Bücher.", "Er liest gern Bücher."),
            ("Möchtest du *ein* Kaffee?", "Möchtest du einen Kaffee?"),
            ("Das Konzert ist *am* acht Uhr.", "Das Konzert ist um acht Uhr."),
        ],
    ),
    4: modul_check(
        LEVEL,
        12,
        dialogue=(
            [
                "A: Entschuldigung, wann fährt der Zug nach Berlin ab?",
                "B: ___",
                "A: Und welches Gleis?",
                "B: Gleis 4.",
            ],
            "Um 10:15 Uhr.",
            "Mit dem Bus.",
            "Ich bin gestern gefahren.",
        ),
        qa=[
            ("Was hast du gestern gemacht?", "Ich habe gelernt."),
            ("Wann stehst du auf?", "Um sechs Uhr."),
            ("Wie kommst du zur Arbeit?", "Mit dem Fahrrad."),
            ("Wann hast du Geburtstag?", "Im April."),
            ("Was ist passiert?", "Der Zug ist zu spät gekommen."),
        ],
        odd=[
            ("der Koffer", "der Bus", "der Zug", "das Taxi"),
            ("gestern", "der Januar", "der März", "der Mai"),
            ("der Wein", "der Sommer", "der Winter", "der Herbst"),
            ("schlafen", "einkaufen", "aufstehen", "fernsehen"),
        ],
        reading=(
            """
Letzten Sonntag hat Jonas Geburtstag gefeiert. Am Morgen ist er lange im Bett
geblieben. Dann hat er mit Oma telefoniert. Am Abend sind viele Freunde
gekommen. Sie haben gekocht, gelacht und lange geredet. Jonas hat viele
Geschenke bekommen.
""",
            [
                ("Jonas hat am Sonntag Geburtstag gefeiert.", True),
                ("Am Morgen hat Jonas gearbeitet.", False),
                ("Jonas hat mit Oma telefoniert.", True),
                ("Am Abend sind keine Freunde gekommen.", False),
            ],
        ),
        form=[
            ("spielen → ich habe ___", "gespielt", "gespielen", "spielt"),
            ("schlafen → ich habe ___", "geschlafen", "geschlaft", "schlafte"),
            ("fahren → ich bin ___", "gefahren", "gefahrt", "fahrte"),
            ("aufräumen → ich habe ___", "aufgeräumt", "geaufräumt", "aufgeräumen"),
            ("telefonieren → ich habe ___", "telefoniert", "getelefoniert", "telefonieren"),
        ],
        mistake=[
            ("Ich *habe* nach Berlin gefahren.", "Ich bin nach Berlin gefahren."),
            ("Wir haben gestern Fußball *gespielen*.", "Wir haben gestern Fußball gespielt."),
            ("Ich stehe um sechs Uhr *an*.", "Ich stehe um sechs Uhr auf."),
            ("Mein Geburtstag ist *am* Juli.", "Mein Geburtstag ist im Juli."),
        ],
    ),
    5: modul_check(
        LEVEL,
        15,
        dialogue=(
            [
                "A: Entschuldigung, wo ist die Post?",
                "B: ___",
                "A: Vielen Dank!",
                "B: Bitte schön.",
            ],
            "Gehen Sie geradeaus und dann links.",
            "Die Post ist sehr nett.",
            "Danke, gleichfalls!",
        ),
        qa=[
            ("Wo ist die Bank?", "Neben der Post."),
            ("Wem gehört das Auto?", "Meinem Bruder."),
            ("Wie gefällt dir die Wohnung?", "Sehr gut, sie ist gemütlich."),
            ("Wie hoch ist die Miete?", "900 Euro mit Nebenkosten."),
            ("Wie komme ich zum Bahnhof?", "Immer geradeaus."),
        ],
        odd=[
            ("die Ampel", "die Küche", "das Bad", "das Schlafzimmer"),
            ("geradeaus", "mir", "dir", "uns"),
            ("der Keller", "die Kirche", "das Rathaus", "der Dom"),
            ("helfen", "links", "rechts", "geradeaus"),
        ],
        reading=(
            """
Familie Schulz sucht eine neue Wohnung. Ihre Wohnung in der Altstadt ist zu
klein. Heute haben sie eine Anzeige gelesen: drei Zimmer, Küche, Bad und ein
Balkon, 950 Euro mit Nebenkosten. Die Wohnung ist neben einem Park, und der
Spielplatz ist um die Ecke. Das gefällt den Kindern sehr.
""",
            [
                ("Die alte Wohnung ist zu groß.", False),
                ("Die neue Wohnung hat einen Balkon.", True),
                ("Die Miete ist 950 Euro mit Nebenkosten.", True),
                ("Der Spielplatz ist hinter der Kirche.", False),
            ],
        ),
        form=[
            ("Das Buch gehört ___. (ich)", "mir"),
            ("Wie geht es ___? (du)", "dir"),
            ("Das ist Lisa und ___ Mann. (her)", "ihr"),
            ("Der Park ist neben ___ Schule. (die)", "der"),
            ("Ich wohne in ___ Haus. (das)", "dem"),
        ],
        mistake=[
            ("Die Bank ist neben *die* Post.", "Die Bank ist neben der Post."),
            ("Das Haus gehört *ich*.", "Das Haus gehört mir."),
            ("Paul liebt *ihren* Garten.", "Paul liebt seinen Garten."),
            ("Wie geht es *du*?", "Wie geht es dir?"),
        ],
        dictation=[
            "Die Post ist neben der Bank.",
            "Gehen Sie hier links.",
            "Die Wohnung hat einen Balkon.",
            "Das Buch gehört mir.",
        ],
    ),
    6: modul_check(
        LEVEL,
        18,
        dialogue=(
            [
                "A: Praxis Dr. Berger, guten Tag.",
                "B: Guten Tag, hier ist Tom Kaya. Ich habe Fieber und Halsschmerzen.",
                "A: ___",
                "B: Ja, das passt. Vielen Dank!",
            ],
            "Können Sie heute um 15 Uhr kommen?",
            "Mein Kopf tut auch weh.",
            "Der Föhn funktioniert nicht.",
        ),
        qa=[
            ("Was fehlt Ihnen?", "Ich habe Kopfschmerzen."),
            ("Was soll ich tun?", "Trinken Sie viel Tee."),
            ("Was willst du werden?", "Ich will Ärztin werden."),
            ("Für wen ist das Geschenk?", "Für meine Oma."),
            ("Wann ist der Kurs?", "In einer Woche."),
        ],
        odd=[
            ("die Heizung", "der Kopf", "der Bauch", "der Rücken"),
            ("die Tablette", "die Gitarre", "das Lied", "das Instrument"),
            ("die Salbe", "der Wecker", "der Föhn", "die Dusche"),
            ("pünktlich", "das Knie", "das Bein", "der Fuß"),
        ],
        reading=(
            """
Liebe Frau Roth, leider kann ich morgen nicht zum Kurs kommen. Ich bin krank:
Ich habe Fieber und mein Hals tut weh. Der Arzt sagt, ich soll drei Tage zu
Hause bleiben. Können wir die Prüfung bitte verschieben? Vielen Dank für Ihre
Hilfe! Mit freundlichen Grüßen, Ali Demir
""",
            [
                ("Ali kann morgen zum Kurs kommen.", False),
                ("Ali hat Fieber.", True),
                ("Ali soll eine Woche zu Hause bleiben.", False),
                ("Ali möchte die Prüfung verschieben.", True),
            ],
        ),
        form=[
            ("___ Sie bitte hier! (warten)", "Warten"),
            ("Ich ___ Sängerin werden. (wollen)", "will"),
            ("Er ___ Lehrer. (werden)", "wird"),
            ("Du ___ viel schlafen. (sollen)", "sollst"),
            ("Ich fahre mit ___ Bus. (der)", "dem"),
        ],
        mistake=[
            ("Ich fahre mit *der* Zug.", "Ich fahre mit dem Zug."),
            ("Er *willt* Popstar werden.", "Er will Popstar werden."),
            ("Mein Bauch *tun* weh.", "Mein Bauch tut weh."),
            ("Das Geschenk ist für *mir*.", "Das Geschenk ist für mich."),
        ],
        dictation=[
            "Die Heizung funktioniert nicht.",
            "Ich will Popstar werden.",
            "Mein Kopf tut weh.",
            "Trinken Sie viel Tee.",
        ],
    ),
    7: modul_check(
        LEVEL,
        21,
        dialogue=(
            [
                "A: Mama, darf ich heute ins Kino gehen?",
                "B: ___",
                "A: Okay, ich räume sofort auf!",
                "B: Gut, dann darfst du gehen.",
            ],
            "Ja, aber dein Zimmer ist nicht ordentlich!",
            "Nein, ich war gestern im Kino.",
            "Der Film war sehr komisch.",
        ),
        qa=[
            ("Wie war der Urlaub?", "Super, das Wetter war schön."),
            ("Darf ich hier rauchen?", "Nein, das ist verboten."),
            ("Was musst du heute machen?", "Ich muss die Wäsche waschen."),
            ("Wo warst du gestern?", "Ich war bei meiner Oma."),
            ("Kannst du mir helfen?", "Klar, was soll ich tun?"),
        ],
        odd=[
            ("schlank", "bügeln", "spülen", "wischen"),
            ("der Bart", "der Autofahrer", "der Fußgänger", "der Fahrradfahrer"),
            ("dich", "müssen", "dürfen", "können"),
            ("traurig", "die Wäsche", "das Geschirr", "der Boden"),
        ],
        reading=(
            """
Regeln in unserer Wohngemeinschaft: Wir putzen jede Woche die Küche. Nach 22
Uhr darf man keine laute Musik hören. In der Wohnung ist Rauchen verboten, auf
dem Balkon ist es erlaubt. Am Montag bringt man den Müll raus. Gäste dürfen
gern kommen!
""",
            [
                ("Man darf in der Wohnung rauchen.", False),
                ("Auf dem Balkon darf man rauchen.", True),
                ("Nach 22 Uhr darf man laut Musik hören.", False),
                ("Am Montag bringt man den Müll raus.", True),
            ],
        ),
        form=[
            ("___ bitte das Fenster zu! (machen, du)", "Mach|Mache"),
            ("Gestern ___ ich keine Zeit. (haben)", "hatte"),
            ("Wir ___ letztes Jahr in Spanien. (sein)", "waren"),
            ("Hier ___ man nicht parken. (dürfen)", "darf"),
            ("freundlich ↔ ___", "unfreundlich"),
        ],
        mistake=[
            ("Gestern *habe* ich krank.", "Gestern war ich krank."),
            ("Du *muss* einen Helm tragen.", "Du musst einen Helm tragen."),
            ("Kinder, *räum* euer Zimmer auf!", "Kinder, räumt euer Zimmer auf!"),
            ("Ich liebe *du*.", "Ich liebe dich."),
        ],
        dictation=[
            "Früher hatte er einen Bart.",
            "Komm sofort runter!",
            "Hier darf man nicht parken.",
            "Du musst einen Helm tragen.",
        ],
    ),
    8: modul_check(
        LEVEL,
        24,
        dialogue=(
            [
                "A: Was machen wir am Wochenende?",
                "B: Am liebsten würde ich an den Strand fahren.",
                "A: ___",
                "B: Schade! Dann gehen wir ins Museum.",
            ],
            "Das geht leider nicht, am Samstag regnet es.",
            "Herzlichen Glückwunsch!",
            "Der Rock ist billiger als das Kleid.",
        ),
        qa=[
            ("Wie ist das Wetter?", "Es ist sonnig und warm."),
            ("Was trinkst du lieber, Tee oder Kaffee?", "Lieber Kaffee."),
            ("Welcher Tag ist heute?", "Der siebte März."),
            ("Was würdest du gern machen?", "Ich würde gern reisen."),
            ("Was ziehst du an?", "Meine neue Jacke."),
        ],
        odd=[
            ("der Schnee", "die Hose", "der Rock", "das Kleid"),
            ("der Süden", "der Regen", "der Wind", "der Nebel"),
            ("Weihnachten", "der Hut", "die Mütze", "der Gürtel"),
            ("klug", "sonnig", "windig", "bewölkt"),
        ],
        reading=(
            """
Liebe Sara, am 15. Juli feiere ich meinen 30. Geburtstag! Ich mache eine Party
im Garten. Am liebsten würde ich draußen feiern, aber im Juli regnet es
manchmal. Dann feiern wir im Wohnzimmer. Kommst du auch? Bitte antworte bis zum
ersten Juli. Ich würde mich sehr freuen! Deine Mia
""",
            [
                ("Mia feiert im Juli Geburtstag.", True),
                ("Mia wird 40 Jahre alt.", False),
                ("Bei Regen feiern sie im Wohnzimmer.", True),
                ("Sara soll bis zum ersten Juni antworten.", False),
            ],
        ),
        form=[
            ("groß – größer – am ___", "größten"),
            ("gut – ___ – am besten", "besser"),
            ("Wir ___ gern ein Haus kaufen. (werden → würde)", "würden"),
            ("der 3. Mai = der ___ Mai", "dritte"),
            ("der Wind → Es ist ___.", "windig"),
        ],
        mistake=[
            ("Der Mantel ist teurer *wie* die Jacke.", "Der Mantel ist teurer als die Jacke."),
            ("Am *besser* gefällt mir das Kleid.", "Am besten gefällt mir das Kleid."),
            ("Ich *würdest* gern reisen.", "Ich würde gern reisen."),
            ("Heute *regnen* es.", "Heute regnet es."),
        ],
        dictation=[
            "Heute scheint die Sonne.",
            "Ich trinke lieber Kaffee.",
            "Der Mantel ist teurer als die Jacke.",
            "Wir würden uns sehr freuen.",
        ],
    ),
}
