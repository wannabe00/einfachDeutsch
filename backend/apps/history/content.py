"""The German-history lessons, loaded by `manage.py seed_history`.

Simple German (A1/A2: short sentences, mostly present tense, war/hatte and the
Perfekt), an English translation the reader can show, five quiz questions, and
a public-domain picture from Wikimedia Commons bundled with the frontend
(`frontend/public/history/`). Lessons are matched on `order`.
"""

COMMONS = "Wikimedia Commons, public domain"

LESSONS = [
    {
        "order": 1,
        "era": "Antike",
        "title": "Die Römer und die Germanen",
        "image": "roemer",
        "image_credit": f"Otto Albert Koch, Varusschlacht (1909). {COMMONS}",
        "excerpt": "Vor 2000 Jahren kamen die Römer an den Rhein. Östlich davon lebten die Germanen.",
        "body_de": """Vor etwa 2000 Jahren war das Römische Reich sehr groß und sehr mächtig. Die Römer kamen bis an den Rhein und an die Donau. Dort bauten sie Lager für ihre Soldaten. Aus vielen Lagern wurden später Städte: Köln, Mainz, Trier, Bonn und Augsburg sind sehr alte römische Städte. In Trier steht noch heute ein großes römisches Tor, die Porta Nigra.

Östlich vom Rhein lebten die Germanen. Sie waren kein Volk mit einem Staat, sondern viele Stämme. Sie wohnten in kleinen Dörfern mit Häusern aus Holz. Sie waren Bauern und hielten Tiere. Städte gab es bei ihnen nicht.

Im Jahr 9 nach Christus wollten die Römer auch das Land östlich vom Rhein haben. Aber in einem Wald in Norddeutschland kam es zu einer großen Schlacht. Arminius, ein Anführer der Cherusker, hatte selbst in der römischen Armee gedient. Er kannte die Römer gut und führte ihre Soldaten in eine Falle. Drei römische Legionen und ihr Feldherr Varus verloren die Schlacht. Heute heißt sie die Varusschlacht. Das Bild oben zeigt sie so, wie man sie sich im Jahr 1909 vorstellte.

Danach blieb der Rhein lange die Grenze. Später bauten die Römer zwischen Rhein und Donau eine lange Grenze mit Wällen und Türmen: den Limes. Er war etwa 550 Kilometer lang und ist heute Weltkulturerbe.

Die Römer brachten viel Neues mit: Straßen aus Stein, Häuser mit Fenstern, Bäder und den Wein. Deshalb kommen viele deutsche Wörter aus dem Lateinischen, zum Beispiel Mauer, Fenster, Straße, Keller und Wein. Im 5. Jahrhundert endete die Macht der Römer am Rhein. Aber ihre Städte, ihre Straßen und viele Wörter sind geblieben.""",
        "body_en": """About 2,000 years ago the Roman Empire was very large and very powerful. The Romans came as far as the Rhine and the Danube. There they built camps for their soldiers. Many camps later became towns: Cologne, Mainz, Trier, Bonn and Augsburg are very old Roman towns. In Trier a large Roman gate still stands today, the Porta Nigra.

East of the Rhine lived the Germanic peoples. They were not one people with a state, but many tribes. They lived in small villages with wooden houses. They were farmers and kept animals. They had no towns.

In the year 9 AD the Romans wanted the land east of the Rhine as well. But in a forest in northern Germany there was a great battle. Arminius, a leader of the Cherusci, had served in the Roman army himself. He knew the Romans well and led their soldiers into a trap. Three Roman legions and their commander Varus lost the battle. Today it is called the Battle of the Teutoburg Forest (Varusschlacht). The picture above shows it the way people imagined it in 1909.

After that the Rhine remained the border for a long time. Later the Romans built a long border with ramparts and towers between the Rhine and the Danube: the Limes. It was about 550 kilometres long and is a World Heritage Site today.

The Romans brought many new things: stone roads, houses with windows, baths and wine. That is why many German words come from Latin, for example Mauer (wall), Fenster (window), Straße (street), Keller (cellar) and Wein (wine). In the 5th century Roman power on the Rhine came to an end. But their towns, their roads and many words have remained.""",
        "quiz": [
            {
                "prompt": "Welche Stadt war früher ein römisches Lager?",
                "options": ["Köln", "Berlin", "Hamburg", "Dresden"],
                "answer": "Köln",
            },
            {
                "prompt": "Wie heißt das große römische Tor in Trier?",
                "options": [
                    "die Porta Nigra",
                    "das Brandenburger Tor",
                    "das Holstentor",
                    "das Siegestor",
                ],
                "answer": "die Porta Nigra",
            },
            {
                "prompt": "Wer führte die Germanen in der Varusschlacht?",
                "options": ["Arminius", "Varus", "Augustus", "Karl der Große"],
                "answer": "Arminius",
            },
            {
                "prompt": "Was ist der Limes?",
                "options": ["eine lange römische Grenze", "ein Fluss", "eine Stadt", "ein Wald"],
                "answer": "eine lange römische Grenze",
            },
            {
                "prompt": "Welches Wort kommt aus dem Lateinischen?",
                "options": ["Fenster", "Haus", "Hund", "Brot"],
                "answer": "Fenster",
            },
        ],
    },
    {
        "order": 2,
        "era": "Mittelalter",
        "title": "Karl der Große und das Heilige Römische Reich",
        "image": "karl",
        "image_credit": f"Albrecht Dürer, Kaiser Karl der Große (um 1512). {COMMONS}",
        "excerpt": "Im Jahr 800 wurde Karl der Große Kaiser. Später entstand das Heilige Römische Reich.",
        "body_de": """Nach den Römern lebten in Westeuropa viele Völker. Das stärkste Volk waren die Franken. Ab dem Jahr 768 war Karl ihr König. Er führte viele Kriege und machte sein Reich sehr groß. Es reichte vom heutigen Frankreich über Deutschland bis nach Italien. Darum nennt man ihn Karl den Großen.

Am 25. Dezember 800 krönte der Papst Karl in Rom zum Kaiser. Karl wohnte oft in Aachen. Dort ließ er eine große Kirche bauen, die Pfalzkapelle. Sie ist heute ein Teil vom Aachener Dom, und Karl liegt dort begraben. Karl wollte, dass die Menschen lernen. Er holte kluge Männer an seinen Hof, und Mönche schrieben viele alte Bücher ab.

Karl starb im Jahr 814. Später teilten seine Enkel das Reich in drei Teile. Aus dem westlichen Teil wurde langsam Frankreich, aus dem östlichen Teil langsam Deutschland.

Im Jahr 962 wurde Otto I., ein König aus dem östlichen Teil, in Rom zum Kaiser gekrönt. So begann das Heilige Römische Reich. Es war kein Staat wie heute. Es bestand aus Hunderten von Ländern, Fürstentümern und freien Städten. Jeder Fürst hatte in seinem Land viel Macht. Den König wählten die wichtigsten Fürsten, die Kurfürsten. Der Kaiser hatte oft weniger Macht als die großen Fürsten.

Das Reich bestand fast 850 Jahre lang. Im Jahr 1806 war Napoleon in Europa sehr mächtig. Kaiser Franz II. legte die Krone nieder, und das Reich endete.

Das Bild oben zeigt Karl den Großen so, wie ihn der Maler Albrecht Dürer um 1512 malte. Das war mehr als 700 Jahre nach Karls Tod. Niemand weiß genau, wie Karl wirklich aussah.""",
        "body_en": """After the Romans, many peoples lived in Western Europe. The strongest were the Franks. From the year 768 Charles was their king. He fought many wars and made his empire very large. It stretched from today's France across Germany to Italy. That is why he is called Charles the Great, or Charlemagne.

On 25 December 800 the Pope crowned Charles emperor in Rome. Charles often lived in Aachen. There he had a large church built, the Palatine Chapel. Today it is part of Aachen Cathedral, and Charles is buried there. Charles wanted people to learn. He brought clever men to his court, and monks copied many old books.

Charles died in 814. Later his grandsons divided the empire into three parts. The western part slowly became France, the eastern part slowly became Germany.

In 962 Otto I, a king from the eastern part, was crowned emperor in Rome. This was the beginning of the Holy Roman Empire. It was not a state like today's states. It was made up of hundreds of lands, principalities and free cities. Every prince had a lot of power in his own land. The king was elected by the most important princes, the prince-electors. The emperor often had less power than the great princes.

The empire lasted almost 850 years. In 1806 Napoleon was very powerful in Europe. Emperor Francis II gave up the crown, and the empire ended.

The picture above shows Charlemagne the way the painter Albrecht Dürer painted him around 1512. That was more than 700 years after Charles died. Nobody knows exactly what Charles really looked like.""",
        "quiz": [
            {
                "prompt": "Wann wurde Karl zum Kaiser gekrönt?",
                "options": ["800", "962", "1806", "1517"],
                "answer": "800",
            },
            {
                "prompt": "In welcher Stadt liegt Karl der Große begraben?",
                "options": ["Aachen", "Rom", "Paris", "Wien"],
                "answer": "Aachen",
            },
            {
                "prompt": "Wer teilte das Reich nach Karls Tod?",
                "options": ["seine Enkel", "der Papst", "Napoleon", "die Römer"],
                "answer": "seine Enkel",
            },
            {
                "prompt": "Wer wählte den König im Heiligen Römischen Reich?",
                "options": ["die Kurfürsten", "das ganze Volk", "der Papst", "die Mönche"],
                "answer": "die Kurfürsten",
            },
            {
                "prompt": "Wann endete das Heilige Römische Reich?",
                "options": ["1806", "814", "1648", "1871"],
                "answer": "1806",
            },
        ],
    },
    {
        "order": 3,
        "era": "Frühe Neuzeit",
        "title": "Martin Luther und die Reformation",
        "image": "reformation",
        "image_credit": f"Lucas Cranach der Ältere, Martin Luther (1528). {COMMONS}",
        "excerpt": "1517 schrieb Martin Luther 95 Thesen. Daraus wurde die Reformation.",
        "body_de": """Martin Luther wurde 1483 in Eisleben geboren. Er studierte, wurde Mönch und später Professor in Wittenberg. Luther las viel in der Bibel und dachte viel über Gott nach.

Zu dieser Zeit verkaufte die Kirche sogenannte Ablassbriefe. Die Menschen bezahlten Geld, und die Kirche versprach ihnen, dass Gott ihnen ihre Sünden verzeiht. Luther fand das falsch. Er meinte: Gott verzeiht aus Liebe, nicht für Geld. Im Jahr 1517 schrieb er 95 Thesen gegen den Ablass. Nach einer berühmten Geschichte schlug er sie am 31. Oktober an die Tür der Schlosskirche in Wittenberg. Darum ist der 31. Oktober heute der Reformationstag.

Luthers Ideen waren bald überall bekannt. Das lag an einer neuen Technik: dem Buchdruck. Johannes Gutenberg aus Mainz hatte ihn um 1450 erfunden. Jetzt konnte man Texte schnell und billig drucken.

Der Papst und der Kaiser waren gegen Luther. 1521 musste er auf dem Reichstag in Worms sprechen. Er sollte seine Ideen zurücknehmen, aber er sagte Nein. Danach war er in Gefahr. Freunde versteckten ihn auf der Wartburg bei Eisenach. Dort übersetzte er das Neue Testament ins Deutsche. Sehr viele Menschen lasen seine Bibel, und sie half, eine gemeinsame deutsche Schriftsprache zu bilden.

Aus Luthers Bewegung entstand die evangelische Kirche. Deutschland war nun geteilt: Manche Fürsten blieben katholisch, andere wurden evangelisch. Es gab lange Streit und auch Kriege, zum Beispiel den Dreißigjährigen Krieg von 1618 bis 1648. Bis heute gibt es in Deutschland katholische und evangelische Christen.

Das Bild oben malte Lucas Cranach im Jahr 1528. Cranach war ein Freund von Luther und malte ihn viele Male.""",
        "body_en": """Martin Luther was born in Eisleben in 1483. He studied, became a monk and later a professor in Wittenberg. Luther read the Bible a lot and thought a lot about God.

At that time the Church sold so-called letters of indulgence. People paid money, and the Church promised them that God would forgive their sins. Luther thought this was wrong. He believed that God forgives out of love, not for money. In 1517 he wrote 95 theses against indulgences. According to a famous story, he nailed them to the door of the Castle Church in Wittenberg on 31 October. That is why 31 October is Reformation Day today.

Luther's ideas soon became known everywhere. This was because of a new technology: printing. Johannes Gutenberg from Mainz had invented it around 1450. Now texts could be printed quickly and cheaply.

The Pope and the emperor were against Luther. In 1521 he had to speak at the Imperial Diet in Worms. He was supposed to take back his ideas, but he said no. After that he was in danger. Friends hid him at the Wartburg castle near Eisenach. There he translated the New Testament into German. A great many people read his Bible, and it helped to form a common written German language.

Luther's movement gave rise to the Protestant church. Germany was now divided: some princes stayed Catholic, others became Protestant. There were long quarrels and wars, for example the Thirty Years' War from 1618 to 1648. To this day there are Catholic and Protestant Christians in Germany.

Lucas Cranach painted the picture above in 1528. Cranach was a friend of Luther's and painted him many times.""",
        "quiz": [
            {
                "prompt": "Wo war Luther Professor?",
                "options": ["in Wittenberg", "in Rom", "in Worms", "in Mainz"],
                "answer": "in Wittenberg",
            },
            {
                "prompt": "Wogegen schrieb Luther 1517 seine 95 Thesen?",
                "options": [
                    "gegen den Ablass",
                    "gegen den Buchdruck",
                    "gegen die Bibel",
                    "gegen Gutenberg",
                ],
                "answer": "gegen den Ablass",
            },
            {
                "prompt": "Welche Technik half, Luthers Ideen schnell zu verbreiten?",
                "options": ["der Buchdruck", "das Radio", "die Eisenbahn", "das Telefon"],
                "answer": "der Buchdruck",
            },
            {
                "prompt": "Was machte Luther auf der Wartburg?",
                "options": [
                    "Er übersetzte das Neue Testament ins Deutsche.",
                    "Er baute eine Kirche.",
                    "Er wurde Kaiser.",
                    "Er erfand den Buchdruck.",
                ],
                "answer": "Er übersetzte das Neue Testament ins Deutsche.",
            },
            {
                "prompt": "Wann ist der Reformationstag?",
                "options": ["am 31. Oktober", "am 3. Oktober", "am 9. November", "am 25. Dezember"],
                "answer": "am 31. Oktober",
            },
        ],
    },
    {
        "order": 4,
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
        "order": 5,
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
        "order": 6,
        "era": "20. Jahrhundert",
        "title": "Der Erste Weltkrieg und die Weimarer Republik",
        "image": "weimar",
        "image_credit": f"Das Nationaltheater in Weimar (1919). Internet Archive Book Images, {COMMONS}",
        "excerpt": "Nach dem Ersten Weltkrieg wurde Deutschland zum ersten Mal eine Demokratie.",
        "body_de": """Im Jahr 1914 begann der Erste Weltkrieg. Deutschland und Österreich-Ungarn kämpften gegen Frankreich, Großbritannien, Russland und später auch gegen die USA. Der Krieg dauerte über vier Jahre. Millionen Soldaten starben, allein aus Deutschland etwa zwei Millionen. Auch zu Hause hatten die Menschen oft nicht genug zu essen.

Im Herbst 1918 war der Krieg verloren. Soldaten und Arbeiter protestierten. Kaiser Wilhelm II. musste gehen und floh in die Niederlande. Am 9. November 1918 wurde in Berlin die Republik ausgerufen. Deutschland war jetzt zum ersten Mal eine Demokratie.

Im Februar 1919 traf sich das neue Parlament, die Nationalversammlung. In Berlin war es zu unruhig, darum tagte es in Weimar, im Nationaltheater. Das Bild oben zeigt dieses Theater. Hier entstand die neue Verfassung. Darum heißt diese Zeit die Weimarer Republik. Neu war auch: Frauen durften jetzt wählen und gewählt werden.

Die junge Republik hatte viele Probleme. Im Vertrag von Versailles musste Deutschland Land abgeben und sehr viel Geld bezahlen. Viele Deutsche fanden den Vertrag ungerecht. Im Jahr 1923 verlor das Geld fast jeden Wert. Am Ende kostete ein Brot Milliarden Mark.

Ab 1924 ging es besser. Berlin wurde eine Stadt der Kunst, des Films und der Musik. Man spricht von den „Goldenen Zwanzigern“. In Weimar und später in Dessau arbeitete das Bauhaus, eine berühmte Schule für Design und Architektur.

Aber 1929 kam eine große Weltwirtschaftskrise. Viele Firmen schlossen, und 1932 hatten etwa sechs Millionen Menschen keine Arbeit. Viele wählten nun Parteien, die gegen die Demokratie waren. Am 30. Januar 1933 wurde Adolf Hitler Reichskanzler. Das war das Ende der Weimarer Republik.""",
        "body_en": """In 1914 the First World War began. Germany and Austria-Hungary fought against France, Great Britain, Russia and later also against the USA. The war lasted more than four years. Millions of soldiers died, about two million from Germany alone. At home, too, people often did not have enough to eat.

By autumn 1918 the war was lost. Soldiers and workers protested. Emperor Wilhelm II had to go and fled to the Netherlands. On 9 November 1918 the republic was proclaimed in Berlin. For the first time, Germany was a democracy.

In February 1919 the new parliament, the National Assembly, met. Berlin was too unsettled, so it met in Weimar, in the National Theatre. The picture above shows this theatre. The new constitution was written here. That is why this period is called the Weimar Republic. Something else was new: women could now vote and be elected.

The young republic had many problems. In the Treaty of Versailles Germany had to give up land and pay a great deal of money. Many Germans found the treaty unfair. In 1923 money lost almost all its value. In the end a loaf of bread cost billions of marks.

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
        "order": 7,
        "era": "20. Jahrhundert",
        "title": "Die NS-Zeit und der Zweite Weltkrieg",
        "image": "1945",
        "image_credit": f"Die Ruine des Reichstags in Berlin, 3. Juni 1945. No 5 Army Film & Photographic Unit, {COMMONS}",
        "excerpt": "Von 1933 bis 1945 war Deutschland eine Diktatur. Die Nazis ermordeten Millionen Menschen.",
        "body_de": """Nach dem 30. Januar 1933 machten die Nationalsozialisten, die Nazis, aus Deutschland in wenigen Monaten eine Diktatur. Sie verboten alle anderen Parteien und die freien Gewerkschaften. Zeitungen und Radio durften nur noch sagen, was die Nazis wollten. Wer gegen sie war, kam ins Gefängnis oder in ein Konzentrationslager.

Die Nazis verfolgten vor allem die Juden. Ab 1933 verloren jüdische Menschen Schritt für Schritt ihre Rechte, ihre Arbeit und ihr Eigentum. In der Nacht vom 9. auf den 10. November 1938 brannten in ganz Deutschland Synagogen, und jüdische Geschäfte wurden zerstört. Auch Sinti und Roma, Menschen mit Behinderung, Homosexuelle und politische Gegner wurden verfolgt.

Am 1. September 1939 griff Deutschland Polen an. So begann der Zweite Weltkrieg. Die deutsche Armee besetzte große Teile von Europa. Im ganzen Krieg starben mehr als 60 Millionen Menschen.

Die Nazis ermordeten etwa sechs Millionen europäische Juden. Diesen Völkermord nennt man den Holocaust oder die Shoah. Die meisten Opfer starben in Ghettos und in Vernichtungslagern, zum Beispiel in Auschwitz. Auch Hunderttausende Sinti und Roma wurden ermordet. Es gab auch Menschen, die Widerstand leisteten, zum Beispiel die Studenten der Weißen Rose in München.

Viele deutsche Städte wurden im Krieg zerstört. Am 8. Mai 1945 kapitulierte Deutschland bedingungslos. In Europa war der Krieg zu Ende. Das Bild oben zeigt die Ruine des Reichstags in Berlin im Juni 1945.

Heute erinnert Deutschland an diese Zeit, zum Beispiel mit dem Denkmal für die ermordeten Juden Europas in Berlin und mit vielen Gedenkstätten. Viele Schulklassen besuchen sie. Das Grundgesetz von 1949 beginnt mit dem Satz: „Die Würde des Menschen ist unantastbar.“""",
        "body_en": """After 30 January 1933 the National Socialists, the Nazis, turned Germany into a dictatorship within a few months. They banned all other parties and the free trade unions. Newspapers and radio could only say what the Nazis wanted. Anyone who was against them went to prison or to a concentration camp.

Above all, the Nazis persecuted the Jews. From 1933 Jewish people lost their rights, their work and their property step by step. On the night of 9 to 10 November 1938 synagogues burned all over Germany, and Jewish shops were destroyed. Sinti and Roma, people with disabilities, homosexuals and political opponents were persecuted too.

On 1 September 1939 Germany attacked Poland. This was the beginning of the Second World War. The German army occupied large parts of Europe. In the whole war more than 60 million people died.

The Nazis murdered about six million European Jews. This genocide is called the Holocaust or the Shoah. Most of the victims died in ghettos and in extermination camps, for example in Auschwitz. Hundreds of thousands of Sinti and Roma were also murdered. There were also people who resisted, for example the students of the White Rose in Munich.

Many German cities were destroyed in the war. On 8 May 1945 Germany surrendered unconditionally. In Europe the war was over. The picture above shows the ruins of the Reichstag in Berlin in June 1945.

Today Germany remembers this time, for example with the Memorial to the Murdered Jews of Europe in Berlin and with many memorial sites. Many school classes visit them. The Basic Law of 1949 begins with the sentence: "Human dignity shall be inviolable." """,
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
        "order": 8,
        "era": "Geteiltes Deutschland",
        "title": "Teilung und die Berliner Mauer",
        "image": "mauer",
        "image_credit": f"Die Berliner Mauer, 20. November 1961. U.S. National Archives, {COMMONS}",
        "excerpt": "Nach dem Krieg gab es zwei deutsche Staaten. 1961 baute die DDR die Mauer.",
        "body_de": """Nach dem Krieg teilten die USA, Großbritannien, Frankreich und die Sowjetunion Deutschland in vier Zonen. Auch Berlin wurde in vier Sektoren geteilt.

Bald gab es Streit zwischen den Westmächten und der Sowjetunion. 1948 sperrte die Sowjetunion alle Wege nach West-Berlin. Fast ein Jahr lang brachten die Amerikaner und die Briten Essen und Kohle mit Flugzeugen in die Stadt. Das war die Luftbrücke.

1949 entstanden zwei deutsche Staaten. Im Westen die Bundesrepublik Deutschland mit der Hauptstadt Bonn. Sie war eine Demokratie und hatte das Grundgesetz. Im Osten die Deutsche Demokratische Republik, die DDR. Ihr Name klang demokratisch, aber sie war eine Diktatur der Partei SED. Ihre Hauptstadt war Ost-Berlin.

In der Bundesrepublik wuchs die Wirtschaft schnell. Man sprach vom Wirtschaftswunder. In der DDR gab es weniger Freiheit und weniger Waren. Bis 1961 gingen fast drei Millionen Menschen aus der DDR in den Westen, viele über Berlin.

Am 13. August 1961 begann die DDR, eine Mauer durch Berlin zu bauen. Am Ende war die Mauer etwa 155 Kilometer lang und ging rund um West-Berlin. Familien und Freunde waren plötzlich getrennt. Das Bild oben zeigt die Mauer im November 1961.

Wer über die Mauer fliehen wollte, war in großer Gefahr. Mindestens 140 Menschen starben an der Berliner Mauer. 1963 besuchte der amerikanische Präsident John F. Kennedy West-Berlin und sagte den berühmten Satz: „Ich bin ein Berliner.“

Fast 30 Jahre lang war die Mauer das Zeichen für ein geteiltes Deutschland und ein geteiltes Europa.""",
        "body_en": """After the war the USA, Great Britain, France and the Soviet Union divided Germany into four zones. Berlin, too, was divided into four sectors.

Soon there was conflict between the Western powers and the Soviet Union. In 1948 the Soviet Union blocked all routes into West Berlin. For almost a year the Americans and the British flew food and coal into the city. This was the Berlin Airlift.

In 1949 two German states were founded. In the west, the Federal Republic of Germany with its capital Bonn. It was a democracy and had the Basic Law. In the east, the German Democratic Republic, the GDR. Its name sounded democratic, but it was a dictatorship of the SED party. Its capital was East Berlin.

In the Federal Republic the economy grew fast. People spoke of the economic miracle. In the GDR there was less freedom and fewer goods. By 1961 almost three million people had left the GDR for the West, many of them through Berlin.

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
        "order": 9,
        "era": "Geteiltes Deutschland",
        "title": "Mauerfall und Wiedervereinigung",
        "image": "1989",
        "image_credit": f"Am Brandenburger Tor, Dezember 1989. SSGT F. Lee Corkran, U.S. Air Force, {COMMONS}",
        "excerpt": "1989 fiel die Mauer, und 1990 war Deutschland wieder ein Land.",
        "body_de": """In den 1980er-Jahren waren viele Menschen in der DDR unzufrieden. Sie durften nicht frei reisen, nicht frei sprechen und nicht frei wählen. 1989 änderte sich viel in Osteuropa. In Ungarn öffnete sich die Grenze nach Österreich, und Tausende Menschen aus der DDR flohen über Ungarn in den Westen.

Gleichzeitig gingen in der DDR immer mehr Menschen auf die Straße. Besonders bekannt sind die Montagsdemonstrationen in Leipzig. Am 9. Oktober 1989 demonstrierten dort etwa 70.000 Menschen friedlich. Sie riefen: „Wir sind das Volk!“ Die Regierung schickte keine Soldaten gegen sie.

Am Abend des 9. November 1989 sagte ein Politiker der DDR, Günter Schabowski, in einer Pressekonferenz: Die Menschen dürfen ab sofort reisen. Tausende Ost-Berliner gingen sofort zur Mauer. In der Nacht öffneten die Grenzsoldaten die Grenze. Menschen aus Ost und West feierten zusammen auf der Mauer. Das Bild oben zeigt das Brandenburger Tor im Dezember 1989.

Im März 1990 gab es in der DDR die erste freie Wahl. Im Juli 1990 bekam auch die DDR die D-Mark. Und am 3. Oktober 1990 war es so weit: Die DDR trat der Bundesrepublik bei. Deutschland war wieder ein Land. Seitdem ist der 3. Oktober der Tag der Deutschen Einheit, ein Feiertag.

Berlin wurde wieder die Hauptstadt. 1999 zogen das Parlament und die Regierung von Bonn nach Berlin.

Das Zusammenwachsen von Ost und West war nicht immer leicht. Viele Menschen im Osten verloren ihre Arbeit, und manche Unterschiede gibt es bis heute. Aber junge Menschen kennen die Mauer heute nur noch aus Büchern und Museen.""",
        "body_en": """In the 1980s many people in the GDR were unhappy. They were not allowed to travel freely, speak freely or vote freely. In 1989 a lot changed in Eastern Europe. In Hungary the border to Austria opened, and thousands of people from the GDR fled to the West through Hungary.

At the same time more and more people in the GDR took to the streets. The Monday demonstrations in Leipzig are especially well known. On 9 October 1989 about 70,000 people demonstrated there peacefully. They shouted: "We are the people!" The government did not send soldiers against them.

On the evening of 9 November 1989 a GDR politician, Günter Schabowski, said at a press conference that people could travel, starting immediately. Thousands of East Berliners went straight to the wall. That night the border guards opened the border. People from East and West celebrated together on the wall. The picture above shows the Brandenburg Gate in December 1989.

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
    {
        "order": 10,
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
]
