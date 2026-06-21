from django.db import migrations

LESSONS = [
    {
        "order": 1,
        "title": "Das Heilige Römische Reich",
        "era": "Mittelalter",
        "body_de": (
            "Das Heilige Römische Reich war ein großer Staatenbund in Mitteleuropa. "
            "Es entstand im Jahr 962, als Otto I. zum Kaiser gekrönt wurde. Das Reich "
            "bestand aus vielen kleinen Fürstentümern, Städten und Königreichen. Der "
            "Kaiser hatte oft weniger Macht als die einzelnen Fürsten. Das Reich "
            "existierte bis 1806, als Napoleon es auflöste."
        ),
        "body_en": (
            "The Holy Roman Empire was a large confederation of states in Central "
            "Europe. It began in 962, when Otto I was crowned emperor. The empire was "
            "made up of many small principalities, cities, and kingdoms. The emperor "
            "often had less power than the individual princes. It lasted until 1806, "
            "when Napoleon dissolved it."
        ),
        "quiz": [
            {"prompt": "Wann wurde Otto I. zum Kaiser gekrönt?",
             "options": ["962", "1806", "1517", "1871"], "answer": "962"},
            {"prompt": "Wer löste das Reich 1806 auf?",
             "options": ["Napoleon", "Luther", "Bismarck", "Otto I."], "answer": "Napoleon"},
            {"prompt": "Woraus bestand das Reich?",
             "options": ["aus vielen kleinen Fürstentümern und Städten", "aus nur einer Stadt",
                         "aus zwei Königreichen", "aus einer Republik"],
             "answer": "aus vielen kleinen Fürstentümern und Städten"},
        ],
    },
    {
        "order": 2,
        "title": "Die Reformation",
        "era": "Frühe Neuzeit",
        "body_de": (
            "Im Jahr 1517 veröffentlichte Martin Luther seine 95 Thesen. Er "
            "kritisierte die katholische Kirche, besonders den Verkauf von Ablässen. "
            "Durch den Buchdruck verbreiteten sich seine Ideen sehr schnell. So "
            "entstand die evangelische (protestantische) Kirche. Die Reformation "
            "veränderte Religion, Politik und Sprache in Deutschland tief."
        ),
        "body_en": (
            "In 1517 Martin Luther published his 95 Theses. He criticized the "
            "Catholic Church, especially the sale of indulgences. Thanks to the "
            "printing press, his ideas spread very quickly. This gave rise to the "
            "Protestant church. The Reformation deeply changed religion, politics, "
            "and the language in Germany."
        ),
        "quiz": [
            {"prompt": "Was veröffentlichte Luther 1517?",
             "options": ["seine 95 Thesen", "ein Wörterbuch", "die Verfassung", "eine Landkarte"],
             "answer": "seine 95 Thesen"},
            {"prompt": "Welche Technik half, Luthers Ideen zu verbreiten?",
             "options": ["der Buchdruck", "das Radio", "das Internet", "das Telefon"],
             "answer": "der Buchdruck"},
            {"prompt": "Welche Kirche entstand?",
             "options": ["die evangelische (protestantische) Kirche", "die orthodoxe Kirche",
                         "keine neue Kirche", "eine neue Stadt"],
             "answer": "die evangelische (protestantische) Kirche"},
        ],
    },
    {
        "order": 3,
        "title": "Die deutsche Einigung 1871",
        "era": "19. Jahrhundert",
        "body_de": (
            "Lange Zeit war Deutschland in viele Staaten geteilt. Otto von Bismarck, "
            "der Ministerpräsident von Preußen, wollte sie vereinen. Nach drei Kriegen "
            "wurde 1871 das Deutsche Kaiserreich gegründet. Wilhelm I. wurde Kaiser, "
            "und Bismarck wurde Reichskanzler. Zum ersten Mal gab es einen deutschen "
            "Nationalstaat."
        ),
        "body_en": (
            "For a long time Germany was divided into many states. Otto von Bismarck, "
            "the prime minister of Prussia, wanted to unite them. After three wars, the "
            "German Empire was founded in 1871. Wilhelm I became emperor, and Bismarck "
            "became chancellor. For the first time there was a German nation-state."
        ),
        "quiz": [
            {"prompt": "Wer wollte die deutschen Staaten vereinen?",
             "options": ["Otto von Bismarck", "Martin Luther", "Napoleon", "Otto I."],
             "answer": "Otto von Bismarck"},
            {"prompt": "Wann wurde das Deutsche Kaiserreich gegründet?",
             "options": ["1871", "1517", "962", "1990"], "answer": "1871"},
            {"prompt": "Welches Amt hatte Bismarck?",
             "options": ["Reichskanzler", "Kaiser", "Papst", "König von Bayern"],
             "answer": "Reichskanzler"},
        ],
    },
    {
        "order": 4,
        "title": "Die Weimarer Republik",
        "era": "20. Jahrhundert",
        "body_de": (
            "Nach dem Ersten Weltkrieg wurde 1919 die Weimarer Republik gegründet. Sie "
            "war die erste Demokratie in Deutschland. Die Republik hatte viele "
            "Probleme: eine hohe Inflation und später die Weltwirtschaftskrise. Diese "
            "Krisen schwächten die Demokratie stark. 1933 endete die Republik, als die "
            "Nationalsozialisten an die Macht kamen."
        ),
        "body_en": (
            "After the First World War, the Weimar Republic was founded in 1919. It was "
            "the first democracy in Germany. The republic faced many problems: high "
            "inflation and later the Great Depression. These crises severely weakened "
            "the democracy. It ended in 1933, when the National Socialists came to power."
        ),
        "quiz": [
            {"prompt": "Was war die Weimarer Republik?",
             "options": ["die erste Demokratie in Deutschland", "ein Königreich",
                         "eine Stadt", "eine Kirche"],
             "answer": "die erste Demokratie in Deutschland"},
            {"prompt": "Wann wurde sie gegründet?",
             "options": ["1919", "1871", "1949", "1990"], "answer": "1919"},
            {"prompt": "Welches Problem hatte die Republik?",
             "options": ["eine hohe Inflation", "zu viele Kaiser", "keinen Buchdruck",
                         "keine Hauptstadt"],
             "answer": "eine hohe Inflation"},
        ],
    },
    {
        "order": 5,
        "title": "Teilung und die Berliner Mauer",
        "era": "Nachkriegszeit",
        "body_de": (
            "Nach dem Zweiten Weltkrieg wurde Deutschland 1949 in zwei Staaten "
            "geteilt: die BRD im Westen und die DDR im Osten. Berlin wurde ebenfalls "
            "geteilt. 1961 baute die DDR die Berliner Mauer, um die Flucht in den "
            "Westen zu stoppen. Die Mauer wurde zum Symbol des Kalten Krieges. "
            "Familien und Freunde waren jahrzehntelang getrennt."
        ),
        "body_en": (
            "After the Second World War, Germany was divided into two states in 1949: "
            "West Germany (BRD) and East Germany (DDR). Berlin was divided too. In 1961 "
            "East Germany built the Berlin Wall to stop people fleeing to the West. The "
            "wall became a symbol of the Cold War. Families and friends were separated "
            "for decades."
        ),
        "quiz": [
            {"prompt": "In wie viele Staaten wurde Deutschland 1949 geteilt?",
             "options": ["zwei", "drei", "vier", "fünf"], "answer": "zwei"},
            {"prompt": "Wann wurde die Berliner Mauer gebaut?",
             "options": ["1961", "1949", "1871", "1990"], "answer": "1961"},
            {"prompt": "Wofür wurde die Mauer ein Symbol?",
             "options": ["des Kalten Krieges", "der Reformation", "des Buchdrucks",
                         "des Kaiserreichs"],
             "answer": "des Kalten Krieges"},
        ],
    },
    {
        "order": 6,
        "title": "Die Wiedervereinigung 1990",
        "era": "Gegenwart",
        "body_de": (
            "Im November 1989 fiel die Berliner Mauer. Viele Menschen in der DDR "
            "hatten friedlich protestiert. Am 3. Oktober 1990 wurden die BRD und die "
            "DDR wieder ein Land. Dieser Tag heißt heute „Tag der Deutschen Einheit“ "
            "und ist ein Feiertag. Die Wiedervereinigung war ein historischer Moment "
            "für Europa."
        ),
        "body_en": (
            "In November 1989 the Berlin Wall fell. Many people in East Germany had "
            "protested peacefully. On 3 October 1990, West and East Germany became one "
            "country again. Today that day is called the 'Day of German Unity' and is a "
            "public holiday. Reunification was a historic moment for Europe."
        ),
        "quiz": [
            {"prompt": "Wann fiel die Berliner Mauer?",
             "options": ["1989", "1961", "1949", "1871"], "answer": "1989"},
            {"prompt": "Wann wurde Deutschland wiedervereinigt?",
             "options": ["am 3. Oktober 1990", "1989", "1949", "2000"],
             "answer": "am 3. Oktober 1990"},
            {"prompt": "Wie heißt der Feiertag?",
             "options": ["Tag der Deutschen Einheit", "Tag der Reformation",
                         "Tag der Mauer", "Tag des Kaisers"],
             "answer": "Tag der Deutschen Einheit"},
        ],
    },
]


def seed(apps, schema_editor):
    HistoryLesson = apps.get_model("history", "HistoryLesson")
    for lesson in LESSONS:
        HistoryLesson.objects.update_or_create(
            order=lesson["order"],
            defaults={
                "title": lesson["title"],
                "era": lesson["era"],
                "body_de": lesson["body_de"],
                "body_en": lesson["body_en"],
                "quiz": lesson["quiz"],
            },
        )


def unseed(apps, schema_editor):
    HistoryLesson = apps.get_model("history", "HistoryLesson")
    HistoryLesson.objects.filter(order__in=[lesson["order"] for lesson in LESSONS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("history", "0001_initial"),
    ]

    operations = [migrations.RunPython(seed, unseed)]
