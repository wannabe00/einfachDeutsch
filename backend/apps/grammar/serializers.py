from rest_framework import serializers

from .models import GrammarRule

# The grammar pillars per level, shown together first on the Grammar page; the
# smaller topics stay grouped by kind. Matched by title (tests check they exist).
CORE_TOPICS = {
    "A1": [
        "heißen, kommen, sein",
        "Verben im Präsens",
        "W-Fragen",
        "Ja/Nein-Fragen",
        "Negation mit nicht",
        "der, das, die",
        "ein, eine",
        "kein, keine",
        "Plural",
        "Akkusativ",
        "Das Verb an Position 2",
        "können",
        "möchten",
        "Trennbare Verben",
        "Perfekt mit haben",
        "Perfekt mit sein",
        "Dativ: dem, der, den",
        "Imperativ mit du",
        "Komparativ",
    ],
    "A2": [
        "Präteritum: war und hatte",
        "Wechselpräpositionen: Wo? und Wohin?",
        "Adjektive nach der, die, das",
        "Adjektive nach ein, kein, mein",
        "Adjektive ohne Artikel",
        "Ratschläge: Du solltest ...",
        "Gut, dass ...: dass-Sätze",
        "weil: Gründe nennen",
        "Reflexive Verben: sich freuen, sich treffen",
        "Indirekte Fragen mit ob",
        "wenn: Bedingungen und Gewohnheiten",
        "als: einmal in der Vergangenheit",
        "Passiv Präsens: werden + Partizip",
        "Verben mit Präpositionen",
        "Präteritum: Modalverben",
        "Relativsätze im Nominativ",
        "Präteritum: regelmäßige und unregelmäßige Verben",
    ],
}


class GrammarRuleSerializer(serializers.ModelSerializer):
    # Grammar is grouped Level → topic. The level comes from the
    # rule's chapter (a chapter is one Lektion).
    cefr_level = serializers.CharField(source="chapter.cefr_level", read_only=True)
    core = serializers.SerializerMethodField()

    def get_core(self, rule) -> bool:
        return rule.title in CORE_TOPICS.get(rule.chapter.cefr_level, ())

    class Meta:
        model = GrammarRule
        fields = [
            "id",
            "chapter",
            "title",
            "category",
            "content",
            "example_sentences",
            "created_at",
            "cefr_level",
            "core",
        ]
