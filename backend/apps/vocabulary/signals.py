"""Vocabulary signals.

The old post_save signal that auto-created a WordProgress per Word was removed
in Phase 13.2: progress is now **per-user**, so a Word no longer maps to a
single progress row. WordProgress is created on demand the first time a signed-in
user reviews a word (see WordViewSet.review). Kept as a module so apps.ready()
import stays valid and future per-user signals have a home.
"""
