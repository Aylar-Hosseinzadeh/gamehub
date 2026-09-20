from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Game
from .forms import GameForm

def home(request):
    games = Game.objects.all()

    return render(request, "games/home.html", {"games": games})

def detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    return render(request, "games/detail.html", {"game": game})

def add_game(request):
    if request.method == "POST":
        form = GameForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("game_list")

    else:
        form = GameForm()

    return render(request, "games/add_game.html", {"form": form})
