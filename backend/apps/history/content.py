"""The German-history lessons, loaded by `manage.py seed_history`.

Each level has its own lessons, written for that level:

  * A1: very short sentences, mostly present tense (about 150-200 words)
  * A2: the Perfekt and war/hatte, longer texts (about 250 words)
  * B1: subordinate clauses, the Präteritum and more detail (about 300-400 words)

A user sees the lessons at their level and below. Every lesson has an English
translation the reader can show, five quiz questions (the right answer listed
first; the API shuffles them), and a public-domain picture from Wikimedia
Commons bundled with the frontend (`frontend/public/history/`). Lessons are
matched on `order`.
"""

COMMONS = "Wikimedia Commons, public domain"

LESSONS = [
    {
        "order": 1,
        "level": "A1",
        "era": "Antike",
        "title": "Die Römer in Deutschland",
        "image": "roemer",
        "image_credit": f"Otto Albert Koch, Varusschlacht (1909). {COMMONS}",
        "excerpt": "Vor 2000 Jahren sind die Römer am Rhein. Sie bauen Straßen und Städte.",
        "body_de": """Vor 2000 Jahren sind die Römer in Deutschland. Sie kommen aus Italien. Viele Römer sind Soldaten. Sie bauen Häuser, Straßen und Städte am Rhein. Köln, Mainz, Trier und Bonn sind alte römische Städte.

In Trier gibt es heute noch ein großes Tor. Es heißt Porta Nigra. Es ist fast 2000 Jahre alt.

Östlich vom Rhein wohnen die Germanen. Sie wohnen in Dörfern. Die Häuser sind aus Holz. Die Germanen sind Bauern. Sie haben Kühe und Schweine.

Im Jahr 9 gibt es einen großen Kampf in einem Wald. Der Chef der Germanen heißt Arminius. Die Germanen gewinnen, die Römer verlieren. Das Bild oben zeigt den Kampf. Ein Maler hat es im Jahr 1909 gemalt.

Die Römer bleiben am Rhein. Sie bauen eine lange Grenze mit Türmen: den Limes. Er ist 550 Kilometer lang.

Viele deutsche Wörter kommen von den Römern, zum Beispiel Mauer, Fenster, Straße und Wein.""",
        "body_en": """2,000 years ago the Romans were in Germany. They came from Italy. Many Romans were soldiers. They built houses, roads and towns on the Rhine. Cologne, Mainz, Trier and Bonn are old Roman towns.

In Trier there is still a large gate today. It is called the Porta Nigra. It is almost 2,000 years old.

East of the Rhine lived the Germanic tribes. They lived in villages. The houses were made of wood. The Germanic people were farmers. They had cows and pigs.

In the year 9 there was a big battle in a forest. The leader of the Germanic tribes was called Arminius. The Germanic tribes won and the Romans lost. The picture above shows the battle. A painter painted it in 1909.

The Romans stayed on the Rhine. They built a long border with towers: the Limes. It is 550 kilometres long.

Many German words come from the Romans, for example Mauer (wall), Fenster (window), Straße (street) and Wein (wine).""",
        "quiz": [
            {
                "prompt": "Woher kommen die Römer?",
                "options": ["aus Italien", "aus Spanien", "aus England", "aus Polen"],
                "answer": "aus Italien",
            },
            {
                "prompt": "Wie heißt das große Tor in Trier?",
                "options": ["Porta Nigra", "Brandenburger Tor", "Holstentor", "Siegestor"],
                "answer": "Porta Nigra",
            },
            {
                "prompt": "Wo wohnen die Germanen?",
                "options": ["in Dörfern", "in großen Städten", "in Rom", "in Hotels"],
                "answer": "in Dörfern",
            },
            {
                "prompt": "Wer gewinnt im Jahr 9 den Kampf?",
                "options": ["die Germanen", "die Römer", "die Franzosen", "niemand"],
                "answer": "die Germanen",
            },
            {
                "prompt": "Welches Wort kommt von den Römern?",
                "options": ["Fenster", "Haus", "Hund", "Brot"],
                "answer": "Fenster",
            },
        ],
    },
    {
        "order": 2,
        "level": "A1",
        "era": "Mittelalter",
        "title": "Karl der Große",
        "image": "karl",
        "image_credit": f"Albrecht Dürer, Kaiser Karl der Große (um 1512). {COMMONS}",
        "excerpt": "Karl der Große ist König der Franken. Im Jahr 800 wird er Kaiser.",
        "body_de": """Karl der Große lebt vor etwa 1200 Jahren. Er ist König der Franken. Sein Reich ist sehr groß. Heute sind dort Frankreich, Deutschland, Belgien, die Niederlande und ein Teil von Italien.

Im Jahr 800 ist Karl in Rom. Dort macht ihn der Papst zum Kaiser. Das ist am 25. Dezember, an Weihnachten.

Karl wohnt oft in Aachen. Aachen ist eine Stadt im Westen von Deutschland. Dort baut er eine große Kirche. Heute ist sie ein Teil vom Aachener Dom. Viele Touristen besuchen sie.

Karl findet Schule und Bücher sehr wichtig. Er kann lesen, aber er kann nicht gut schreiben. Mönche schreiben für ihn viele Bücher ab.

Karl stirbt im Jahr 814. Sein Grab ist in Aachen. Später teilen seine Enkel das Reich. Aus einem Teil wird langsam Frankreich, aus einem anderen Teil wird langsam Deutschland.

Das Bild oben ist von Albrecht Dürer. Er malt Karl 700 Jahre später. Wie Karl wirklich aussieht, weiß niemand.""",
        "body_en": """Charlemagne lived about 1,200 years ago. He was King of the Franks. His empire was very large. Today France, Germany, Belgium, the Netherlands and part of Italy lie there.

In the year 800 Charles was in Rome. There the Pope made him emperor. That was on 25 December, at Christmas.

Charles often lived in Aachen. Aachen is a town in the west of Germany. There he built a large church. Today it is part of Aachen Cathedral. Many tourists visit it.

Charles thought school and books were very important. He could read, but he could not write well. Monks copied many books for him.

Charles died in 814. His grave is in Aachen. Later his grandsons divided the empire. One part slowly became France, another part slowly became Germany.

The picture above is by Albrecht Dürer. He painted Charles 700 years later. Nobody knows what Charles really looked like.""",
        "quiz": [
            {
                "prompt": "Wann wird Karl Kaiser?",
                "options": ["im Jahr 800", "im Jahr 1800", "im Jahr 9", "im Jahr 1517"],
                "answer": "im Jahr 800",
            },
            {
                "prompt": "Wer macht Karl zum Kaiser?",
                "options": ["der Papst", "ein Mönch", "sein Enkel", "Albrecht Dürer"],
                "answer": "der Papst",
            },
            {
                "prompt": "In welcher Stadt wohnt Karl oft?",
                "options": ["in Aachen", "in Berlin", "in Hamburg", "in Wien"],
                "answer": "in Aachen",
            },
            {
                "prompt": "Was findet Karl sehr wichtig?",
                "options": ["Schule und Bücher", "Fußball", "Autos", "Kino"],
                "answer": "Schule und Bücher",
            },
            {
                "prompt": "Wer teilt später das Reich?",
                "options": ["seine Enkel", "die Römer", "der Papst", "die Touristen"],
                "answer": "seine Enkel",
            },
        ],
    },
    {
        "order": 3,
        "level": "A1",
        "era": "Frühe Neuzeit",
        "title": "Martin Luther",
        "image": "reformation",
        "image_credit": f"Lucas Cranach der Ältere, Martin Luther (1528). {COMMONS}",
        "excerpt": "Martin Luther schreibt 1517 die 95 Thesen und übersetzt die Bibel ins Deutsche.",
        "body_de": """Martin Luther wird 1483 in Eisleben geboren. Eisleben ist eine kleine Stadt in Sachsen-Anhalt. Luther studiert und wird Mönch. Später ist er Professor in Wittenberg.

Luther liest viel in der Bibel. Er hat eine Frage: Kann man mit Geld in den Himmel kommen? Die Kirche sagt damals: Ja, man kann Ablassbriefe kaufen. Luther sagt: Nein, das ist falsch!

Im Jahr 1517 schreibt er 95 Sätze, die 95 Thesen. Viele Menschen lesen sie, denn man kann Texte jetzt drucken.

Der Papst und der Kaiser sind böse auf Luther. Luther muss sich verstecken. Er wohnt auf der Wartburg, einer Burg bei Eisenach. Dort übersetzt er die Bibel ins Deutsche. Jetzt können viele Menschen die Bibel auf Deutsch lesen.

Danach gibt es in Deutschland zwei große Kirchen: die katholische und die evangelische. Das ist bis heute so.

Der 31. Oktober ist der Reformationstag. In manchen Bundesländern ist er ein Feiertag. Das Bild oben ist von Lucas Cranach. Er ist ein Freund von Luther.""",
        "body_en": """Martin Luther was born in Eisleben in 1483. Eisleben is a small town in Saxony-Anhalt. Luther studied and became a monk. Later he was a professor in Wittenberg.

Luther read the Bible a lot. He had a question: can you get into heaven with money? The Church said at that time: yes, you can buy letters of indulgence. Luther said: no, that is wrong!

In 1517 he wrote 95 sentences, the 95 theses. Many people read them, because texts could now be printed.

The Pope and the emperor were angry with Luther. Luther had to hide. He lived at the Wartburg, a castle near Eisenach. There he translated the Bible into German. Now many people could read the Bible in German.

After that there were two big churches in Germany: the Catholic and the Protestant church. It is still like that today.

31 October is Reformation Day. In some federal states it is a public holiday. The picture above is by Lucas Cranach. He was a friend of Luther's.""",
        "quiz": [
            {
                "prompt": "Wo wird Luther geboren?",
                "options": ["in Eisleben", "in Rom", "in Berlin", "in Aachen"],
                "answer": "in Eisleben",
            },
            {
                "prompt": "Was sagt Luther zu den Ablassbriefen?",
                "options": ["Das ist falsch.", "Das ist gut.", "Das ist billig.", "Das ist neu."],
                "answer": "Das ist falsch.",
            },
            {
                "prompt": "Wie viele Thesen schreibt Luther?",
                "options": ["95", "9", "31", "1517"],
                "answer": "95",
            },
            {
                "prompt": "Wo übersetzt Luther die Bibel?",
                "options": ["auf der Wartburg", "in Rom", "in Köln", "in Paris"],
                "answer": "auf der Wartburg",
            },
            {
                "prompt": "Wann ist der Reformationstag?",
                "options": ["am 31. Oktober", "am 3. Oktober", "am 25. Dezember", "am 1. Mai"],
                "answer": "am 31. Oktober",
            },
        ],
    },
    {
        "order": 4,
        "level": "A1",
        "era": "Gegenwart",
        "title": "Deutschland heute",
        "image": "heute",
        "image_credit": f"Die Fahne auf dem Reichstagsgebäude in Berlin. {COMMONS}",
        "excerpt": "Deutschland hat 16 Bundesländer und etwa 84 Millionen Menschen. Die Hauptstadt ist Berlin.",
        "body_de": """Deutschland liegt in der Mitte von Europa. Es hat neun Nachbarländer, zum Beispiel Frankreich, Polen, Österreich und die Schweiz.

In Deutschland leben etwa 84 Millionen Menschen. Die Hauptstadt ist Berlin. Berlin ist auch die größte Stadt. Andere große Städte sind Hamburg, München und Köln.

Deutschland hat 16 Bundesländer. Drei Bundesländer sind Städte: Berlin, Hamburg und Bremen. Das größte Bundesland ist Bayern.

Die Fahne ist schwarz, rot und gold. Das Bild oben zeigt die Fahne auf dem Reichstag in Berlin. Dort arbeitet das Parlament, der Bundestag.

Man bezahlt in Deutschland mit dem Euro. Die Sprache ist Deutsch. Man spricht Deutsch auch in Österreich, in der Schweiz und in Liechtenstein.

Viele Menschen in Deutschland kommen aus anderen Ländern, oder ihre Eltern kommen aus anderen Ländern. Deutschland ist ein Land mit vielen Kulturen.

Der Nationalfeiertag ist der 3. Oktober, der Tag der Deutschen Einheit.""",
        "body_en": """Germany lies in the middle of Europe. It has nine neighbouring countries, for example France, Poland, Austria and Switzerland.

About 84 million people live in Germany. The capital is Berlin. Berlin is also the biggest city. Other big cities are Hamburg, Munich and Cologne.

Germany has 16 federal states. Three federal states are cities: Berlin, Hamburg and Bremen. The biggest federal state is Bavaria.

The flag is black, red and gold. The picture above shows the flag on the Reichstag in Berlin. The parliament, the Bundestag, works there.

In Germany people pay with the euro. The language is German. German is also spoken in Austria, Switzerland and Liechtenstein.

Many people in Germany come from other countries, or their parents come from other countries. Germany is a country of many cultures.

The national holiday is 3 October, the Day of German Unity.""",
        "quiz": [
            {
                "prompt": "Wie viele Bundesländer hat Deutschland?",
                "options": ["16", "9", "3", "84"],
                "answer": "16",
            },
            {
                "prompt": "Was ist die Hauptstadt?",
                "options": ["Berlin", "München", "Hamburg", "Bonn"],
                "answer": "Berlin",
            },
            {
                "prompt": "Welche Farben hat die Fahne?",
                "options": [
                    "Schwarz, Rot und Gold",
                    "Blau, Weiß und Rot",
                    "Rot und Weiß",
                    "Grün, Weiß und Rot",
                ],
                "answer": "Schwarz, Rot und Gold",
            },
            {
                "prompt": "Womit bezahlt man in Deutschland?",
                "options": ["mit dem Euro", "mit dem Franken", "mit dem Dollar", "mit der Krone"],
                "answer": "mit dem Euro",
            },
            {
                "prompt": "Was ist das größte Bundesland?",
                "options": ["Bayern", "Bremen", "Berlin", "Hamburg"],
                "answer": "Bayern",
            },
        ],
    },
    {
        "order": 5,
        "level": "A2",
        "era": "19. Jahrhundert",
        "title": "Die Revolution von 1848",
        "image": "1848",
        "image_credit": f"Die Nationalversammlung in der Paulskirche, Lithografie (1848). {COMMONS}",
        "excerpt": "1848 wollten viele Deutsche Freiheit und einen gemeinsamen Staat.",
        "body_de": """Nach Napoleon gab es kein deutsches Reich mehr, sondern den Deutschen Bund. Das waren fast 40 Staaten. In den meisten Staaten regierten Fürsten und Könige, und das Volk hatte wenig zu sagen. Zeitungen durften nicht frei schreiben, denn es gab Zensur.

Viele Menschen wollten das ändern. Sie wünschten sich drei Dinge: Freiheit, eine Verfassung und einen gemeinsamen deutschen Staat. Ihr Zeichen waren die Farben Schwarz, Rot und Gold.

Im Jahr 1848 gab es in vielen Ländern Europas Revolutionen, zuerst in Frankreich. Im März 1848 gingen auch in Deutschland viele Menschen auf die Straße. In Berlin kämpften am 18. März Bürger auf Barrikaden gegen Soldaten. Viele Menschen starben. Danach versprach der König von Preußen Reformen. Man nennt diese Zeit die Märzrevolution.

Im Mai 1848 traf sich in Frankfurt am Main zum ersten Mal ein Parlament für ganz Deutschland. Die Abgeordneten waren frei gewählt, aber es waren nur Männer. Sie tagten in einer Kirche, der Paulskirche. Das Bild oben zeigt sie bei der Arbeit. Sie schrieben eine Verfassung mit Grundrechten, zum Beispiel der Meinungsfreiheit und der Pressefreiheit.

1849 boten sie dem König von Preußen, Friedrich Wilhelm IV., die Kaiserkrone an. Aber der König wollte keine Krone vom Volk. Er sagte Nein. Danach schickten die Fürsten Soldaten, und 1849 war die Revolution zu Ende. Viele Revolutionäre mussten fliehen, manche bis nach Amerika.

Die Revolution hatte ihr Ziel nicht erreicht. Aber ihre Ideen lebten weiter. Schwarz, Rot und Gold sind heute die Farben der deutschen Fahne, und viele Grundrechte von 1848 stehen heute im Grundgesetz.""",
        "body_en": """After Napoleon there was no longer a German empire, but the German Confederation. It was made up of almost 40 states. In most of them princes and kings ruled, and the people had little say. Newspapers could not write freely, because there was censorship.

Many people wanted to change this. They wished for three things: freedom, a constitution and a common German state. Their symbol was the colours black, red and gold.

In 1848 there were revolutions in many European countries, first in France. In March 1848 many people took to the streets in Germany too. In Berlin, on 18 March, citizens fought soldiers on barricades. Many people died. Afterwards the King of Prussia promised reforms. This period is called the March Revolution.

In May 1848 a parliament for the whole of Germany met for the first time, in Frankfurt am Main. Its members were freely elected, but they were only men. They met in a church, St Paul's Church (the Paulskirche). The picture above shows them at work. They wrote a constitution with basic rights, for example freedom of opinion and freedom of the press.

In 1849 they offered the imperial crown to the King of Prussia, Frederick William IV. But the king did not want a crown from the people. He said no. Then the princes sent soldiers, and by 1849 the revolution was over. Many revolutionaries had to flee, some as far as America.

The revolution did not reach its goal. But its ideas lived on. Black, red and gold are the colours of the German flag today, and many of the basic rights of 1848 are in today's Basic Law, the German constitution.""",
        "quiz": [
            {
                "prompt": "Was wünschten sich viele Menschen vor 1848?",
                "options": [
                    "Freiheit, eine Verfassung und einen deutschen Staat",
                    "einen Kaiser aus Frankreich",
                    "mehr Zensur",
                    "einen Krieg gegen Preußen",
                ],
                "answer": "Freiheit, eine Verfassung und einen deutschen Staat",
            },
            {
                "prompt": "In welcher Stadt kämpften am 18. März 1848 Bürger auf Barrikaden?",
                "options": ["in Berlin", "in Hamburg", "in Köln", "in Trier"],
                "answer": "in Berlin",
            },
            {
                "prompt": "Wo traf sich das erste Parlament für ganz Deutschland?",
                "options": [
                    "in der Paulskirche in Frankfurt",
                    "im Reichstag in Berlin",
                    "im Dom in Aachen",
                    "auf der Wartburg",
                ],
                "answer": "in der Paulskirche in Frankfurt",
            },
            {
                "prompt": "Was tat Friedrich Wilhelm IV. mit der Kaiserkrone?",
                "options": [
                    "Er sagte Nein.",
                    "Er nahm sie an.",
                    "Er verkaufte sie.",
                    "Er gab sie Napoleon.",
                ],
                "answer": "Er sagte Nein.",
            },
            {
                "prompt": "Welche Farben waren das Zeichen der Revolution?",
                "options": [
                    "Schwarz, Rot und Gold",
                    "Schwarz, Weiß und Rot",
                    "Blau und Weiß",
                    "Rot und Weiß",
                ],
                "answer": "Schwarz, Rot und Gold",
            },
        ],
    },
    {
        "order": 6,
        "level": "A2",
        "era": "19. Jahrhundert",
        "title": "Die deutsche Einigung 1871",
        "image": "1871",
        "image_credit": f"Anton von Werner, Die Kaiserproklamation am 18. Januar 1871 (1885). {COMMONS}",
        "excerpt": "1871 entstand das Deutsche Kaiserreich, mit Bismarck als erstem Kanzler.",
        "body_de": """Auch nach 1848 gab es noch keinen deutschen Staat. Die zwei größten Länder im Deutschen Bund waren Preußen und Österreich. Beide wollten die Führung haben.

In Preußen war ab 1862 Otto von Bismarck Ministerpräsident. Er wollte Deutschland unter der Führung von Preußen einigen, aber ohne Österreich. Er sagte, große Fragen löst man nicht mit Reden, sondern „durch Eisen und Blut“. Er führte drei Kriege: 1864 gegen Dänemark, 1866 gegen Österreich und 1870/71 gegen Frankreich. Preußen und seine Partner gewannen alle drei.

Am 18. Januar 1871 wurde der König von Preußen, Wilhelm I., zum Deutschen Kaiser ausgerufen. Das passierte nicht in Deutschland, sondern im Spiegelsaal vom Schloss Versailles bei Paris. Das Bild oben zeigt diesen Moment. In der Mitte, in einer weißen Uniform, steht Bismarck. Er wurde der erste Reichskanzler. Die Hauptstadt war Berlin.

Das neue Deutsche Kaiserreich wuchs schnell. Es gab viele neue Fabriken, Eisenbahnen und große Städte. Viele Menschen zogen vom Land in die Städte und arbeiteten dort in Fabriken. Die Arbeit war hart, und die Löhne waren klein.

In den 1880er-Jahren führte Bismarck neue Gesetze ein: eine Krankenversicherung, eine Unfallversicherung und eine Rentenversicherung für Arbeiter. Diese Idee war damals neu in der Welt. Auch heute gibt es diese Versicherungen in Deutschland.

Aber das Kaiserreich war keine Demokratie wie heute. Der Kaiser und der Kanzler hatten viel Macht, und das Parlament, der Reichstag, hatte weniger. Frauen durften noch nicht wählen. Das Kaiserreich bestand bis 1918.""",
        "body_en": """Even after 1848 there was still no German state. The two biggest countries in the German Confederation were Prussia and Austria. Both wanted to lead.

From 1862 Otto von Bismarck was Prime Minister of Prussia. He wanted to unite Germany under Prussian leadership, but without Austria. He said that great questions are not decided by speeches but "by iron and blood". He fought three wars: in 1864 against Denmark, in 1866 against Austria and in 1870/71 against France. Prussia and its partners won all three.

On 18 January 1871 the King of Prussia, Wilhelm I, was proclaimed German Emperor. This did not happen in Germany but in the Hall of Mirrors of the Palace of Versailles near Paris. The picture above shows this moment. In the middle, in a white uniform, stands Bismarck. He became the first Chancellor of the Empire. The capital was Berlin.

The new German Empire grew quickly. There were many new factories, railways and big cities. Many people moved from the countryside to the cities and worked in factories there. The work was hard and the wages were low.

In the 1880s Bismarck introduced new laws: health insurance, accident insurance and pension insurance for workers. At the time this idea was new in the world. These insurances still exist in Germany today.

But the Empire was not a democracy like today's. The emperor and the chancellor had a lot of power, and the parliament, the Reichstag, had less. Women were not yet allowed to vote. The Empire lasted until 1918.""",
        "quiz": [
            {
                "prompt": "Wer war ab 1862 Ministerpräsident in Preußen?",
                "options": ["Otto von Bismarck", "Martin Luther", "Napoleon", "Karl der Große"],
                "answer": "Otto von Bismarck",
            },
            {
                "prompt": "Gegen welches Land kämpfte Preußen 1870/71?",
                "options": ["gegen Frankreich", "gegen Dänemark", "gegen Italien", "gegen Polen"],
                "answer": "gegen Frankreich",
            },
            {
                "prompt": "Wo wurde Wilhelm I. zum Kaiser ausgerufen?",
                "options": ["im Schloss Versailles", "in Berlin", "in Aachen", "in Wien"],
                "answer": "im Schloss Versailles",
            },
            {
                "prompt": "Welches Land gehörte nicht zum neuen Kaiserreich?",
                "options": ["Österreich", "Preußen", "Bayern", "Sachsen"],
                "answer": "Österreich",
            },
            {
                "prompt": "Was führte Bismarck in den 1880er-Jahren ein?",
                "options": [
                    "eine Krankenversicherung für Arbeiter",
                    "den Euro",
                    "das Wahlrecht für Frauen",
                    "die Republik",
                ],
                "answer": "eine Krankenversicherung für Arbeiter",
            },
        ],
    },
    {
        "order": 7,
        "level": "A2",
        "era": "19. Jahrhundert",
        "title": "Die Industrialisierung",
        "image": "industrie",
        "image_credit": f"Adolph Menzel, Das Eisenwalzwerk (1872-1875). {COMMONS}",
        "excerpt": "Im 19. Jahrhundert kamen Maschinen, Fabriken und die Eisenbahn nach Deutschland.",
        "body_de": """Vor 1800 haben die meisten Menschen in Deutschland auf dem Land gelebt. Sie waren Bauern und haben fast alles mit der Hand gemacht.

Im 19. Jahrhundert hat sich das stark geändert. In England hat man die Dampfmaschine verbessert, und bald hat man sie auch in Deutschland benutzt. Jetzt haben Maschinen in Fabriken viel Arbeit gemacht, zum Beispiel beim Weben und in Stahlwerken.

1835 ist die erste deutsche Eisenbahn gefahren, von Nürnberg nach Fürth. Die Strecke war nur sechs Kilometer lang. Später hat man überall in Deutschland Eisenbahnen gebaut.

Besonders im Ruhrgebiet sind viele Kohlebergwerke und Stahlwerke entstanden. Viele Menschen sind vom Land in die Städte gezogen, weil sie dort Arbeit gesucht haben. Städte wie Essen, Dortmund und Berlin sind sehr schnell gewachsen.

Das Leben der Arbeiter war schwer. Sie haben oft zwölf Stunden oder mehr am Tag gearbeitet, auch viele Kinder. Die Wohnungen waren klein und dunkel. Deshalb haben die Arbeiter Gewerkschaften und Parteien gegründet. Sie wollten mehr Lohn und kürzere Arbeitszeiten.

In dieser Zeit haben deutsche Erfinder wichtige Dinge entwickelt: Werner von Siemens hat 1866 den Dynamo erfunden, und Carl Benz hat 1886 das erste Auto gebaut.

Das Bild oben hat der Maler Adolph Menzel zwischen 1872 und 1875 gemalt. Es zeigt Arbeiter in einem Eisenwalzwerk.""",
        "body_en": """Before 1800 most people in Germany lived in the countryside. They were farmers and did almost everything by hand.

In the 19th century this changed a lot. In England the steam engine was improved, and soon it was used in Germany too. Now machines in factories did a lot of the work, for example in weaving and in steelworks.

In 1835 the first German railway ran, from Nuremberg to Fürth. The line was only six kilometres long. Later railways were built all over Germany.

Many coal mines and steelworks appeared, especially in the Ruhr area. Many people moved from the countryside to the cities because they were looking for work there. Cities such as Essen, Dortmund and Berlin grew very fast.

Workers' lives were hard. They often worked twelve hours or more a day, and many children did too. The flats were small and dark. That is why the workers founded trade unions and parties. They wanted higher wages and shorter working hours.

In this period German inventors developed important things: Werner von Siemens invented the dynamo in 1866, and Carl Benz built the first car in 1886.

The painter Adolph Menzel painted the picture above between 1872 and 1875. It shows workers in an iron-rolling mill.""",
        "quiz": [
            {
                "prompt": "Wo haben vor 1800 die meisten Menschen gelebt?",
                "options": ["auf dem Land", "in großen Städten", "in Fabriken", "in Amerika"],
                "answer": "auf dem Land",
            },
            {
                "prompt": "Wann ist die erste deutsche Eisenbahn gefahren?",
                "options": ["1835", "1871", "1900", "1789"],
                "answer": "1835",
            },
            {
                "prompt": "Welche Region hatte viele Kohlebergwerke?",
                "options": ["das Ruhrgebiet", "die Alpen", "die Nordsee", "der Schwarzwald"],
                "answer": "das Ruhrgebiet",
            },
            {
                "prompt": "Was wollten die Arbeiter?",
                "options": [
                    "mehr Lohn und kürzere Arbeitszeiten",
                    "mehr Arbeit",
                    "weniger Freizeit",
                    "keine Gewerkschaften",
                ],
                "answer": "mehr Lohn und kürzere Arbeitszeiten",
            },
            {
                "prompt": "Wer hat 1886 das erste Auto gebaut?",
                "options": [
                    "Carl Benz",
                    "Werner von Siemens",
                    "Adolph Menzel",
                    "Otto von Bismarck",
                ],
                "answer": "Carl Benz",
            },
        ],
    },
    {
        "order": 8,
        "level": "A2",
        "era": "Gegenwart",
        "title": "Deutschland in Europa",
        "image": "europa",
        "image_credit": f"Die Flagge Europas. {COMMONS}",
        "excerpt": "Nach dem Krieg begann Deutschland, mit seinen Nachbarn zusammenzuarbeiten. Heute ist es Teil der EU.",
        "body_de": """Nach dem Zweiten Weltkrieg wollten viele Politiker in Europa vor allem eins: nie wieder Krieg. Eine Idee war, dass die Länder zusammenarbeiten und miteinander handeln. 1951 gründeten sechs Länder die Europäische Gemeinschaft für Kohle und Stahl: die Bundesrepublik Deutschland, Frankreich, Italien, Belgien, die Niederlande und Luxemburg. 1957 unterschrieben sie die Römischen Verträge. Daraus wurde später die Europäische Union, die EU.

Besonders wichtig war die Freundschaft zwischen Deutschland und Frankreich. Früher waren die beiden Länder oft Feinde. 1963 unterschrieben sie den Élysée-Vertrag, einen Vertrag über Freundschaft und Zusammenarbeit. Seitdem besuchen sich jedes Jahr viele junge Menschen aus beiden Ländern.

Heute hat die EU 27 Länder. Vieles ist für die Menschen leichter geworden. Im Schengen-Raum gibt es normalerweise keine Kontrollen an den Grenzen. Man darf in einem anderen EU-Land wohnen, arbeiten und studieren. Seit 2002 bezahlt man in Deutschland mit dem Euro. Vorher gab es die D-Mark.

Deutschland liegt in der Mitte von Europa und hat neun Nachbarländer: Dänemark, Polen, Tschechien, Österreich, die Schweiz, Frankreich, Luxemburg, Belgien und die Niederlande. In Deutschland leben etwa 84 Millionen Menschen, mehr als in jedem anderen EU-Land. Das Land hat 16 Bundesländer, und die Hauptstadt ist Berlin.

Deutschland ist heute ein Land mit vielen Kulturen. Mehr als ein Viertel der Menschen hat eine Migrationsgeschichte: Sie selbst oder ihre Eltern kamen aus einem anderen Land.

Die Flagge oben, mit zwölf goldenen Sternen, ist die Flagge von Europa. Wer Deutsch lernt, lernt also nicht nur eine Sprache, sondern auch ein Land mitten in Europa kennen.""",
        "body_en": """After the Second World War many politicians in Europe wanted one thing above all: never again war. One idea was for the countries to work together and trade with each other. In 1951 six countries founded the European Coal and Steel Community: the Federal Republic of Germany, France, Italy, Belgium, the Netherlands and Luxembourg. In 1957 they signed the Treaties of Rome. This later became the European Union, the EU.

The friendship between Germany and France was especially important. In the past the two countries were often enemies. In 1963 they signed the Élysée Treaty, a treaty of friendship and cooperation. Since then many young people from both countries visit each other every year.

Today the EU has 27 countries. Many things have become easier for people. In the Schengen Area there are normally no checks at the borders. You may live, work and study in another EU country. Since 2002 people in Germany have paid with the euro. Before that there was the Deutsche Mark.

Germany lies in the middle of Europe and has nine neighbours: Denmark, Poland, the Czech Republic, Austria, Switzerland, France, Luxembourg, Belgium and the Netherlands. About 84 million people live in Germany, more than in any other EU country. The country has 16 federal states, and the capital is Berlin.

Germany today is a country of many cultures. More than a quarter of the people have a migration history: they or their parents came from another country.

The flag above, with twelve golden stars, is the flag of Europe. So anyone who learns German learns not only a language but also a country in the middle of Europe.""",
        "quiz": [
            {
                "prompt": "Wie viele Länder gründeten 1951 die Gemeinschaft für Kohle und Stahl?",
                "options": ["sechs", "zwei", "zwölf", "siebenundzwanzig"],
                "answer": "sechs",
            },
            {
                "prompt": "Mit welchem Land unterschrieb Deutschland 1963 den Élysée-Vertrag?",
                "options": ["mit Frankreich", "mit Polen", "mit Österreich", "mit Dänemark"],
                "answer": "mit Frankreich",
            },
            {
                "prompt": "Seit wann bezahlt man in Deutschland mit dem Euro?",
                "options": ["seit 2002", "seit 1990", "seit 1957", "seit 1871"],
                "answer": "seit 2002",
            },
            {
                "prompt": "Wie viele Nachbarländer hat Deutschland?",
                "options": ["neun", "vier", "sechzehn", "siebenundzwanzig"],
                "answer": "neun",
            },
            {
                "prompt": "Wie viele Bundesländer hat Deutschland?",
                "options": ["16", "9", "27", "4"],
                "answer": "16",
            },
        ],
    },
    {
        "order": 9,
        "level": "B1",
        "era": "20. Jahrhundert",
        "title": "Der Erste Weltkrieg und die Weimarer Republik",
        "image": "weimar",
        "image_credit": f"Das Nationaltheater in Weimar (1919). Internet Archive Book Images, {COMMONS}",
        "excerpt": "Nach dem Ersten Weltkrieg wurde Deutschland zum ersten Mal eine Demokratie.",
        "body_de": """Im Jahr 1914 begann der Erste Weltkrieg. Deutschland und Österreich-Ungarn kämpften gegen Frankreich, Großbritannien, Russland und später auch gegen die USA. Der Krieg dauerte über vier Jahre. Millionen Soldaten starben, allein aus Deutschland etwa zwei Millionen. Auch zu Hause hatten die Menschen oft nicht genug zu essen.

Wie es zum Krieg kam, ist kompliziert. Im Juni 1914 wurde der österreichische Thronfolger Franz Ferdinand in Sarajevo ermordet. Weil die großen Mächte Europas Bündnisse geschlossen hatten, wurde aus dem Konflikt zwischen Österreich-Ungarn und Serbien innerhalb weniger Wochen ein Krieg, an dem fast ganz Europa beteiligt war. Viele glaubten anfangs, dass er nach wenigen Monaten vorbei sein würde. Stattdessen erstarrte die Front im Westen: Die Soldaten lagen jahrelang in Schützengräben, und neue Waffen wie Maschinengewehre und Giftgas forderten unzählige Opfer.

Im Herbst 1918 war der Krieg verloren. Soldaten und Arbeiter protestierten. Kaiser Wilhelm II. musste gehen und floh in die Niederlande. Am 9. November 1918 wurde in Berlin die Republik ausgerufen. Deutschland war jetzt zum ersten Mal eine Demokratie.

Im Februar 1919 traf sich das neue Parlament, die Nationalversammlung. In Berlin war es zu unruhig, darum tagte es in Weimar, im Nationaltheater. Das Bild oben zeigt dieses Theater. Hier entstand die neue Verfassung. Darum heißt diese Zeit die Weimarer Republik. Neu war auch: Frauen durften jetzt wählen und gewählt werden.

Die junge Republik hatte viele Probleme. Im Vertrag von Versailles musste Deutschland Land abgeben und sehr viel Geld bezahlen. Viele Deutsche fanden den Vertrag ungerecht. Im Jahr 1923 verlor das Geld fast jeden Wert. Am Ende kostete ein Brot Milliarden Mark.

Die Republik wurde außerdem von links und von rechts angegriffen. Im November 1923 versuchte Adolf Hitler in München, mit einem Putsch die Macht zu übernehmen. Der Putsch scheiterte, und Hitler musste für einige Monate ins Gefängnis, wo er sein Buch „Mein Kampf“ schrieb.

Ab 1924 ging es besser. Berlin wurde eine Stadt der Kunst, des Films und der Musik. Man spricht von den „Goldenen Zwanzigern“. In Weimar und später in Dessau arbeitete das Bauhaus, eine berühmte Schule für Design und Architektur.

Aber 1929 kam eine große Weltwirtschaftskrise. Viele Firmen schlossen, und 1932 hatten etwa sechs Millionen Menschen keine Arbeit. Viele wählten nun Parteien, die gegen die Demokratie waren. Am 30. Januar 1933 wurde Adolf Hitler Reichskanzler. Das war das Ende der Weimarer Republik.""",
        "body_en": """In 1914 the First World War began. Germany and Austria-Hungary fought against France, Great Britain, Russia and later also against the USA. The war lasted more than four years. Millions of soldiers died, about two million from Germany alone. At home, too, people often did not have enough to eat.

How the war came about is complicated. In June 1914 the heir to the Austrian throne, Franz Ferdinand, was murdered in Sarajevo. Because Europe's great powers had made alliances, the conflict between Austria-Hungary and Serbia turned within a few weeks into a war in which almost all of Europe took part. At first many people believed it would be over within a few months. Instead the Western Front froze: soldiers lay in trenches for years, and new weapons such as machine guns and poison gas claimed countless victims.

By autumn 1918 the war was lost. Soldiers and workers protested. Emperor Wilhelm II had to go and fled to the Netherlands. On 9 November 1918 the republic was proclaimed in Berlin. For the first time, Germany was a democracy.

In February 1919 the new parliament, the National Assembly, met. Berlin was too unsettled, so it met in Weimar, in the National Theatre. The picture above shows this theatre. The new constitution was written here. That is why this period is called the Weimar Republic. Something else was new: women could now vote and be elected.

The young republic had many problems. In the Treaty of Versailles Germany had to give up land and pay a great deal of money. Many Germans found the treaty unfair. In 1923 money lost almost all its value. In the end a loaf of bread cost billions of marks.

The republic was also attacked from the left and the right. In November 1923 Adolf Hitler tried to seize power in Munich with a putsch. The putsch failed, and Hitler had to go to prison for a few months, where he wrote his book Mein Kampf.

From 1924 things got better. Berlin became a city of art, film and music. People speak of the "Golden Twenties". In Weimar, and later in Dessau, the Bauhaus was at work, a famous school of design and architecture.

But in 1929 a great world economic crisis came. Many companies closed, and in 1932 about six million people had no work. Many now voted for parties that were against democracy. On 30 January 1933 Adolf Hitler became Chancellor. That was the end of the Weimar Republic.""",
        "quiz": [
            {
                "prompt": "Wann begann der Erste Weltkrieg?",
                "options": ["1914", "1918", "1939", "1871"],
                "answer": "1914",
            },
            {
                "prompt": "Wo traf sich die Nationalversammlung 1919?",
                "options": ["in Weimar", "in Bonn", "in Frankfurt", "in München"],
                "answer": "in Weimar",
            },
            {
                "prompt": "Was war 1919 neu für Frauen?",
                "options": [
                    "Sie durften wählen.",
                    "Sie durften Bücher lesen.",
                    "Sie durften reisen.",
                    "Sie durften Brot kaufen.",
                ],
                "answer": "Sie durften wählen.",
            },
            {
                "prompt": "Was passierte 1923 mit dem Geld?",
                "options": [
                    "Es verlor fast jeden Wert.",
                    "Der Euro kam.",
                    "Es wurde mehr wert.",
                    "Es gab keine Münzen mehr.",
                ],
                "answer": "Es verlor fast jeden Wert.",
            },
            {
                "prompt": "Wann wurde Hitler Reichskanzler?",
                "options": [
                    "am 30. Januar 1933",
                    "am 9. November 1918",
                    "am 1. September 1939",
                    "am 8. Mai 1945",
                ],
                "answer": "am 30. Januar 1933",
            },
        ],
    },
    {
        "order": 10,
        "level": "B1",
        "era": "20. Jahrhundert",
        "title": "Die NS-Zeit und der Zweite Weltkrieg",
        "image": "1945",
        "image_credit": f"Die Ruine des Reichstags in Berlin, 3. Juni 1945. No 5 Army Film & Photographic Unit, {COMMONS}",
        "excerpt": "Von 1933 bis 1945 war Deutschland eine Diktatur. Die Nazis ermordeten Millionen Menschen.",
        "body_de": """Nach dem 30. Januar 1933 machten die Nationalsozialisten, die Nazis, aus Deutschland in wenigen Monaten eine Diktatur. Sie verboten alle anderen Parteien und die freien Gewerkschaften. Zeitungen und Radio durften nur noch sagen, was die Nazis wollten. Wer gegen sie war, kam ins Gefängnis oder in ein Konzentrationslager.

Wie konnte das geschehen? Historiker nennen mehrere Gründe: die schwere Wirtschaftskrise, die Angst vieler Menschen vor dem Kommunismus, die Schwäche der demokratischen Parteien und die geschickte Propaganda der Nazis. Viele Deutsche machten mit, viele schauten weg, und nur wenige leisteten Widerstand.

Die Nazis verfolgten vor allem die Juden. Ab 1933 verloren jüdische Menschen Schritt für Schritt ihre Rechte, ihre Arbeit und ihr Eigentum. In der Nacht vom 9. auf den 10. November 1938 brannten in ganz Deutschland Synagogen, und jüdische Geschäfte wurden zerstört. Auch Sinti und Roma, Menschen mit Behinderung, Homosexuelle und politische Gegner wurden verfolgt.

Am 1. September 1939 griff Deutschland Polen an. So begann der Zweite Weltkrieg. Die deutsche Armee besetzte große Teile von Europa. Im ganzen Krieg starben mehr als 60 Millionen Menschen.

Die Nazis ermordeten etwa sechs Millionen europäische Juden. Diesen Völkermord nennt man den Holocaust oder die Shoah. Die meisten Opfer starben in Ghettos und in Vernichtungslagern, zum Beispiel in Auschwitz. Auch Hunderttausende Sinti und Roma wurden ermordet. Es gab auch Menschen, die Widerstand leisteten, zum Beispiel die Studenten der Weißen Rose in München.

Am 20. Juli 1944 versuchte eine Gruppe von Offizieren um Claus Schenk Graf von Stauffenberg, Hitler mit einer Bombe zu töten und den Krieg zu beenden. Das Attentat scheiterte, und die meisten Beteiligten wurden hingerichtet. Heute ist der 20. Juli ein wichtiger Gedenktag für den Widerstand.

Viele deutsche Städte wurden im Krieg zerstört. Am 8. Mai 1945 kapitulierte Deutschland bedingungslos. In Europa war der Krieg zu Ende. Das Bild oben zeigt die Ruine des Reichstags in Berlin im Juni 1945.

Heute erinnert Deutschland an diese Zeit, zum Beispiel mit dem Denkmal für die ermordeten Juden Europas in Berlin und mit vielen Gedenkstätten. Viele Schulklassen besuchen sie. Das Grundgesetz von 1949 beginnt mit dem Satz: „Die Würde des Menschen ist unantastbar.“""",
        "body_en": """After 30 January 1933 the National Socialists, the Nazis, turned Germany into a dictatorship within a few months. They banned all other parties and the free trade unions. Newspapers and radio could only say what the Nazis wanted. Anyone who was against them went to prison or to a concentration camp.

How could this happen? Historians name several reasons: the severe economic crisis, many people's fear of communism, the weakness of the democratic parties and the Nazis' skilful propaganda. Many Germans took part, many looked away, and only a few resisted.

Above all, the Nazis persecuted the Jews. From 1933 Jewish people lost their rights, their work and their property step by step. On the night of 9 to 10 November 1938 synagogues burned all over Germany, and Jewish shops were destroyed. Sinti and Roma, people with disabilities, homosexuals and political opponents were persecuted too.

On 1 September 1939 Germany attacked Poland. This was the beginning of the Second World War. The German army occupied large parts of Europe. In the whole war more than 60 million people died.

The Nazis murdered about six million European Jews. This genocide is called the Holocaust or the Shoah. Most of the victims died in ghettos and in extermination camps, for example in Auschwitz. Hundreds of thousands of Sinti and Roma were also murdered. There were also people who resisted, for example the students of the White Rose in Munich.

On 20 July 1944 a group of officers around Claus Schenk Graf von Stauffenberg tried to kill Hitler with a bomb and end the war. The attempt failed, and most of those involved were executed. Today 20 July is an important day of remembrance for the resistance.

Many German cities were destroyed in the war. On 8 May 1945 Germany surrendered unconditionally. In Europe the war was over. The picture above shows the ruins of the Reichstag in Berlin in June 1945.

Today Germany remembers this time, for example with the Memorial to the Murdered Jews of Europe in Berlin and with many memorial sites. Many school classes visit them. The Basic Law of 1949 begins with the sentence: "Human dignity shall be inviolable.\"""",
        "quiz": [
            {
                "prompt": "Was machten die Nazis ab 1933 aus Deutschland?",
                "options": [
                    "eine Diktatur",
                    "eine Demokratie",
                    "ein Königreich",
                    "eine Republik mit freien Wahlen",
                ],
                "answer": "eine Diktatur",
            },
            {
                "prompt": "Was passierte am 1. September 1939?",
                "options": [
                    "Deutschland griff Polen an.",
                    "Die Mauer fiel.",
                    "Der Euro kam.",
                    "Luther schrieb seine Thesen.",
                ],
                "answer": "Deutschland griff Polen an.",
            },
            {
                "prompt": "Wie viele europäische Juden ermordeten die Nazis?",
                "options": [
                    "etwa sechs Millionen",
                    "etwa sechstausend",
                    "etwa sechzigtausend",
                    "etwa sechshunderttausend",
                ],
                "answer": "etwa sechs Millionen",
            },
            {
                "prompt": "Wann kapitulierte Deutschland?",
                "options": [
                    "am 8. Mai 1945",
                    "am 3. Oktober 1990",
                    "am 30. Januar 1933",
                    "am 13. August 1961",
                ],
                "answer": "am 8. Mai 1945",
            },
            {
                "prompt": "Wie beginnt das Grundgesetz?",
                "options": [
                    "„Die Würde des Menschen ist unantastbar.“",
                    "„Alle Macht dem Kaiser.“",
                    "„Deutschland ist ein Königreich.“",
                    "„Wir sind das Volk.“",
                ],
                "answer": "„Die Würde des Menschen ist unantastbar.“",
            },
        ],
    },
    {
        "order": 11,
        "level": "B1",
        "era": "Geteiltes Deutschland",
        "title": "Teilung und die Berliner Mauer",
        "image": "mauer",
        "image_credit": f"Die Berliner Mauer, 20. November 1961. U.S. National Archives, {COMMONS}",
        "excerpt": "Nach dem Krieg gab es zwei deutsche Staaten. 1961 baute die DDR die Mauer.",
        "body_de": """Nach dem Krieg teilten die USA, Großbritannien, Frankreich und die Sowjetunion Deutschland in vier Zonen. Auch Berlin wurde in vier Sektoren geteilt.

Bald gab es Streit zwischen den Westmächten und der Sowjetunion. 1948 sperrte die Sowjetunion alle Wege nach West-Berlin. Fast ein Jahr lang brachten die Amerikaner und die Briten Essen und Kohle mit Flugzeugen in die Stadt. Das war die Luftbrücke.

1949 entstanden zwei deutsche Staaten. Im Westen die Bundesrepublik Deutschland mit der Hauptstadt Bonn. Sie war eine Demokratie und hatte das Grundgesetz. Im Osten die Deutsche Demokratische Republik, die DDR. Ihr Name klang demokratisch, aber sie war eine Diktatur der Partei SED. Ihre Hauptstadt war Ost-Berlin.

In der Bundesrepublik wuchs die Wirtschaft schnell. Man sprach vom Wirtschaftswunder. In der DDR gab es weniger Freiheit und weniger Waren. Bis 1961 gingen fast drei Millionen Menschen aus der DDR in den Westen, viele über Berlin.

Der Alltag in der DDR wurde vom Staat streng kontrolliert. Die Geheimpolizei, die Stasi, beobachtete Millionen von Menschen. Sie arbeitete mit vielen inoffiziellen Mitarbeitern zusammen, die ihre Nachbarn, Kollegen oder sogar Familienmitglieder ausspionierten. Wer den Staat kritisierte, konnte seine Arbeit verlieren oder ins Gefängnis kommen. Gleichzeitig gab es für alle Arbeit, Kindergärten und billige Wohnungen, woran sich manche Menschen bis heute gern erinnern.

Am 13. August 1961 begann die DDR, eine Mauer durch Berlin zu bauen. Am Ende war die Mauer etwa 155 Kilometer lang und ging rund um West-Berlin. Familien und Freunde waren plötzlich getrennt. Das Bild oben zeigt die Mauer im November 1961.

Wer über die Mauer fliehen wollte, war in großer Gefahr. Mindestens 140 Menschen starben an der Berliner Mauer. 1963 besuchte der amerikanische Präsident John F. Kennedy West-Berlin und sagte den berühmten Satz: „Ich bin ein Berliner.“

Fast 30 Jahre lang war die Mauer das Zeichen für ein geteiltes Deutschland und ein geteiltes Europa.""",
        "body_en": """After the war the USA, Great Britain, France and the Soviet Union divided Germany into four zones. Berlin, too, was divided into four sectors.

Soon there was conflict between the Western powers and the Soviet Union. In 1948 the Soviet Union blocked all routes into West Berlin. For almost a year the Americans and the British flew food and coal into the city. This was the Berlin Airlift.

In 1949 two German states were founded. In the west, the Federal Republic of Germany with its capital Bonn. It was a democracy and had the Basic Law. In the east, the German Democratic Republic, the GDR. Its name sounded democratic, but it was a dictatorship of the SED party. Its capital was East Berlin.

In the Federal Republic the economy grew fast. People spoke of the economic miracle. In the GDR there was less freedom and fewer goods. By 1961 almost three million people had left the GDR for the West, many of them through Berlin.

Everyday life in the GDR was strictly controlled by the state. The secret police, the Stasi, watched millions of people. It worked with many unofficial informers who spied on their neighbours, colleagues or even family members. Anyone who criticised the state could lose their job or go to prison. At the same time everyone had work, a kindergarten place and a cheap flat, which some people still remember fondly today.

On 13 August 1961 the GDR began to build a wall through Berlin. In the end the wall was about 155 kilometres long and went all the way around West Berlin. Families and friends were suddenly separated. The picture above shows the wall in November 1961.

Anyone who tried to escape over the wall was in great danger. At least 140 people died at the Berlin Wall. In 1963 the American president John F. Kennedy visited West Berlin and said the famous sentence: "Ich bin ein Berliner" (I am a Berliner).

For almost 30 years the wall was the symbol of a divided Germany and a divided Europe.""",
        "quiz": [
            {
                "prompt": "In wie viele Zonen wurde Deutschland nach dem Krieg geteilt?",
                "options": ["in vier", "in zwei", "in drei", "in sechs"],
                "answer": "in vier",
            },
            {
                "prompt": "Was war die Luftbrücke?",
                "options": [
                    "Flugzeuge brachten Essen nach West-Berlin.",
                    "eine Brücke über den Rhein",
                    "eine Straße nach Bonn",
                    "ein Zug nach Paris",
                ],
                "answer": "Flugzeuge brachten Essen nach West-Berlin.",
            },
            {
                "prompt": "Was war die Hauptstadt der Bundesrepublik?",
                "options": ["Bonn", "Ost-Berlin", "München", "Frankfurt"],
                "answer": "Bonn",
            },
            {
                "prompt": "Wann begann der Bau der Berliner Mauer?",
                "options": [
                    "am 13. August 1961",
                    "am 9. November 1989",
                    "am 8. Mai 1945",
                    "am 3. Oktober 1990",
                ],
                "answer": "am 13. August 1961",
            },
            {
                "prompt": "Wer sagte 1963 „Ich bin ein Berliner“?",
                "options": ["John F. Kennedy", "Otto von Bismarck", "Martin Luther", "Napoleon"],
                "answer": "John F. Kennedy",
            },
        ],
    },
    {
        "order": 12,
        "level": "B1",
        "era": "Geteiltes Deutschland",
        "title": "Mauerfall und Wiedervereinigung",
        "image": "1989",
        "image_credit": f"Am Brandenburger Tor, Dezember 1989. SSGT F. Lee Corkran, U.S. Air Force, {COMMONS}",
        "excerpt": "1989 fiel die Mauer, und 1990 war Deutschland wieder ein Land.",
        "body_de": """In den 1980er-Jahren waren viele Menschen in der DDR unzufrieden. Sie durften nicht frei reisen, nicht frei sprechen und nicht frei wählen. 1989 änderte sich viel in Osteuropa. In Ungarn öffnete sich die Grenze nach Österreich, und Tausende Menschen aus der DDR flohen über Ungarn in den Westen.

Gleichzeitig gingen in der DDR immer mehr Menschen auf die Straße. Besonders bekannt sind die Montagsdemonstrationen in Leipzig. Am 9. Oktober 1989 demonstrierten dort etwa 70.000 Menschen friedlich. Sie riefen: „Wir sind das Volk!“ Die Regierung schickte keine Soldaten gegen sie.

Am Abend des 9. November 1989 sagte ein Politiker der DDR, Günter Schabowski, in einer Pressekonferenz: Die Menschen dürfen ab sofort reisen. Tausende Ost-Berliner gingen sofort zur Mauer. In der Nacht öffneten die Grenzsoldaten die Grenze. Menschen aus Ost und West feierten zusammen auf der Mauer. Das Bild oben zeigt das Brandenburger Tor im Dezember 1989.

Dass die Mauer in dieser Nacht fiel, war eigentlich ein Versehen. Schabowski hatte einen Zettel mit einer neuen Reiseregelung bekommen, die erst am nächsten Tag gelten sollte. Als ein Journalist fragte, ab wann sie gelte, antwortete er: „Das tritt nach meiner Kenntnis … ist das sofort, unverzüglich.“ Die Nachricht lief sofort im Fernsehen. Am Grenzübergang Bornholmer Straße wurde die Menge immer größer, und weil der Offizier Harald Jäger keine klaren Befehle bekam, öffnete er gegen 23:30 Uhr als Erster den Schlagbaum.

Im März 1990 gab es in der DDR die erste freie Wahl. Im Juli 1990 bekam auch die DDR die D-Mark. Und am 3. Oktober 1990 war es so weit: Die DDR trat der Bundesrepublik bei. Deutschland war wieder ein Land. Seitdem ist der 3. Oktober der Tag der Deutschen Einheit, ein Feiertag.

Berlin wurde wieder die Hauptstadt. 1999 zogen das Parlament und die Regierung von Bonn nach Berlin.

Das Zusammenwachsen von Ost und West war nicht immer leicht. Viele Menschen im Osten verloren ihre Arbeit, und manche Unterschiede gibt es bis heute. Aber junge Menschen kennen die Mauer heute nur noch aus Büchern und Museen.""",
        "body_en": """In the 1980s many people in the GDR were unhappy. They were not allowed to travel freely, speak freely or vote freely. In 1989 a lot changed in Eastern Europe. In Hungary the border to Austria opened, and thousands of people from the GDR fled to the West through Hungary.

At the same time more and more people in the GDR took to the streets. The Monday demonstrations in Leipzig are especially well known. On 9 October 1989 about 70,000 people demonstrated there peacefully. They shouted: "We are the people!" The government did not send soldiers against them.

On the evening of 9 November 1989 a GDR politician, Günter Schabowski, said at a press conference that people could travel, starting immediately. Thousands of East Berliners went straight to the wall. That night the border guards opened the border. People from East and West celebrated together on the wall. The picture above shows the Brandenburg Gate in December 1989.

That the Wall fell that night was really a mistake. Schabowski had been given a note about a new travel rule that was only meant to apply from the next day. When a journalist asked from when it applied, he answered: "As far as I know, it takes effect ... immediately, without delay." The news was on television at once. At the Bornholmer Straße border crossing the crowd kept growing, and because the officer Harald Jäger received no clear orders, at about 23:30 he was the first to open the barrier.

In March 1990 the GDR held its first free election. In July 1990 the GDR got the Deutsche Mark too. And on 3 October 1990 the day came: the GDR joined the Federal Republic. Germany was one country again. Since then 3 October has been the Day of German Unity, a public holiday.

Berlin became the capital again. In 1999 the parliament and the government moved from Bonn to Berlin.

Growing together was not always easy for East and West. Many people in the East lost their jobs, and some differences remain to this day. But young people today know the wall only from books and museums.""",
        "quiz": [
            {
                "prompt": "In welcher Stadt gab es die Montagsdemonstrationen?",
                "options": ["in Leipzig", "in Bonn", "in München", "in Hamburg"],
                "answer": "in Leipzig",
            },
            {
                "prompt": "Was riefen die Menschen bei den Demonstrationen?",
                "options": [
                    "„Wir sind das Volk!“",
                    "„Ich bin ein Berliner!“",
                    "„Eisen und Blut!“",
                    "„Nie wieder Krieg!“",
                ],
                "answer": "„Wir sind das Volk!“",
            },
            {
                "prompt": "Wann öffnete sich die Berliner Mauer?",
                "options": [
                    "am 9. November 1989",
                    "am 13. August 1961",
                    "am 3. Oktober 1990",
                    "am 9. Oktober 1989",
                ],
                "answer": "am 9. November 1989",
            },
            {
                "prompt": "Was feiert man am 3. Oktober?",
                "options": [
                    "den Tag der Deutschen Einheit",
                    "den Reformationstag",
                    "Weihnachten",
                    "den Tag der Arbeit",
                ],
                "answer": "den Tag der Deutschen Einheit",
            },
            {
                "prompt": "Wann zogen Parlament und Regierung nach Berlin?",
                "options": ["1999", "1949", "1871", "2002"],
                "answer": "1999",
            },
        ],
    },
]
