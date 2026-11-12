from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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

class AuthenticationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="aylar",
            password="testpassword123"
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "aylar",
                "password": "testpassword123",
            }
        )

        self.assertRedirects(
            response,
            reverse("game_list")
        )

        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "aylar",
                "password": "wrongpassword",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_logout_with_post(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(
            response,
            reverse("game_list")
        )

        self.assertFalse(
            response.wsgi_request.user.is_authenticated
        )

    def test_logout_rejects_get(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

class LibraryAuthorizationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="aylar",
            password="testpassword123"
        )

        self.other_user = User.objects.create_user(
            username="other_user",
            password="testpassword123"
        )

        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

    def test_guest_cannot_add_game_to_library(self):
        response = self.client.post(
            reverse("add_to_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            self.game.users.filter(pk=self.user.pk).exists()
        )

    def test_guest_cannot_remove_game_from_library(self):
        response = self.client.post(
            reverse("remove_from_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_add_game_to_library(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("add_to_library", args=[self.game.pk])
        )

        self.assertRedirects(
            response,
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertTrue(
            self.game.users.filter(pk=self.user.pk).exists()
        )

    def test_authenticated_user_can_remove_game_from_library(self):
        self.game.users.add(self.user)

        self.client.force_login(self.user)

        response = self.client.post(
            reverse("remove_from_library", args=[self.game.pk])
        )

        self.assertRedirects(
            response,
            reverse("game_detail", args=[self.game.pk])
        )

        self.assertFalse(
            self.game.users.filter(pk=self.user.pk).exists()
        )

    def test_user_cannot_remove_game_from_another_users_library(self):
        self.game.users.add(self.other_user)

        self.client.force_login(self.user)

        self.client.post(
            reverse("remove_from_library", args=[self.game.pk])
        )

        self.assertTrue(
            self.game.users.filter(pk=self.other_user.pk).exists()
        )

    def test_add_to_library_rejects_get(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("add_to_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 405)

    def test_remove_from_library_rejects_get(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("remove_from_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 405)

class AddGameAuthorizationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="normal_user",
            password="testpassword123"
        )

        self.staff_user = User.objects.create_user(
            username="staff_user",
            password="testpassword123",
            is_staff=True
        )

        self.game_data = {
            "title": "Hollow Knight",
            "description": "A challenging action adventure.",
            "release_date": "2017-02-24",
            "developer": "Team Cherry",
            "publisher": "Team Cherry",
            "rating": "9.1",
        }

    def test_guest_cannot_access_add_game(self):
        response = self.client.get(
            reverse("game_add")
        )

        self.assertEqual(response.status_code, 302)

    def test_normal_user_cannot_access_add_game(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("game_add")
        )

        self.assertEqual(response.status_code, 302)

    def test_staff_user_can_access_add_game(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("game_add")
        )

        self.assertEqual(response.status_code, 200)

    def test_staff_user_can_create_game(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("game_add"),
            self.game_data
        )

        self.assertRedirects(
            response,
            reverse("game_list")
        )

        self.assertTrue(
            Game.objects.filter(title="Hollow Knight").exists()
        )

    def test_normal_user_cannot_create_game(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("game_add"),
            self.game_data
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Game.objects.filter(title="Hollow Knight").exists()
        )