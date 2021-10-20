from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from accounts.models import *
from django.contrib.auth import logout
import string
import random
# Create your views here.


def create_game(request):
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        game = Game(
            room_code = room_code,
            game_creater = user.id,
            game_opponent = None,
            is_over = False 
        )
        game.save()
        return redirect('/play/'+room_code+"?username="+user.username)
    else:
        return redirect('/login/')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse("Logged out successfully")


def play(request, room_code):
    if request.user is None:
        return redirect('/')
    user = User.objects.get(id = request.user.id)
    game = Game.objects.get(room_code = room_code)
    if game is None:
        return HttpResponse('Game does not exist')
    if game.game_creater != user.id:
        if game.game_opponent:
            print(game.game_creater)
            print(game.game_opponent)
            print(user.id)
            if game.game_opponent != user.id and game.game_creater != user.id:
                return HttpResponse("Game is not open to you")
        else:
            game.game_opponent = user.id
            game.save()
    if game.is_over:
        return HttpResponse("Game is over")
    print(game.game_opponent)
    print(game.game_creater)
    print(user.id)
    if game.game_creater == user.id:
        player = 'game_creator'
    else:
        player = 'game_opponent'
    print(player)
    context = {
        'username' :user.username,
        'room_code' : room_code,
        'player' : player
    }
    return render(request, 'play.html', context)

def join_game(request):
    if request.user is None:
        return redirect('/')
    room_code = request.GET['room_code']
    user = User.objects.get(id = request.user.id)
    return redirect('/play/' + room_code + '?username=' + user.username)