"""The core grammar list on the Grammar page."""

from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .models import GrammarRule
from .serializers import CORE_TOPICS, GrammarRuleSerializer


class CoreTopicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_path", stdout=StringIO())

    def test_every_core_topic_exists_on_its_level(self):
        for level, titles in CORE_TOPICS.items():
            have = set(
                GrammarRule.objects.filter(chapter__cefr_level=level).values_list(
                    "title", flat=True
                )
            )
            self.assertEqual(sorted(set(titles) - have), [], level)  # a renamed topic?

    def test_serializer_marks_core(self):
        core = GrammarRule.objects.get(title="Akkusativ")
        small = GrammarRule.objects.get(title="Das Wetter")
        self.assertTrue(GrammarRuleSerializer(core).data["core"])
        self.assertFalse(GrammarRuleSerializer(small).data["core"])
