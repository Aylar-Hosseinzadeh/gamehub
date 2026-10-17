from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Game
from .forms import GameForm
from django.core.paginator import Paginator
from django.contrib import messages

def game_list(request):
    search_query = request.GET.get("search")
    rating = request.GET.get("rating")
    sort = request.GET.get("sort")
    page_number = request.GET.get("page")
    params = request.GET.copy()
    params.pop("page", None)

    query_string = params.urlencode()

    games = Game.objects.all()
    if search_query:
        games = games.filter(title__icontains=search_query)

    if rating:
        games = games.filter(rating__gte=rating)

    sort_options = {
        "rating_desc": "-rating",
        "rating_asc": "rating",
        "title_asc": "title",
        "title_desc": "-title",
    }

    if sort in sort_options:
        games = games.order_by(sort_options[sort])

    paginator = Paginator(games, 2)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "games/game_list.html",
        {
            "games": page_obj,
            "search_query": search_query,
            "rating" : rating,
            "sort" : sort,
            "query_string" : query_string,
        }
    )

def home(request):
    return render(request, "games/home.html")

def login_view(request):
    print(request.GET)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect("game_list")
        messages.error(request, "Invalid username or password.")

    return render(request, "games/login.html")

def logout_view(request):
    logout(request)
    return redirect("game_list")

def detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    in_library = False

    if request.user.is_authenticated:
        in_library = request.user.games.filter(pk=game.pk).exists()

    return render(
        request,
        "games/detail.html",
        {
            "game": game,
            "in_library": in_library,
        }
    )

from django.contrib.auth.decorators import login_required
@login_required(login_url="/login/")
def add_to_library(request, pk):
    game = get_object_or_404(Game, pk=pk)

    game.users.add(request.user)
    messages.success(request, "Game added to your library.")

    return redirect("game_detail", pk=game.pk)

@login_required(login_url="/login/")
def remove_from_library(request, pk):
    game = get_object_or_404(Game, pk=pk)

    game.users.remove(request.user)
    messages.success(request, "Game removed from your library.")

    return redirect("game_detail", pk=game.pk)

@staff_member_required(login_url="/login/")
def add_game(request):
    if request.method == "POST":
        form = GameForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("game_list")

    else:
        form = GameForm()

    return render(request, "games/add_game.html", {"form": form})

