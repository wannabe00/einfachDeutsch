"""The curated watch and listen suggestions, loaded by `manage.py seed_videos`.

Each pick says what it is, who it's for, its format and cost, and how to use it
for learning. YouTube picks show the thumbnail of one real video from the
channel (`i.ytimg.com`, allowed by the CSP in frontend/vercel.json); the rest
get the drawn platform tile.
"""


def thumb(video_id: str) -> str:
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


NICOS_WEG = "https://learngerman.dw.com/en/nicos-weg/c-36519789"

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
        "cefr_level": "C1",
        "description": "ZDF's satirical news show: the week's politics with jokes, "
        "wordplay and parody.",
        "audience": "C1; you need to know the news to get the jokes.",
        "format": "About 30 minutes, every Friday.",
        "cost": "Free",
        "tips": ["Read the week's headlines first, then watch."],
    },
]
