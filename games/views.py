from django.shortcuts import render
from django.http import HttpResponse
from .models import Game

def home(request):
    games = Game.objects.all()

    return render(request, "games/home.html", {"games": games})


