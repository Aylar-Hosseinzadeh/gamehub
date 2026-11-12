from datetime import date
from decimal import Decimal

from django.test import TestCase

from .models import Game


class GameModelTests(TestCase):
    
    def setUp(self):
        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

    def test_game_str(self):
        self.assertEqual(str(self.game), "Hades")

    def test_game_timestamps(self):
        self.assertIsNotNone(self.game.created_at)
        self.assertIsNotNone(self.game.updated_at)