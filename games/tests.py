from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

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
    
    def test_game_creation(self):
        self.assertEqual(self.game.title, "Hades")
        self.assertEqual(self.game.developer, "Supergiant Games")
        self.assertEqual(self.game.rating, Decimal("9.2"))

    def test_game_str(self):
        self.assertEqual(str(self.game), "Hades")

    def test_game_timestamps(self):
        self.assertIsNotNone(self.game.created_at)
        self.assertIsNotNone(self.game.updated_at)

class HomeViewTests(TestCase):
    
    def test_home_page_status_code(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse("home"))

        self.assertTemplateUsed(response, "games/home.html")

    def test_home_page_content(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Welcome to GameHub")


class GameListViewTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

    def test_game_list_status_code(self):
        response = self.client.get(reverse("game_list"))

        self.assertEqual(response.status_code, 200)

    def test_game_list_template(self):
        response = self.client.get(reverse("game_list"))

        self.assertTemplateUsed(response, "games/game_list.html")

    def test_game_list_contains_game(self):
        response = self.client.get(reverse("game_list"))

        self.assertContains(response, "Hades")

    def test_game_list_pagination(self):

        Game.objects.create(
            title="Hollow Knight",
            description="A challenging action adventure.",
            release_date=date(2017, 2, 24),
            developer="Team Cherry",
            publisher="Team Cherry",
            rating=Decimal("9.1")
        )

        Game.objects.create(
            title="Celeste",
            description="A platforming adventure.",
            release_date=date(2018, 1, 25),
            developer="Maddy Makes Games",
            publisher="Maddy Makes Games",
            rating=Decimal("9.0")
        )

        response = self.client.get(reverse("game_list"))

        games = response.context["games"]

        self.assertEqual(games.paginator.num_pages, 2)
        self.assertEqual(len(games), 2)

    def test_game_list_second_page(self):

        Game.objects.create(
            title="Hollow Knight",
            description="A challenging action adventure.",
            release_date=date(2017, 2, 24),
            developer="Team Cherry",
            publisher="Team Cherry",
            rating=Decimal("9.1")
        )

        Game.objects.create(
            title="Celeste",
            description="A platforming adventure.",
            release_date=date(2018, 1, 25),
            developer="Maddy Makes Games",
            publisher="Maddy Makes Games",
            rating=Decimal("9.0")
        )

        response = self.client.get(
            reverse("game_list"),
            {"page": 2}
        )

        games = response.context["games"]

        self.assertEqual(games.number, 2)
        self.assertEqual(len(games), 1)


class GameDetailViewTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

    def test_game_detail_status_code(self):

        response = self.client.get(
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_game_detail_template(self):

        response = self.client.get(
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertTemplateUsed(response, "games/detail.html")

    def test_game_detail_content(self):

        response = self.client.get(
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertContains(response, "Hades")
        self.assertContains(response, "Supergiant Games")

    def test_game_detail_context(self):

        response = self.client.get(
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertEqual(response.context["game"], self.game)

    def test_game_detail_not_found(self):

        response = self.client.get(
            reverse("game_detail", args=[99999])
        )

        self.assertEqual(response.status_code, 404)


class GameURLTests(TestCase):

    def test_home_url(self):
        self.assertEqual(reverse("home"), "/")

    def test_game_list_url(self):
        self.assertEqual(reverse("game_list"), "/games/")

    def test_game_detail_url(self):
        self.assertEqual(
            reverse("game_detail", args=[1]),
            "/games/1/"
        )