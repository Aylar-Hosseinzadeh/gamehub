from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Game

def home(request):
    games = Game.objects.all()

    return render(request, "games/home.html", {"games": games})

def detail(request, pk):
    game = get_object_or_404(Game, pk=pk)

    return render(request, "games/detail.html", {"game": game})