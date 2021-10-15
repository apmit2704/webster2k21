from django.shortcuts import render, redirect
from .models import *
# Create your views here.


def home(request):
    return render(request, 'profile.html')

def play(request, room_code):
    # user = User.objects.get(id = request.user.id)
    # game = Game.objects.get(room_code = room_code)
    # if game.game_creator != user and game.game_opponent != user:
    #     return redirect('/')
    # if game.is_over:
    #     return redirect('/')
    context = {
        'username' : request.GET['username'],
        'room_code' : room_code
    }
    return render(request, 'play.html', context)