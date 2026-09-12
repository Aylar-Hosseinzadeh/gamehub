from django.shortcuts import render
from django.http import HttpResponse
from .models import Game

def home(request):
    games = Game.objects.all()

    return render(request, "games/home.html", {"games": games})

def detail(request, pk):
    game = Game.objects.get(pk=pk)

    return render(request, "games/detail.html", {"game": game})