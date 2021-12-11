from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from accounts.models import *
from django.contrib.auth import logout
import string
import random
import math, json
# Create your views here.

def home(request):
    return render(request, 'profile.html')
    
def create_game(request):
    user = User.objects.get(id = request.user.id)
    if user.is_authenticated:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        game = Game(
            room_code = room_code,
            game_creater = user.id,
            game_opponent = None,
            is_over = False,
            turn = 0,
            red_score = 12,
            black_score = 12
        )
        game.save()
        for i in range(0,64,1):
            sq = BoardSquare(
                square_no = i,
                square_value = None,
                game = game
            )
            if i%2 == 1 and i < 24:
                sq.square_value = math.floor(i/2)
            elif i%2 == 0 and i > 38:
                sq.square_value = math.floor((i-16)/2)
            sq.save()
        
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
    game_squares = BoardSquare.objects.filter(game = game).order_by('-square_no')
    #print(game_squares)
    square_list = []
    for i in game_squares:
        square_list.append(i.square_value)
    #print(square_list)
    context = {
        'username' :user.username,
        'room_code' : room_code,
        'player' : player,
        'game' : game,
        'game_squares' : json.dumps(square_list)
    }
    
    return render(request, 'play.html', context)

def join_game(request):
    if request.user is None:
        return redirect('/')
    room_code = request.GET['room_code']
    user = User.objects.get(id = request.user.id)
    return redirect('/play/' + room_code + '?username=' + user.username)

def indexPage(request):
    context = {

    }
    return render(request,'index.html',context)