"""The curated watch and listen suggestions, loaded by `manage.py seed_videos`.

Each pick says what it is, who it's for, its format and cost, and how to use it
for learning. YouTube picks show the thumbnail of one real video from the
channel (`i.ytimg.com`, allowed by the CSP in frontend/vercel.json); the rest
get the drawn platform tile. Other sites use the share image they publish for
link previews (their hosts are allowed in the same CSP); sites without a
usable one get the drawn platform tile.
"""


def thumb(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


NICOS_WEG = "https://learngerman.dw.com/en/nicos-weg/c-36519789"
NICOS_WEG_IMAGE = "https://static.dw.com/image/62607222_401.png"

VIDEOS = [
    # ---- A1 ----
    {
        "title": "DW Learn German",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@dwlearngerman",
        "cefr_level": "A1",
        "image_url": thumb("K61dtTLGKFU"),
        "description": "Deutsche Welle's channel for learners: grammar explained in "
        "English, short news in easy German (Kurz und leicht) and the Nicos Weg series.",
        "audience": "Complete beginners up to B1.",
        "format": "Short videos, 3-15 minutes, new ones most weekdays.",
        "cost": "Free",
        "tips": [
            "Watch a Kurz und leicht news clip with German subtitles, then again without.",
            "Pause after each sentence and say it out loud.",
            "Pick the grammar video that matches the Lektion you're on.",
        ],
    },
    {
        "title": "Easy German",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@EasyGerman",
        "cefr_level": "A1",
        "image_url": thumb("RbtIMGCizu0"),
        "description": "Street interviews and everyday topics in real spoken German, "
        "with German and English subtitles on screen.",
        "audience": "A1 and up. Start with the Super Easy German episodes.",
        "format": "Episodes of 10-20 minutes, new ones every week.",
        "cost": "Free",
        "tips": [
            "Read both subtitle lines first, then cover the English and watch again.",
            "Write down three phrases per episode and add them to your Word Bank.",
            "Copy the speakers' answers to the interview question out loud.",
        ],
    },
    {
        "title": "Nico's Weg A1",
        "platform": "DW",
        "url": NICOS_WEG,
        "image_url": NICOS_WEG_IMAGE,
        "cefr_level": "A1",
        "description": "A story-based course from Deutsche Welle: follow Nico, who has "
        "just arrived in Germany, through many short episodes with exercises.",
        "audience": "Beginners working through A1.",
        "format": "Episodes of a few minutes, each with exercises, in the browser or the DW app.",
        "cost": "Free",
        "tips": [
            "Do one episode a day, like a small lesson.",
            "Do the exercises straight after each episode.",
            "Repeat the dialogues out loud, playing one of the roles.",
        ],
    },
    # ---- A2 ----
    {
        "title": "Dinge Erklärt - Kurzgesagt",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@KurzgesagtDE",
        "cefr_level": "A2",
        "image_url": thumb("5_jcvQ0-vhI"),
        "description": "The German channel of Kurzgesagt: animated videos about space, "
        "biology, technology and society, run by funk (ARD and ZDF).",
        "audience": "Late A2 with patience; comfortable from B1.",
        "format": "Animated videos of 8-15 minutes, a new one about every two weeks.",
        "cost": "Free",
        "tips": [
            "Watch the English version on the main Kurzgesagt channel first, then the German.",
            "Turn on German subtitles and slow the video down to 0.75x.",
            "Pause on the pictures and name what you see in German.",
        ],
    },
    {
        "title": "logo! Kindernachrichten",
        "platform": "ZDF",
        "url": "https://www.zdf.de/kinder/logo",
        "image_url": "https://www.logo.de/assets/logo-sendungsteaser-2024-100~768x432?cb=1746516502175",
        "cefr_level": "A2",
        "description": "ZDF's daily news for children: today's stories in slow, clear "
        "German, with the background explained simply.",
        "audience": "A2 learners who want real news without hard vocabulary.",
        "format": "About 10 minutes, every day, in the ZDF Mediathek.",
        "cost": "Free",
        "tips": [
            "Watch one episode a day at the same time.",
            "Note three new words per episode.",
            "Retell one story in three sentences of your own.",
        ],
    },
    {
        "title": "Nico's Weg A2",
        "platform": "DW",
        "url": NICOS_WEG,
        "image_url": NICOS_WEG_IMAGE,
        "cefr_level": "A2",
        "description": "The A2 part of Nico's story: work, flat hunting and friendships, "
        "with exercises after every episode.",
        "audience": "Learners working through A2.",
        "format": "Episodes of a few minutes with exercises.",
        "cost": "Free",
        "tips": [
            "Watch first without subtitles and guess what happens.",
            "Then watch with subtitles and check.",
            "Write a short summary of the episode.",
        ],
    },
    # ---- B1 ----
    {
        "title": "Deutschland-Labor",
        "platform": "DW",
        "url": "https://learngerman.dw.com",
        "cefr_level": "B1",
        "description": "Short DW videos about everyday life in Germany: food, work, "
        "traditions and clichés, each with a transcript and exercises.",
        "audience": "A2-B1 learners who want to understand German culture.",
        "format": "Short videos with transcripts and exercises.",
        "cost": "Free",
        "tips": [
            "Read the transcript after watching and mark words you didn't catch.",
            "Compare the topic with your own country in a few sentences.",
        ],
    },
    {
        "title": "Easy German Podcast",
        "platform": "Podcast",
        "url": "https://www.easygerman.fm",
        "cefr_level": "B1",
        "description": "Manuel and Cari talk about life in Germany, the language and "
        "listeners' questions in natural, everyday German.",
        "audience": "B1 and up.",
        "format": "Audio episodes of 30-60 minutes, every week.",
        "cost": "Free to listen; transcripts come with a paid membership.",
        "tips": [
            "Listen while walking or commuting, without stopping.",
            "Pick one ten-minute stretch and listen to it three times.",
        ],
    },
    {
        "title": "Nico's Weg B1",
        "platform": "DW",
        "url": NICOS_WEG,
        "image_url": NICOS_WEG_IMAGE,
        "cefr_level": "B1",
        "description": "The B1 part of Nico's story, with longer dialogues and more "
        "everyday situations.",
        "audience": "Learners working through B1.",
        "format": "Episodes of a few minutes with exercises.",
        "cost": "Free",
        "tips": ["Shadow a dialogue: speak along with the actors, a moment behind them."],
    },
    # ---- B2 ----
    {
        "title": "Dark",
        "platform": "Netflix",
        "url": "https://www.netflix.com/title/80100172",
        "cefr_level": "B2",
        "description": "A German mystery series about four families in a small town and "
        "a time-travel puzzle that spans generations.",
        "audience": "B2 and up; the plot is demanding even for native speakers.",
        "format": "3 seasons, episodes of about 50-60 minutes.",
        "cost": "Netflix subscription",
        "tips": [
            "Use German audio with German subtitles.",
            "Keep a small map of who is who.",
            "Rewatch key scenes once you know what happens.",
        ],
    },
    {
        "title": "Tagesschau",
        "platform": "ARD",
        "url": "https://www.tagesschau.de",
        "image_url": "https://images.tagesschau.de/image/89045d82-5cd5-46ad-8f91-73911add30ee/AAABlpITK5s/AAABnSSvrFg/16x9-big/tagesschau-logo-100.jpg?width=640",
        "cefr_level": "B2",
        "description": "Germany's main evening news: clear standard German and the "
        "day's important stories.",
        "audience": "B2 and up; start with the 100-second version.",
        "format": "15 minutes daily at 20:00, plus tagesschau in 100 Sekunden.",
        "cost": "Free",
        "tips": [
            "Start with tagesschau in 100 Sekunden every day.",
            "Read the matching article on tagesschau.de afterwards.",
            "Summarise one story out loud in a minute.",
        ],
    },
    {
        "title": "Y-Kollektiv",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@ykollektiv",
        "cefr_level": "B2",
        "image_url": thumb("kdM8hfA3404"),
        "description": "Young reporters from funk try things out and meet people for "
        "personal documentaries about life in Germany.",
        "audience": "B2 and up; lots of young, spoken German.",
        "format": "Documentaries of 15-30 minutes.",
        "cost": "Free",
        "tips": ["Note the colloquial phrases people use and look them up afterwards."],
    },
    # ---- C1 ----
    {
        "title": "Tatort",
        "platform": "ARD",
        "url": "https://www.ardmediathek.de/tatort",
        "image_url": "https://www.ardmediathek.de/img?imwidth=640&url=https%3A%2F%2Fapi.ardmediathek.de%2Fimage-service%2Fimages%2Furn%3Aard%3Aimage%3A2cc19573ff22f5f0%3Fch%3Deb6d25ba442552cf%26w%3D%7Bwidth%7D",
        "cefr_level": "C1",
        "description": "Germany's longest-running crime series: each film is set in a "
        "different city, with its own detectives and regional accents.",
        "audience": "C1; fast dialogue and a lot of dialect.",
        "format": "90-minute films, Sundays at 20:15, many in the ARD Mediathek.",
        "cost": "Free",
        "tips": [
            "Choose a city whose accent you want to get used to.",
            "Watch with German subtitles the first time.",
        ],
    },
    {
        "title": "heute-show",
        "platform": "ZDF",
        "url": "https://www.zdf.de/comedy/heute-show",
        "image_url": "https://www.zdf.de/assets/sendungsteaser-heute-show-100~768x432?cb=1783088176368",
        "cefr_level": "C1",
        "description": "ZDF's satirical news show: the week's politics with jokes, "
        "wordplay and parody.",
        "audience": "C1; you need to know the news to get the jokes.",
        "format": "About 30 minutes, every Friday.",
        "cost": "Free",
        "tips": ["Read the week's headlines first, then watch."],
    },
    # ---- more picks (2026-10-13) ----
    {
        "title": "Deutsch für Euch",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@DeutschFuerEuch",
        "cefr_level": "A1",
        "image_url": thumb("JnG4HTTHV8w"),
        "description": "Grammar explained clearly in English by a German teacher: "
        "cases, word order, verbs with prepositions and much more.",
        "audience": "A1 to B2 learners who want the rules explained properly.",
        "format": "Lessons of 10-30 minutes, organised in playlists by topic.",
        "cost": "Free",
        "tips": [
            "Watch the video for the grammar topic of the Lektion you're on.",
            "Write the example sentences into your own notes.",
        ],
    },
    {
        "title": "lingoni GERMAN",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@lingonigerman",
        "cefr_level": "A1",
        "image_url": thumb("-Q9PypJ33L4"),
        "description": "Short lessons sorted by level, from A1 grammar to everyday "
        "phrases, plus interviews with people in German-speaking countries.",
        "audience": "A1 to B1.",
        "format": "Short videos of 5-15 minutes, sorted into A1, A2 and B1 playlists.",
        "cost": "Free",
        "tips": ["Follow the A1 playlist in order, one video a day."],
    },
    {
        "title": "Learn German with Anja",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@LearnGermanwithAnja",
        "cefr_level": "A1",
        "image_url": thumb("VcxhtNKGsqg"),
        "description": "Cheerful lessons on vocabulary, grammar and everyday situations, "
        "with quizzes and short exercises.",
        "audience": "Beginners and A2 learners.",
        "format": "Videos of 5-20 minutes, plus short quizzes.",
        "cost": "Free",
        "tips": ["Pause the quizzes and answer out loud before the solution appears."],
    },
    {
        "title": "YourGermanTeacher",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@YourGermanTeacher",
        "cefr_level": "A1",
        "image_url": thumb("DhuCVn3KLFE"),
        "description": "Clear lessons on the mistakes learners make most: word order, "
        "verbs, and words that are easy to mix up, marked by level.",
        "audience": "A1 to B1.",
        "format": "Videos of 10-20 minutes, labelled with their level.",
        "cost": "Free",
        "tips": ["Write down the mistakes you recognise from your own German."],
    },
    {
        "title": "Coffee Break German",
        "platform": "Podcast",
        "url": "https://coffeebreaklanguages.com/coffeebreakgerman/",
        "cefr_level": "A1",
        "description": "A podcast course: a teacher and a learner go through German step "
        "by step, explaining everything in English.",
        "audience": "Complete beginners.",
        "format": "Audio lessons of about 20 minutes, in seasons.",
        "cost": "Free to listen; extra materials are paid.",
        "tips": ["Answer the learner's questions out loud before she does."],
    },
    {
        "title": "DW Deutschtrainer",
        "platform": "DW",
        "url": "https://learngerman.dw.com/en/deutschtrainer/c-56705009",
        "cefr_level": "A1",
        "description": "Short vocabulary units from Deutsche Welle for everyday topics, "
        "with audio and exercises.",
        "audience": "A1 and A2.",
        "format": "Short units with audio and exercises, in the browser or the DW app.",
        "cost": "Free",
        "tips": ["Do the unit that matches the topic of your current Lektion."],
    },
    {
        "title": "Die Sendung mit der Maus",
        "platform": "WDR",
        "url": "https://www.wdrmaus.de",
        "cefr_level": "A2",
        "image_url": "https://www.wdrmaus.de/_teaserbilder/671254_512.jpg",
        "description": "Germany's classic children's show: how things are made and why "
        "the world works the way it does, explained very clearly.",
        "audience": "A2; children's German, but real topics.",
        "format": "Short stories of a few minutes inside a 30-minute show.",
        "cost": "Free",
        "tips": ["Watch one Sachgeschichte and explain it again in three sentences."],
    },
    {
        "title": "Slow German",
        "platform": "Podcast",
        "url": "https://slowgerman.com",
        "cefr_level": "A2",
        "image_url": "https://slowgerman.com/wp-content/uploads/2014/10/3.jpg",
        "description": "Annik Rubens talks slowly and clearly about life and culture in "
        "Germany; transcripts are on the website.",
        "audience": "A2 to B1.",
        "format": "Audio episodes of about 10 minutes.",
        "cost": "Free to listen; some extras are paid.",
        "tips": ["Read the transcript while you listen the first time."],
    },
    {
        "title": "Langsam gesprochene Nachrichten",
        "platform": "DW",
        "url": "https://learngerman.dw.com/de/langsam-gesprochene-nachrichten/s-60040332",
        "cefr_level": "B1",
        "description": "DW's daily world news, read slowly and clearly, with the text "
        "to read along.",
        "audience": "B1 and B2.",
        "format": "About 7 minutes, Monday to Friday.",
        "cost": "Free",
        "tips": [
            "Listen first, then read the text and mark what you missed.",
            "Listen once more without the text.",
        ],
    },
    {
        "title": "Terra X History",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@TerraXHistory",
        "cefr_level": "B1",
        "image_url": thumb("mnZm9R9rGdw"),
        "description": "ZDF's history documentaries: archaeology, the Middle Ages and "
        "German history, with pictures that help you follow.",
        "audience": "B1 and up; fits well with the History lessons here.",
        "format": "Documentaries of 10-45 minutes.",
        "cost": "Free",
        "tips": ["Pick a topic you've read about in History here, then watch."],
    },
    {
        "title": "MrWissen2go",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@MrWissen2go",
        "cefr_level": "B2",
        "image_url": thumb("uN1Zx-Ia-SE"),
        "description": "Politics, history and current events explained quickly by "
        "journalist Mirko Drotschmann (funk).",
        "audience": "B2; fast and full of new words.",
        "format": "Videos of 10-20 minutes.",
        "cost": "Free",
        "tips": ["Note the key terms and look them up after watching."],
    },
    {
        "title": "How to Sell Drugs Online (Fast)",
        "platform": "Netflix",
        "url": "https://www.netflix.com/title/80218448",
        "cefr_level": "B2",
        "description": "A German comedy series about a teenager who starts an online "
        "business from his bedroom; lots of young, everyday German.",
        "audience": "B2; rated 16+.",
        "format": "Several seasons of 30-minute episodes.",
        "cost": "Netflix subscription",
        "tips": ["Use German audio and German subtitles."],
    },
    {
        "title": "MAITHINK X",
        "platform": "YouTube",
        "url": "https://www.youtube.com/@maithinkx",
        "cefr_level": "C1",
        "image_url": thumb("7ubXCVtRk4Y"),
        "description": "Science journalist Mai Thi Nguyen-Kim checks facts and explains "
        "science and health topics (formerly maiLab).",
        "audience": "C1; fast, precise language.",
        "format": "Episodes of 15-30 minutes.",
        "cost": "Free",
        "tips": ["Summarise her argument in your own words afterwards."],
    },
    {
        "title": "Babylon Berlin",
        "platform": "ARD",
        "url": "https://www.daserste.de/unterhaltung/serie/babylon-berlin/index.html",
        "cefr_level": "C1",
        "description": "A crime drama set in Berlin in 1929, the Weimar Republic seen "
        "through a police investigation; five seasons.",
        "audience": "C1; period language and Berlin dialect.",
        "format": "Five seasons of episodes of about 45 minutes, in the ARD Mediathek.",
        "cost": "Free",
        "tips": ["Read the Weimar Republic lesson in History first."],
    },
    {
        "title": "Lage der Nation",
        "platform": "Podcast",
        "url": "https://lagedernation.org",
        "cefr_level": "C1",
        "description": "A weekly politics podcast from Berlin: two hosts discuss the "
        "week's news in Germany in depth.",
        "audience": "C1.",
        "format": "Audio episodes of 60-90 minutes, weekly.",
        "cost": "Free; extras with a paid subscription.",
        "tips": ["Listen to one segment at a time rather than a whole episode."],
    },
]
