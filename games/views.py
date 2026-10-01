from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Game
from .forms import GameForm

def home(request):
    search_query = request.GET.get("search")
    if search_query:
        games = Game.objects.filter(
            title__icontains=search_query
        )
    else:
        games = Game.objects.all()

    return render(request, "games/home.html", {"games": games})

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
            return redirect("game_list")

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

    return redirect("game_detail", pk=game.pk)

@login_required(login_url="/login/")
def remove_from_library(request, pk):
    game = get_object_or_404(Game, pk=pk)

    game.users.remove(request.user)

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

