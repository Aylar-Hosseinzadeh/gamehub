from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .forms import GameForm
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

class CSRFSecurityTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="csrf_user",
            password="testpassword123"
        )

        self.staff_user = User.objects.create_user(
            username="csrf_staff",
            password="testpassword123",
            is_staff=True
        )

        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

        self.csrf_client = Client(enforce_csrf_checks=True)

    def test_login_rejects_post_without_csrf_token(self):

        response = self.csrf_client.post(
            reverse("login"),
            {
                "username": "csrf_user",
                "password": "testpassword123",
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_logout_rejects_post_without_csrf_token(self):

        self.csrf_client.force_login(self.user)

        response = self.csrf_client.post(
            reverse("logout")
        )

        self.assertEqual(response.status_code, 403)

    def test_add_to_library_rejects_post_without_csrf_token(self):

        self.csrf_client.force_login(self.user)

        response = self.csrf_client.post(
            reverse("add_to_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_remove_from_library_rejects_post_without_csrf_token(self):

        self.game.users.add(self.user)

        self.csrf_client.force_login(self.user)

        response = self.csrf_client.post(
            reverse("remove_from_library", args=[self.game.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_add_game_rejects_post_without_csrf_token(self):

        self.csrf_client.force_login(self.staff_user)

        response = self.csrf_client.post(
            reverse("game_add"),
            {
                "title": "Hollow Knight",
                "description": "A challenging action adventure.",
                "release_date": "2017-02-24",
                "developer": "Team Cherry",
                "publisher": "Team Cherry",
                "rating": "9.1",
            }
        )

        self.assertEqual(response.status_code, 403)

    def test_valid_csrf_token_allows_library_operation(self):

        self.csrf_client.force_login(self.user)

        detail_url = reverse(
            "game_detail",
            args=[self.game.pk]
        )

        response = self.csrf_client.get(detail_url)

        csrf_token = response.cookies["csrftoken"].value

        response = self.csrf_client.post(
            reverse("add_to_library", args=[self.game.pk]),
            HTTP_X_CSRFTOKEN=csrf_token
        )

        self.assertRedirects(
            response,
            detail_url
        )

        self.assertTrue(
            self.game.users.filter(pk=self.user.pk).exists()
        )

class GameInputValidationTests(TestCase):
    
    def setUp(self):
        self.game = Game.objects.create(
            title="Hades",
            description="A rogue-like dungeon crawler.",
            release_date=date(2020, 9, 17),
            developer="Supergiant Games",
            publisher="Supergiant Games",
            rating=Decimal("9.2")
        )

        self.second_game = Game.objects.create(
            title="Celeste",
            description="A platforming adventure.",
            release_date=date(2018, 1, 25),
            developer="Maddy Makes Games",
            publisher="Maddy Makes Games",
            rating=Decimal("8.5")
        )

    def test_valid_rating_filter(self):

        response = self.client.get(
            reverse("game_list"),
            {"rating": "9.0"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["games"].paginator.count,
            1
        )

    def test_invalid_rating_filter_does_not_crash(self):

        response = self.client.get(
            reverse("game_list"),
            {"rating": "abc"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["games"].paginator.count,
            2
        )

    def test_rating_filter_rejects_out_of_range_values(self):

        for rating in ["-1", "11"]:
            with self.subTest(rating=rating):

                response = self.client.get(
                    reverse("game_list"),
                    {"rating": rating}
                )

                self.assertEqual(response.status_code, 200)

                self.assertEqual(
                    response.context["games"].paginator.count,
                    2
                )

    def test_game_form_rejects_rating_above_10(self):

        form = GameForm(
            data={
                "title": "Test Game",
                "description": "Test description.",
                "release_date": "2020-01-01",
                "developer": "Test Developer",
                "publisher": "Test Publisher",
                "rating": "11",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)

    def test_game_form_rejects_negative_rating(self):

        form = GameForm(
            data={
                "title": "Test Game",
                "description": "Test description.",
                "release_date": "2020-01-01",
                "developer": "Test Developer",
                "publisher": "Test Publisher",
                "rating": "-1",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)


class DatabaseOptimizationTests(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="testpassword123"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="testpassword123"
        )

        self.game1 = Game.objects.create(
            title="Game One",
            description="First test game.",
            release_date=date(2020, 1, 1),
            developer="Developer One",
            publisher="Publisher One",
            rating=Decimal("9.0")
        )

        self.game2 = Game.objects.create(
            title="Game Two",
            description="Second test game.",
            release_date=date(2021, 1, 1),
            developer="Developer Two",
            publisher="Publisher Two",
            rating=Decimal("8.5")
        )

        self.game3 = Game.objects.create(
            title="Game Three",
            description="Third test game.",
            release_date=date(2022, 1, 1),
            developer="Developer Three",
            publisher="Publisher Three",
            rating=Decimal("8.0")
        )

        self.game1.users.add(self.user1)
        self.game2.users.add(self.user2)

    def test_without_prefetch_related(self):

        with self.assertNumQueries(4):

            games = Game.objects.all()

            for game in games:
                list(game.users.all())

    def test_with_prefetch_related(self):

        with self.assertNumQueries(2):

            games = Game.objects.prefetch_related("users")

            for game in games:
                list(game.users.all())